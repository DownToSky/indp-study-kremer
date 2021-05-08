class InterCoeff:
    """ a coefficients holder
    """

    def __init__(self):
        """Initialization
        """
        self.a = 0.0
        self.b = 0.0
        self.c = 0.0

    def addQuadCoeff(self, a):
        """Set the quad coeff
        :param a: quad coeff value
        """
        self.a = a

    def addLinearCoeff(self, b):
        """Set the linear coeff
        :param b: linear coeff value
        """
        self.b = b

    def addConstCoeff(self, c):
        """Set the constant coeff
        :param c: constant coeff value
        """
        self.c = c

    def retrieveCoeffs(self):
        """ Return the values
        :return: [quad, linear, constant]
        """
        return self.a, self.b, self.c
