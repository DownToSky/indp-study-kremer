from os import system
from Core.Rapids_Classes.QuadRSDG import QuadRSDG
from .psd import *
from Core.Util import *


def populateQuadRSDG(observed, quad):
    # get the segments
    paras, quadpara = genQuadContProblem(observed, quad, True)  # Ture = cost
    system("gurobi_cl OutputFlag=0 LogToFile=gurobi.log "
           "ResultFile=./debug/max.sol ./debug/fitting.lp")
    costrsdg = getContRSDG(paras, quadpara, quad, True)
    system("mv ./debug/max.sol ./debug/maxcost.sol")
    system("mv ./debug/fitting.lp ./debug/fittingcost.lp")
    paras, quadpara = genQuadContProblem(observed, quad, False)  # Ture = quad
    system("gurobi_cl BarHomogeneous=1 OutputFlag=0 LogToFile=gurobi.log "
           "ResultFile=./debug/max.sol ./debug/fitting.lp")
    mvrsdg = getContRSDG(paras, quadpara, quad, False)
    system("mv ./debug/max.sol ./debug/maxmv.sol")
    system("mv ./debug/fitting.lp ./debug/fittingmv.lp")
    return costrsdg, mvrsdg


# Tools needed for generating QUAD contigous RSDG
# observed is a file
def genQuadContProblem(observed, quad, COST):
    prob = open("./debug/fitting.lp", 'w')
    constraints, paras, quadparas, errors = readContFactAndGenConstraint(
        observed, quad, COST)
    # write obj, err^2 - 2 err +1
    quadobj = "[ "
    for err in errors:
        quadobj += err + " ^ 2 + "
    quadobj = quadobj[:-3]
    quadobj += " ]\n"
    prob.write("Minimize\n")
    prob.write(quadobj + "\n")
    # write constraint
    prob.write("Subject To\n")
    for c in constraints:
        prob.write(c)
        prob.write("\n")
    # write Bounds
    bounds = genBounds(errors, paras)
    prob.write(bounds)
    prob.close()
    return paras, quadparas


def genBounds(errors, paras):
    bounds = "Bounds \n"
    for err in errors:
        # the quad term has to be greater than 0
        bounds += "-9999 < " + err + " < 9999\n"
    return bounds


def getContRSDG(paras, quadparas, quad, COST):
    result = open("./debug/max.sol", 'r')
    rsdg = QuadRSDG()
    for line in result:
        col = line.split()
        if not (len(col) == 2):
            continue
        name = col[0]
        val = col[1]
        if name in paras:
            curPara = name.split("_")
            knob = curPara[0]
            coeff = curPara[1]
            lvl = 0
            dependent = ""
            if coeff == "2":
                lvl = 2
            elif coeff == "1":
                lvl = 1
            elif coeff == "c":
                lvl = 0
            if not knob in rsdg.knob_table:
                rsdg.addKnob(knob)
            if not lvl == -1:
                rsdg.addKnobVal(knob, float(val), coeff)
        if name in quadparas:
            curPara = name.split("_")
            knob_a = curPara[0]
            knob_b = curPara[1]
            part = curPara[2]
            rsdg.addInterCoeff(knob_a, knob_b, part, float(val))
    # make the coefficients PSD
    if quad:
        for knob in rsdg.coeffTable:
            for dep in rsdg.coeffTable[knob]:
                coeffs = rsdg.coeffTable[knob][dep]
                a = coeffs.a
                b = coeffs.b
                c = coeffs.c
                coeffs.a, coeffs.b, coeffs.c = nearestPDcorr(a, b, c)
                print
                "before"
                print
                a, b, c
                print
                "after PSD"
                print
                coeffs.a, coeffs.b, coeffs.c
    rsdg.printRSDG(COST)
    return rsdg
    # now check the rate


def compareQuadRSDG(groundTruth, rsdg, quad, PRINT):
    outfile = None
    if PRINT:
        outfile = open("outputs/modelValid.csv", 'w')
    error = 0.0
    count = 0
    for configuration in groundTruth.configurations:
        count += 1
        rsdgCost = rsdg.calCost(configuration)
        measurement = groundTruth.getCost(configuration)
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
            outfile.write(str((measurement - rsdgCost) / measurement))
            outfile.write("\n")
    if PRINT:
        outfile.close()
        print
        error / count
    return error / count
    #
    # fact = open(factfile, "r")
    # rsdg = open("./outputs/rsdgcont", 'w')
    # rsdg_map = {}
    # relation_map = {}
    # report = open("./outputs/ModelValid.csv",'w')
    # total = 0.0
    # totErr = 0.0
    # for line in fact:
    #     total += 1
    #     col = line.split(',')
    #     curPredict = 0.0
    #     curService = ""
    #     value_map = {}
    #     for i in range(0,len(col)):
    #         if(i == len(col)-1):
    #             # add the interrelation
    #             if quad:
    #                 for svc in value_map.items():
    #                     svc_name = svc[0]
    #                     svc_val = svc[1]
    #                     for dep in relation_map[svc_name].items():
    #                         dep_name = dep[0]
    #                         inter_val = dep[1]
    #                         curPredict+=svc_val * inter_val * value_map[
    #                         dep_name]
    #             measurement = float(col[i])
    #             abs_err = abs((measurement - curPredict)/measurement)
    #             totErr += abs_err
    #             report.write(str(curPredict) + "," + str(measurement) + ",
    #             " + str(1.0-abs_err) + "\n")
    #             curService = ""
    #             curPredict = 0.0
    #             break
    #         if (col[i].isdigit() and curService!=""):
    #             val = float(col[i])
    #             value_map[curService] = float(col[i])
    #             if quad:
    #                 o2 = rsdg_map[curService][2]
    #             o1 = rsdg_map[curService][1]
    #             c = rsdg_map[curService][0]
    #             if quad:
    #                 curPredict += o2*val*val + o1*val + c
    #             else:
    #                 curPredict += o1*val + c
    #         else:
    #             curService = col[i]
    # report.write("Mean Error:" + str(totErr / total))
    # report.close()


def readContFactAndGenConstraint(observed, quad, COST):
    errors = set()
    constraints = set()  # list of constraints
    paras = set()  # set of parameters, o2, o1, and c for each service
    quadparas = set()
    # added this for inter-relationship higher order constraint
    err_id = 0
    knobs = []
    for configuration in observed.configurations:
        costVal = 0.0
        if COST:
            costVal = observed.getCost(configuration)
        else:
            costVal = observed.getMV(configuration)
        costestimate = ""
        quadconstraint = ""  # this is the inter-service relationship
        # generate all single service terms
        for config in configuration.retrieve_configs():
            knob_name = config.knob.set_name
            if not knob_name in knobs:
                knobs.append(knob_name)
            knob_val = config.val
            costestimate += str(
                knob_val) + " " + knob_name + "_1 + " + knob_name + "_c + "
            paras.add(knob_name + "_1")
            paras.add(knob_name + "_c")
            if quad:
                costestimate += str(
                    knob_val * knob_val) + " " + knob_name + "_2" + " + "
                paras.add(knob_name + "_2")
        costestimate = costestimate[:-3]
        # generate all inter service terms
        inter_cost = ""
        configs = configuration.retrieve_configs()
        length = len(configs)
        if quad and (not length == 1) and COST:
            total_num = length
            for i in range(0, length - 1):
                knoba = configs[i].knob.set_name
                knoba_val = configs[i].val
                for j in range(i + 1, length):
                    knobb = configs[j].knob.set_name
                    knobb_val = configs[j].val
                    corr_a = knoba + "_" + knobb + "_a"
                    corr_b = knoba + "_" + knobb + "_b"
                    corr_c = knoba + "_" + knobb + "_c"
                    inter_cost += str(
                        knoba_val * knoba_val) + " " + corr_a + " + "
                    inter_cost += str(
                        knobb_val * knobb_val) + " " + corr_b + " + "
                    inter_cost += str(
                        knoba_val * knobb_val) + " " + corr_c + " + "
                    quadparas.add(corr_a)
                    quadparas.add(corr_b)
                    quadparas.add(corr_c)
            inter_cost = inter_cost[:-3]
        err_name = "err" + str(err_id)
        err_id += 1
        errors.add(err_name)
        if quad:
            quadconstraint += inter_cost
        if quad and (not quadconstraint == ""):
            costestimate += " + " + quadconstraint
        constraint = err_name + " + " + costestimate + " = " + str(costVal)
        constraints.add(constraint)
        # Inter PSD
        if not inter_cost == "":
            constraint2 = " [ " + corr_c + " ^ 2 - " + " 4 " + corr_a + " * " \
                          + corr_b + " ] <= 0"
            constraints.add(constraint2)
    return constraints, paras, quadparas, errors


# A function that generates cost / qual function in a way that Gurobi
# understands
def readContFactAndGenModConstraint(fact):
    services = {}
    constraints = []  # list of constraints
    paras = set()  # set of parameters, o2, o1, and c for each service
    # added this for inter-relationship higher order constraint
    num = 0
    f = open(fact, 'r')
    for line in f:
        col = line.split(',')
        length = len(col)
        involved_services = []  # a list of involved services
        constraint = ""
        quadconstraint = ""  # this is the inter-service relationship
        for i in range(0, length):
            if i == length - 1:
                constraint += " err" + str(num + 1) + " + "
                # the last column which is the cost
                cost = float(col[i])
                # construct the quadconstraint that has PSD property
                # first construct the Svc ^ 2
                # for service in involved_services:
                #    quadconstraint += str(services[service] * services[
                #    service]) + " " + service+"_o2 " + " + "
                # then construct the inter relation
                quadconstraint += " [ "
                for i in range(0, len(involved_services) - 1):
                    cur_service = involved_services[i]
                    for j in range(i + 1, len(involved_services)):
                        inter_service = involved_services[j]
                        quadterm = cur_service + "_" + inter_service
                        quadterm_t = inter_service + "_" + cur_service
                        val = services[cur_service]
                        val_inter = services[inter_service]
                        # print(val,val_inter,2*val*val_inter)
                        quad_cons = str(
                            val * val) + " " + quadterm + " ^ 2 + " + str(
                            val_inter * val_inter) + " " + quadterm_t + " ^ 2 " \
                                                                        "" \
                                                                        "" \
                                                                        "" \
                                                                        "- " \
                                    + str(
                            2 * val_inter * val) + " " + quadterm + " * " + \
                                    quadterm_t + " + "
                        quadconstraint += quad_cons
                # clean the quad constraint
                length = len(quadconstraint)
                quadconstraint = quadconstraint[:length - 2]
                quadconstraint += " ] "
                # append the quadconstraint to constraint
                constraint += quadconstraint
                # greater_constraint = constraint + " >= "+str(cost-0.1)+"\n"
                smaller_constraint = constraint + " <= " + str(cost +
                                                               0.1) + "\n"
                # constraints.append(greater_constraint)
                constraints.append(smaller_constraint)
                # clear the constraint
                constraint = ""
                quadconstraint = ""
                services.clear()
                involved_services = []
                continue
            cur = col[i]
            if not (cur.isdigit()):  # this is a service name
                name = cur
                involved_services.append(name)
            else:
                value = float(cur)
                # add the inter-service relationship to the quad constraint
                # for service in services:
                #     inter_para = value * services[service]
                #     quadconstraint += str(inter_para) + " " + name + "_" +
                #     service + " + "
                services[
                    name] = value  # record the current value for this service
                # write the 2-order constraint
                # o2para = name+"_2"
                o1para = name + "_1"
                cpara = name + "_c"
                # paras.add(o2para)
                paras.add(o1para)
                paras.add(cpara)
                constraint += str(value) + " " + o1para + " + " + cpara + " + "
        num += 1

    return constraints, num, paras


# if i == length-1:
#                #the last column which is the cost
#                cost = float(col[i])
#                # at this point, "services" contains all the services being
#                used in current observation
#                # clean up the last "+"
#                length = len(quadconstraint)
#                quadconstraint = quadconstraint[:length-2]
#                # append the quadconstraint to constraint
#                # uncomment the line below to support quad terms
#                if quad:
#                    constraint += quadconstraint
#                # in case there's only 1 quad-constraints
#                #if quadconstraint != "":
#                #    constraint += " - "
#                constraint += " -"+str(cost)+" err"+str(num+1)+" = 0\n"
#                constraints.append(constraint)
#                #clear the constraint
#                constraint = ""
#                quadconstraint = ""
#                services.clear()
#                continue
#            cur = col[i]
#            #print("cur="+cur)
#            if not (cur.replace(".", "", 1).isdigit()): # this is a service
#            name
#                name = cur
#            else:
#                value = float(cur)
#                # add the inter-service relationship to the quad constraint
#                for service in services:
#                    inter_para = value * services[service]
#                    quadconstraint += str(inter_para) + " " + name + "_" +
#                    service + " + "
#                    if quad:
#                        paras.add(name + "_" + service)
#                services[name] = value  # record the current value for this
#                service
#                # write the 2-order constraint
#                o2para = name+"_2"
#                o1para = name+"_1"
#                cpara = name + "_c"
#                if quad:
#                    paras.add(o2para)
#                    paras.add(o1para)
#                    paras.add(cpara)
#                if quad:
#                    constraint +=  str(value*value) + " " + o2para + " + "
#                constraint += str(value) + " " + o1para + " + " + cpara + " + "
#        num += 1
