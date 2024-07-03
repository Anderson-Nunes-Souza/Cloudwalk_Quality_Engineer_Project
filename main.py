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
        #print(type(content)) #<class 'list'>

        #Splits the list information
        for line in content:
            line = line.split()
            #print(type(line)) #list
            if not line:
                continue
             
             #identifies Start game
            if "InitGame:" in line:
                if current_game is not None:
                    #Adds the line to the games list
                    games.append(current_game)
                current_game = {
                    'players':{},
                    'kills':0
                }
            
            #Identifies the end of a Game
            elif "ShutdownGame:" in line:
                if current_game is not None:
                        games.append(current_game)
                        current_game=None
            #Collects players info
            elif "ClientUserinfoChanged:" in line:
                #print(f'linha 45 {line}')
                player_id = line[2]
                regex = 'r"n\\(.+?)\\t"'
                new_line = ' '.join(line[3:])
                #print(f'linha 49 {new_line}')
                #match = re.search(regex, new_line)

                #Regex to adjust Player's Names with spaces
                player_name = re.search(r'n\\(.*?)\\t', new_line)
                player_name = player_name.group(1)
                #print(f'linha 54: {player_name.group(1)}')
                if player_id not in current_game["players"]:
                    current_game["players"][player_id] = {
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
# 12
#  linha 57: ['14:46', 'Kill:', '3', '8', '10:', 'Dono', 'da', 'Bola', 'killed', 'Mal', 'by', 'MOD_RAILGUN']
# 12
#  linha 57: ['15:17', 'Kill:', '7', '7', '7:', 'Assasinu', 'Credi', 'killed', 'Assasinu', 'Credi', 'by', 'MOD_ROCKET_SPLASH']
# linha 57: ['15:13', 'Kill:', '3', '8', '10:', 'Dono', 'da', 'Bola', 'killed', 'Mal', 'by', 'MOD_RAILGUN']
                    victim_name = parts[7]
                if killer_name != victim_name:
                    current_game["kills"] += 1
                if killer_name in current_game["players"]:
                    current_game["players"][killer_name]["kills"] += 1            
            

    # Add the last game case it was not
    if current_game is not None:
        games.append(current_game)

    #Showing the results
    for i, game in enumerate(games, 1):
        #print(game) #{'players': {}, 'kills': 94}
        print(f"Game {i}:")
        print(f"  Total Kills: {game['kills']}")
        print("  Players: {")
        for player_id, player_info in game["players"].items():
            print(f"    {player_info['name']}: \n   {player_info['kills']} kills \n")
        print(' }')

        #print(f'content 0: {content[0]}')#content 0: ['0:00', '------------------------------------------------------------']
        #print(f'content 1: {content[1]}')#content 1: ['0:00', 'InitGame:', '\\sv_floodProtect\\1\\sv_maxPing\\0\\sv_minPing\\0\\sv_maxRate\\10000\\sv_minRate\\0\\sv_hostname\\Code', 'Miner', 'Server\\g_gametype\\0\\sv_privateClients\\2\\sv_maxclients\\16\\sv_allowDownload\\0\\dmflags\\0\\fraglimit\\20\\timelimit\\15\\g_maxGameClients\\0\\capturelimit\\8\\version\\ioq3', '1.36', 'linux-x86_64', 'Apr', '12', '2009\\protocol\\68\\mapname\\q3dm17\\gamename\\baseq3\\g_needpass\\0']
        #print(f'content 2: {content[2]}')#content 2: ['15:00', 'Exit:', 'Timelimit', 'hit.']

except FileNotFoundError:
    print(f"Log file {file_path} not found")
except Exception as e:
    print(f'theres a error to read the file, please verify if the file is correct: {e}')