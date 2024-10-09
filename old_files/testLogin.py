import requests
from configTest import *  # Import all variables from config.py

# NFL Import
from espn_api.football import League

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def create_authenticated_session(swid, espn_s2):
    session = requests.session()
    session.cookies.set('swid', swid)
    session.cookies.set('espn_s2', espn_s2)
    session.headers.update(headers)
    return session

def get_basic_info(session, league_id, season_id):
    url = f"https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/{league_id}?seasonId={season_id}&view=mTeam"
    response = session.get(url)
    
    if response.status_code == 200:
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            print("Response content is not in JSON format:")
            print(response.text)
            return None
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        print(response.text)
        return None


# Create a session and fetch team information
session = create_authenticated_session(swid, espn_s2)
team_info = get_basic_info(session, league_id, season_id)

if team_info:
    print("Team Information:")
    print(team_info)