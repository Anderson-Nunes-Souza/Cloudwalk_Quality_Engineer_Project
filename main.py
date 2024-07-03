import re

games = []
current_game = None

#Assets path to simplify to the user
assets_path = ('./assets/')

#File must be on the "Assets" folder - 
# USER CHANGE THIS ACCORDLINGLY WITH THE FILE
file_name = ('qgames.log')

file_path = (f'{assets_path}' + f'{file_name}')

try:
    #Reads the assets folder, looking for a log file and saves it to a list
    with open(file_path, 'r', encoding='cp1252') as file:
        content = file.readlines()

        #Splits the list information
        for line in content:
            line = line.split()

            if not line:
                continue
             
             #identifies Start game
            if "InitGame:" in line:
                if current_game is not None:
                    #Adds the line to the games list
                    games.append(current_game)
                current_game = {
                    'players':{},
                    'kills_total':0
                }
            
            #Identifies the end of a Game
            elif "ShutdownGame:" in line:
                if current_game is not None:
                        games.append(current_game)
                        current_game=None

            #Collects players info
            elif "ClientUserinfoChanged:" in line:
                player_id = line[2]
                regex = 'r"n\\(.+?)\\t"'
                new_line = ' '.join(line[3:])

                #Regex to adjust Player's Names with spaces
                player_name = re.search(r'n\\(.*?)\\t', new_line)
                player_name = player_name.group(1)

                if player_id not in current_game["players"]:
                    current_game["players"] = {
                        "player_id": player_id,
                        "name": player_name,
                        "kills": 0
                    }
                else:
                    current_game["players"][player_id]["name"] = player_name
            
            #Collects the kill Information
            elif "killed" in line:
                if current_game is not None:
                    parts = line

                    #join to adjust the Player's Names with spaces
                    killer_name = ' '.join(parts[5:parts.index('killed')])
                    killed_index = parts.index('killed') +1
                    by_index = parts.index('by')
                    victim_name = ' '.join(parts[killed_index:by_index])

                # Verifies if the killer name is different from the victim name
                # and add +1 to the game kill count
                if killer_name != victim_name:
                    current_game["kills_total"] += 1

                    #Runs the current game itens list
                    for key, value in current_game.items():

                        #Verifies if the name is present in the current game lists of names
                        #and if its the same, adds +1 to the player killcount
                        if isinstance(value, dict):
                            if 'name' in value:
                                if killer_name == value['name']:
                                    current_game["players"]["kills"] += 1
            

    #Add the last game case it was not
    if current_game is not None:
        games.append(current_game)

    #Showing the results
    for i, game in enumerate(games, 1):
        print(f"Game {i}:")
        print(f"  Total Kills: {game['kills_total']}")
        print("  Players: {")
        for player_id, player_info in game["players"].items():
            print(f"    {player_info['name']}: \n   {player_info['kills']} kills \n")
        print(' }')

except FileNotFoundError:
    print(f"Log file {file_path} not found")
except Exception as e:
    print(f'theres a error to read the file, please verify if the file is correct: {e}')