# a RAPIDS profile
import random, math

class Profile:
    """ a profile table, could be observed, or ground truth
    """

    def __init__(self):
        """ Initialization
        """
        self.profile_table = {}
        self.metrics = {}
        self.configurations = set()
        self.mvprofile_table = {}
        self.numOfMVs = 1

    def getCostRange(self):
        min_c = min(self.profile_table.values())
        max_c = max(self.profile_table.values())
        return min_c, max_c

    def removeConfig(self, configuration):
        hash_id = self.hashConfig(configuration)
        del self.profile_table[hash_id]
        del self.mvprofile_table[hash_id]
        self.configurations.remove(configuration)

    def addCostEntry(self, configuration, cost):
        """ Record the cost for a configuration
        :param configuration: the configuration
        :param cost: the cost
        """
        self.profile_table[self.hashConfig(configuration)] = cost
        self.configurations.add(configuration)
        return

    def addMVEntry(self, configuration, mvs):
        """ Record the MV for a configuration
        :param configuration: the configuration
        :param mv: the mv
        """
        self.mvprofile_table[self.hashConfig(configuration)] = mvs
        self.numOfMVs = len(mvs)
        return

    def addEntry(self, configuration, cost, mvs):
        self.addCostEntry(configuration, cost)
        self.addMVEntry(configuration, mvs)
        return

    def updateEntry(self, configuration, val, COST=True):
        """ update the value of a configuration
        :param configuration: the configuration
        :param val: the new value
        :param COST: if True, update the cost entry, else the MV entry
        """
        table = None
        if COST:
            table = self.profile_table
        else:
            table = self.mvprofile_table
        if not self.hashConfig(configuration) in table:
            print
            "cannot found entry"
            hashcode = self.hashConfig(configuration)
            print
            configuration.printSelf(), hashcode
            print
            self.profile_table
            return
        table[self.hashConfig(configuration)] = val

    def hashConfig(self, configuration):
        """ generate a unique string as ID for a configuration
        :param configuration: the configuration
        :return: a string ID for that configuration
        """
        if type(configuration) is dict:
            return self.hashConfigMap(configuration)
        tmp_map = {}
        settings = configuration.retrieve_configs()
        for c in settings:
            name = c.knob.set_name
            val = c.val
            tmp_map[name] = val
        hash_result = ""
        # sort the map
        tmp_map_sorted = sorted(tmp_map)
        for m in tmp_map_sorted:
            hash_result += m + "," + str(tmp_map[m]) + ","
        hash_result = hash_result[:-1]
        return hash_result

    def hashConfigMap(self, configMap):
        """ generate a unique string as ID for a configuration in the form of a map
        :param configuration: the configuration map
        :return: a string ID for that configuration
        """
        hash_result = ""
        # sort the map
        tmp_map_sorted = sorted(configMap)
        for m in tmp_map_sorted:
            hash_result += m + "," + str(configMap[m]) + ","
        hash_result = hash_result[:-1]
        return hash_result

    def setMetrics(self, metrics):
        """ Set the submetrics
        :param metrics: metrics as list
        :return: none
        """
        id = 0
        for metric in metrics:
            self.metrics[metric] = id
            id+=1
        self.numOfMVs = len(self.metrics)

    def addMetrics(self, metrics):
        """ Append the submetrics, might be helpers
        :param metrics: metrics as list
        :return: none
        """
        cur_total = len(self.metrics)
        for metric in metrics:
            self.metrics[metric] = cur_total
            cur_total+=1
        self.numOfMVs = len(self.metrics)

    def setCost(self, configuration, val):
        """Set the cost of a configuration
        :param configuration: the configuration
        :param val: the cost
        """
        self.profile_table[self.hashConfig(configuration)] = val

    def getCost(self, configuration):
        """Get the cost of a configuration
        :param configuration: the configuration
        :return: the cost
        """
        entry = self.hashConfig(configuration)
        return self.profile_table[entry]

    def setMV(self, configuration, vals):
        """Set the MV of a configuration
        :param configuration: the configuration
        :param vals: the MVs
        """
        self.numOfMVs = len(vals)
        self.mvprofile_table[self.hashConfig(configuration)] = vals

    def getMV(self, configuration):
        """Get the MV of a configuration
        :param configuration: the configuration
        :return: the MV
        """
        entry = self.hashConfig(configuration)
        if entry in self.mvprofile_table:
            return self.mvprofile_table[entry]
        return [0.0]

    def getOptimal(self, budget, submetric = "all"):
        """Get the optimal mv for a given budget (for validation only)
        :param budget: budget
        :return: the optimal mv
        """
        best_overall_mv = -1 * math.inf
        lowest_cost = math.inf
        best_config = ""
        for hash_config, mv in self.mvprofile_table.items():
            cost = self.profile_table[hash_config]
            if cost > budget:
                continue
            if self.numOfMVs > 1:
                mv = mv[-1]
            if mv < best_overall_mv:
                continue
            best_overall_mv = mv
            lowest_cost = cost
            best_config = hash_config
        # take the sub_metric
        if self.numOfMVs > 1:
            metricIndex = self.metrics[submetric]
            best_mv = self.mvprofile_table[best_config][metricIndex]
        else:
            best_mv = self.mvprofile_table[best_config]
        return lowest_cost, best_mv, best_config, self.mvprofile_table[best_config]

    def hasEntry(self, configuration):
        """ Check if a configuration is recorded
        :param configuration: the configuration
        :return: True if exists, else if not
        """
        hashedID = self.hashConfig(configuration)
        return hashedID in self.profile_table

    def printProfile(self, outputfile):
        """ Print the profile to a file
        :param outputfile: the path to the output
        """
        output = open(outputfile, 'w')
        tmp = sorted(self.mvprofile_table.items(), key=lambda x: x[1][-1])

        for config in tmp:
            config = config[0]
            output.write(config)
            output.write(",")
            output.write(str(self.profile_table[config]))
            output.write("," + str(self.mvprofile_table[config]))
            output.write("\n")
        output.close()

    def genMultipleMV(self):
        profiles = []
        for i in range(0, self.numOfMVs):
            profile = Profile()
            profile.profile_table = self.profile_table
            profile.configurations = self.configurations
            profile.mvprofile_table = {
                k: v[i]
                for k, v in self.mvprofile_table.items()
            }
            profile.numOfMVs = 1
            profiles.append(profile)
        return profiles

    def genRSSubset(self, config_list):
        profile = Profile()
        for config in config_list:
            profile.addCostEntry(config, self.getCost(config))
            profile.addMVEntry(config, self.getMV(config))
        partitions = Profile.getPartitions(config_list)
        return profile, partitions

    def genRandomSubset(self, n):
        profile = Profile()
        n = min(n, len(self.configurations))  # if not 20, then use the overall
        randomConfigs = random.sample(self.configurations, n)
        for config in randomConfigs:
            profile.addCostEntry(config, self.getCost(config))
            profile.addMVEntry(config, self.getMV(config))
        partitions = Profile.getPartitions(randomConfigs)
        return profile, partitions

    @staticmethod
    def getPartitions(configurations):
        partitions = {}
        for config in configurations:
            settings = config.retrieve_configs()
            for c in settings:
                knob_min = c.knob.min
                knob_max = c.knob.max
                name = c.knob.set_name
                val = c.val
                if name not in partitions:
                    partitions[name] = [knob_min, knob_max]
                if val not in partitions[name]:
                    partitions[name].append(val)
        for knob in partitions.keys():
            partitions[knob].sort()
        return partitions
