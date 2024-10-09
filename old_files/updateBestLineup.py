import requests
from espn_api.football import League
from constant import POSITION_MAP
from configTest import *
import datetime


league = League(league_id, season_id, espn_s2, swid)
sinceStart = datetime.date.today() - datetime.date(year= 2024, month= 9, day= 2)
scoringPeriodId = int(sinceStart.days / 7) + 1

class TransactionItemsMissingException(Exception):
    """Exception raised when transaction items are missing in the API request."""
    pass

def createAuthenticationSession():
    # Define the session
    session = requests.Session()
    
    # Set the necessary cookies
    session.cookies.set('swid', swid)
    session.cookies.set('espn_s2', espn_s2)
    
    return session

# Function to remove duplicates based on a specific key
def remove_duplicates(dicts, unique_key):
    """
    Remove duplicates based on a unique key, merge them, and filter out entries where
    'fromLineupSlotId' and 'toLineupSlotId' are the same after merging.

    Args:
        dicts (list): List of dictionaries to filter.
        unique_key (str): The key to use for identifying duplicates.

    Returns:
        list: Filtered list of unique dictionaries.
    """
    seen = {}  # Dictionary to track unique key values and their entries

    for d in dicts:
        key_value = d[unique_key]  # Extract the value of the unique key

        # If it's a new unique key, add it to the 'seen' dictionary
        if key_value not in seen:
            seen[key_value] = d
        else:
            # If a duplicate is found, merge 'from' of the first and 'to' of the duplicate
            seen[key_value]['toLineupSlotId'] = d['toLineupSlotId']

    # Convert the 'seen' dictionary back to a list
    unique_dicts = list(seen.values())

    # Remove entries where 'fromLineupSlotId' and 'toLineupSlotId' are the same
    filtered_dicts = [d for d in unique_dicts if d['fromLineupSlotId'] != d['toLineupSlotId']]

    return filtered_dicts

def getChanges():
    team = league.teams[team_id-1]  # Get the third team from the league
    roster = team.roster  # Get the roster of the team
    
    # Initialize slots
    changes = []
    
    starting_positions = {0, 2, 4, 6, 16, 17, 23}  # Example positions: QB, RB, WR, TE, D/ST, K, FLEX
    bench_position = 20  # Bench position slot ID
    
    starters = []
    bench = []
    
    def comparePlayers(player1, player2):
        return player1.stats[scoringPeriodId]['projected_points'] > player2.stats[scoringPeriodId]['projected_points']
    
    for player in roster:
        if POSITION_MAP[player.lineupSlot] in starting_positions:
            starters.append(player)
        elif POSITION_MAP[player.lineupSlot] == bench_position:
            bench.append(player)
            
    starters.sort(key=lambda starter: POSITION_MAP[starter.lineupSlot])
    for starter in starters:
        starterPosition = {POSITION_MAP[starter.lineupSlot]}
        if starterPosition == 23:
            starterPosition = {23, 2, 4, 6}
        
        best_replacement = None
        
        for bench_player in bench:
            benchEligible = {POSITION_MAP[pos] for pos in bench_player.eligibleSlots}
            
            if any(element in starterPosition for element in benchEligible):
                if comparePlayers(bench_player, starter) and (not best_replacement or comparePlayers(bench_player, best_replacement)):
                    best_replacement = bench_player
        
        if best_replacement:
            change = [
                {
                    "playerId": best_replacement.playerId,
                    "type": "LINEUP",
                    "fromLineupSlotId": POSITION_MAP[best_replacement.lineupSlot],
                    "toLineupSlotId": POSITION_MAP[starter.lineupSlot]
                },
                {
                    "playerId": starter.playerId,
                    "type": "LINEUP",
                    "fromLineupSlotId": POSITION_MAP[starter.lineupSlot],
                    "toLineupSlotId": POSITION_MAP[best_replacement.lineupSlot]
                }
            ]
            changes.extend(change)
            
            starter.lineupSlot = 'BE'
            bench.append(starter)
            bench.remove(best_replacement)
    
    return remove_duplicates(changes, 'playerId')

session = createAuthenticationSession()

url = f"https://lm-api-writes.fantasy.espn.com/apis/v3/games/ffl/seasons/{season_id}/segments/0/leagues/{league_id}/transactions/"

payload = {
    "isLeagueManager": False,
    "teamId": team_id,
    "type": "ROSTER",
    "memberId": swid,
    "scoringPeriodId": scoringPeriodId,
    "executionType": "EXECUTE",
    "items": getChanges()
}

# Send the POST request to update the lineup
response = session.post(url, headers=headers, json=payload)

# Check the response status
if response.status_code == 200:
    print("Lineup updated successfully!")
elif response.status_code == 409 and response.json()['messages'] == ['TransactionItems are missing, unable to process the transaction.']:
    print("Lineup already optimized!")
else:
    print(f"Failed to update lineup: {response.status_code}")
    print(response.text)