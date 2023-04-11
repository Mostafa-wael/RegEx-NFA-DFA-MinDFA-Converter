import re
import graphviz

def shunt_yard(regex):
    operators = {'*': 5, '+': 4, '?': 3, '.': 2, '|': 1}

    postfix, stack = "", ""

    for i in range(len(regex)):
        c = regex[i]
        if c == '[':
            j = i + 1
            while regex[j] != ']':
                if regex[j].isalnum() and regex[j + 1].isalnum():
                    regex = regex[:j + 1] + '|' + regex[j + 1:]
                j += 1

    regex = regex.replace('[', '(')
    regex = regex.replace(']', ')')

    hyphen_count = regex.count('-')
    for i in range(hyphen_count):
        for j in range(len(regex)):
            c = regex[j]
            if c == '-':
                final = regex[j + 1]
                first = regex[j - 1]
                temp_list = ''
                for k in range(int(ord(final) - ord(first))):
                    temp_list = temp_list + '|'
                    char = chr(ord(first) + k + 1)
                    temp_list = temp_list + char
                regex = regex[0: j] + temp_list + regex[j + 2:]
                break

    for i in range(len(regex) - 1):
        print(regex[i])
        if (regex[i].isalnum() and regex[i + 1].isalnum()) or (regex[i] in ('*', '+', '?') and regex[i + 1] != '.') or (regex[i].isalnum() and regex[i + 1] == '('):
            regex = regex[:i + 1] + '.' + regex[i + 1:]

    print(regex)
    for i in range(len(regex)):
        c = regex[i]
        if c == '(':
            stack = stack + c
        
        elif c == ')':
            while stack[-1] != '(':
                postfix = postfix + stack[-1]  # places the character at the end of the stack in the postfix expression
                stack = stack[:-1]  # [:-1] denotes up to or including the last character
            stack = stack[:-1]  # removes the open bracket in the stack

        elif c in operators:
            while stack and operators.get(c, 0) <= operators.get(stack[-1], 0):
                postfix, stack = postfix + stack[-1], stack[:-1]
            stack = stack + c
        
        else:
            postfix = postfix + c

    while stack:
        postfix, stack = postfix + stack[-1], stack[:-1]

    return postfix


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


class NFA:
    def __init__(self, start=None, accept=None):
        self.start = start
        self.accept = accept

    def to_dict(self):
        states = {}
        for state in self.get_states():
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

    def get_states(self):
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

    def visualize(self):
        nfa_json = self.to_dict()
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
        return graph


def postfix_to_nfa(postfix):
    nfaStack = []
    i = 1

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



# postfix = shunt_yard("([A-Ea-c]+.1)|(2.[0-9]*.K?.[ABC].A.B.C)")
postfix = shunt_yard("([A-Ea-c]+1)|(2[0-9]*K?[ABC]ABC)")
# print(postfix)
# nfa = postfix_to_nfa(postfix)
# print(nfa.to_dict())
# graph = nfa.visualize()
# graph.render('nfa.gv', view=False)