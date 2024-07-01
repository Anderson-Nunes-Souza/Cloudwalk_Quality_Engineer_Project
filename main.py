
games = {'timestamp': None,'event': None}

current_game = None
#Assets path to simplify to the user
assets_path = ('./assets/')

#File must be on the "Assets" folder - 
# USER CHANGE THIS ACCORDLINGLY WITH THE FILE
file_name = ('qgames.log')
i=0

file_path = (f'{assets_path}' + f'{file_name}')

try:
    #Reads the assets folder, looking for a log file and saves it to a list
    with open(file_path, 'r', encoding='cp1252') as file:
        content = file.readlines()
        #print(type(content)) #<class 'list'>

        #Splits the list information
        for line in content:
             content[i] = line.split()
             i=i+1

        # print(f'content 0: {content[0]}')#content 0: ['0:00', '------------------------------------------------------------']
        # print(f'content 1: {content[1]}')#content 1: ['0:00', 'InitGame:', '\\sv_floodProtect\\1\\sv_maxPing\\0\\sv_minPing\\0\\sv_maxRate\\10000\\sv_minRate\\0\\sv_hostname\\Code', 'Miner', 'Server\\g_gametype\\0\\sv_privateClients\\2\\sv_maxclients\\16\\sv_allowDownload\\0\\dmflags\\0\\fraglimit\\20\\timelimit\\15\\g_maxGameClients\\0\\capturelimit\\8\\version\\ioq3', '1.36', 'linux-x86_64', 'Apr', '12', '2009\\protocol\\68\\mapname\\q3dm17\\gamename\\baseq3\\g_needpass\\0']
        # print(f'content 2: {content[2]}')#content 2: ['15:00', 'Exit:', 'Timelimit', 'hit.']

except FileNotFoundError:
    print(f"Log file {file_path} not found")
except Exception as e:
    print(f'theres a error to read the file: {e}')
finally:
         print(content[0])