class Config:

    # Player order: Main Tank, Off Tank, Hitscan DPS, Flex DPS, Main Support, Flex Support
    ## This should match the ordering of player slots in the lobby, from top to bottom.
    ## In lobby, Team 1 is the team on the left, Team 2 is the team on the right.
	## TEAM NAMES MUST MATCH LOBBY TEAM NAMES!

    Teams = ['Team 1', 'Team 2']
    Players = [[
        'Player1', 'Player2', 'Player3', 'Player4', 'Player5', 'Player6'
    ], ['Player1', 'Player2', 'Player3', 'Player4', 'Player5', 'Player6']]
