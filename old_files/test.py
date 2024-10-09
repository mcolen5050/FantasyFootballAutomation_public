from configChrissy import *  # Import all variables from config.py

import requests

# Set up your session and cookies
session = requests.Session()
session.cookies.set('swid', swid)
session.cookies.set('espn_s2', espn_s2)
scoring_period_id = 4
# Define the GET request URL
url = f"https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/{league_id}?seasonId=2024&teamId={team_id}&scoringPeriodId={scoring_period_id}&view=mRoster"

# Send the GET request to retrieve the current lineup
response = session.get(url, headers=headers, params={'view': ['mTeam', 'mRoster', 'mMatchup', 'mSettings', 'mStandings']})

# Check the response status and print raw content if not JSON
if response.status_code == 200:
    try:
        data = response.json()  # Attempt to parse JSON
        # print(data)  # Print the parsed JSON data
    except requests.exceptions.JSONDecodeError:
        print("Response content is not in JSON format:")
        # print(response.text)  # Print raw response text
else:
    print(f"Failed to retrieve lineup: {response.status_code}")
    print(response.text)

# if response.status_code == 200:
#     data = response.json()
#     roster = data[0]['teams'][0]['roster']['entries']
    
#     # Initialize a list to hold the lineup information
#     lineup_info = []

#     # Print each player's details from the roster
#     print("Current Lineup:")
#     for player in roster:
#         player_name = player['playerPoolEntry']['player']['fullName']
#         position = player['lineupSlotId']
#         projected_points = player['playerPoolEntry'].get('appliedStatTotal', 0)  # Get projected points or 0 if not available
        
#         # Convert position ID to a readable format
#         position_map = {
#             0: "QB", 2: "RB", 4: "WR", 6: "TE", 16: "D/ST", 17: "K", 20: "Bench"
#             # Add more lineupSlotId mappings as needed
#         }
#         position_name = position_map.get(position, "Unknown")

#         # Append formatted player data to the lineup_info list
#         lineup_info.append(f"{player_name} - Position: {position_name}, Projected Points: {projected_points}")

#     # Print the lineup information
#     for info in lineup_info:
#         print(info)
# else:
#     print(f"Failed to retrieve lineup: {response.status_code}")
#     print(response.text)