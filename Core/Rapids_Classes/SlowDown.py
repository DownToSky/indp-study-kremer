# Slowdown Class with write table function
import hashlib

class SlowDown:
    def __init__(self, configuration):
        self.configuration = configuration
        self.slowdown_table = dict()
        self.metrics = dict()
        self.stresser_info = dict()

    def add_slowdown(self, metric, slowdown, stresser_info=''):
        signature = self.get_md5(metric).hexdigest()
        self.slowdown_table[signature] = slowdown
        self.metrics[signature] = metric
        if stresser_info != '':
            self.stresser_info[signature] = stresser_info

    def get_md5(self, metric):
        return hashlib.md5(metric.printAsCSVLine(',').encode())

    def get_metric(self, md5string):
        return self.metrics[md5string].printAsCSVLine(
            ',') if md5string in self.metrics else ''

    def get_slowdown(self, metric):
        md5hex = self.get_md5(metric).hexdigest()
        return self.slowdown_table[
            md5hex] if md5hex in self.slowdown_table else -1.

    def writeSlowDownTable(self, filestream):
        # write the metric
        for metricmd5, slowdown in self.slowdown_table.items():
            # write the config
            filestream.write(self.configuration.printSelf('-'))
            filestream.write(',')
            if metricmd5 in self.stresser_info:
                filestream.write(self.stresser_info[metricmd5])
                filestream.write(',')
            filestream.write(self.get_metric(metricmd5))
            filestream.write(',')
            filestream.write(str(slowdown))
            filestream.write('\n')
