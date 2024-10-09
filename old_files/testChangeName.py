import requests
from configTest import *  # Import all variables from config.py

# Define the session
session = requests.Session()

# Set the necessary cookies
session.cookies.set('swid', swid)
session.cookies.set('espn_s2', espn_s2)

# Define headers
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'X-Fantasy-Platform': 'kona-PROD-a35fb116c6d2671fa6b0d31d6f6d431c21a114eb',
    'X-Fantasy-Source': 'kona'
}

# Define the payload (the new team name and abbreviation)
payload = {
    "abbrev": "MD",
    "name": "Mahomes Depot"
}

# Define the POST request URL
url = "https://lm-api-writes.fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leagues/541245259/teams/8"

# Send the POST request to update the team name
response = session.post(url, headers=headers, json=payload)

# Check the response status
if response.status_code == 200:
    print("Team name updated successfully!")
else:
    print(f"Failed to update team name: {response.status_code}")
    print(response.text)