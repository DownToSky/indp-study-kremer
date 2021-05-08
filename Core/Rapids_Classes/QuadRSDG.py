class QuadRSDG:
    """A RSDG calculated based on quadratic regression model
    """

    def __init__(self):
        self.knob_table = {}  # constains the coefficients of all knobs
        self.coeffTable = {}

    def addKnob(self, knob):
        """ Initialize a knob
        for each entry, the value is [quad, linear, constant]
        :param knob: the knob to be added
        """
        self.knob_table[knob] = [0.0, 0.0, 0.0]

    def addKnobVal(self, knob, val, lvl):
        """ udpate the value for a knob
        :param knob: the knob
        :param val: the coeff value
        :param lvl: c -> constant, 1 -> linear, 2 (default) -> quad
        """
        if lvl == "c":
            self.knob_table[knob][2] = val
        elif lvl == "1":
            self.knob_table[knob][1] = val
        else:
            self.knob_table[knob][0] = val

    def addInterCoeff(self, a, b, abc, val):
        """ Add a inter-knob coefficient
        :param a: the first knob
        :param b: the second knob
        :param abc: the level of coefficient,
        :param val: the value
        :return:
        """
        if a not in self.coeffTable:
            self.coeffTable[a] = {}
        if b not in self.coeffTable[a]:
            self.coeffTable[a][b] = InterCoeff()
        if abc == "a":
            self.coeffTable[a][b].addQuadCoeff(val)
        elif abc == "b":
            self.coeffTable[a][b].addLinearCoeff(val)
        elif abc == "c":
            self.coeffTable[a][b].addConstCoeff(val)

    def printRSDG(self, COST=True, KDG=True, RS=False):
        """ print the RSDG to a file
        The output path is ./outputs/[cost/mv].rsdg
        :param COST: if True, print the Cost rsdg, else the MV rsdg
        """
        outfilename = ""
        if COST:
            outfilename = "./outputs/cost_bb.rsdg"
            if KDG:
                outfilename = "./outputs/cost.rsdg"
            if RS:
                outfilename = "./outputs/cost_rs.rsdg"
        else:
            outfilename = "./outputs/mv_bb.rsdg"
            if KDG:
                outfilename = "./outputs/mv.rsdg"
            if RS:
                outfilename = "./outputs/mv_rs.rsdg"
        rsdg = open(outfilename, 'w')
        for knob in self.knob_table:
            rsdg.write(knob + "\n")
            rsdg.write("\t")
            rsdg.write("o2:")
            rsdg.write(str(self.knob_table[knob][0]) + " ; ")
            rsdg.write("o1:")
            rsdg.write(str(self.knob_table[knob][1]) + " ; ")
            rsdg.write("c:")
            rsdg.write(str(self.knob_table[knob][2]) + " ; \n")
        rsdg.write("COEFF\n")
        for knob in self.coeffTable:
            for b in self.coeffTable[knob]:
                rsdg.write("\t")
                rsdg.write(knob + "_" + b + ":" +
                           str(self.coeffTable[knob][b].a) + "/" +
                           str(self.coeffTable[knob][b].b) + "/" +
                           str(self.coeffTable[knob][b].c) + "\n")
        rsdg.close()

    def calCost(self, configuration):
        """ calculate the estimated cost of a configuration by RSDG
        :param configuration: the configuration
        :return: the estimated cost value
        """
        totalcost = 0.0

        # calculate linear cost
        for config in configuration.retrieve_configs():
            knob_name = config.knob.set_name
            knob_val = config.val
            coeffs = self.knob_table[knob_name]
            totalcost += coeffs[0] * knob_val * knob_val + coeffs[1] * \
                         knob_val + coeffs[2]

        # calculate inter cost
        configs = []
        for config in configuration.retrieve_configs():
            configs.append(config)
        for i in range(0, len(configs)):
            for j in range(0, len(configs)):
                if i == j:
                    continue
                if configs[i].knob.set_name in self.coeffTable:
                    if configs[j].knob.set_name in self.coeffTable[
                            configs[i].knob.set_name]:
                        knoba_val = configs[i].val
                        knobb_val = configs[j].val
                        coeff_entry = self.coeffTable[configs[i].knob.set_name]
                        coeff_inter = coeff_entry[configs[j].knob.set_name]
                        a, b, c = coeff_inter.retrieveCoeffs()
                        totalcost += float(knoba_val) * float(
                            knoba_val) * a + float(knobb_val) * float(
                                knobb_val) * b + float(knobb_val) * float(
                                    knoba_val) * c

        return totalcost
