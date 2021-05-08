import imp
import json, os, math
from .Rapids_Classes.PieceRSDG import PieceRSDG
from .Util import genTrainingSet, readFact
from .AppMets.AppMethods import AppMethods
from .KDG_Constr.constructRSDG import constructRSDG
from .Rapids_Classes.KDG import Configuration
from enum import Enum

THRESHOLD = 0.08
MODEL = "piecewise"
EPS = 1e-3

class ERROR_CODE(Enum):
    SUCCESS = 0
    OVER_BUDGET = 1
    INVALID = 2
    TARGET_NOT_REACHED = 4

def simulateResult(challenge, preferences):
    configPath = challenge["cfg_location"]
    budget = challenge['budget']
    targetMetric = challenge["sub-metric"]
    targetMetricValue = challenge["target"]
    isVirtual = challenge["knob_type"] == "virtual"
    RAPIDS_HOME = os.environ["RAPIDS_HOME"]
    error_code = ERROR_CODE.SUCCESS
    with open(configPath) as configJson:
        config = json.load(configJson)
        app_name = config['basic']['app_name']
        desc = RAPIDS_HOME + "/" + config['desc']

        # load in app met
        methods_path = config['appMet']
        module = imp.load_source("", methods_path)
        appMethod = module.appMethods("", "")

        # load in facts
        knobs, groundTruth_profile, knob_samples, bb_profile = genTrainingSet(
            desc, 10)
        readFact(RAPIDS_HOME + "/" + config['basic']['cost_path'], knobs,
                 groundTruth_profile)
        print("cost range:", groundTruth_profile.getCostRange())
        readFact(RAPIDS_HOME + "/" + config['basic']['mv_path'], knobs, groundTruth_profile, False)

        # load in all rsdgs
        cost_rsdg = PieceRSDG()
        cost_rsdg.fromFile(RAPIDS_HOME + "/" + config['cost_rsdg'])
        mv_rsdgs = {}
        for knob_name, rsdg_path in config['mv_rsdgs'].items():
            rsdg = PieceRSDG()
            rsdg.fromFile(RAPIDS_HOME + "/" + rsdg_path)
            mv_rsdgs[knob_name] = rsdg
            if knob_name[0] == "_":#helper
                groundTruth_profile.addMetrics([knob_name])

    if (isVirtual):
        # normalize the pref
        min_val = min(preferences.values())
        for metric, metric_val in preferences.items():
            preferences[metric] = (float(metric_val) - 1) / 100.0 * 4.0 + 1.0
        print("your preference,", preferences)
        #factfile, mvfactfile = genFactWithRSDG(app_name, groundTruth_profile,
        #                                       cost_rsdg, mv_rsdgs, appMethod,
        #                                       preferences)
        # update the mv

        for config, mvs in groundTruth_profile.mvprofile_table.items():
            new_vals = mvs[0:-1]
            # assembly the vals
            vals = {}
            for metric in mv_rsdgs.keys():
                index = groundTruth_profile.metrics[metric]
                vals[metric] = new_vals[index]
            new_vals.append(appMethod.computeQoSWeight(preferences, vals))
            groundTruth_profile.mvprofile_table[config] = new_vals
        #readFact(mvfactfile, knobs, groundTruth_profile, False)
        #new_cost_rsdg, new_mv_rsdgs, _, _, _, _, _ = constructRSDG(
        #    groundTruth_profile, knob_samples, THRESHOLD, knobs, True,
        #    MODEL, None)
        groundTruth_profile.printProfile("debug/tmp-profile.txt")
        # find the optimal solution
        #optimal_config = getOptimalSolution(groundTruth_profile.configurations, budget, cost_rsdg, new_mv_rsdgs[-1])
        final_cost, final_mv, optimal_config, all_mvs = groundTruth_profile.getOptimal(budget, targetMetric)
        print(all_mvs)
        # get the sub-metrics
        #mvs = groundTruth_profile.getMV(optimal_config)
        #final_cost = groundTruth_profile.getCost(optimal_config)
        #final_mv = mvs[groundTruth_profile.metrics[targetMetric]]

    else:
        configs = {}
        # construct the knob actual value
        for k, v in preferences.items():
            knob_min = knobs.getKnob(k).min
            knob_max = knobs.getKnob(k).max
            # get the closest config available
            total_settings = len(knob_samples[k])
            index = int(total_settings * float(v) / 100.0)
            configs[k] = knob_samples[k][index-1]
        print("your config:", configs)
        # assembly a tmp configuration
        optimal_config = Configuration()
        optimal_config.genTmpConfigfromMap(configs)
        # calculate the cost
        if not groundTruth_profile.hasEntry(optimal_config):
            return -1, -1, ERROR_CODE.INVALID
        final_cost = groundTruth_profile.getCost(optimal_config)
        if final_cost > budget:
            error_code = ERROR_CODE.OVER_BUDGET
            final_mv = -1
        else:
            mv_index = groundTruth_profile.metrics[targetMetric]
            mvs = groundTruth_profile.getMV(optimal_config)
            final_mv = mvs[mv_index]
            optimal_config = optimal_config.printSelf(",")

    print(targetMetric, ":", final_mv, "cost:", final_cost, "config:", optimal_config)

    # summarize the result
    budget_util = final_cost / float(budget)
    if budget_util > 1.0:
        error_code = ERROR_CODE.OVER_BUDGET
    elif abs(final_mv-targetMetricValue)>EPS:
        print(abs(final_mv-targetMetricValue))
        error_code = ERROR_CODE.TARGET_NOT_REACHED
    return final_mv, budget_util, error_code


def getOptimalSolution(configurations, budget, cost_rsdg, mv_rsdg):
    best_config = None
    max_mv = -1 * math.inf
    for configuration in configurations:
        cost = cost_rsdg.calCost(configuration)
        if cost > budget:
            continue
        if mv_rsdg.calCost(configuration) > max_mv:
            best_config = configuration
    return best_config


def genFactWithRSDG(appname, config_table, cost_rsdg, mv_rsdgs, appMethod,
                    preferences):
    # generate the fact file using existing rsdg
    cost_path = "debug/tmp_" + appname + "-cost-gen" + ".fact"
    mv_path = "debug/tmp_" + appname + "-mv-gen" + ".fact"
    costFile = open(cost_path, 'w')
    mvFile = open(mv_path, 'w')
    configurations = config_table.configurations
    for configuration in configurations:
        cost = cost_rsdg.calCost(configuration)
        AppMethods.writeConfigMeasurementToFile(costFile, configuration, cost)
        mvs = dict(map(lambda x: (x[0], x[1].calCost(configuration)), mv_rsdgs.items()))
        combined_mv = appMethod.computeQoSWeight(preferences, mvs)
        mvs["all"] = combined_mv
        mv_list = [0.0] * len(mvs)
        for metric, mv in mvs.items():
            if (metric[0] == '_'):# helper rsdg
                continue
            if (metric == "all"):
                index = -1
            else:
                index = config_table.metrics[metric]
            mv_list[index] = mv
        AppMethods.writeConfigMeasurementToFile(mvFile, configuration,
                                                mv_list)
    return cost_path, mv_path
