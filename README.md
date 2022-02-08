# IMPORTANT

- Make sure before starting for the day's matches that you check back here and update if needed. You can tell by checking the Releases section and seeing if a new release has been made available.
- Make sure that you always import the lobby code instead of saving as a preset. Otherwise it may not be up-to-date.

## To setup

1. Put this folder in your Overwatch folder (usually C:/Users/User/Documents/Overwatch/). It should be in the same directory as the "Workshop" folder.
2. Enable the Workshop Inspector and Workshop Inspector Log File in your Overwatch Gameplay Settings.
3. Install Python 3 for Windows https://www.python.org/downloads/
4. (You may need to install pip, you can Google how to) Hold Left Shift, and right click in this directory and click "Open PowerShell window here". Type the command "pip install -r requirements.txt" and hit enter.

## To use

1. Create the lobby in Overwatch, and import the workshop code 9Z22B. It is important that you import this and not save it as a preset, as it will be updated throughout the week.
2. Before each match, modify the config.py file in this directory to match your team names and player names for the lobby. If you switch the sides of the teams between maps but in the same match, make sure to check and see if you need to update the config.py file.
3. Hold Left Shift, and right click in this directory and click "Open PowerShell window here". Type the command "python app.py" and hit enter. You can now minimize (but not exit) this window.
4. In your web browser, visit http://localhost:8080 and then start the lobby whenever you'd like to start collecting data.
5. When the game is done and you no longer want the data to be collected, OR you want to move to the next map, open the PowerShell window back up and hold Control + C until the program stops (the lines will stop flowing). Before starting the next map, again type "python app.py" and hit enter.

## Note

You can access raw numbers that auto-update, such as for use in a browser source in OBS, by visiting http://localhost:8080/data_json/team<TEAM_NUMBER>/player<PLAYER_NUMBER>/<STAT> where <TEAM_NUMBER> is 0 for Team 1 or 1 for Team 2, <PLAYER_NUMBER> is a number 0 through 5 which matches in-game player slots top-to-bottom 1 through 6, and <STAT> is the statistic you want to get. For example:

http://localhost:8080/data_json/team0/player0/Hero%20Damage%20Dealt

Would grab the Hero Damage Dealt for the first player on the left team (Team 1).

The list of stats you can use:

Impact Score
Hero
Hero Damage Dealt
Barrier Damage Dealt
Damage Blocked
Damage Taken
Deaths
Eliminations
Final Blows
Environmental Deaths
Environmental Kills
Healing Dealt
Objective Kills
Solo Kills
Ultimates Earned
Ultimates Used
Healing Received
Ultimate Charge