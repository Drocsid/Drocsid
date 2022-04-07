import os

def findInPref(target,prefix):
    for path, dirs, files in os.walk(prefix):
        if target in dirs:
            return os.path.join(path, target)p

def findSteam():
    PREFIXES =['C:\\','D:\\']
    for prefix in PREFIXES:
        output = findInPref('Steam',prefix)
        if output:
            return output
    
    
    
def getSteamFils():
    steampwd = findSteam()
    os.chdir(steampwd)
    files = []
    for file in os.listdir():
        if file.startswith('ssfn'):
            files.append(steampwd+ '\\' + file)
    return files