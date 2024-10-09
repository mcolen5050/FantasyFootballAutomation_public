import requests
from espn_api.football import League
from constant import POSITION_MAP
from configCGPS import *
import datetime
import json

league = League(league_id, season_id, espn_s2, swid)

def test_player_stats():
    team = league.teams[team_id-1]  # Get your team (modify team_id as needed)
    roster = team.roster  # Get the roster of the team
    
    print(roster[1].name)
    
    stats = roster[1].stats
    
    sinceStart = datetime.date.today() - datetime.date(year= 2024, month= 9, day= 2)
    scoringPeriodId = int(sinceStart.days / 7) + 1
    
    print(json.dumps(stats, indent=4))
    print(stats[scoringPeriodId]['projected_points'])

if __name__ == "__main__":
    test_player_stats()
