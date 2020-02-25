import re

def getConfigFile(filename):
    config_file = open(filename,"r")
    return config_file

def parseFile( configFile):
    for line in configFile:
        for word in line.split():
            if(re.match('\"preferences\"', word)!= None):
               tokenArr =  re.split('[":,{}]', line)
               tokenArr = list(filter(None, tokenArr))
               tokenArr = [token for token in tokenArr if token.strip()]
               map = (generateMap(tokenArr))
               break
                   
    configFile.close()
    return map

def generateMap(tokenArr):
    print(tokenArr)
    index = 1;
    hashmap = {}

    while(index < len(tokenArr)):
        key = tokenArr[index]
        index +=1
        val = tokenArr[index]
        hashmap[key] = val
        index +=1
    return hashmap

def parse():
    return parseFile(getConfigFile("ferret_run.config"))


