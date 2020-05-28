# The system usage table used for generating the xxx-sys.csv

class SysUsageTable:
    def __init__(self):
        self.table = dict()
        self.metrics = []

    def add_entry(self, configuration, metric):
        self.table[configuration] = metric
        if not self.metrics:
            self.metrics = metric.metric_names

    def printAsCSV(self, filestream, delimiter):
        # write the header
        header_written = False
        # write the body
        for configuration, metric in self.table.items():
            # write the header
            if not header_written:
                filestream.write(metric.printAsHeader(delimiter))
                filestream.write('\n')
                header_written = True
            # write the configuration
            filestream.write(configuration + delimiter)
            filestream.write(metric.printAsCSVLine(delimiter))
            filestream.write("\n")
        filestream.close()
