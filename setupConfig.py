#!/usr/bin/env python3

import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def extract_ids_from_url(url):
    """Extracts league_id, team_id, and season_id from the ESPN team URL."""
    from urllib.parse import parse_qs, urlparse

    query_params = parse_qs(urlparse(url).query)
    try:
        league_id = int(query_params['leagueId'][0])
        team_id = int(query_params['teamId'][0])
        season_id = int(query_params['seasonId'][0])
        return league_id, team_id, season_id
    except (KeyError, ValueError) as e:
        raise ValueError("Error: Unable to extract league_id, team_id, or season_id from the URL.") from e

def scrape_cookies_and_team_info():
    """Use Selenium to scrape cookies and extract team info from the URL."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Navigate to ESPN login and wait for cookies
    driver.get("https://www.espn.com/fantasy/football")

    # Wait for an element on the page to confirm it has loaded before triggering the alert
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Triggering a JavaScript alert after 10 seconds
    driver.execute_script("alert('Please log in and navigate to your team page. Once done, the web browser will close and your team data will be located in \"config.json\".');")
    
    # Wait for the alert to be displayed and accepted
    try:
        WebDriverWait(driver, 300).until(EC.alert_is_present())
        WebDriverWait(driver, 300).until(lambda d: not EC.alert_is_present()(d))
        print("confirmed alert")
    except:
        print("Timeout: Alert not handled correctly.")
        driver.quit()
        exit()

    # After alert is closed, check for the team URL
    try:
        WebDriverWait(driver, 300).until(lambda d: "teamId" in d.current_url)
        current_url = driver.current_url
        print(f"Team page detected. Current URL: {current_url}")
    except:
        print("Timeout: Team page URL not detected. Please ensure you are on your team page.")
        driver.quit()
        exit()

    # Extract league_id, team_id, and season_id from the URL
    try:
        league_id, team_id, season_id = extract_ids_from_url(current_url)
        print(f"Extracted league_id: {league_id}, team_id: {team_id}, season_id: {season_id}")
    except ValueError as e:
        print(e)
        driver.quit()
        exit()

    # Extract team name from the page
    try:
        team_name_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.teamName.truncate"))
        )
        team_name = team_name_element.text
        print(f"Extracted team name: {team_name}")
    except:
        print("Error: Unable to extract the team name.")
        driver.quit()
        exit()

    # Retrieve necessary cookies
    cookies_dict = {
        "swid": driver.get_cookie('SWID').get('value'),
        "espn_s2": driver.get_cookie('espn_s2').get('value')
    }

    driver.quit()

    if 'espn_s2' not in cookies_dict or 'swid' not in cookies_dict:
        raise Exception("Error: Required cookies 'espn_s2' and 'swid' not found.")

    return cookies_dict['espn_s2'], cookies_dict['swid'], league_id, team_id, season_id, team_name

def update_config_file(team_name, league_id, team_id, season_id, swid, espn_s2):
    """Updates the config.json file by adding a new team or creating the file if it doesn't exist.
       If the team already exists, it updates the team's data.
    """
    config_file = 'config.json'
    new_team_data = {
        team_name: {
            "league_id": league_id,
            "season_id": season_id,
            "team_id": team_id,
            "swid": swid,
            "espn_s2": espn_s2
        }
    }

    # Check if config.json exists
    if os.path.exists(config_file):
        # Load existing config.json
        with open(config_file, 'r') as f:
            config_data = json.load(f)

        # Check if the team already exists in the config
        if team_name in config_data:
            print(f"Team '{team_name}' already exists in config.json. Updating its data.")
        else:
            print(f"Adding new team '{team_name}' to config.json.")

        # Update the team data (either add new or update existing)
        config_data[team_name] = new_team_data[team_name]

        # Write the updated data back to the file
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=4)

        print(f"Updated {config_file} with team: {team_name}")
    else:
        # Create a new config.json with the team data if file doesn't exist
        with open(config_file, 'w') as f:
            json.dump(new_team_data, f, indent=4)

        print(f"Created new {config_file} with team: {team_name}")

if __name__ == "__main__":
    # Scrape cookies, team info, and extract necessary data
    espn_s2, swid, league_id, team_id, season_id, team_name = scrape_cookies_and_team_info()

    # Add the scraped data to the config.json file
    update_config_file(team_name, league_id, team_id, season_id, swid, espn_s2)

    print("Config setup completed successfully.")
