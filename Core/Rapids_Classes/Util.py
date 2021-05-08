def recoverTimeRecord(appInfo, units):
    ''' estimate the total training time from a trained cost profile '''
    time_record = {}
    with open(appInfo.FILE_PATHS['COST_FILE_PATH'], 'r') as costfile:
        for line in costfile:
            col = line.split()
            unit_cost = col[-1]
            configs = []
            config_part = col[0:-1]
            for i in range(0, len(config_part) - 1, 2):
                name = config_part[i]
                val = config_part[i + 1]
                configs.append(name + "-" + val)
            config = "-".join(sorted(configs))
            time_record[config] = float(unit_cost) * units
    return time_record