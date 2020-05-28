""" the parent class of app-specific methods
Developers will inherit from this class to implement the app-specific
methods. RAPID(C) will run their
implementations to
1) get the groundtruth of the app by running the app in default mode.
2) get the training Data by running the app in different configurations
"""
import os, time, csv, functools, subprocess, signal, json
import pandas as pd
from Core.Rapids_Classes.SysUsageTable import SysUsageTable
from Core.Rapids_Classes.SlowDown import SlowDown
from Core.Rapids_Classes.SysArgs import SysArgs
from Core.Rapids_Classes.Stresser import Stresser
from Core.Rapids_Classes.KDG import *
from Core.Rapids_Classes.Metric import *
from Core.Rapids_Classes.Util import recoverTimeRecord
from collections import OrderedDict


class AppMethods():
    PCM_PREFIX = [
        '/home/liuliu/Research/pcm/pcm.x', '-r', '0.5', '-nc', '-ns',
        '2>/dev/null', '-csv=tmp.csv', '--'
    ]
    NO_RECONFIG = -1

    def __init__(self, name, obj_path):
        """ Initialization with app name
        :param name:
        """
        self.appName = name
        self.obj_path = obj_path
        self.sys_usage_table = SysUsageTable()
        self.training_units = 1
        self.fullrun_units = 1
        self.run_config = ''
        self.run_dir = '../Rapids_Classes/'  # default working dir

    def setRunDir(self, rundir):
        self.run_dir = rundir

    def setTrainingUnits(self, unit):
        self.training_units = unit

    def getCommandWithConfig(self, config_str, qosRun=False, fullRun=True):
        ''' use config string to generate a config and get command '''
        elements = config_str.split('-')
        configs = []
        for i in range(0, len(elements)):
            if i % 2 == 0:  # knob name
                knob = Knob(elements[i], elements[i], -99999, 99999)
                configs.append(Config(knob, elements[i + 1]))
                i += 1
        return self.getCommand(configs, qosRun, fullRun)

    # Implement this function
    def getCommand(self, configs=None, qosRun=False, fullRun=True):
        """ Assembly the CMD line for running the app
        :param configs: a concrete configuration with knob settings
                        Default setting would assemble command for GT
        """
        return ""

    def getRapidsCommand(self):
        """ Developer needs to implement this """
        pass

    def parseLog(self):
        name = self.run_dir + "mission_" + self.appName + "_log.csv"
        fail_result = {
            'totReconfigTime': -1,
            'totReconfig': -1,
            'success': -1,
            'slowdown_scale': -1,
            'rc_by_budget': -1,
            'rc_by_rapidm': -1,
            'failed_reason': 'no file',
            'runtime': -1
        }
        # go to the last line
        if os.stat(name).st_size == 0:
            return fail_result
        with open(name) as logfile:
            for line in logfile:
                pass
            try:
                last_col = line.split(',')
                totTime = float(last_col[-7])
                totReconfig = int(last_col[-6])
                runtime = float(last_col[-4])
                totScaleUp = int(last_col[-3])
                success = last_col[-2]
                failed_reason = last_col[-1].rstrip()
            except:
                return fail_result
        # find details
        df = pd.read_csv(name)
        triggered_by_budget = df['RC_by_budget'].sum()
        triggered_by_rapidm = df['RC_by_rapidm'].sum()
        return {
            'totReconfigTime': totTime,
            'totReconfig': totReconfig,
            'success': success,
            'slowdown_scale': totScaleUp,
            'rc_by_budget': triggered_by_budget,
            'rc_by_rapidm': triggered_by_rapidm,
            'failed_reason': failed_reason,
            'runtime': runtime
        }

    def setRunConfigFile(self, config_file_path):
        self.run_config = config_file_path

    def updateRunConfig(self,
                        budget,
                        unit=-1,
                        offline_search=False,
                        remote=True,
                        gurobi=True,
                        cont=True,
                        rapid_m=False,
                        mission_log=True,
                        debug=False,
                        rush_to_end=False,
                        power_saving=False):
        # update the run_config
        '''
        unit: UNIT_PER_CHECK, if not set, use default 10 reconfigs
        ...
        '''
        if unit == -1:
            unit = self.fullrun_units / 10
        elif unit == self.NO_RECONFIG:
            unit = 999999
        config = None
        if os.path.isfile(self.run_config):
            with open(self.run_config) as config_json:
                config = json.load(config_json, object_pairs_hook=OrderedDict)
                config['mission']['budget'] = budget
                config['mission']['UNIT_PER_CHECK'] = unit
                config['mission']['OFFLINE_SEARCH'] = offline_search
                config['mission']['REMOTE'] = remote
                config['mission']['GUROBI'] = gurobi
                config['mission']['CONT'] = cont
                config['mission']['DEBUG'] = debug
                config['mission']['RAPID_M'] = rapid_m
                config['mission']['MISSION_LOG'] = mission_log
                config['mission']['RUSH_TO_END'] = rush_to_end
                config['mission']['POWER_SAVING'] = power_saving
        config_json = open(self.run_config, 'w')
        json.dump(config, config_json, indent=2)

    def overheadMeasure(self, budget=0.5):
        print("measuring overhead")
        #self.runGT(True)
        budget = (self.min_cost + budget * (self.max_cost - self.min_cost)
                  ) * self.fullrun_units / 1000.0  #budget in the middle
        report = []
        # generate the possible units
        units = list(range(1, 20)) + list(range(20, 101, 10))
        for unit in units:
            if int(self.fullrun_units / unit) < 1:
                # finest granularity
                continue
            self.updateRunConfig(budget,
                                 unit=unit,
                                 offline_search=False,
                                 remote=False,
                                 gurobi=True,
                                 cont=True,
                                 rapid_m=False,
                                 mission_log=True)
            cmd = self.getRapidsCommand()
            for i in range(1, 3):  # for each run, 5 times
                print("running budget", str(budget), "itr", str(i))
                start_time = time.time()
                os.system(" ".join(cmd))
                elapsed_time = time.time() - start_time
                mv = self.getQoS()
                if type(mv) is list:
                    mv = mv[-1]  # use the default qos metric
                logger = self.parseLog()
                totTime = logger['totTime']
                totReconfig = logger['totReconfig']
                success = logger['success']
                triggered_by_budget = logger['rc_by_budget']
                report.append({
                    'Unit':
                    unit,
                    'MV':
                    mv,
                    'Augmented_MV':
                    0.0 if elapsed_time > 1.05 * budget else mv,
                    'Budget':
                    budget,
                    'Exec_Time':
                    elapsed_time,
                    'OverBudget':
                    elapsed_time > 1.05 * budget,
                    'RC_TIME':
                    totTime,
                    'RC_NUM':
                    totReconfig,
                    'SUCCESS':
                    success,
                    'overhead_pctg':
                    float(totTime) / (1000.0 * float(elapsed_time)),
                    'RC_by_budget':
                    triggered_by_budget
                })
        return report

    def qosRun(self, OFFLINE=False):
        print("running QOS run")
        self.runGT(True)  # first generate the groundtruth
        step_size = (self.max_cost - self.min_cost) / 10.0
        report = []
        for percentage in range(1, 11):
            budget = (self.min_cost + float(percentage) *
                      step_size) * self.fullrun_units / 1000.0
            run_unit = self.fullrun_units / 10  # reconfig 10 times
            print("RUNNING BUDGET:", str(budget))
            self.updateRunConfig(budget,
                                 unit=run_unit,
                                 offline_search=OFFLINE,
                                 remote=False,
                                 gurobi=True,
                                 cont=True,
                                 rapid_m=False,
                                 mission_log=True)
            cmd = self.getRapidsCommand()
            start_time = time.time()
            os.system(" ".join(cmd))
            elapsed_time = time.time() - start_time
            mv = self.getQoS()
            if type(mv) is list:
                mv = mv[-1]  # use the default qos metric
            report.append({
                'Percentage':
                percentage,
                'MV':
                mv,
                'Augmented_MV':
                0.0 if elapsed_time > 1.05 * budget else mv,
                'Budget':
                budget,
                'Exec_Time':
                elapsed_time
            })
            print("mv:" + str(mv))
        return report

    # Implement this function
    def train(self,
              config_table,
              bb_profile,
              numOfFixedEnv,
              appInfo,
              upload=False):
        """ Train the application with all configurations in config_table and
        write Cost / Qos in costFact and mvFact.
        :param config_table: A table of class Profile containing all
        configurations to train
        :param bb_profile: A table of class Profile containing all
        configurations(invalid+valid)
        :param numOfFixedEnv: number of environments if running for fixed env
        :param appInfo: a obj of Class AppSummary
        :param upload: whether to upload the measuremnet to RAPID_M server
        """
        # perform a single run for training
        configurations = config_table.configurations  # get the
        configurations_bb = bb_profile.configurations
        # configurations in the table
        train_conf = appInfo.TRAINING_CFG
        withCost = not appInfo.isCostTrained()
        withMV = train_conf['withQoS'] and not appInfo.isMVTrained()
        withSys = train_conf['withSys'] and not appInfo.isSysTrained()
        withPerf = train_conf['withPerf'] and not appInfo.isPerfTrained()
        withMModel = train_conf['withMModel'] and not appInfo.isMModelTrained()
        if withCost:
            costFact = open(appInfo.FILE_PATHS['COST_FILE_PATH'], 'w')
        if withMV:
            mvFact = open(appInfo.FILE_PATHS['MV_FILE_PATH'], 'w')
        if withSys:
            sysFact = open(appInfo.FILE_PATHS['SYS_FILE_PATH'], 'w')
        if withPerf:
            slowdownProfile = open(appInfo.FILE_PATHS['PERF_FILE_PATH'], 'w')
            slowdownHeader = False
        if withMModel:
            m_slowdownProfile = open(appInfo.FILE_PATHS['M_FILE_PATH'], 'w')
            m_slowdownHeader = False

        # comment the lines below if need random coverage
        multi_env = SysArgs()
        single_env = Stresser(self.appName)
        env_commands = []
        if numOfFixedEnv != -1:
            # half single half multi
            for i in range(0, int(numOfFixedEnv /
                                  2)):  # run different environment
                #env_commands.append(env.getRandomEnv())
                env_commands.append(single_env.getRandomStresser())
                env_commands.append(multi_env.getRandomEnv())
        training_time_record = {}
        # iterate through configurations
        total = len(configurations_bb)
        current = 1
        for configuration in configurations_bb:
            print("*****TRAINING:" + str(current) + "/" + str(total) + "*****")
            current += 1
            # the purpose of each iteration is to fill in the two values below
            cost = 0.0
            mv = [0.0]
            configs = configuration.retrieve_configs(
            )  # extract the configurations
            # assembly the command
            command = self.getCommand(configs, fullRun=False)
            metric = None
            # basic run or with sys
            if not appInfo.isCostTrained() or withSys or withMV:
                # 1) COST Measuremnt
                total_time, cost, metric = self.getCostAndSys(
                    command, self.training_units, withSys)
                if withSys and metric is None:
                    # the total runtime is too small for measuring the metric
                    command = self.getCommand(configs, fullRun=True)
                    total_time_not_used, cost, metric = self.getCostAndSys(
                        command, self.fullrun_units, withSys)
                training_time_record[configuration.printSelf('-')] = total_time
                # write the cost to file
                if withCost:
                    AppMethods.writeConfigMeasurementToFile(
                        costFact, configuration, cost)
                # 2) MV Measurement
                if withMV:
                    mv = self.getQoS()
                    # write the mv to file
                    AppMethods.writeConfigMeasurementToFile(
                        mvFact, configuration, mv)
                # 3) SYS Profile Measurement
                if withSys:
                    self.recordSysUsage(configuration, metric)
            # running with others
            if withPerf or withMModel:
                # get the standalone sys
                if metric is None:
                    total_time, cost, metric = self.getCostAndSys(
                        command, self.training_units, True)
                    if metric is None:
                        # the total runtime is too small for measuring the metric
                        command = self.getCommand(configs, fullRun=True)
                        total_time_not_used, cost, metric = self.getCostAndSys(
                            command, self.fullrun_units, True)

                # 4) Performance Measurement
                if withPerf:
                    # examine the execution time slow-down
                    print("START STRESS TRAINING")
                    slowdownTable, m_slowdownTable = self.runStressTest(
                        configuration, cost, env_commands, withMModel)
                    # write the header
                    if not slowdownHeader:
                        slowdownProfile.write(metric.printAsHeader(','))
                        slowdownProfile.write(",SLOWDOWN")
                        slowdownProfile.write('\n')
                        if withMModel:
                            m_slowdownProfile.write(metric.printAsHeader(','))
                            m_slowdownProfile.write(",SLOWDOWN")
                            m_slowdownProfile.write('\n')
                        slowdownHeader = True
                    slowdownTable.writeSlowDownTable(slowdownProfile)
                    # 5) M-Model Performance Measurement
                    if withMModel:
                        m_slowdownTable.writeSlowDownTable(m_slowdownProfile)
            self.cleanUpAfterEachRun(configs)
        # write the metric to file
        if withCost:
            costFact.close()
        if withMV:
            mvFact.close()
        if withSys:
            self.printUsageTable(sysFact)
        if withPerf:
            slowdownProfile.close()
        if withMModel:
            m_slowdownProfile.close()
        if upload:
            print("preparing to upload to server")
            self.uploadToServer(appInfo)
        # udpate the status
        appInfo.setTrained(cost=True, mv=train_conf['withQoS'])
        appInfo.setPerfTrained(train_conf['withSys'], train_conf['withPerf'],
                               train_conf['withMModel'])
        # if training time record has been done before, recover it
        if not withCost:
            training_time_record = recoverTimeRecord(appInfo,
                                                     self.training_units)
        return training_time_record

    # Send the system profile up to the RAPID_M server
    def uploadToServer(self, appInfo):
        # get the app system profile text
        with open(appInfo.FILE_PATHS['SYS_FILE_PATH'], 'r') as sysF:
            sys_data = sysF.read()
        # get the app performance profile text
        with open(appInfo.FILE_PATHS['PERF_FILE_PATH'], 'r') as perfF:
            perf_data = perfF.read()
        with open(appInfo.FILE_PATHS['MV_FILE_PATH'], 'r') as perfF:
            mv_data = perfF.read()
        with open(appInfo.FILE_PATHS['COST_FILE_PATH'], 'r') as perfF:
            cost_data = perfF.read()
        # get the machine id
        hostname = socket.gethostname()

        INIT_ENDPOINT = "http://algaesim.cs.rutgers.edu/rapid_server/init.php"
        INIT_ENDPOINT = INIT_ENDPOINT + "?" + 'machine=' + hostname + \
            '&app=' + appInfo.APP_NAME

        # set up the post params
        POST_PARAMS = {
            'buckets': sys_data,
            'p_model': perf_data,
            'mv': mv_data,
            'cost': cost_data
        }

        req = requests.post(url=INIT_ENDPOINT, data=POST_PARAMS)

        response = req.text
        print("response:" + response)

    # Implement this function
    def runGT(self, qosRun=False):
        """ Perform a default run of non-approxiamte version of the
        application to generate groundtruth result for
        QoS checking later in the future. The output can be application
        specific, but we recommend to output the
        result to a file.
        """
        print("GENERATING GROUND TRUTH for " + self.appName)
        command = self.getCommand(None, qosRun, fullRun=False)
        if not len(command) == 0:
            os.system(" ".join(command))
        self.afterGTRun()

    def runStressTest(self,
                      configuration,
                      orig_cost,
                      env_commands=[],
                      withMModel=False):
        app_command = self.getCommand(configuration.retrieve_configs(),
                                      fullRun=False,
                                      qosRun=False)
        env = SysArgs()
        slowdownTable = SlowDown(configuration)
        m_slowdownTable = SlowDown(configuration)
        # if running random coverage, create the commands
        if len(env_commands) == 0:
            print("No commands input, get 10 synthetic stressers")
            for i in range(0, 10):  # run 10 different environment
                env_command = env.getRandomEnv()
                env_commands.append(env_command)
        id = 0
        for env_command in env_commands:
            # if withMModel, check the environment first
            if withMModel:
                print('running stresser alone', env_command['configuration'],
                      id, env_command['command'])
                id += 1
                #command = " ".join(self.PCM_PREFIX + env_command + ['-t', '5'])
                #os.system(command)
                command = " ".join(self.PCM_PREFIX + env_command['command'] +
                                   ['2> /dev/null'])
                info = env_command['app'] + ":" + env_command['configuration']
                env_metric = None
                while env_metric is None:
                    # broken, rerun
                    os.system('rm tmp.csv')
                    stresser = subprocess.Popen(command,
                                                shell=True,
                                                preexec_fn=os.setsid)
                    time.sleep(5)  #profile for 5 seconds
                    os.killpg(os.getpgid(stresser.pid), signal.SIGKILL)
                    env_metric = AppMethods.parseTmpCSV()

            # start the env
            #env_creater = subprocess.Popen(
            #    " ".join(env_command), shell=True, preexec_fn=os.setsid)
            print('running stresser+app')
            env_creater = subprocess.Popen(" ".join(env_command['command'] +
                                                    ['&> /dev/null']),
                                           shell=True,
                                           preexec_fn=os.setsid)

            total_time, cost, metric = self.getCostAndSys(
                app_command, self.training_units, True)
            if metric is None:
                # too fast
                app_command = self.getCommand(configuration.retrieve_configs(),
                                              fullRun=True,
                                              qosRun=False)
                total_time_not_used, cost, metric = self.getCostAndSys(
                    app_command, self.fullrun_units, True)
            # end the env
            os.killpg(os.getpgid(env_creater.pid), signal.SIGKILL)
            # write the measurement to file
            slowdown = cost / orig_cost
            slowdownTable.add_slowdown(metric, slowdown)
            if withMModel:
                m_slowdownTable.add_slowdown(env_metric, slowdown, info)
        return slowdownTable, m_slowdownTable

    def runMModelTest(self, configuration, orig_cost):
        app_command = self.getCommand(configuration.retrieve_configs())
        env = SysArgs()
        slowdownTable = SlowDown(configuration)
        # if running random coverage, create the commands
        for i in range(0, 5):  # run 5 different environment
            env_command = env.getRandomEnv()
            # measure the env
            command = " ".join(self.PCM_PREFIX + env_command + ['-t', '5'])
            os.system(command)
            env_metric = AppMethods.parseTmpCSV()
            # measure the combined env
            env_creater = subprocess.Popen(" ".join(env_command),
                                           shell=True,
                                           preexec_fn=os.setsid)
            total_time, cost, total_metric = self.getCostAndSys(
                app_command, self.training_units, True)
            # end the env
            os.killpg(os.getpgid(env_creater.pid), signal.SIGKILL)
            # write the measurement to file
            slowdown = cost / orig_cost
            slowdownTable.add_slowdown(env_metric, slowdown)
        return slowdownTable

    # Some default APIs
    def getName(self):
        """ Return the name of the app
        :return: string
        """
        return self.name

    # some utilities might be useful
    def getCostAndSys(self, command, work_units=1, withSys=False):
        """ return the execution time of running a single work unit using
        func in milliseconds
        To measure the cost of running the application with a configuration,
        each training run may finish multiple
        work units to average out the noise.
        :param command: The shell command to use in format of ["app_binary",
        "arg1","arg2",...]
        :param work_units: The total work units in each run
        :param withSys: whether to check system usage or not
        :return: the average execution time for each work unit
        """
        # remove csv if exists
        if os.path.isfile(self.run_dir + 'tmp.csv'):
            os.system('rm ' + self.run_dir + 'tmp.csv')
        time1 = time.time()
        metric_value = None
        if withSys:
            # reassemble the command with pcm calls
            # sudo ./pcm.x -csv=results.csv
            command = self.PCM_PREFIX + command
        os.system(" ".join(command))
        time2 = time.time()
        total_time = time2 - time1
        avg_time = (time2 - time1) * 1000.0 / work_units
        # parse the csv
        if withSys:
            if total_time < 1:
                # the time is too small for parsetmpcsv
                print('TOTAL TIME < 1s', total_time)
                print(" ".join(command))
                metric_value = None
            else:
                metric_value = AppMethods.parseTmpCSV()
                while metric_value is None:
                    print("rerun", " ".join(command))
                    # rerun
                    os.system('rm tmp.csv')
                    os.system(" ".join(command))
                    metric_value = AppMethods.parseTmpCSV()
        return total_time, avg_time, metric_value

    @staticmethod
    def parseTmpCSV():
        NEG_IN_REDUCED_CORE = ['PhysIPC', 'PhysIPC%', 'INSTnom', 'INSTnom%']
        metric_value = Metric()
        with open('tmp.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            metric = []
            values = []
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                elif line_count == 1:  # header line
                    if len(row) != 34:  #broken line
                        print("tmp csv file broken with line", len(row))
                        return None
                    for item in row:
                        metric.append(item)
                    line_count += 1
                else:  # value line
                    value = []
                    if len(row) != len(metric):
                        # discard the row, especially the last row
                        continue
                    for item in row:
                        try:
                            float(item)
                            if float(item) < -1:
                                item = 0
                        except:
                            pass
                        value.append(item)
                    values.append(value)
            for i in range(0, len(metric)):
                if metric[i] != '':
                    try:
                        float(values[0][i])
                    except:
                        if i <= 1:  # date and time
                            continue
                        else:
                            print("not valid number found in csv", values[0],
                                  i)
                            return None
                    # calculate the average value
                    avg_value = functools.reduce(
                        (lambda x, y: (float(y[i]) + float(x))), values,
                        0.) / float(len(values))
                    if avg_value <= -1 and (
                            metric[i] not in NEG_IN_REDUCED_CORE):
                        # broken line
                        print('-1 found in line', metric[i])
                        return None
                    metric_value.add_metric(metric[i], avg_value)
        csv_file.close()
        return metric_value

    def getScaledQoS(self):
        ''' return the scaled QoS from 0 to 100 '''
        return self.getQoS()

    def getQoS(self):
        """ Return the QoS for a configuration"""
        return [0.0]

    def moveFile(self, fromfile, tofile):
        """ move a file to another location
        :param fromfile: file current path
        :param tofile: file new path
        """
        command = ["mv", fromfile, tofile]
        os.system(" ".join(command))

    @staticmethod
    def writeConfigMeasurementToFile(filestream, configuration, values):
        """ write a configuration with its value (could be cost or mv) to a
        opened file stream
        :param filestream: the file stream, need to be opened with 'w'
        :param configuration: the configuration
        :param value: the value in double or string
        """
        filestream.write(configuration.printSelf() + " ")
        if type(values) is dict:
            for submetric, value in values.items():
                filestream.write(str(value) + " ")
        else:
            filestream.write(str(values))
        filestream.write('\n')

    def recordSysUsage(self, configuration, metric):
        """ record the system usage of a configuration
        :param configuration: the configuration
        :param metric: the dict of metric measured
        """
        self.sys_usage_table.add_entry(configuration.printSelf('-'), metric)

    def printUsageTable(self, filestream):
        self.sys_usage_table.printAsCSV(filestream, ',')

    def cleanUpAfterEachRun(self, configs=None):
        """ This function will be called after every training iteration for a
        config
        """
        pass

    def afterGTRun(self):
        """ This function will be called after runGT()
        """
        pass

    def computeQoSWeight(self, preferences, values):
        """ This function will be called by C++ end to finalize a xml
        """
        return 0.0

    def pinTime(self, filestream):
        filestream.write(str(datetime.datetime.now()) + " ")
