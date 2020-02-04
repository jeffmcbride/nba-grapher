import plotly
from nba_api.stats.endpoints import teamyearbyyearstats
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import *


class Team:

    def __init__(self, id, per_mode):
        self.dict = teams.find_team_name_by_id(id)
        self.name = self.dict['nickname']
        self.teamstats = teamyearbyyearstats.TeamYearByYearStats(id, per_mode_simple=per_mode).get_data_frames()[0]

    def get_stats(self, stat, start, end):
        stats_in_range = self.teamstats[(self.teamstats['YEAR'] <= end)]
        stats_in_range = stats_in_range[(self.teamstats['YEAR'] >= start)]
        return stats_in_range.set_index("YEAR")[stat]


class Player:

    def __init__(self, id, per_mode):
        self.dict = players.find_player_by_id(id)
        self.name = self.dict['full_name']
        self.playerstats = playercareerstats.PlayerCareerStats(id, per_mode_simple=per_mode).get_data_frames()[0]

    def get_stats(self, stat, start, end):
        stats_in_range = self.playerstats[self.playerstats['SEASON_ID'] <= end]
        stats_in_range = stats_in_range[self.playerstats['SEASON_ID'] >= start]
        return stats_in_range.set_index("SEASON_ID")[stat]







