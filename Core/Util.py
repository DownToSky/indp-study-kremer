import itertools
import numpy as np
from .Rapids_Classes.KDG import *
from .Rapids_Classes.Profile import Profile


# stage_1 generate valid training set from constraints
def genTrainingSet(cfg_file, granularity=10):
    config_file = open(cfg_file, 'r')  # input file
    # parsing the file
    knobs, and_constriants, or_constraints, sub_metrics = processFile(config_file)
    # generate the training
    all_training, knob_samples = genAllTraining(knobs, granularity)
    # flat the all_training
    flatted = flatAll(all_training)
    # filter out the invalid configs
    flatted_all_training = Profile()
    flatted_all_training.setMetrics(sub_metrics)
    flatted_blackbox_training = Profile()
    invalid = 0
    for config in flatted:
        configuration = Configuration()
        configuration.addConfig(config)
        if validate(config, knobs, and_constriants, or_constraints):
            # add the list to configs
            flatted_all_training.addCostEntry(configuration, 0.0)
        else:
            invalid += 1
        flatted_blackbox_training.addCostEntry(configuration, 0.0)
    print("total: " + str(len(flatted)) + " omitted:" + str(invalid) + " / final:" + str(len(flatted) - invalid))
    # prepare a Knobs
    knobs_class = Knobs()
    for k in knobs:
        knobs_class.addKnob(k)
    return knobs_class, flatted_all_training, knob_samples, flatted_blackbox_training


# read in a description file
def processFile(cfg_file):
    knobs = set()
    and_constriants = set()
    or_constraints = set()
    subs = []
    for line in cfg_file:
        col = line.split(' ')
        if col[0] == "submetrics:":  # sub metrics
            subs = col[1].split(',')
        if len(col) == 4:  # knob definition
            knob_name = col[0]
            setting = col[1]
            setting_min = col[2]
            setting_max = col[3]
            print
            knob_name
            knobs.add(Knob(knob_name, setting, setting_min, setting_max))
        elif len(col) == 7:  # it's a edge
            type = col[0]
            sink = col[1]
            source = col[2]
            source_min = col[5]
            source_max = col[6]
            sink_min = col[3]
            sink_max = col[4]
            if type == "or":
                or_constraints.add(
                    Constraint(type, source, sink, source_min, source_max,
                               sink_min, sink_max))
            else:
                and_constriants.add(
                    Constraint(type, source, sink, source_min, source_max,
                               sink_min, sink_max))
    return knobs, and_constriants, or_constraints, subs


# flat a single tuple
def flat(tup, finallist):
    if type(tup) is tuple:
        if (len(tup) == 0):
            return
        flat(tup[0], finallist)
        flat(tup[1:], finallist)
    else:
        finallist.append(tup)


# flatten a list of tuples
def flatAll(listOfTuples):
    result = []
    for t in listOfTuples:
        tmp_result = []
        flat(t, tmp_result)
        result.append(tmp_result)
    return result


# generate all possible combinations given a set of knobs
# return:
# product - a cross product containing bunch of Configurations
# knob_samples - a disctionary contains all sampled configs
def genAllTraining(knobs, granularity):
    final_sets = set()
    knob_samples = {}
    for knob in knobs:
        single_set = []
        name = knob.set_name
        v_min = int(knob.min)
        v_max = int(knob.max)
        # if less than 'granularity', select all
        knob_vs = np.linspace(v_min, v_max, num=min(granularity, (v_max - v_min + 1)))
        # step = (max - min) / (granularity-1.0)
        # if step < 1:
        #    step = 1
        # print "step size for "+name + "is " + str(step)
        # knob_samples[name] = []
        # i = min
        # single_set.append(Config(knob, int(i)))
        # knob_samples[name].append(int(i))
        # while i < max:
        #     i = i + step
        #     if i + step > max:
        #         i = max
        #     single_set.append(Config(knob, int(i)))
        #     knob_samples[name].append(int(i))
        knob_samples[name] = list(map(lambda x: int(x), knob_vs))
        single_set = list(map(lambda x: Config(knob, int(x)), knob_vs))
        frozen_single = frozenset(single_set)
        final_sets.add(frozen_single)
    product = crossproduct(final_sets)
    return product, knob_samples


# do a cross product of a set of configuration lists
def crossproduct(final_sets):
    pro = {}
    inited = False
    for i in final_sets:
        if inited:
            pro = itertools.product(pro, i)
        else:
            # print "init pro"
            pro = i
            inited = True
    return pro


# validate if a config is valid
def validate(configs, knobs, and_constraints, or_constraints):
    config_map = dict()
    # setup the map
    for config in configs:
        config_map[config.knob.set_name] = config.val
    # iterate through range constraints
    for knob in knobs:
        set_name = knob.set_name
        set_min = knob.min
        set_max = knob.max
        if not (set_name in config_map.keys()):
            print
            "configuration does not have such setting name:" + set_name
            return False
        set_val = int(config_map[set_name])
        if set_val < set_min or set_val > set_max:
            print
            "configuration exeeds range" + str(set_val) + ":" + str(
                set_min) + "->" + str(set_max)
            return False
    # iterate through and_constraints
    for and_cons in and_constraints:
        # for each and_constraint, check whether the config satisfy
        source = and_cons.source
        sink = and_cons.sink
        source_min = and_cons.source_min
        sink_min = and_cons.sink_min
        source_max = and_cons.source_max
        sink_max = and_cons.sink_max
        # now check
        if not (sink in config_map and source in config_map):
            # this is assume to be a valid setting
            print
            "cannot find sink or source in config+map"
            return True
        sink_val = config_map[sink]
        source_val = config_map[source]
        if sink_val >= sink_min and sink_val <= sink_max:
            if source_val < source_min or source_val > source_max:
                return False
    # iterate through or_constraints
    # TBD
    return True


# write out to the training file
def beautifyAndWriteOut(empty_profile, outfile):
    output_buffer = set()
    flatted_configurations = empty_profile.profile_table
    for configuration_string in flatted_configurations:
        # config_list = configuration.retrieve_configs()
        # tmp_output = ""
        # for i in range(len(config_list)):
        #    tmp_output+=config_list[i].knob.set_name + "," + str(
        #    config_list[i].val)
        #    if not (i == len(config_list)-1):
        #        tmp_output+=","
        output_buffer.add(configuration_string)
    for o in sorted(output_buffer):
        outfile.write(o)
        outfile.write("\n")


def is_float(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


# read in a fact and generate a dictionary where the key is a config set,
# and the value is the cost
def readFact(fact_file, knobs, gt, COST=True):
    fact = open(fact_file, 'r')
    if fact is None:
        print
        "RAPID-C / STAGE-4 : reading trained profile failed"
        return
    for line in fact:
        col = line.split()
        knob_name = ""
        knob_val = 0.0
        configuration = Configuration()
        is_digit = False
        vals = []
        for i in range(len(col)):
            if col[i].isdigit() or is_float(col[i]):
                if is_digit:
                    # this is the start of values
                    for j in range(i, len(col)):
                        vals.append(col[j])
                    break
                is_digit = True
                knob_val = int(col[i])
                configuration.addConfig(
                    [Config(knobs.getKnob(knob_name), knob_val)])
                continue
            else:
                is_digit = False
                knob_name = col[i]
        if not gt.hasEntry(configuration):
            continue
        if COST:
            gt.setCost(configuration, float(vals[0]))
        else:
            gt.setMV(configuration, list(map(lambda x: float(x), vals)))
    if COST:
        print("Cost file loaded, total:" + str(len(gt.configurations)))
    else:
        print("MV file loaded, total:" + str(len(gt.configurations)))
    return


def getAbsPath(path):
    if path[0] == '/':  # this is an absolute path
        return path
    RAPIDS_HOME = os.environ["RAPIDS_HOME"]
    return RAPIDS_HOME + "/" + path
