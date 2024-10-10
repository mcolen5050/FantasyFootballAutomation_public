# Fantasy Football Lineup Automation

This project is designed to automate ESPN Fantasy Football lineup management using Python.  
The tool allows you to automatically set the best lineup for your fantasy teams based on projected points and player eligibility.

## Setup

### Prerequisites

- Python 3.x
- Selenium (`pip install selenium`)
- Chrome WebDriver (Make sure it's installed and accessible)
- `webdriver_manager` package (`pip install webdriver_manager`)
- `espn_api` for getting player info (`pip install espn_api`)

To download packages, paste and run in terminal:
```bash
pip install selenium webdriver_manager espn_api
```

### Quick Setup with VSCode

To set up everything quickly in VSCode, follow these steps:

1. **Create a Folder for the Project**:
   - Open VSCode.
   - Create a new folder where you want to store the project files. You can do this directly in VSCode:
     - Go to `File` > `Open Folder...`, then select or create a new folder.

2. **Clone the Repository**:
   - Open the integrated terminal in VSCode (`Ctrl+J` or `Cmd+J` on macOS).
   - Navigate to the folder you just created by running:
   
     ```bash
     cd path/to/your/folder
     ```

   - Clone the repository using the following command:
   
     ```bash
     git clone https://github.com/mcolen5050/FantasyFootballAutomation_public.git
     ```

   - Once the cloning is done, navigate to the project directory:

     ```bash
     cd FantasyFootballAutomation_public
     ```

3. **Run the `setup.sh` File**:
   - Run the `setup.sh` file to install all dependencies and set up the virtual environment:
   
     ```bash
     bash setup.sh
     ```

   - The script will automatically create and activate a virtual environment (`fantasy_env`), and install the necessary Python packages.

4. **Set Up Python Environment in VSCode**:
   - After running the `setup.sh` file, a prompt may appear in VSCode asking if you want to switch to the newly created virtual environment. If the prompt appears, select "Yes" to activate it.
   - If the prompt does **not** appear, manually set the virtual environment:
     - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) to open the Command Palette.
     - Search for `Python: Select Interpreter`.
     - Select the `fantasy_env` virtual environment associated with the project.

5. **Running the Code**:
   - Open any Python file in the repository (e.g., `main.py`).
   - At the top of the window, click the green **Run** button or press `F5` to run the file.

6. **Launching from the Terminal**:
   - You can also run the code from the built-in VSCode terminal by opening the terminal (`Ctrl+J` or `Cmd+J` on macOS) and running the Python script:
   
     ```bash
     python main.py
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
