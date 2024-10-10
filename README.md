# Fantasy Football Lineup Automation

This project is designed to automate ESPN Fantasy Football lineup management using Python.  
The tool allows you to automatically set the best lineup for your fantasy teams based on projected points and player eligibility.

## Setup

### Prerequisites

- Python 3.x
- Selenium (`pip install selenium`)
- Chrome WebDriver (Make sure it's installed and accessible)
- `webdriver_manager` package (`pip install webdriver_manager`)

To download packages, paste and run in terminal:
```bash
pip install selenium webdriver_manager
```

### Step 1: Setting up the `config.json` file

Before you can run the automation, you'll need to set up the `config.json` file that contains authentication information for your ESPN fantasy football teams. Follow the steps below:

1. **Run `setupConfig.py`:**

Run the `setupConfig.py` file to scrape your ESPN login cookies and team data.

```bash  
python setupConfig.py  
```

2. **Login to ESPN:**

When the browser opens, log in to your ESPN account and navigate to the **team page** of the fantasy football team you want to automate.

3. **Confirmation:**

The script will wait until you're on the correct team page. Once you confirm, the necessary cookies (`swid` and `espn_s2`), as well as team and league information, will be extracted and saved in the `config.json` file.

4. **Repeat if Needed:**

You can run `setupConfig.py` multiple times to add additional teams to the `config.json` file. The script will append new teams rather than overwrite the existing configuration.

### Step 2: Running the Lineup Automation

Once your `config.json` file is set up, you can use `main.py` to automate your team lineup changes.

#### Updating all teams in the `config.json` file:

To update all teams in the `config.json` file, simply run the `main.py` file or input into terminal:

```bash
./main.py
```
or
```bash
python main.py
```

#### Updating a specific team:

To update a specific team, specify the team name as an argument:

```bash  
./main.py myTeam
```

Replace `myTeam` with the name of the team you want to update (as it appears in `config.json`).

#### Using verbose mode:

You can also use the `-v` or `--verbose` flag to enable verbose mode, which will show the full JSON payload sent to ESPN and the player changes being made:

```bash  
./main.py -v  
```

or for a specific team:

```bash  
./main.py -v myTeam  
```
