import re
import json
import graphviz

def validate_regex(regex):
    try:
        re.compile(regex)
    except re.error:
        print(f"Invalid regular expression: {regex}")
        return False
    return True

class State:
    def __init__(self, label, transitions=[], parents = [], is_start=False, is_accept=True):
        self.label = label
        self.parents = []
        self.transitions = [] 
        self.is_start = is_start
        self.is_accept = is_accept

    def add_transition(self, symbol, state):       
        self.transitions.append((symbol, state))
        self.is_accept = False
        state.parents.append(self)
        print(f"Transition from {self.label} to {state.label} on {symbol}")

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
            for char, next_state in state.transitions.items():
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
            print(state.transitions)
            for (transition) in state.transitions:
                if transition not in visited:
                    visited.add(transition)
                    queue.append(transition)

        return states

    def visualize(self):
        nfa_json = self.to_dict()
        graph = graphviz.Digraph(engine='dot')
        start_state = nfa_json['startingState']
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
                graph.edge(state, next_state, label=char)
        return graph


def compile(regex):
    stack = [State(f"s0", None)]
    state_count = 1
    for c in regex:
        if c == 'ϵ':
            pass
        elif c == '(':
            # start a new group
            stack.append(State(f"s{state_count}"))
            state_count += 1
        elif c == ')':
            # end the current group
            if len(stack) == 0:
                raise Exception("Invalid regular expression")
            group_state = stack.pop()
            if len(stack) > 0:
                stack[-1].add_transition('ϵ', group_state)
            else:
                return group_state
        elif c == '|':
            # create an alternate branch
            if len(stack) == 0:
                raise Exception("Invalid regular expression")
            current_state = stack[-1]
            current_state.add_transition('ϵ', State(f"s{state_count}"))
            state_count += 1
            # stack.append(current_state.get_transition('ϵ'))
        elif c == '*':
            # Kleene star closure
            if len(stack) < 2:
                raise Exception("Invalid regular expression")
            old_accept_state = stack.pop()
            previous_state = stack.pop()
            new_temp_state1 = State(f"s{state_count + 1}")
            new_temp_state2 = State(f"s{state_count + 2}")
            state_count += 2
            previous_state.add_transition('ϵ', new_temp_state1)
            new_temp_state2.add_transition('ϵ', old_accept_state)
            new_temp_state2.add_transition('ϵ', new_temp_state1)
            previous_state_transitions = previous_state.transitions
            print("trans", previous_state_transitions)
            for symbol in [t[0] for t in previous_state_transitions if t[1] == old_accept_state]:
                new_temp_state1.add_transition(symbol, new_temp_state2)
                previous_state_transitions.remove((symbol, old_accept_state))
               
            previous_state.add_transition('ϵ', old_accept_state)
            stack.append(previous_state)
            stack.append(new_temp_state1)
            stack.append(new_temp_state2)
            stack.append(old_accept_state)
        elif c == '+':
            # one or more
            if len(stack) == 0:
                raise Exception("Invalid regular expression")
            previous_state = stack.pop()
            previous_state_parents = previous_state.get_parents()
            for parent in previous_state_parents:
                parent.add_transition('ϵ', previous_state)
                previous_state.add_transition('ϵ', parent)
            new_state = State(f"s{state_count}")
            state_count += 1
            previous_state.add_transition('ϵ', new_state)
            stack.append(new_state)
        else:
            # create a new state for the character
            new_state = State(f"s{state_count}")
            state_count += 1
            if len(stack) == 0:
                raise Exception("Invalid regular expression")
            previous_state = stack[-1]
            previous_state.add_transition(c, new_state)
            stack.append(new_state)

    # if len(stack) != 1:
    #     raise Exception("Invalid regular expression")

    return stack[0]

def main():
    # regex = input("Enter regular expression: ")
    regex = "A"
    if not validate_regex(regex):
        return
    state = compile(regex)
    nfa = NFA(start=state)
    d = nfa.to_dict()
    # Output
    print("Regex: ", regex)
    print("NFA: ")
    print(json.dumps(d, indent=4))
    graph = nfa.visualize()
    graph.render('nfa.gv', view=False)

if __name__ == "__main__":
    main()

# TODO: you have changed the transitions attribute to a list, but you haven't changed the add_transition method to add to the list nor the rest of the functions

# TODO:
# Alteration -> A | B
# 1 or more -> A+
# 0 or more > A*
# Optional -> A?
# ORing (aka Char/Num classes) -> [ABC] or [345]
# Ranges -> [0-9] or [a-z]
# Brackets or grouping -> (ABD)+
#? Done 
# Concatenation -> AB, ϵA

