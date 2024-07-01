
#Reads the assets folder, looking for a log file
file = open("./assets/qgames.log", "r", encoding="cp1252")
content = file.read()

#prints the content of the log file
print(content)

file.close()