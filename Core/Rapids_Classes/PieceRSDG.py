from .InterCoeff import InterCoeff
from .KDG import *

class PieceRSDG:
    """A RSDG calculated based on piece-wise linear regression model
    """

    def fromFile(self, rsdgFile):
        """ Generate a RSDG object from a file
        """
        file = open(rsdgFile, 'r')
        knob_name = ""
        segs = []
        START_COEFF = False
        for line in file:
            if START_COEFF:
                # this is the coeff lines
                [knob_a, knob_b] = line.split()[0].split(':')[0].split('_')
                [a, b, c] = line.split()[0].split(':')[1].split('/')
                self.addInterCoeff(knob_a, knob_b, float(a), 'a')
                self.addInterCoeff(knob_a, knob_b, float(b), 'b')
                self.addInterCoeff(knob_a, knob_b, float(c), 'c')
                continue

            col = line.split()
            if len(col) == 0:
                # this is the break line
                # add the knob
                self.addKnob(knob_name)
                for seg in segs:
                    self.addSeg(knob_name, seg)
                segs = []
                continue

                # add the seg
            if len(col) == 1:
                # this is the knob name line
                knob_name = col[0]
                if knob_name == "COEFF":
                    START_COEFF = True

            else:
                # this is the segment line
                [min, max, seg_name, a, b] = col
                seg = Segment(seg_name, knob_name, float(min), float(max))
                seg.setLinearCoeff(float(a))
                seg.setConstCoeff(float(b))
                seg.setID(seg_name.split('_')[1])
                segs.append(seg)

    def __init__(self):
        self.knob_table = {}
        self.coeffTable = {}

    def addKnob(self, knob):
        """ Initialize a knob entry
        for each entry, the value is a list of segments
        :param knob: the knob to be added
        """
        self.knob_table[knob] = []

    def addSeg(self, knob, seg):
        """ add a segment to the knob entry
        :param knob: the knob
        :param seg: the segment to be added
        """
        self.knob_table[knob].append(seg)

    def addInterCoeff(self, a, b, val, abc):
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

    def printRSDG(self, COST=True, id=0, KDG=True, RS=False):
        """ print the RSDG to a file
        The output path is ./outputs/[cost/mv].rsdg
        :param COST: if True, print the Cost rsdg, else the MV rsdg
        """
        outfilename = ""
        if COST:
            outfilename = "./outputs/cost_bb.rsdg"
            if KDG:
                outfilename = "tmp_cost.rsdg"
            if RS:
                outfilename = "./outputs/cost_rs.rsdg"
        else:
            outfilename = "./outputs/mv" + str(id) + "_bb.rsdg"
            if KDG:
                outfilename = "tmp_mv" + str(id) + ".rsdg"
            if RS:
                outfilename = "./outputs/mv" + str(id) + "_rs.rsdg"
        rsdg = open(outfilename, 'w')
        # print the segments
        for knob in self.knob_table:
            seglist = self.knob_table[knob]
            rsdg.write(knob + "\n")
            for seg in seglist:
                rsdg.write("\t")
                rsdg.write(str(seg.min) + " " + str(seg.max) + " ")
                rsdg.write(seg.printID() + " " + str(seg.a) + " " +
                           str(seg.b) + "\n")
            rsdg.write("\n")
        # print the coeff
        rsdg.write("COEFF\n")
        for knob in self.coeffTable:
            for b in self.coeffTable[knob]:
                rsdg.write("\t")
                rsdg.write(knob + "_" + b + ":" +
                           str(self.coeffTable[knob][b].a) + "/" +
                           str(self.coeffTable[knob][b].b) + "/" +
                           str(self.coeffTable[knob][b].c) + "\n")
        rsdg.close()
        return outfilename

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
            seg = self.findSeg(knob_name, knob_val)
            totalcost += knob_val * seg.a + seg.b
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

    def findSeg(self, knob_name, knob_val):
        """ Locate the segment that a concrete value falls into
        :param knob_name: the knob name
        :param knob_val: the knob value
        :return: the segment that this value falls into
        """
        seglist = self.knob_table[knob_name]
        highest = -1
        highest_seg = None
        for seg in seglist:
            if seg.max > highest:
                highest = seg.max
                highest_seg = seg
            if knob_val >= seg.min and knob_val <= seg.max:
                return seg
        # IF NOTHING MATCHES, USE THE HIGHEST SEG
        return highest_seg
