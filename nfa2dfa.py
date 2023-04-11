import graphviz
from collections import deque


class DFA:
    def __init__(self, nfa):
        self.nfa = nfa
        self.states = self.nfa_to_dfa(nfa)
    def getStateByLabel(self, label):
        return self.nfa.getStateByLabel(label)
    def getStatesByLabel(self, labels):
        return self.nfa.getStatesByLabel(labels)
    def checkIfAcceptingState(self, states):
        for state in states:
            if state.is_accept:
                return True
        return False
    def getSymbols(self):
        return self.nfa.get_symbols()
    def epsilon_closure(self, states):
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

    def nfa_to_dfa(self, nfa):
        nfaStates = nfa.get_states()
        symbols = nfa.get_symbols()
        # initial state
        start_state = self.epsilon_closure([nfaStates[0]])
        self.states = {'startingState': start_state}
        # the rest of the nfaStates
        queue = deque([start_state])
        seen = set([start_state])
        while queue:
            current_state = queue.popleft()
            for symbol in symbols:
                next_states = self.epsilon_closure(self.move(nfa, current_state, symbol))
                if next_states == '' or next_states == ' ':
                    continue
                if next_states not in seen:
                    queue.append(next_states)
                    seen.add(next_states)
                self.states.setdefault(current_state, {})[symbol] = next_states
            self.states.setdefault(current_state, {})['isTerminatingState'] = nfa.checkIfAcceptingState(nfa.getStatesByLabel(current_state))
        return self.states
    def to_dict(self):
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




