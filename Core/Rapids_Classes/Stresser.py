# generate a new real-app stresser
import imp, os, random
from Core.App.AppSummary import AppSummary
from Core.Util import genTrainingSet
from Core.Util import getAbsPath

class Stresser:
    APP_FILES = {
        'facedetect':
        '../data/facePort',
        'ferret':
        '../data/facePort',
        'swaptions':
        '../data/swapPort',
        'svm': '../data/svmPort'
    }

    def __init__(self, target_app):
        self.target_app = target_app
        self.apps = {}
        self.loadAll()

    def loadAll(self):
        for app_name, config_file in self.APP_FILES.items():
            if app_name == self.target_app:
                continue
            config_file = getAbsPath(config_file)
            app = AppSummary(config_file + '/config_algae.json')
            knobs, config_table, knob_samples, flatted_blackbox_training = genTrainingSet(
                getAbsPath(app.DESC))
            # groundTruth_profile contains all the config_table
            module = imp.load_source("", app.METHODS_PATH)
            appMethods = module.appMethods(app.APP_NAME, app.OBJ_PATH)
            self.apps[app_name] = {
                'appMethods': appMethods,
                'configs': list(config_table.configurations)
            }

    def getRandomStresser(self):
        app = random.choice(list(self.apps.keys()))
        configuration = random.choice(self.apps[app]['configs'])
        cmd = self.apps[app]['appMethods'].getCommand(
                configuration.retrieve_configs(), qosRun=False,
                fullRun=True)  #set to true to return the full run command
        return {
            'app': app,
            'configuration': configuration.printSelf('-'),
            'command': cmd
        }
