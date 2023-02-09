from predictor.models import Player, PlayerFixture
import pandas as pd


def get_latest_predictions():
    current_gameweek = 10
    players = Player.objects.all().values()
    player_df = pd.DataFrame.from_records(players)
    print(player_df.columns)
    for player in player_df['id']:
        fixtures_qs = PlayerFixture.objects.filter(player = player).filter(gameweek__gt = current_gameweek - 10).values()
        if not fixtures_qs:
            expected_value = 0
        else:
            fixtures = pd.DataFrame.from_records(fixtures_qs)
            expected_value = fixtures['points_scored'].mean()
        
        print(expected_value)
        Player.objects.filter(id = player).update(expected_points = int(expected_value))
    print(pd.DataFrame.from_records(Player.objects.all().values())) 