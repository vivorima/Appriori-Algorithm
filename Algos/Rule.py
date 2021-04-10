class regle:

    def __init__(self, cons, conf, lift):
        self.tuple = cons
        self.confidence = conf
        self.lift = lift

    def __repr__(self):
        return str(self.tuple) + "   Conf= " + str(self.confidence) + "  Lift= " + str(self.lift)

    def __str__(self):
        return str(self.tuple) + "   Conf= " + str(self.confidence) + "  Lift= " + str(self.lift)
