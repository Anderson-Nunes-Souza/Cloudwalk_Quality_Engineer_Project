import re
import json

games = []
current_game = None

#Assets path to simplify to the user
assets_path = ('./assets/')

#File must be on the "Assets" folder - 
# USER CHANGE THIS ACCORDLINGLY WITH THE FILE
file_name = ('qgames.log')

file_path = (f'{assets_path}' + f'{file_name}')
    
#Reads the assets folder, looking for a log file and saves it to a list
def readfile():
    with open(file_path, 'r', encoding='cp1252') as file:
        content = file.readlines()
    return content

try:
    content = readfile()
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
                'kills_total': 0,
                'players':[],
                'kills': {},
            }
        
        #Identifies the end of a Game
        elif "ShutdownGame:" in line:
            if current_game is not None:
                    games.append(current_game)
                    current_game=None

        #Collects players info
        elif "ClientUserinfoChanged:" in line:
            #player_id = line[2]
            regex = 'r"n\\(.+?)\\t"'
            new_line = ' '.join(line[3:])

            #Regex to adjust Player's Names with spaces
            player_name = re.search(r'n\\(.*?)\\t', new_line)
            player_name = player_name.group(1)
            existPlayer = False
            if len(current_game['players']) == 0:
                current_game['players'].append(player_name)
                current_game['kills'][player_name]=0
            else:
                for player in current_game['players']:
                    if player == player_name:
                        existPlayer = True
                if not existPlayer:
                    current_game["players"].append(player_name)
                    current_game['kills'][player_name]=0            
            

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
            # and add +1 to the the player kill count and adds the game killcount too
            if killer_name != victim_name:
                current_game["kills_total"] += 1
                kill_count = 0
                if '<world>' != killer_name:
                    killer = killer_name
                    kill_count = 1
                else:
                    killer = victim_name 
                    kill_count = -1
                current_game['kills'][killer] += kill_count

#     #Exibihit the end Result     
    x=0
    for game in games:
        data = json.dumps(game, indent=3)
        print(f'game_{x+1}')
        print(data)
        x+=1

except FileNotFoundError:
    print(f"Log file {file_path} not found")
except Exception as e:
    print(f'theres a error to read the file, please verify if the file is correct: {e}')