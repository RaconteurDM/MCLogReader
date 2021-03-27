from ..state import State

class Date:

    def __init__(self, init):
        initTab = init.split('-')
        self.state = State.INVALID
        if (len(initTab) == 4):
            self.year = initTab[0]
            self.month = initTab[1]
            self.day = initTab[2]
            self.num = initTab[3]
            self.date = initTab[0] + "/" + initTab[1] + "/" + initTab[2]
            self.state = State.VALID