import re
import json

games = []

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

#Identifies the Start of a Game
def identifiesStartGame(line,current_game):
    if "InitGame:" in line:
            if current_game is not None:
                #Adds the line to the games list
                games.append(current_game)
            current_game = {
                'kills_total': 0,
                'players':[],
                'kills': {},
            }
    return current_game

#Identifies the end of a Game
def identifiesEndGame(line, current_game):
    if "ShutdownGame:" in line:
        if current_game is not None:
            games.append(current_game)
            current_game=None
    return current_game

#Collects players info
def collectsPlayersInfo(line, current_game, regex):
    
    if "ClientUserinfoChanged:" in line:
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
    return current_game

#Collects the kill Information
def collectsKillInformation(line, current_game):
        if "killed" in line:
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
        return current_game

#Exibihit the end Result     
def showResults():
    x=0
    for game in games:
        data = json.dumps(game, indent=3)
        print(f'game_{x+1}')
        print(data)
        x+=1
        
#Main Function
def main():
    try:
        current_game = None
        regex = 'r"n\\(.+?)\\t"'
        content = readfile()

        #Splits the list information
        for line in content:
            line = line.split()
            if not line:
                continue
            #Executes all the verifications for the Script
            current_game = identifiesStartGame(line,current_game) 
            current_game = identifiesEndGame(line, current_game)
            current_game = collectsPlayersInfo(line, current_game, regex)
            current_game = collectsKillInformation(line, current_game)
    
    #Treats the files Errors and exceptions
    except FileNotFoundError:
        print(f"Log file {file_path} not found")
    except Exception as e:
        print(f'theres a error to read the file, please verify if the file is correct: {e}')
    #Showr the Final Results
    finally:
        showResults()

if __name__ == "__main__":
    main()