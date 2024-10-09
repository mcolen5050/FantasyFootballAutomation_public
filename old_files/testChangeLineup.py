import requests
from configTest import *  # Import all variables from config.py

# Define the POST request URL
url = f"https://lm-api-writes.fantasy.espn.com/apis/v3/games/ffl/seasons/{season_id}/segments/0/leagues/{league_id}/transactions/"

# Define the session
session = requests.Session()

# Set the necessary cookies
session.cookies.set('swid', swid)
session.cookies.set('espn_s2', espn_s2)

# Define the payload
payload = {
    "isLeagueManager": False,
    "teamId": team_id,
    "type": "ROSTER",
    "memberId": swid,
    "scoringPeriodId": 1,
    "executionType": "EXECUTE",
    "items": [
        {
            "playerId": 4258173,
            "type": "LINEUP",
            "fromLineupSlotId": 4,
            "toLineupSlotId": 20
        },
        {
            "playerId": 16800,
            "type": "LINEUP",
            "fromLineupSlotId": 20,
            "toLineupSlotId": 4
        }
    ]
}

# Send the POST request to update the lineup
response = session.post(url, headers=headers, json=payload)

# Check the response status
if response.status_code == 200:
    print("Lineup updated successfully!")
else:
    print(f"Failed to update lineup: {response.status_code}")
    print(response.text)