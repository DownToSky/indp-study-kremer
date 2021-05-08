# a fake stress tool instance generator
import random

class SysArgs:
    def __init__(self):
        self.env = {}
        self.env["cpu_num"] = [0, 0, 0, 1, 2, 3, 4, 5]
        self.env["io"] = [0, 0, 1, 2, 3]
        self.env["vm"] = [0, 0, 1, 2, 3, 4]
        self.env["vm_bytes"] = ["128K", "256K", "512K", "1M"]

    def getRandomEnv(self):
        cpu_num = random.choice(self.env['cpu_num'])
        io = random.choice(self.env['io'])
        vm = random.choice(self.env['vm'])
        vm_bytes = random.choice(self.env['vm_bytes'])
        # in case everyone is 0
        if cpu_num + io + vm == 0:
            cpu_num = 1
        command = ['/usr/bin/stress', '-q']
        cpu_substr = '' if cpu_num == 0 else '--cpu ' + str(cpu_num)
        io_substr = '' if io == 0 else '--io ' + str(io)
        vm_substr = '' if vm == 0 else '--vm ' + str(
            vm) + ' --vm-bytes ' + vm_bytes
        command.append(cpu_substr)
        command.append(io_substr)
        command.append(vm_substr)
        config_name = 'cpu_' + str(cpu_num) + '_io_' + str(io) + '_vm_' + str(
            vm) + '_vmbytes_' + str(vm_bytes)
        return {
            'app': 'stress',
            'configuration': config_name,
            'command': command
        }
