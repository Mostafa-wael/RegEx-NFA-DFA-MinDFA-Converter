class State:
    def __init__(self, label, transitions=[], parents=[], is_start=False, is_accept=True):
        self.label = label
        self.parents = []
        self.transitions = []
        self.is_start = is_start
        self.is_accept = is_accept

    def add_transition(self, symbol, state):
        self.transitions.append((symbol, state))
        self.is_accept = False
        state.parents.append(self)

    def get_parents(self):
        return self.parents.copy()