# represent the system environment metric

class Metric:
    EXCLUDED_METRIC = {
        "Date",
        "Time",
        "Proc Energy (Joules)",
        'C0res%',
        'C10res%',
        'C1res%',
        'C2res%',
        'C3res%',
        'C6res%',
        'C7res%',
        'C8res%',
        'C9res%',
    }

    def __init__(self, addtl_exclusion={}):
        self.metrics = dict()
        self.metric_names = []
        self.addtl_exclusion = {}

    def add_metric(self, name, value):
        if name not in self.EXCLUDED_METRIC and name not in self.addtl_exclusion:
            self.metrics[name] = value
            self.metric_names.append(name)
            self.metric_names = sorted(self.metric_names)

    def printAsCSVLine(self, delimiter):
        metricsNames = map(lambda metric: str(self.metrics[metric]),
                           self.metric_names)
        return delimiter.join(metricsNames)

    def printAsHeader(self, delimiter, leading="Configuration", id=''):
        if leading == "Configuration":
            leading = leading + delimiter
        updated_metrics = map(lambda x: x + id, self.metric_names)
        return leading + delimiter.join(sorted(updated_metrics))
