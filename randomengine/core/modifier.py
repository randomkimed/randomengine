# randomengine.core > modifier

class Modifier:
    def __init__(self):
        self.name = __class__

    def START(self):
        pass

    def AWAKE(self):
        pass

    def UPDATE(self):
        pass

    def LATE_UPDATE(self):
        pass

    def FIXED_UPDATE(self):
        pass

    def EXIT(self):
        pass