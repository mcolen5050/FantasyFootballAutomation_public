#!/usr/bin/env python3

import argparse
import json
import requests
from espn_api.football import League
from Player import Player
from constant import POSITION_MAP
import datetime

# Calculate scoring period
since_start = datetime.date.today() - datetime.date(year=2024, month=9, day=2)
scoring_period_id = int(since_start.days / 7) + 1

# player id map (for verbose print)
id_map = {}

class TransactionItemsMissingException(Exception):
    """Exception raised when transaction items are missing in the API request."""
    pass

def load_config(file_path):
    """Load the JSON configuration file."""
    with open(file_path) as config_file:
        return json.load(config_file)

def create_authentication_session(swid, espn_s2):
    """Create an authenticated session with cookies set."""
    session = requests.Session()
    session.cookies.set('swid', swid)
    session.cookies.set('espn_s2', espn_s2)
    return session

def get_players(roster):
    """Create and return a list of Player objects from the roster."""
    players = []
    
    for player in roster:
        p = Player(
            player_id=player.playerId,
            full_name=player.name,
            lineup_slot=POSITION_MAP[player.lineupSlot],
            projected_points=player.stats[scoring_period_id]['projected_points'],
            eligible_slots = [POSITION_MAP[slot] for slot in player.eligibleSlots],
            injury_status=player.injuryStatus
        )
        players.append(p)
        id_map[p.player_id] = p.full_name
        
    return players

def set_best_starters(roster):
    """loop and get the best possible starters"""
    positions = {
        'QB': ([], 1),
        'RB': ([], 2),
        'WR': ([], 2),
        'TE': ([], 1),
        'D/ST': ([], 1),
        'K': ([], 1)
    }
    
    for position, (position_list, num_starters) in positions.items():  # Iterate through the dictionary
        for player in roster:
            if POSITION_MAP[position] in player.eligible_slots:  # Check if the position is in the player's eligible slots
                position_list.append(player)  # Append the player to the corresponding list
        position_list.sort()
        for i in range(num_starters):
            position_list.pop().set_new_lineup_slot(POSITION_MAP[position])
    
    # Handle FLEX
    flex_candidates = positions['RB'][0] + positions['WR'][0] + positions['TE'][0]
    flex_candidates.sort()
    flex_candidates.pop().set_new_lineup_slot(23)

def get_changes(league, team_id):
    """Get the necessary lineup changes for the best lineup."""
    team = league.teams[team_id - 1]
    
    # Create Player objects and make a roster
    roster = get_players(team.roster)
    
    # Handle Injury Reserve
    for player in roster:
        if player.on_ir():
            player.set_new_lineup_slot(21)
    
    set_best_starters(roster)
    
    changes = []
    for player in roster:
        change = player.to_lineup_change_dict()
        if change:
            changes.append(change)
        
    return changes

def update_lineup(team_config, verbose):
    """Update the lineup for a specific team."""
    league = League(team_config['league_id'], team_config['season_id'], team_config['espn_s2'], team_config['swid'])

    session = create_authentication_session(team_config['swid'], team_config['espn_s2'])

    # Get changes
    changes = get_changes(league, team_config['team_id'])

    # Prepare POST request payload
    payload = {
        "isLeagueManager": False,
        "teamId": team_config['team_id'],
        "type": "ROSTER",
        "memberId": team_config['swid'],
        "scoringPeriodId": scoring_period_id,
        "executionType": "EXECUTE",
        "items": changes
    }

    if verbose:
        # Print full payload in verbose mode
        print("Sending the following JSON payload:")
        print(json.dumps(payload, indent=4))

        # Print human-readable player changes
        print("\nPlayer changes:")
        for change in changes:
            print(f"Player {id_map[change['playerId']]} moved from {POSITION_MAP[change['fromLineupSlotId']]} to {POSITION_MAP[change['toLineupSlotId']]}")

    # Send POST request
    url = f"https://lm-api-writes.fantasy.espn.com/apis/v3/games/ffl/seasons/{team_config['season_id']}/segments/0/leagues/{team_config['league_id']}/transactions/"
    response = session.post(url, headers={'Content-Type': 'application/json'}, json=payload)

    # Handle response
    if response.status_code == 200:
        print("Lineup updated successfully!")
    elif response.status_code == 409 and "TransactionItems are missing" in response.text:
        print("Lineup already optimized!")
    else:
        print(f"Failed to update lineup: {response.status_code}")
        print(response.text)

# Main execution with argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate ESPN Fantasy Football lineup changes.")
    parser.add_argument('team', nargs='?', default=None, help='Update a specific team in the config file (default: update all teams)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode to show full JSON payload and changes')

    args = parser.parse_args()

    # Load the configuration
    config_data = load_config('config.json')

    if args.team:
        # Update the specified team
        team_config = config_data.get(args.team)
        if team_config:
            print(f"Updating lineup for {args.team}...")
            update_lineup(team_config, verbose=args.verbose)
        else:
            print(f"Error: Team '{args.team}' not found in the config file. Available teams: {', '.join(config_data.keys())}")
    else:
        # Update all teams if no specific team is provided
        print("Updating all teams in the config file...")
        for team_name, team_config in config_data.items():
            print(f"Updating lineup for {team_name}...")
            update_lineup(team_config, verbose=args.verbose)
