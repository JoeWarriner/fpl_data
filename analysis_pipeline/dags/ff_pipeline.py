from datetime import datetime, timedelta
from textwrap import dedent
import pendulum
import requests

from airflow.models import Variable


from airflow.providers.google.cloud.hooks.cloud_sql import CloudSQLHook, CloudSQLDatabaseHook
from airflow.providers.google.cloud.hooks.gcs import GCSHook

from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.sensors.python import PythonSensor
from mysql.connector.connection import MySQLConnection

from airflow.decorators import dag, task

@dag(
    schedule=None,
    start_date=pendulum.datetime(2022, 1,1),
    catchup=False,
    tags=['example']
)
def my_pipeline():


    def check_for_update():
        '''
        Check if the next week's points and bonuses have been updated.
        '''
        
        current_game_week = Variable.get('current_game_week')        
        game_week_status = requests.get('https://fantasy.premierleague.com/api/event-status').json()
        for status in game_week_status['status']:
            if status['event'] == current_game_week:
                return False
            if not status['bonus_added']:
                return False
        return True


    waiting_for_update = PythonSensor(
        task_id = 'waiting_for_update',
        python_callable = check_for_update
    )
    
    


    @task()
    def call_player_api_and_save():
        import requests
        import json
        current_game_week = int(Variable.get('current_game_week'))
        current_game_week += 1 
        gcs_hook = GCSHook()
        name = f'api_dump_{datetime.now()}.json'
        data = requests.get(f"https://fantasy.premierleague.com/api/event/{current_game_week}/live").json()
        gcs_hook.upload(
            bucket_name = 'joes-fantasy-football-bucket',
            object_name = name, 
            data = json.dumps(data)
            )
        return name

    @task
    def api_data_to_database(object_name):
        import pandas as pd
        import json

        gcs_hook = GCSHook()
        raw_json = gcs_hook.download(
            bucket_name = 'joes-fantasy-football-bucket',
            object_name = object_name, 
        )
        json_dict = json.loads(raw_json)
        output_data = []
        for element in json_dict['elements'] :
            row = [element['id']]
            row.extend(list(element['stats'].keys()))
            output_data.append(row)
            
        
        output = pd.DataFrame(
            columns=[
                "player_id",
                "minutes",
                "goals_scored",
                "assists",
                "clean_sheets",
                "goals_conceded",
                "own_goals",
                "penalties_saved",
                "penalties_missed",
                "yellow_cards",
                "red_cards",
                "saves",
                "bonus",
                "bps",
                "influence",
                "creativity",
                "threat",
                "ict_index",
                "starts",
                "expected_goals",
                "expected_assists",
                "expected_goal_involvements",
                "expected_goals_conceded",
                "total_points",
                "in_dreamteam",

            ],
            data = output_data
        )
        gameweek = int(Variable.get('current_game_week')) + 1
        db = CloudSQLDatabaseHook()
        conn = db.create_connection()
        db_hook: MySqlHook = db.get_database_hook(conn)
        connection = db_hook.get_conn()
        output.to_sql(con = connection, name= f'gameweek_{gameweek}_data', if_exists = 'append', index= False)
        connection.close()
        db.cleanup_database_hook()
        

    
    waiting_for_update
    object_name = call_player_api_and_save()
    api_data_to_database(object_name)        

my_pipeline()

