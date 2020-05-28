"""
This is an example file for prepraing ferret for RAPID(C)
"""

from Core.AppMets.AppMethods import AppMethods
import os

class appMethods(AppMethods):
    database_path = "/home/liuliu/Research/mara_bench/parsec_rapid/pkgs/apps" \
                    "/ferret/run/corelnative/"
    table = "lsh"
    query_path = "/home/liuliu/Research/mara_bench/parsec_rapid/pkgs/apps" \
                 "/ferret/run/queries50"
    fullrun_query_path = "/home/liuliu/Research/mara_bench/parsec_rapid/pkgs" \
                         "/apps/ferret/run/queries1000"

    def __init__(self, name, obj_path):
        """ Initialization with app name
        :param name:
        """
        AppMethods.__init__(self, name, obj_path)
        self.training_units = 50
        self.fullrun_units = 1000  # two are . and ..
        self.max_cost = 99
        self.min_cost = 68
        self.min_mv = 58.69
        self.max_mv = 100
        self.gt_path = '/home/liuliu/Research/rapidlib-linux/modelConstr/Rapids/training_outputs/ferret-gt.txt'
        self.gt_full_path = '/home/liuliu/Research/rapidlib-linux/modelConstr/Rapids/training_outputs/ferret-gt-full.txt'
        self.run_config = ''

    def cleanUpAfterEachRun(self, configs=None):
        # backup the generated output to another location
        itr = 500
        hash = 8
        probe = 20
        if configs is not None:
            for config in configs:
                name = config.knob.set_name
                if name == "hash":
                    hash = pow(2,config.val)  # retrieve the setting for each knob
                elif name == "probe":
                    probe = config.val  # retrieve the setting for each knob
                elif name == "itr":
                    itr = config.val  # retrieve the setting for each knob

        self.moveFile(
            self.run_dir + "output.txt",
            self.run_dir + "training_outputs/output_" + str(hash) + "_" +
            str(probe) + "_" + str(itr) + ".txt")

    def afterGTRun(self):
        if not os.path.exists(self.gt_path):
            output_path = self.run_dir + "output.txt"
            self.moveFile(output_path, self.gt_path)

    def getRapidsCommand(self):
        if not os.path.exists(self.run_config):
            print("no config file exists:", self.appName, self.run_config)
            return []
        cmd = [
            self.obj_path,
            self.database_path,
            self.table,
            self.fullrun_query_path,
            "50",
            "20",
            "1",
            self.run_dir + "output.txt",
            "-rsdg",
            self.run_config  #,'1>/dev/null'
        ]
        return cmd

    # helper function to assembly the command
    def getCommand(self, configs=None, qosRun=False, fullRun=True):
        if qosRun and os.path.exists(self.gt_full_path):
            self.gt_path = self.gt_full_path
            return []  # return dummy command
        itr = 500
        hash = 8
        probe = 20
        if configs is not None:
            for config in configs:
                name = config.knob.set_name
                if name == "hash":
                    hash = pow(2,config.val)  # retrieve the setting for each knob
                elif name == "probe":
                    probe = config.val  # retrieve the setting for each knob
                elif name == "itr":
                    itr = config.val  # retrieve the setting for each knob
        if qosRun or fullRun:
            query_path = self.fullrun_query_path
        else:
            query_path = self.query_path
        return [
            self.obj_path, self.database_path, self.table, query_path, "50",
            "20", "1", self.run_dir + "output.txt", '-l',
            str(hash), '-t',
            str(probe), '-itr',
            str(itr)
        ]

    def computeQoSWeight(self, preferences, values):
        # preferences is the preferecne and values contains the raw mv weight
        ranking = values["ranking"]
        coverage = values["coverage"]
        ranking_pref = preferences["ranking"]
        coverage_pref = preferences["coverage"]
        maxError = (2 * coverage_pref - ranking_pref) * 50 * 51
        # 50 images in real run
        ranking_res = (1.0 +
                       (ranking_pref * ranking + 2 * coverage_pref * coverage)
                       / float(maxError)) * 100.0
        return ranking_res

    def rank(self, img, imglist):
        if img in imglist:
            return imglist.index(img) + 1
        return 0

    def compute1(self, list1, imgset):
        res = 0
        for img in imgset:
            res += self.rank(img, list1)
        return res

    def compute2(self, list1, list2, imgset):
        res = 0
        for img in imgset:
            res += abs(self.rank(img, list1) - self.rank(img, list2))
        return res

    # helper function to evaluate the QoS
    def getQoS(self):
        truth = open(self.gt_path, "r")
        mission = open(self.run_dir + "output.txt", "r")
        truthmap = {}
        missionmap = {}
        truth_res = []
        mission_res = []
        # check if both file contains the same number of lines
        for line in mission:
            col = line.split('\t')
            name = col[0].split("/")[-1]
            missionmap[name] = []
            for i in range(1, len(col)):  # 50 results
                missionmap[name].append(col[i].split(':')[0])
        for line in truth:
            col = line.split('\t')
            name = col[0].split("/")[-1]
            truthmap[name] = []
            for i in range(1, len(col)):  # 50 results
                truthmap[name].append(col[i].split(':')[0])
        #if len(missionmap) != len(truthmap):
        # mission failed in between
        #    print(len(missionmap), len(truthmap))
        #    return [0.0, 0.0, 0.0]
        # now that 2 maps are set, compare each item
        # setup the Z / S/ and T
        Z = set()
        S = set()
        T = set()
        totAcuracy = 0.0
        totCoverage = 0.0
        totRanking = 0.0
        totimg = 0.0
        for query_image in truthmap:
            totimg += 1.0
            truth_res = truthmap[query_image]
            try:
                mission_res = missionmap[query_image]
                # compute the worst case senario, where Z = empty
                maxError = len(truth_res) * (len(truth_res) + 1)
                # setup S and T
                S.update(truth_res)
                T.update(mission_res)
                Z = S & T  # Z includes images both in S and T
                # clear S and T
                for s in Z:
                    T.remove(s)
                    S.remove(s)
                # now that Z, S, and T are set, compute the ranking function
                # two Sub QoS
                coverage = -1 * (len(truth_res) - len(Z)) * (len(truth_res) +
                                                             1)
                ranking = -1 * (self.compute2(truth_res, mission_res, Z) -
                                self.compute1(truth_res, S) -
                                self.compute1(mission_res, T))
                ranking_res = (
                    1.0 + (2 * coverage + ranking) / float(maxError)) * 100.0
            except:
                ranking_res = 0.0
                ranking = 0.0
                coverage = 0.0
            totAcuracy += ranking_res
            totRanking += ranking
            totCoverage += coverage
            S.clear()
            T.clear()
            Z.clear()
        return [
            totCoverage / float(totimg), totRanking / float(totimg),
            totAcuracy / float(totimg)
        ]
