import graphviz
from State import State 
class NFA:
    def __init__(self, start=None, accept=None, postfix=None):
        self.start = start
        self.accept = accept
        if not start and not accept and postfix:
            obj = self.postfix2nfa(postfix)
            self.start = obj.start
            self.accept = obj.accept
    # utility functions
    def getStateByLabel(self, label):
        for state in self.getStates():
            if state.label == label:
                return state
        return None
    def getStatesByLabel(self, labels):
        labels = labels.split()
        statesList = []
        for label in labels:
            for state in self.getStates():
                if state.label == label:
                    statesList.append(state)
        return statesList
    def checkIfAcceptingState(self, states):
        for state in states:
            if state.is_accept:
                return True
        return False
    def getStates(self):
        visited = set()
        states = []
        queue = [self.start]
        visited.add(self.start)
        while queue:
            state = queue.pop(0)
            states.append(state)
            for (transition) in state.transitions:
                if transition[1] not in visited:
                    visited.add(transition[1])
                    queue.append(transition[1])

        return states
    def getSymbols(self):
        """
        Returns the set of symbols that can be used to transition between NFA states.
        """
        states = self.getStates()
        symbols = set()
        for state in states:
            for symbol, next_state in state.transitions:
                if symbol != 'ϵ':
                    symbols.add(symbol)
        # convert to list of symbols
        return list(symbols)
    # Conversion from postfix to NFA
    def postfix2nfa(self, postfix): # shunting yard algorithm
        nfaStack = []
        i = 0
        for c in postfix:
            if c == '*':
                nfa1 = nfaStack.pop()
                start, accept = State('S' + str(i)), State('S' + str(i + 1))
                start.add_transition('ϵ', nfa1.start)
                start.add_transition('ϵ', accept)
                nfa1.accept.add_transition('ϵ', start)
                nfa1.accept.add_transition('ϵ', accept)
                nfaStack.append(NFA(start, accept))
                i += 2

            elif c == '.':
                nfa2, nfa1 = nfaStack.pop(), nfaStack.pop()
                nfa1.accept.add_transition('ϵ', nfa2.start)
                nfaStack.append(NFA(nfa1.start, nfa2.accept))

            elif c == '|':
                nfa2, nfa1 = nfaStack.pop(), nfaStack.pop()
                start, accept = State('S' + str(i)), State('S' + str(i + 1))
                start.add_transition('ϵ', nfa1.start)
                start.add_transition('ϵ', nfa2.start)
                nfa1.accept.add_transition('ϵ', accept)
                nfa2.accept.add_transition('ϵ', accept)
                nfaStack.append(NFA(start, accept))
                i += 2

            elif c == '+':
                nfa1 = nfaStack.pop()
                start, accept = State('S' + str(i)), State('S' + str(i + 1))
                start.add_transition('ϵ', nfa1.start)
                nfa1.accept.add_transition('ϵ', start)
                nfa1.accept.add_transition('ϵ', accept)
                nfaStack.append(NFA(start, accept))
                i += 2

            elif c == '?':
                nfa1 = nfaStack.pop()
                start, accept = State('S' + str(i)), State('S' + str(i + 1))
                start.add_transition('ϵ', nfa1.start)
                start.add_transition('ϵ', accept)
                nfa1.accept.add_transition('ϵ', accept)
                nfaStack.append(NFA(start, accept))
                i += 2

            else:
                start, accept = State('S' + str(i)), State('S' + str(i + 1))
                start.add_transition(c, accept)
                nfaStack.append(NFA(start, accept))
                i += 2

        return nfaStack.pop()
    # For exporting NFA
    def toDict(self):
        states = {}
        for state in self.getStates():
            state_dict = {
                'isTerminatingState': state.is_accept,
            }
            for char, next_state in state.transitions:
                if char not in state_dict:
                    state_dict[char] = next_state.label
                else:
                    state_dict[char] += ',' + next_state.label
            states[state.label] = state_dict

        return {
            'startingState': self.start.label,
            **states,
        }
    def visualize(self, name='output/nfa.gv', view=False):
        nfa_json = self.toDict()
        graph = graphviz.Digraph(engine='dot')
        for state, transitions in nfa_json.items():
            if state == 'startingState':
                continue
            if transitions['isTerminatingState']:
                graph.node(state, shape='doublecircle')
            else:
                graph.node(state, shape='circle')
            for char, next_state in transitions.items():
                if char == 'isTerminatingState':
                    continue
                children_states = next_state.split(',')
                for child in children_states:
                    graph.edge(state, child, label=char)
        graph.render(name, view=view)
        return graph
