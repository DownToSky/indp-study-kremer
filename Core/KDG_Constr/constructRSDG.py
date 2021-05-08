from .piecewiseProb import *
from .quadProb import *
from Core.Rapids_Classes.Profile import Profile
from Core.Util import *

# contains functions to compute the representative list of a RSDG, given the
# fact profile
def constructRSDG(gt,
                  knob_samples,
                  threshold,
                  knobs,
                  PRINT,
                  model,
                  training_time_record=None,
                  seglvl=0,
                  KDG=True):
    # gT is a dictionary where entry is the config and value is hte cost
    # profile_configs is the structured configuration
    # segmentation level
    # initial error rate set to 100%
    error = 1.0
    maxT = 5
    if model == "rand20":
        # ramdom generate 20 configurations
        rand20list, partitions = gt.genRandomSubset(20)
        costrsdg, mvrsdgs, costpath, mvpaths = populate(
            rand20list, partitions, model, KDG)
        trainingsize= 20
    elif model == "quad" or model == "piecewise" or model == "allpiece":
        if model == "quad":
            maxT = 3
        if model == "allpiece":
            seglvl = 5
        if seglvl == 0 and model is not "allpiece":
            print("finding right seg lvl")
            while error >= threshold:
                if seglvl >= maxT:
                    print("Reached Highest Segmentation Granularity, error="+str(error))
                    break
                seglvl += 1
                partitions = partition(seglvl, knob_samples)
                observed_profile = retrieve(partitions, gt, knobs)
                costrsdg, mvrsdgs, costpath, mvpaths = populate(
                    observed_profile, partitions, model, KDG, False)
                error = compare(costrsdg, gt, False, model)
                print(error)
            trainingsize = len(observed_profile.configurations)
        else:
            print("prefix seg lvl:",seglvl)
            partitions = partition(seglvl, knob_samples)
            observed_profile = retrieve(partitions, gt, knobs)
            costrsdg, mvrsdgs, costpath, mvpaths = populate(
                observed_profile, partitions, model,KDG)
            trainingsize = len(observed_profile.configurations)
            error = compare(costrsdg, gt, False, model)
    elif model == "rs":
        return None, None, '', '', -1, {}, -1
    if PRINT:
        error = compare(costrsdg, gt, True, model)
        print("error = " + str(error))
    if training_time_record is not None:
        # need to compare the training time
        training_time = {}
        # the total time:
        total_time = 0.0
        for config in gt.configurations:
            name = config.printSelf('-')
            if name in training_time_record:
                total_time += training_time_record[name]
        if KDG:
            training_time['KDG'] = total_time
        else:
            training_time['FULL'] = total_time
        # the rand20 time:
        # repeat 10 times
        times = []
        for exp in range(0, 10):
            total_time = 0.0
            rand20list = map(lambda x: x.printSelf('-'),
                             gt.genRandomSubset(20)[0].configurations)
            for config in rand20list:
                total_time += training_time_record[
                    config] if config in training_time_record else 0.0
            times.append(total_time)
        training_time['rand20'] = sum(times) / float(len(times))
        # the piecewise:
        total_time = 0.0
        partitions = partition(seglvl, knob_samples)
        configlist = retrieve(partitions, gt, knobs).configurations
        for config in configlist:
            config_name = config.printSelf('-')
            total_time += training_time_record[
                config_name] if config_name in training_time_record else 0.0
        if KDG:
            training_time['PIECEWISE'] = total_time
        else:
            training_time['PIECEWISE_bb'] = total_time
        return costrsdg, mvrsdgs, costpath, mvpaths, seglvl, training_time, \
               trainingsize

    return costrsdg, mvrsdgs, costpath, mvpaths, seglvl, None, trainingsize


# given a partion level, return a list of configurations
def partition(seglvl, knob_samples):
    partitions = {}
    # seglvl indicate the number of partition lvl on each knob
    for knob in knob_samples:
        val_range = knob_samples[knob]
        length = len(val_range)
        partitions[knob] = []
        max = length - 1
        min = 0
        # determine the step size
        # num_of_partitions = 2 ** (seglvl - 1)
        # step = length / num_of_partitions -1
        # print length,num_of_partitions,step
        # if step < 1:
        #        step = 1
        #        for i in range(min, max + 1, step):
        #            print i
        ids = [min, max]
        for i in range(1, seglvl):
            new_ids = []
            for j in range(0, len(ids)):
                if j == len(ids) - 1:
                    new_ids.append(ids[j])
                    break
                new_ids.append(ids[j])
                half = (ids[j + 1] + ids[j]) / 2
                if half == ids[j]:
                    continue
                new_ids.append(half)
            ids = new_ids
        for id in ids:
            id = int(id)
            if val_range[id] not in partitions[knob]:
                partitions[knob].append(val_range[id])
    return partitions


# given a partition list, retrieve the data points in ground truth
# return a profile by observation
def retrieve(partitions, gt, knobs):
    observed_profile = Profile()
    final_sets = set()
    # partitions contains a dictionary of all knob samples
    for knob in partitions:
        samples = partitions[knob]
        single_set = []
        for sample in samples:
            single_set.append(Config(knobs.getKnob(knob), sample))
        final_sets.add(frozenset(single_set))
    product = crossproduct(final_sets)
    flatted_observed = flatAll(product)
    for config in flatted_observed:
        configuration = Configuration()
        configuration.addConfig(config)
        # filter out the invalid config, invalid if not present in groundTruth
        if not gt.hasEntry(configuration):
            print('no such configuration', configuration.printSelf())
            continue
        costval = gt.getCost(configuration)
        mvvals = gt.getMV(configuration)
        observed_profile.addCostEntry(configuration, costval)
        observed_profile.addMVEntry(configuration, mvvals)
    return observed_profile


# given an observed profile, generate the continuous problem and populate the
# rsdg
def populate(observed, partitions, model, KDG, RS=False):
    if model in ["piecewise","rand20","allpiece","rs"] :
        return populatePieceWiseRSDG(observed, partitions, KDG, RS)
    elif model == "quad":
        return populateQuadRSDG(observed, True)
    elif model == "linear":
        return populateQuadRSDG(observed, False)


def compare(rsdg, groundTruth, PRINT, model):
    if model == "piecewise" or model == 'rand20' or model == "allpiece":
        return modelValid(rsdg, groundTruth, PRINT)
    elif model == "quad":
        return compareQuadRSDG(groundTruth, rsdg, True, PRINT)
    elif model == "linear":
        return compareQuadRSDG(groundTruth, rsdg, False, PRINT)
