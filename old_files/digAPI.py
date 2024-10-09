from espn_api.requests.espn_requests import EspnFantasyRequests
from configCGPS import *  # Import your configuration (swid, espn_s2, etc.)

# Configuration for the request
sport = 'nfl'
cookies = {
    'swid': swid,
    'espn_s2': espn_s2
}

# Initialize the request class
espn_request = EspnFantasyRequests(sport=sport, year=season_id, league_id=league_id, cookies=cookies)

# Get league data including rosters
player_data = espn_request.get_league()

# Retrieve all teams
teams = player_data.get('teams', [])

# Find the specific team using team_id
team = next((team for team in teams if team.get('id') == team_id), None)

if team:
    print(f"Found Team: {team.get('location')} {team.get('nickname')} (ID: {team_id})")
    
    # Extract and print the order of players in the lineup
    roster_entries = team.get('roster', {}).get('entries', [])
    for entry in roster_entries:
        player_info = entry.get('playerPoolEntry', {}).get('player', {})
        full_name = player_info.get('fullName', 'Unknown Player')
        position_id = entry.get('lineupSlotId', 'Unknown Position')
        print(f"  Player: {full_name}, Position ID: {position_id}")
else:
    print(f"Team with ID {team_id} not found.")
