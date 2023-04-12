import graphviz
from collections import deque


class DFA:
    def __init__(self, nfa):
        self.nfa = nfa
        self.states = self.nfa2dfa(nfa)
    # utility functions
    def getStateByLabel(self, label):
        return self.nfa.getStateByLabel(label)
    def getStatesByLabel(self, labels):
        return self.nfa.getStatesByLabel(labels)
    def getSymbols(self):
        return self.nfa.getSymbols()
    # DFA functions
    def epsilonClosure(self, states):
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            for symbol, next_state in state.transitions:
                if next_state not in closure:
                    if symbol == "ϵ":
                        closure.add(next_state)
                        stack.append(next_state)
        # convert set to list
        closureList =  list(closure)
        # sort the list
        closureList.sort(key=lambda x: x.label)
        # convert into a string representation
        closureString = ''
        for state in closureList:
            closureString += ' ' + state.label
        # remove the first space
        return closureString[1:]
    def move(self, nfa, states, symbol):
        move_states = set()
        # convert string to list
        statesList = states.split()
        # convert list of labels to list of states
        states = []
        for label in statesList:
            states.append(nfa.getStateByLabel(label))
        for state in states:
            for s, next_state in state.transitions:
                if s == symbol:
                    move_states.add(next_state)
        return move_states
    # Conversion from NFA to DFA
    def nfa2dfa(self, nfa):
        nfaStates = nfa.getStates()
        symbols = nfa.getSymbols()
        # initial state
        start_state = self.epsilonClosure([nfaStates[0]])
        self.states = {'startingState': start_state}
        # the rest of the nfaStates
        queue = deque([start_state])
        seen = set([start_state])
        while queue:
            current_state = queue.popleft()
            for symbol in symbols:
                next_states = self.epsilonClosure(self.move(nfa, current_state, symbol))
                if next_states == '' or next_states == ' ':
                    continue
                if next_states not in seen:
                    queue.append(next_states)
                    seen.add(next_states)
                self.states.setdefault(current_state, {})[symbol] = next_states
            self.states.setdefault(current_state, {})['isTerminatingState'] = nfa.checkIfAcceptingState(nfa.getStatesByLabel(current_state))
        return self.states
    # for exporting the DFA
    def toDict(self):
        return self.states.copy()
    def visualize(self, name='output/dfa.gv', view=False):
        graph = graphviz.Digraph(engine='dot')
        for state, transitions in self.states.items():
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
        graph.render("output/dfa", view=False)




