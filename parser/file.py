import re

def getConfigFile(filename):
    config_file = open(filename,"r")
    return config_file

def parseFile( configFile):
    for line in configFile:
        for word in line.split():
            if(re.match('\"preferences\"', word)!= None):
               for token in  line.split('" '):
                   print(token)
                   #generate map entry
                   
    configFile.close()



parseFile(getConfigFile("ferret_run.config"))
