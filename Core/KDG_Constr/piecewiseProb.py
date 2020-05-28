from os import system

from .contigous import *
from .psd import *
from Core.Rapids_Classes.PieceRSDG import PieceRSDG
from Core.Util import *


def populatePieceWiseRSDG(observed, partitions, KDG, RS):
    # get the segments
    segments, seg_values, segconst, inter_coeff = generatePieceWiseContProblem(
        observed, partitions)
    costrsdg, cost_path = solveAndPopulateRSDG(segments,
                                               seg_values,
                                               segconst,
                                               inter_coeff,
                                               KDG=KDG,
                                               RS=RS)
    system("mv ./debug/max.sol ./debug/maxcost.sol")
    system("mv ./debug/fitting.lp ./debug/fittingcost.lp")
    # generate multiple RSDG
    mvprofiles = observed.genMultipleMV()
    mvrsdgs = []
    mv_paths = []
    id = 0
    for mvprofile in mvprofiles:
        # solve and retrieve the result
        segments_mv, seg_values_mv, segconst_mv, inter_coeff_mv = \
            generatePieceWiseContProblem(
                mvprofile, partitions, False)

        mvrsdg, mv_path = solveAndPopulateRSDG(segments_mv,
                                               seg_values_mv,
                                               segconst_mv,
                                               inter_coeff_mv,
                                               False,
                                               id,
                                               KDG=KDG)
        system("mv ./debug/max.sol ./debug/maxmv" + str(id) + ".sol")
        system("mv ./debug/fitting.lp ./debug/fittingmv" + str(id) + ".lp")
        mvrsdgs.append(mvrsdg)
        mv_paths.append(mv_path)
        id += 1
    return costrsdg, mvrsdgs, cost_path, mv_paths


# generate a cont problem
def generatePieceWiseContProblem(observed, partitions, COST=True):
    # genContProblem("observed.csv","quad")
    observed.printProfile("./observed.csv")
    # get the segments
    segments = getSegments(partitions)
    # get the variables
    seg_indicators, seg_values, segconst, knob_values = getVariables(
        partitions, segments)
    # get the constraints
    costConstraints, segConstraints, errors, inter_coeff = genConstraints(
        segments, observed, COST)
    # get obj functions
    obj = errorFunction(errors)
    # get the bounds
    intBounds, floatBounds = genBounds(seg_indicators, seg_values, segconst,
                                       knob_values, errors, COST)
    # beatutifyProblem
    beautifyProblem(obj, costConstraints, segConstraints, intBounds,
                    floatBounds, seg_indicators)
    return segments, seg_values, segconst, inter_coeff


# construct variables
def getSegments(samples):
    segments = {}
    for knob in samples:
        name = knob
        points = samples[name]
        segments[name] = []
        id = 0
        min = points[0]
        for i in range(1, len(points)):
            segname = name
            max = points[i]
            if max == min + 1:  # adjacent points, treated as single value
                max = min
            seg = Segment(segname, name, min, max)
            seg.setID(id)
            segments[name].append(seg)
            id += 1
            min = points[i]
            # check if the last item is adjacent to the second last
            if i == len(points) - 1 and i > 0 and points[i] == points[i -
                                                                      1] + 1:
                seg = Segment(segname, name, points[i], points[i])
                seg.setID(id)
                segments[name].append(seg)
    return segments


# construct variables
def getVariables(partitions, segments):
    seg_indicators = set()
    seg_values = set()
    seg_const = set()
    knob_values = set()
    for knob in partitions:
        name = knob
        knob_values.add(name)
    for segment in segments:
        knob_segs = segments[segment]
        for knob_seg in knob_segs:
            seg_indicators.add(knob_seg.printID())
            seg_values.add(knob_seg.printVar())
            seg_const.add(knob_seg.printConst())
    return seg_indicators, seg_values, seg_const, knob_values


# generate the error function
def errorFunction(errors):
    num = len(errors)
    obj = ""
    quadobj = "[ "
    for i in range(0, num):
        # obj += "-2 " + errors[i]
        quadobj += errors[i] + " ^ 2"
        if not (i == num - 1):
            # obj += " + "
            quadobj += " + "
    quadobj += " ] \n"
    obj += " + " + quadobj
    return obj


# construct costFunction based on modes
# mode=="piece-wise" || mode == "quadratic"
def costFunction(segments, observed):
    costFunction = ""
    if True:
        # generate piece wise linear cost fuctions
        # first_order_coeff = 0
        # const_coeff = 0
        # first order
        for configuration in observed.configurations:
            for config in configuration.retrieve_configs():
                knob_name = config.knob.set_name
                knob_val = config.val
                for seg in segments[knob_name]:
                    costFunction += str(knob_val) + " " + seg.printVar(
                    ) + " + " + str(knob_val) + " + " + seg.printID() + " + "
            costFunction = costFunction[:-3]
    return costFunction


def genConstraints(segments, observed, COST=True):
    if True:
        # generate piece wise linear cost fuctions
        costConstraints = set()
        segConstraints = set()
        inter_coeff = set()
        errors = []
        # generate the cost Constraints"
        err_id = 0
        for configuration in observed.configurations:
            costVal = 0.0
            if COST:
                costVal = observed.getCost(configuration)
            else:
                costVal = observed.getMV(configuration)
            fall_within_segs = {}
            for config in configuration.retrieve_configs():
                knob_name = config.knob.set_name
                knob_val = config.val
                for seg in segments[knob_name]:
                    if knob_val < seg.min or knob_val > seg.max:
                        continue
                    if knob_name not in fall_within_segs:
                        fall_within_segs[knob_name] = []
                    fall_within_segs[knob_name].append(seg)
                    # generate the seg Constraints
                    # posSegConstraint = seg.printID() + " = 1 -> " +
                    # seg.printVar() + " = " + knob_name
                    # negSegConstraint = seg.printID() + " = 0 -> " +
                    # seg.printVar() + " = 0"
                    # seg_sum += seg.printID() + " + "
                    # segConstraints.add(posSegConstraint)
                    # segConstraints.add(negSegConstraint)
                # seg_sum = seg_sum[:-3]
                # segConstraints.add(seg_sum+ " = 1")
                # get all combinations of fall_within_segs
            flatted_segs = getFlattedSeg(fall_within_segs)
            costEstimates = []
            for flatted_seg_list in flatted_segs:
                costEstimate = ""
                for flatted_seg in flatted_seg_list:
                    knob_val = configuration.getSetting(flatted_seg.knob_name)
                    costEstimate += str(knob_val) + " " + flatted_seg.printVar(
                    ) + " + " + flatted_seg.printConst() + " + "
                costEstimate = costEstimate[:-3]
                costEstimates.append(costEstimate)
            # generate inter-service
            inter_cost = ""
            if (not len(configuration.retrieve_configs()) == 1) and COST:
                # inter_cost = " [ "
                configs = configuration.retrieve_configs()
                total_num = len(configs)
                for i in range(0, total_num - 1):
                    s1 = configs[i].knob.set_name
                    s1_val = configs[i].val
                    for j in range(i + 1, total_num):
                        s2 = configs[j].knob.set_name
                        s2_val = configs[j].val
                        corr_a = s1 + "_" + s2 + "_a"
                        corr_b = s1 + "_" + s2 + "_b"
                        corr_c = s1 + "_" + s2 + "_c"
                        # inter_cost+=str(s1_val * s1_val) + " " + s1+"_"+s2
                        # + " + "
                        inter_cost += str(
                            s1_val * s1_val) + " " + corr_a + " + "
                        inter_cost += str(
                            s2_val * s2_val) + " " + corr_b + " + "
                        inter_cost += str(
                            s1_val * s2_val) + " " + corr_c + " + "
                        # inter_coeff.add(s1+"_"+s2)
                        inter_coeff.add(corr_a)
                        inter_coeff.add(corr_b)
                        inter_coeff.add(corr_c)
                inter_cost = inter_cost[:-3]
                # inter_cost += " ]"
            for costEstimate in costEstimates:
                err_name = "err" + str(err_id)
                err_id += 1
                errors.append(err_name)
                if not inter_cost == "":
                    costEstimate += " + " + inter_cost
                constraint = err_name + " + " + costEstimate + " = " + str(
                    costVal)
                costConstraints.add(constraint)
                # add the PSD constraints
                if not inter_cost == "":
                    constraint2 = " [ " + corr_c + " ^ 2 - " + " 4 " + corr_a \
                                  + " * " + corr_b + " ] <= 0"
                    costConstraints.add(constraint2)
    return costConstraints, segConstraints, errors, inter_coeff


# get a combination of cost estimates
def getFlattedSeg(fall_within_segs):
    finalsets = set()
    for knob in fall_within_segs:
        singleset = frozenset(fall_within_segs[knob])
        finalsets.add(singleset)
    prod = crossproduct(finalsets)
    flatted = flatAll(prod)
    return flatted


def genBounds(seg_indicators, seg_values, segconst, knob_values, errors, COST):
    integerBounds = set()
    floatBounds = set()
    # segIDs
    for seg_indicator in seg_indicators:
        bound = seg_indicator + " <= 1"
        integerBounds.add(bound)

    for seg_value in seg_values:
        if COST:
            floatBound = seg_value + " >= 0"
        else:
            floatBound = seg_value + " free"
        floatBounds.add(floatBound)
    for seg_value in segconst:
        floatBound = seg_value + " free"
        floatBounds.add(floatBound)
    # for seg_value in segconst:
    #    floatBound = "-99999 <= " + seg_value + " <= 99999"
    #    floatBounds.add(floatBound)
    # for knob_value in knob_values:
    #    floatBound = "-99999 <= " + knob_value + " <= 99999"
    #    floatBounds.add(floatBound)
    for error in errors:
        floatBound = error + " free"
        floatBounds.add(floatBound)
    return integerBounds, floatBounds


def beautifyProblem(obj, costConstraints, segConstraints, intBounds,
                    floatBounds, seg_indicators):
    probfile = open("./debug/fitting.lp", 'w')
    probfile.write("Minimize\n")
    probfile.write(obj)
    probfile.write("\nSubject To\n")
    for costConstraint in costConstraints:
        probfile.write(costConstraint)
        probfile.write("\n")
    for segConstraint in segConstraints:
        probfile.write(segConstraint)
        probfile.write("\n")
    probfile.write("Bounds\n")
    # for bound in intBounds:
    #    probfile.write(bound + "\n")
    for bound in floatBounds:
        probfile.write(bound + "\n")
    # probfile.write("Integers\n")
    # for seg in seg_indicators:
    #        probfile.write(seg + "\n")
    probfile.close()


def solveAndPopulateRSDG(segments,
                         seg_values,
                         segconst,
                         inter_coeff,
                         COST=True,
                         id=0,
                         KDG=True,
                         RS=False):
    system("gurobi_cl OutputFlag=0 LogToFile=gurobi.log "
           "ResultFile=./debug/max.sol ./debug/fitting.lp > licenseinfo")
    result = open("./debug/max.sol", 'r')
    rsdg = PieceRSDG()
    # setup the knob table
    for knob in segments:
        rsdg.addKnob(knob)
        for seg in segments[knob]:
            rsdg.addSeg(knob, seg)
    for line in result:
        col = line.split()
        if not (len(col) == 2):
            continue
        name = col[0]
        val = float(col[1])
        # if val > 9999 or val < -9999:
        #        print "found not derived value", name, val
        #            if val > 0:
        # val = 99999 - val
        # else:
        # val = -99999 - val
        if name in seg_values:
            # knob_id_V
            cols = name.split("_")
            knob_name = cols[0]
            seglist = rsdg.knob_table[knob_name]
            for seg in seglist:
                segname = seg.printVar()
                if segname == name:
                    seg.setLinearCoeff(val)
                    continue
        if name in segconst:
            # knob_id_V
            cols = name.split("_")
            knob_name = cols[0]
            seglist = rsdg.knob_table[knob_name]
            for seg in seglist:
                segname = seg.printConst()
                if segname == name:
                    seg.setConstCoeff(val)
                    continue
        if name in inter_coeff:
            cols = name.split("_")
            knob_a = cols[0]
            knob_b = cols[1]
            part = cols[2]
            rsdg.addInterCoeff(knob_a, knob_b, val, part)
    # make the coeff PSD
    if COST:
        for knob in rsdg.coeffTable:
            for dep in rsdg.coeffTable[knob]:
                coeffs = rsdg.coeffTable[knob][dep]
                a = coeffs.a
                b = coeffs.b
                c = coeffs.c
                coeffs.a, coeffs.b, coeffs.c = nearestPDcorr(a, b, c)
    file_path = rsdg.printRSDG(COST, id, KDG, RS)
    return rsdg, file_path


def modelValid(rsdg, groundTruth, PRINT):
    outfile = None
    if PRINT:
        outfile = open("outputs/modelValid.csv", 'w')
    error = 0.0
    count = 0
    for configuration in groundTruth.configurations:
        count += 1
        rsdgCost = rsdg.calCost(configuration)
        measurement = groundTruth.getCost(configuration)
        if measurement == 0:
            measurement = rsdgCost
        if measurement == 0:
            error += 0.0
        else:
            error += abs(measurement - rsdgCost) / measurement
        if PRINT:
            for config in configuration.retrieve_configs():
                outfile.write(config.knob.set_name)
                outfile.write(",")
                outfile.write(str(config.val))
                outfile.write(",")
            outfile.write(str(measurement))
            outfile.write(",")
            outfile.write(str(rsdgCost))
            outfile.write(",")
            if measurement == 0:
                outfile.write("0.0")
            else:
                outfile.write(str((measurement - rsdgCost) / measurement))
            outfile.write("\n")
    if PRINT:
        outfile.close()
    return error / count
