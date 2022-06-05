'''
SCRIPT TO SEED THE DATABASE AT THE START OF A SEASON

STEPS:
- Download data directory from: https://github.com/vaastav/Fantasy-Premier-League
- Copy it into inputs folder.
- Run this script.
- Run:
    - manage.py loaddata <fixturename>
'''
from distutils.command.build import build
from time import thread_time_ns
from predictor.models import Team, Player, PlayerFixture
from django.core.management.base import BaseCommand, CommandError
import json
import pandas as pd




class Command(BaseCommand):


    def handle(self, *args, **kwargs):

        with open('inputs/overall_data_example.json', 'r', encoding='utf-8') as fp:
            api_data = json.load(fp)


        Team.objects.all().delete()
        Player.objects.all().delete()
        PlayerFixture.objects.all().delete()
        
        merged_seasons =  pd.read_csv('inputs/data/cleaned_merged_seasons.csv')
        merged_seasons_2021 = merged_seasons.query('season_x == "2020-21"')
        merged_seasons_2122 = merged_seasons.query('season_x == "2021-22"')

        all_teams = []



        for team in api_data['teams']:
            all_teams.append(
                Team(
                    name = team['name'],
                    short_name = team['short_name'],
                    this_season_id = team['id']
                )
            )

        Team.objects.bulk_create(all_teams)


        last_season_teams = pd.read_csv('inputs/data/2020-21/teams.csv')

        for _, row in last_season_teams.iterrows():
            try:
                Team.objects.get(name = row['name'])
            except Team.DoesNotExist:
                Team.objects.create(
                    name = row['name'],
                    short_name = row['short_name'],
                    this_season_id = 9999
                )



        all_players = []

        for player in api_data['elements']:
            if player['status'] == 'a':
                try:
                    
                    full_name = f'{player["first_name"]} {player["second_name"]}'
                    temp_df = merged_seasons_2122.query(f'GW == 1 & name == "{full_name}"')
                    temp_df.reset_index(inplace=True)
                    all_players.append(
                        Player(
                            this_season_id = player['id'],
                            first_name =  player['first_name'],
                            second_name = player['second_name'],
                            position = temp_df['position'][0],
                            current_value =  temp_df['value'][0],
                            expected_points = 0,
                            current_team = Team.objects.get(name = temp_df['team_x'][0])
                        )
                    )
                    
                except KeyError:
                    pass
                    
        Player.objects.bulk_create(all_players)

        player_fixtures = []

        for player in Player.objects.all().iterator():
            player: Player
            temp_df = merged_seasons_2021.query(f'name == "{player.first_name} {player.second_name}"')
            if len(temp_df.index) <= 38:
                for _, row in temp_df.iterrows():
                    player_fixtures.append(PlayerFixture(
                        points_scored = row['total_points'],
                        season = 20,
                        gameweek = row['GW'],
                        player = player,
                        team_for = Team.objects.get(name = row['team_x']),
                        team_against = Team.objects.get(name = row['opp_team_name']),
                        position = row['position']
            ))
        
        PlayerFixture.objects.bulk_create(player_fixtures)







