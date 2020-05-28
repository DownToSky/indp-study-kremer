# classes for basic abstractions in RSDG

class Knob:
    """a knob setting with max and min settings. It's the smallest unit for
    RAPID-C
    """

    def __init__(self, svc_name, set_name, min, max):
        """ Initialization
        :param svc_name: name of service
        :param set_name: name of setting
        :param min: lower bound
        :param max: upper bound
        """
        self.svc_name = svc_name
        self.set_name = set_name
        self.min = int(min)
        self.max = int(max)


class Knobs:
    """ a collection of Knob
    The Knob object can be retrieved by name
    """

    def __init__(self):
        self.knobs = {}

    def addKnob(self, knob):
        """ Add a knob
        :param knob: the knob to be added
        :return: none
        """
        self.knobs[knob.set_name] = knob

    def getKnob(self, name):
        """ Get a knob
        :param name: name of the knob
        :return: the object
        """
        return self.knobs[name]


class Config:
    """ a config for a certain knob
    """

    def __init__(self, knob, val):
        """ set a knob to a value
        :param knob: a knob instance
        :param val: the value for that knob
        """
        self.knob = knob
        self.val = val


#
class Configuration:
    """ a collection of Config
    """

    def __init__(self):
        self.knob_settings = []

    def addConfig(self, config):
        """ Add a list of configs
        :param config: A list of Config instances
        :return: none
        """
        for c in config:
            self.knob_settings.append(c)

    def retrieve_configs(self):
        """ Return the list of configs
        :return: as described
        """
        return self.knob_settings

    def getSetting(self, knob_name):
        """ Get the value for a particular knob
        :param knob_name: name of the interested knob
        :return: the setting value of that knob
        """
        for c in self.knob_settings:
            if knob_name == c.knob.set_name:
                return c.val

    def __eq__(self, other):
        if isinstance(other, Configuration):
            return other.printSelf() == self.printSelf()
        else:
            return False

    def __hash__(self):
        return hash(self.printSelf())

    def printSelf(self, delimiter=' '):
        """ print the configuration to a readable string, separated by
        white-space
        :return: as described
        """
        items = list(
            map((lambda x: x.knob.set_name + delimiter + str(x.val)),
                self.knob_settings))
        items.sort()
        return delimiter.join(sorted(items))
        # for config in self.knob_settings:
        #    result += " " + config.knob.set_name + " " + str(config.val)
        # return result

class Constraint:
    """ a continuous constraint with source and sink
    The syntax of a constraint is:
    if sink_min <= sink <= sink_max, then source_min <= source <= source_max
    """

    def __init__(self, type, source, sink, source_min, source_max, sink_min,
                 sink_max):
        """ Initialization
        :param type: AND or OR, in string
        :param source: string
        :param sink: string
        :param source_min: lower bound of source
        :param source_max: upper bound of source
        :param sink_min: lower bound of sink
        :param sink_max: upper bound of sink
        """
        self.type = type
        self.source = source
        self.sink = sink
        self.source_min = int(source_min)
        self.source_max = int(source_max)
        self.sink_min = int(sink_min)
        self.sink_max = int(sink_max)

class Segment:
    """ a segment of a knob
    The segment of knob can be used both in dependencies and constraint
    """

    def __init__(self, seg_name, knob_name, min, max):
        """ Initilization
        :param seg_name: segment name
        :param knob_name: knob name
        :param min: lower bound of the segment
        :param max: upper bound of the segment
        """
        self.seg_name = seg_name
        self.knob_name = knob_name
        self.min = min
        self.max = max
        self.a = 0.0  # the linear coefficient value
        self.b = 0.0  # the constant coefficient value

    def setID(self, id):
        """Set the id of the segment
        :param id: an integer ID
        :return: None
        """
        self.id = id

    def printID(self):
        """ Return the readable segment id
        :return: seg_name + [id]
        """
        return self.seg_name + "_" + str(self.id)

    def printVar(self):
        """ Return the variable name in LP representing the linear coefficient
        :return: a string
        """
        return self.seg_name + "_" + str(self.id) + "_V"

    def printConst(self):
        """ Return the variable name in LP representing the constant coefficient
        :return:
        """
        return self.seg_name + "_" + str(self.id) + "_C"

    def setLinearCoeff(self, a):
        """ Setter of the linear coeff
        :param a: a double value
        """
        self.a = a

    def setConstCoeff(self, b):
        """ Setter of the Constant coeff
        :param b: a double value
        """
        self.b = b
