from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=5)
    this_season_id = models.IntegerField()

    def __str__(self) -> str:
        return self.team_name


class Player(models.Model):
    first_name = models.CharField(max_length=200)
    second_name = models.CharField(max_length=200)
    this_season_id = models.IntegerField()
    current_value = models.IntegerField()
    expected_points = models.IntegerField()
    position = models.CharField(max_length=50)
    current_team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.second_name}'

class PlayerFixture(models.Model):
    points_scored = models.IntegerField()
    season = models.IntegerField()
    gameweek = models.IntegerField()
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team_for = models.ForeignKey(Team, related_name='team_for', on_delete=models.CASCADE)
    team_against = models.ForeignKey(Team, related_name='team_against', on_delete=models.CASCADE)
    position = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.player}, week: {self.gameweek}, {self.season}'



