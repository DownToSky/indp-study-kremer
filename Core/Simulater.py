import imp
import json, os
from .Rapids_Classes.PieceRSDG import PieceRSDG
from .Util import genTrainingSet, readFact
from .AppMets.AppMethods import AppMethods
from .KDG_Constr.constructRSDG import constructRSDG

THRESHOLD = 0.05
MODEL = "piecewise"

def simulateResult(configPath, budget, targetMetric, isVirtual=True):
    RAPIDS_HOME = os.environ["RAPIDS_HOME"]
    with open(configPath) as configJson:
        config = json.load(configJson)
        app_name = config['basic']['app_name']
        field = "virtual" if isVirtual else "concrete"
        preferences = config[field]
        desc = RAPIDS_HOME+"/"+config['desc']
        lvl = config['seglvl']

        # load in app met
        methods_path = config['appMet']
        module = imp.load_source("", methods_path)
        appMethod = module.appMethods("", "")

        # load in facts
        knobs, groundTruth_profile, knob_samples, bb_profile = genTrainingSet(
            desc, 10)
        readFact(RAPIDS_HOME+"/"+config['basic']['cost_path'], knobs,
                 groundTruth_profile)

        # load in all rsdgs
        cost_rsdg = PieceRSDG()
        cost_rsdg.fromFile(RAPIDS_HOME+"/"+config['cost_rsdg'])
        mv_rsdgs = {}
        for knob_name, rsdg_path in config['mv_rsdgs'].items():
            rsdg = PieceRSDG()
            rsdg.fromFile(RAPIDS_HOME+"/"+rsdg_path)
            mv_rsdgs[knob_name] = rsdg

    # normalize the pref
    min_val = min(preferences.values())
    for metric, metric_val in preferences.items():
        preferences[metric] = float(metric_val) / float(min_val)
    print("your preference,", preferences)

    factfile, mvfactfile = genFactWithRSDG(app_name, groundTruth_profile,
                                           cost_rsdg, mv_rsdgs, appMethod,
                                           preferences)
    readFact(mvfactfile, knobs, groundTruth_profile, False)
    cost, mv = groundTruth_profile.getOptimal(budget, targetMetric)
    print(targetMetric,":", mv)
    return cost/budget, mv

def genFactWithRSDG(appname, config_table, cost_rsdg, mv_rsdgs, appMethod,
                    preferences):
    # generate the fact file using existing rsdg
    cost_path = "tmp_" + appname + "-cost-gen" + ".fact"
    mv_path = "tmp_" + appname + "-mv-gen" + ".fact"
    costFile = open(cost_path, 'w')
    mvFile = open(mv_path, 'w')
    configurations = config_table.configurations
    for configuration in configurations:
        cost = cost_rsdg.calCost(configuration)
        AppMethods.writeConfigMeasurementToFile(costFile, configuration, cost)
        mvs = dict(map(lambda x: (x[0], x[1].calCost(configuration)), mv_rsdgs.items()))
        combined_mv = appMethod.computeQoSWeight(preferences, mvs)
        mvs["all"]=combined_mv
        AppMethods.writeConfigMeasurementToFile(mvFile, configuration,
                                                mvs)
    return cost_path, mv_path