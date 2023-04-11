import re
import graphviz


def validate_regex(regex):
    try:
        re.compile(regex)
    except re.error:
        print(f"Invalid regular expression: {regex}")
        return False
    return True


def shunt_yard(regex):
    # Map each operator to its precedence level.
    # The operators supported by this code are * (kleene star), + (one or more), ? (zero or one), . (concatenation), and | (alternation).
    operators = {'*': 5, '+': 4, '?': 3, '.': 2, '|': 1}
    # postfix will eventually store the postfix notation of the input regular expression,.
    # stack is used as an intermediate stack in the Shunting Yard algorithm.
    postfix, stack = "", ""
    # Check if the regular expression contains any character classes (denoted by square brackets).
    # If a character class is found, the function converts it to an alternation between the characters inside the class.
    # For example, the character class [abc] would be converted to the regular expression (a|b|c).
    # This is done using a while loop that iterates over the characters of the regular expression, finds the opening and closing brackets of the character class, and replaces the contents of the class with an alternation.
    for i in range(len(regex)):
        c = regex[i]
        if c == '[':
            j = i + 1
            while regex[j] != ']':
                if regex[j].isalnum() and regex[j + 1].isalnum():
                    regex = regex[:j + 1] + '|' + regex[j + 1:]
                j += 1

    # Replace all remaining square brackets with parentheses.
    # This is done because parentheses are used to group sub-expressions in regular expressions
    regex = regex.replace('[', '(')
    regex = regex.replace(']', ')')

    print("postfix1: ", regex)

    # Replace any hyphen character (-) in the regular expression with an alternation between the characters on either side of the hyphen.
    # For example, the expression a-z would be converted to (a|b|c|...|y|z).
    # This is done using another for loop that iterates over the characters of the regular expression, finds the hyphen character, and replaces it with an alternation.
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
    print("postfix2: ", regex)
    # Insert a concatenation operator (.) between any two adjacent characters(characters that are not operators), unless the characters are already separated by an operator, or the second character is an opening parenthesis.
    dotIndices = []
    for i in range(len(regex) - 1):
        twoConsecutiveChar = regex[i].isalnum() and regex[i + 1].isalnum()
        operatorsNotFollowedByDot = regex[i] in ('*', '+', '?') and regex[i + 1] != '.'
        charFollowedByOpenBracket = regex[i].isalnum() and regex[i + 1] == '('
        if twoConsecutiveChar or operatorsNotFollowedByDot or charFollowedByOpenBracket:
            dotIndices.append(i)
    for i in range(len(dotIndices)):
        regex = regex[:dotIndices[i] + 1 + i] + '.' + regex[dotIndices[i] + 1 + i:]
    print("postfix3: ", regex)
    # Iterate over each character of the regular expression and performs the Shunting Yard algorithm.
    for i in range(len(regex)):
        c = regex[i]
        # If the character is an opening parenthesis, push it onto the stack.
        if c == '(':
            stack = stack + c

        # If the character is a closing parenthesis, pop operators off the stack and append them to the postfix string until an opening parenthesis is found. Then pop the opening parenthesis from the stack.
        elif c == ')':
            while stack[-1] != '(':
                # places the character at the end of the stack in the postfix expression
                postfix = postfix + stack[-1]
                # [:-1] denotes up to or including the last character
                stack = stack[:-1]
            stack = stack[:-1]  # removes the open bracket in the stack

        # If the character is an operator, pop operators off the stack and append them to the postfix string as long as they have higher or equal precedence to the current operator. Then push the current operator onto the stack.
        elif c in operators:
            while stack and operators.get(c, 0) <= operators.get(stack[-1], 0):
                postfix, stack = postfix + stack[-1], stack[:-1]
            stack = stack + c

        # If the character is a operand (i.e. not an operator or parenthesis), append it to the postfix string.
        else:
            postfix = postfix + c

    # After iterating over all characters of the regular expression, the function pops any remaining operators off the stack and appends them to the postfix string.
    while stack:
        postfix, stack = postfix + stack[-1], stack[:-1]
    print("postfix4: ", regex)

    # Finally, the function returns the postfix notation of the input regular expression.
    return postfix


def postfix_to_nfa(postfix):
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
    def getClosure(self, state, symbol="ϵ"):
        # return the set of states that can be reached from this state
        # using the given symbol or epsilon
        closure = set()
        stack = [state]
        while stack:
            curr_state = stack.pop()
            closure.add(curr_state)

            for action, next_state in curr_state.transitions:
                if next_state not in closure:
                    if action == "ϵ" or action == symbol:
                        stack.append(next_state)
        return closure
    def get_symbols(self):
        """
        Returns the set of symbols that can be used to transition between NFA states.
        """
        states = self.get_states()
        symbols = set()
        for state in states:
            for symbol, next_state in state.transitions:
                if symbol != 'ϵ':
                    symbols.add(symbol)
        # convert to list of symbols
        return list(symbols)
    def visualize(self, name='nfa.gv', view=False):
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
        graph.render(name, view=view)
        return graph



from collections import deque
def epsilon_closure(states):
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


def getStateByLabel(states, label):
    for state in states:
        if state.label == label:
            return state
    return None

def move(nfaStates, states, symbol):
    move_states = set()
    # convert string to list
    statesList = states.split()
    # convert list of labels to list of states
    states = []
    for label in statesList:
        states.append(getStateByLabel(nfaStates, label))
    for state in states:
        for s, next_state in state.transitions:
            if s == symbol:
                move_states.add(next_state)
    return move_states

def checkIfAcceptingState(nfaStates, statesList):
    statesList = statesList.split()
    states = []
    for label in statesList:
        states.append(getStateByLabel(nfaStates, label))
    for state in states:
        if state.is_accept:
            return True
    return False
def nfa_to_dfa(nfa):
    nfaStates = nfa.get_states()
    nfaDict = nfa.to_dict()
    symbols = nfa.get_symbols()
    # initial state
    start_state = epsilon_closure([nfaStates[0]])
    dfa = {'startingState': start_state}
    # the rest of the nfaStates
    queue = deque([start_state])
    seen = set([start_state])
    while queue:
        current_state = queue.popleft()
        for symbol in symbols:
            next_states = epsilon_closure(move(nfaStates, current_state, symbol))
            if next_states == '' or next_states == ' ':
                continue
            if next_states not in seen:
                queue.append(next_states)
                seen.add(next_states)
            dfa.setdefault(current_state, {})[symbol] = next_states
        dfa.setdefault(current_state, {})['isTerminatingState'] = checkIfAcceptingState(nfaStates, current_state)
    return dfa




def main():
    # regex = "([A-Ea-c]+.1)|(2.[0-9]*.K?.[ABC].A.B.C)"
    regex = "([A-Ea-c]+1)|(2[0-9]*K?[ABC]ABC)"
    # regex = "ab(b|c)*d+"
    regex = "(a+b)*"
    # regex = input("Enter regular expression: ")
    if not validate_regex(regex):
        return
    print("regex:", regex)
    postfix = shunt_yard(regex)
    print("postfix:", postfix)
    # print("expected:", "A|B|C|D|E|a|b|c1+20|1|2|3|4|5|6|7|8|9K*A|B|CABC?|")
    nfa = postfix_to_nfa(postfix)
    print("NFA: ", nfa.to_dict())
    nfa.visualize(name='nfa.gv', view=False)
    print("----------------------------------------------------------------")
    dfa = nfa_to_dfa(nfa)
    print("DFA: ", dfa)
    # Print the DFA states
    graph = graphviz.Digraph(engine='dot')
    for state, transitions in dfa.items():
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
    graph.render("dfa", view=False)
    


if __name__ == '__main__':
    main()
