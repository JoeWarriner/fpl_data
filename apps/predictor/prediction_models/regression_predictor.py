
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
import statsmodels.api as sm
from statsmodels.regression.mixed_linear_model import MixedLM

from apps.predictor.models import Player, PlayerFixture, Team
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 


from statsmodels.regression.linear_model import OLS
from statsmodels.tools.tools import add_constant


def generate_predictions():

    # Get player fixture data:
    qs = PlayerFixture.objects.all().values()
    data = pd.DataFrame.from_records(qs)


    data = data.set_index('id')

    #Calculate rolling points per player:
    data_rolling = pd.DataFrame()
    for player in Player.objects.all():
        temp_data = data[data['player_id'] == player.pk].copy()
    
        #Only look at regular starters:
        if len(temp_data) == 0:
            continue
        if len(temp_data.loc[(temp_data['points_scored'] == 0)].index) > len(temp_data.index) * 0.8:
            continue

        # For the 2020 season calculate rolling 20 game points average.
        temp_data_20 = temp_data[(temp_data.season == 20)].copy()
        temp_data_20.sort_values(by = ['gameweek'], inplace=True)
        temp_data_20.loc[:, 'rolling_points'] = temp_data_20.loc[:,'points_scored'].rolling(20, closed = 'left').mean().copy()

        #For 2021 season just use average for last 20 games of last season.
        points_val_21 = temp_data_20.loc[:,'points_scored'].tail(20).mean()
        temp_data_21 = temp_data[(temp_data.season == 21)].copy()
        temp_data_21.loc[:,'rolling_points'] = points_val_21

        #Put it all together!
        temp_data = pd.concat([temp_data_20,temp_data_21])
        data_rolling = pd.concat([data_rolling,temp_data])

    #Get rid of the nas - we don't want them messing up our model.
    data = data_rolling.dropna()

    goalkeepers = data.loc[(data.position == 'GK')]
    defenders = data.loc[(data.position == 'DEF')]
    midfielders = data.loc[(data.position == 'MID')]
    forwards = data.loc[(data.position == 'FWD')]

    # Get relevant opponent statistics:

    for data in [goalkeepers, defenders]:
        data.loc[:,'opp_team_stat'] = data.loc[:,'team_against_id'].apply(lambda x: Team.objects.get(pk = x).strength_attack)

    for data in [midfielders, forwards]:
        data.loc[:,'opp_team_stat'] = data.loc[:,'team_against_id'].apply(lambda x: Team.objects.get(pk = x).strength_defence)


    # Calculate moderator term:

    for data in [goalkeepers, defenders, midfielders, forwards]:
        data.loc[:,'rolling_points * opp_team_stat'] = data.loc[:, 'rolling_points'] * data.loc[:, 'opp_team_stat']


    # split into test and training:

    goalkeepers_test = goalkeepers.loc[(goalkeepers.season == 21)].copy()
    goalkeepers_training = goalkeepers.loc[goalkeepers.season == 20].copy()

    defenders_test = defenders.loc[defenders.season == 21].copy()
    defenders_training = defenders.loc[defenders.season == 20].copy()

    midfielders_test = midfielders.loc[midfielders.season == 21].copy()
    midfielders_training = midfielders.loc[midfielders.season == 20].copy()

    forwards_test = forwards.loc[forwards.season == 21].copy()
    forwards_training = forwards.loc[forwards.season == 20].copy()

    ###MODELS

    #GK
    exog = add_constant(goalkeepers_training[['rolling_points', 'opp_team_stat', 'rolling_points * opp_team_stat']])
    gk_model = OLS(goalkeepers_training['points_scored'], exog)
    gk_results = gk_model.fit()      
    gk_results.summary()
    # plt.clf()
    # plt.hist(gk_results.resid)
    # plt.show()


    test_exog = add_constant(goalkeepers_test[['rolling_points', 'opp_team_stat', 'rolling_points * opp_team_stat']])

    gk_predictions = gk_results.predict(test_exog)
    gk_predictions.name = 'gk_predictions'
    goalkeepers_eval = goalkeepers_test.join(gk_predictions, how='right')
    goalkeepers_eval.loc[:,'Model_Abs_Error'] = np.abs(goalkeepers_eval.loc[:,'points_scored'] - goalkeepers_eval.loc[:,'gk_predictions'])
    goalkeepers_eval.loc[:,'Naive_Abs_Error'] = np.abs(goalkeepers_eval.loc[:,'points_scored'] - goalkeepers_eval.loc[:,'rolling_points'])


    print(f'Model MAE: {goalkeepers_eval["Model_Abs_Error"].mean()}')
    print(f'Naive MAE: {goalkeepers_eval["Naive_Abs_Error"].mean()}')



    #DEF

    exog = add_constant(defenders_training[['rolling_points', 'opp_team_stat', 'rolling_points * opp_team_stat']])
    def_model = OLS(defenders_training['points_scored'], exog)
    def_results = def_model.fit()      
    def_results.summary()
    # plt.clf()
    # plt.hist(def_results.resid)
    # plt.show()


    test_exog = add_constant(defenders_test[['rolling_points', 'opp_team_stat', 'rolling_points * opp_team_stat']])

    def_predictions = def_results.predict(test_exog)
    def_predictions.name = 'def_predictions'
    defenders_eval = defenders_test.join(def_predictions, how='right')
    defenders_eval.loc[:,'Model_Abs_Error'] = np.abs(defenders_eval.loc[:,'points_scored'] - defenders_eval.loc[:,'def_predictions'])
    defenders_eval.loc[:,'Naive_Abs_Error'] = np.abs(defenders_eval.loc[:,'points_scored'] - defenders_eval.loc[:,'rolling_points'])

    print(f'Model MAE: {defenders_eval["Model_Abs_Error"].mean()}')
    print(f'Naive MAE: {defenders_eval["Naive_Abs_Error"].mean()}')

    #Remove points from season we are trying to predict (but keep hold of them so we can compare later)
    data['actual_points'] = data.loc[(data.season == 21), ('points_scored')]
    data.loc[(data.season == 21), ('points_scored')] = 0


    # MID

    exog = add_constant(midfielders_training[['rolling_points', 'opp_team_stat', 'rolling_points * opp_team_stat']])
    mid_model = OLS(midfielders_training['points_scored'], exog)
    mid_results = mid_model.fit()      
    mid_results.summary()
    print(mid_results.summary())

    test_exog = add_constant(midfielders_test[['rolling_points', 'opp_team_stat', 'rolling_points * opp_team_stat']])

    mid_predictions = mid_results.predict(test_exog)
    mid_predictions.name = 'mid_predictions'
    midfielders_eval = midfielders_test.join(mid_predictions, how='right')
    midfielders_eval.loc[:,'Model_Abs_Error'] = np.abs(midfielders_eval.loc[:,'points_scored'] - midfielders_eval.loc[:,'mid_predictions'])
    midfielders_eval.loc[:,'Naive_Abs_Error'] = np.abs(midfielders_eval.loc[:,'points_scored'] - midfielders_eval.loc[:,'rolling_points'])


    print('HIIII')
    print(f'Model MAE: {midfielders_eval["Model_Abs_Error"].mean()}')
    print(f'Naive MAE: {midfielders_eval["Naive_Abs_Error"].mean()}')


    #FWD

    exog = add_constant(forwards_training[['rolling_points', 'opp_team_stat', 'rolling_points * opp_team_stat']])
    fwd_model = OLS(forwards_training['points_scored'], exog)
    fwd_resullts = fwd_model.fit()      
    print(fwd_resullts.summary())


    # plt.clf()
    # plt.hist(fwd_resullts.resid)
    # plt.show()


    test_exog = add_constant(forwards_test[['rolling_points', 'opp_team_stat', 'rolling_points * opp_team_stat']])

    fwd_predictions = fwd_resullts.predict(test_exog)
    fwd_predictions.name = 'fwd_predictions'
    forwards_eval = forwards_test.join(fwd_predictions, how='right')
    forwards_eval.loc[:,'Model_Abs_Error'] = np.abs(forwards_eval.loc[:,'points_scored'] - forwards_eval.loc[:,'fwd_predictions'])
    forwards_eval.loc[:,'Naive_Abs_Error'] = np.abs(forwards_eval.loc[:,'points_scored'] - forwards_eval.loc[:,'rolling_points'])

    print(f'Model MAE: {forwards_eval["Model_Abs_Error"].mean()}')
    print(f'Naive MAE: {forwards_eval["Naive_Abs_Error"].mean()}')
