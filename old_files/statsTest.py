import requests
from espn_api.football import League
from constant import POSITION_MAP
from configTest import *
import datetime

league = League(league_id, season_id, espn_s2, swid)

def test_player_stats():
    team = league.teams[team_id-1]  # Get your team (modify team_id as needed)
    roster = team.roster  # Get the roster of the team
    
    for player in roster:
        player_name = player.name
        lineup_slot = POSITION_MAP[player.lineupSlot]
        eligible_slots = [POSITION_MAP[slot] for slot in player.eligibleSlots]
        
        sinceStart = datetime.date.today() - datetime.date(year= 2024, month= 9, day= 2)
        scoringPeriodId = int(sinceStart.days / 7)

        # Check if stats are available
        if scoringPeriodId in player.stats:
            projected_points = player.stats[scoringPeriodId].get('projected_points', 'N/A')
        else:
            projected_points = 'No stats available'
        
        print(f"Player: {player_name}")
        print(f"Lineup Slot: {lineup_slot}")
        print(f"Eligible Slots: {eligible_slots}")
        print(f"Projected Points: {projected_points}")
        print("-" * 40)

if __name__ == "__main__":
    test_player_stats()
