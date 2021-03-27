from ..state import State

class Time:

    def __init__(self, init):
        self.time = init
        initRaw = init.replace("[", "")
        initRaw = init.replace("]", "")
        initTab = initRaw.split(':')
        self.state = State.INVALID
        if (len == 3):
            self.hour = initTab[0]
            self.minute = initTab[1]
            self.second = initTab[2]
            self.state = State.VALID