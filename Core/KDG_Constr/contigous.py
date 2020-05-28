# Tools needed for generating contigous RSDG
def genContProblem(observed, model):
    prob = open("outputs/contproblem.lp", 'w')
    constraints, num, paras = readContFactAndGenConstraint(observed, model)
    # write obj, err^2 - 2 err +1
    obj = ""
    quadobj = "[ "
    for i in range(1, num + 1):
        obj += "-2 err" + str(i)
        quadobj += "err" + str(i) + " ^ 2"
        if not (i == num):
            obj += " + "
            quadobj += " + "
    quadobj += " ]\n"
    obj += " + " + quadobj
    prob.write("Minimize\n")
    prob.write(obj + "\n")
    # write constraint
    prob.write("Subject To\n")
    for c in constraints:
        prob.write(c)
    # write Bounds
    bounds = genBounds(len(constraints), paras)
    prob.write(bounds)
    return paras


def genBounds(num_of_err, paras):
    bounds = "Bounds \n"
    para_copy = paras.copy()
    for i in range(1, num_of_err + 1):
        para_copy.add("err" + str(i))
    for j in para_copy:
        # the quad term has to be greater than 0
        col = j.split('_')
        if len(col) == 2:
            if col[1] == '2':
                bounds += "0 < " + j + "\n"
                continue
        bounds += "-99999 < " + j + " < 99999\n"
    return bounds


def getContRSDGandCheckRate(paras, factfile, quad):
    result = open("outputs/max.sol", 'r')
    rsdg = open("outputs/rsdgcont", 'w')
    fact = open(factfile, "r")
    rsdg_map = {}
    relation_map = {}
    for line in result:
        col = line.split()
        if not (len(col) == 2):
            continue
        name = col[0]
        val = col[1]
        if not (name in paras):
            continue
        curPara = name.split("_")
        service = curPara[0]
        coeff = curPara[1]
        lvl = 0
        dependent = ""
        if coeff == "2":
            lvl = 2
        elif coeff == "1":
            lvl = 1
        elif coeff == "c":
            lvl = 0
        else:
            lvl = -1
            dependent = coeff
        if not (service in rsdg_map):
            rsdg_map[service] = [0.0] * 3
        if not (service in relation_map):
            relation_map[service] = {}
        if not lvl == -1:
            rsdg_map[service][lvl] = float(val)
        else:
            relation_map[service][dependent] = float(val)
        rsdg.write(name + " " + val + "\n")
    rsdg.close()
    # now check the rate
    report = open("outputs/report.csv", 'w')
    total = 0.0
    totErr = 0.0
    for line in fact:
        total += 1
        col = line.split(',')
        curPredict = 0.0
        curService = ""
        value_map = {}
        for i in range(0, len(col)):
            if (i == len(col) - 1):
                # add the interrelation
                if quad:
                    for svc in value_map.items():
                        svc_name = svc[0]
                        svc_val = svc[1]
                        for dep in relation_map[svc_name].items():
                            dep_name = dep[0]
                            inter_val = dep[1]
                            curPredict += svc_val * inter_val * value_map[
                                dep_name]
                measurement = float(col[i])
                abs_err = abs((measurement - curPredict) / measurement)
                totErr += abs_err
                report.write(
                    str(curPredict) + "," + str(measurement) + "," + str(
                        1.0 - abs_err) + "\n")
                curService = ""
                curPredict = 0.0
                break
            if (col[i].isdigit() and curService != ""):
                val = float(col[i])
                value_map[curService] = float(col[i])
                if quad:
                    o2 = rsdg_map[curService][2]
                o1 = rsdg_map[curService][1]
                c = rsdg_map[curService][0]
                if quad:
                    curPredict += o2 * val * val + o1 * val + c
                else:
                    curPredict += o1 * val + c
            else:
                curService = col[i]
    report.write("Mean Error:" + str(totErr / total))
    report.close()


def readContFactAndGenConstraint(fact, quad):
    services = {}
    constraints = []  # list of constraints
    paras = set()  # set of parameters, o2, o1, and c for each service
    # added this for inter-relationship higher order constraint
    num = 0
    f = open(fact, 'r')
    for line in f:
        col = line.split(',')
        length = len(col)
        name = ""
        constraint = ""
        quadconstraint = ""  # this is the inter-service relationship
        for i in range(0, length):
            if i == length - 1:
                # the last column which is the cost
                cost = float(col[i])
                # at this point, "services" contains all the services being
                # used in current observation
                # clean up the last "+"
                length = len(quadconstraint)
                quadconstraint = quadconstraint[:length - 2]
                # append the quadconstraint to constraint
                # uncomment the line below to support quad terms
                if quad:
                    constraint += quadconstraint
                # in case there's only 1 quad-constraints
                # if quadconstraint != "":
                #    constraint += " - "
                constraint += " -" + str(cost) + " err" + str(
                    num + 1) + " = 0\n"
                constraints.append(constraint)
                # clear the constraint
                constraint = ""
                quadconstraint = ""
                services.clear()
                continue
            cur = col[i]
            # print("cur="+cur)
            if not (
                    cur.replace(".", "",
                                1).isdigit()):  # this is a service name
                name = cur
            else:
                value = float(cur)
                # add the inter-service relationship to the quad constraint
                for service in services:
                    inter_para = value * services[service]
                    quadconstraint += str(
                        inter_para) + " " + name + "_" + service + " + "
                    if quad:
                        paras.add(name + "_" + service)
                services[
                    name] = value  # record the current value for this service
                # write the 2-order constraint
                o2para = name + "_2"
                o1para = name + "_1"
                cpara = name + "_c"
                if quad:
                    paras.add(o2para)
                    paras.add(o1para)
                    paras.add(cpara)
                if quad:
                    constraint += str(value * value) + " " + o2para + " + "
                constraint += str(value) + " " + o1para + " + " + cpara + " + "
        num += 1

    return constraints, num, paras


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
                smaller_constraint = constraint + " <= " + str(
                    cost + 0.1) + "\n"
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
