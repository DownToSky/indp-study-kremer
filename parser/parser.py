import json

def readConfig( configFilePath):
    with open(configFilePath) as json_file:
        data =  json.load(json_file)
        return data
    
def getVKnobs(data):
    return(data['preferences'])

def updateKnobValue(data, knobName, value):
    data[knobName] = value

def writeConfig(jFile, configFilePath):
    with open(configFilePath, 'w') as outfile:
        json.dump(jFile, outfile)


