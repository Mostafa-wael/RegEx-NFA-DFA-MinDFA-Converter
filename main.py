
import re
#? Implementing Thompson's construction algorithm:
# This code implements Thompson's construction algorithm to convert a regular expression into an NFA represented as a graph of State objects. 
# Each State object has a label, a dictionary of transitions keyed by input symbols, and boolean flags indicating whether it is a start state or an accepting state.
class State:
    def __init__(self, label, transitions=None, is_start=False, is_accept=False):
        self.label = label
        self.transitions = transitions or {}
        self.is_start = is_start
        self.is_accept = is_accept

    def add_transition(self, symbol, state):
        self.transitions[symbol] = state

    def get_transition(self, symbol):
        return self.transitions.get(symbol)

# This function takes a regular expression string as input and returns an NFA object that represents the same language as the regular expression. 
# The function implements Thompson's construction algorithm by iteratively building NFA fragments from the regular expression string, and combining these fragments using operations like concatenation, union, and Kleene star.
# The function maintains a stack of NFA fragments, and iterates over the characters in the regular expression string one at a time. 
# For each character, the function performs a different operation on the top one or two fragments on the stack, depending on the character:
# If the character is an opening parenthesis, the function pushes an empty fragment onto the stack.
# If the character is a vertical bar (|), the function pops the top two fragments off the stack, creates a new start and accept state for the resulting fragment, and connects these states to the start and accept states of the two fragments using epsilon transitions.
# If the character is a dot (.), the function concatenates the top two fragments on the stack

def compile(regex):
    stack = []
    state_count = 0

    for c in regex:
        if c == '(':
            # start a new group
            stack.append(State(f"s{state_count}"))
            state_count += 1
        elif c == ')':
            # end the current group
            group_state = stack.pop()
            if len(stack) > 0:
                stack[-1].add_transition(None, group_state)
            else:
                return group_state
        elif c == '|':
            # create an alternate branch
            current_state = stack[-1]
            current_state.add_transition(None, State(f"s{state_count}"))
            state_count += 1
            stack.append(current_state.get_transition(None))
        elif c == '*':
            # Kleene star closure
            current_state = stack[-1]
            new_state = State(f"s{state_count}")
            state_count += 1
            new_state.add_transition(None, current_state)
            current_state.add_transition(None, new_state)
            stack[-1] = new_state
        else:
            # create a new state for the character
            new_state = State(f"s{state_count}")
            state_count += 1
            new_state.is_accept = True
            stack.append(new_state)
            if len(stack) > 1:
                stack[-2].add_transition(c, new_state)
    
    if len(stack) != 1:
        raise Exception("Invalid regular expression")

    return stack[0]

#? Converting the NFA to a JSON representation:
import json

def to_json(state):
    state_dict = {}
    for symbol, transition_state in state.transitions.items():
        state_dict[symbol] = transition_state.label
    return {
        "isTerminatingState": state.is_accept,
        **state_dict,
    }

def nfa_to_json(state):
    json_data = {"startingState": state.label}
    queue = [state]
    seen = set()

    while queue:
        current_state = queue.pop(0)
        if current_state.label in seen:
            continue
        seen.add(current_state.label)
        json_data[current_state.label] = to_json(current_state)
        queue.extend(current_state.transitions.values())

    return json.dumps(json)

# def parse_regex(regex):
#     stack = [] # stack of NFA objects, to keep track of the NFA states
#     state_count = 0
#     start = State(label=f"q{state_count}", is_start=True)
#     accept = State(label=f"q{state_count + 1}", is_accept=True)
#     # iterate over each char in the regex
#     for char in regex:
#         if char.isalpha() or char.isdigit(): # if char is a letter or digit, this is the trivial case
#             state_count += 1
#             start_state = State(f"q{state_count}") # start state
#             accept_state = State(f"q{state_count + 1}", is_accept=True) # 
#             start_state.add_transition(char, accept_state) # add transition
#             start = start_state
#             accept = accept_state
#             stack.append(NFA(start=start_state, accept=accept_state)) # add to stack
#         # handle the special characters
#         elif char == '*':
#             nfa = stack.pop() # get the last char
#             new_start = State(f"q{state_count + 1}") # create new start state
#             new_accept = State(f"q{state_count + 2}", is_accept=True) # create new accept state
#             # apply all the transition possibilities on epsilon
#             new_start.add_transition('eps', nfa.start)
#             new_start.add_transition('eps', new_accept)
#             nfa.accept.add_transition('eps', new_accept)
#             nfa.accept.add_transition('eps', nfa.start)
#             state_count += 2
#             start = new_start
#             accept = new_accept
#             stack.append(NFA(start=new_start, accept=new_accept))
#         elif char == '|':
#             # pop the last two NFA objects from the stack
#             nfa2 = stack.pop()
#             nfa1 = stack.pop()
#             new_start = State(f"q{state_count + 1}")
#             new_accept = State(f"q{state_count + 2}", is_accept=True)
#             # the new start state has epsilon transitions to the start states of the two NFAs
#             new_start.add_transition('eps', nfa1.start)
#             new_start.add_transition('eps', nfa2.start)
#             # the two accept states have epsilon transitions to the new accept state
#             nfa1.accept.add_transition('eps', new_accept)
#             nfa2.accept.add_transition('eps', new_accept)
#             state_count += 2
#             start = new_start
#             accept = new_accept
#             stack.append(NFA(start=new_start, accept=new_accept))
#         elif char == '.':
#             # pop the last two NFA objects from the stack
#             nfa1 = stack.pop()
#             nfa2 = stack.pop()
#             # the first NFA's accept state has an epsilon transition to the second NFA's start state
#             nfa1.accept.add_transition('eps', nfa2.start, is_accept=True)
#             nfa1.accept.is_accept = False
#             state_count += 1
#             start = nfa1.start
#             stack.append(NFA(start=nfa1.start, accept=nfa2.accept))

#     # return stack.pop()
#     return NFA(start=start, accept=accept)

def main():
    # prompt user to enter a regular expression
    # regex = input("Enter a regular expression: ")
    regex = "mostafa|mostafa*"

    # validate the regular expression
    try:
        re.compile(regex)
    except re.error:
        print("Invalid regular expression")
        return

    # compile the regular expression into an NFA
    nfa = compile(regex)

    # convert the NFA to a JSON representation
    json_data = nfa_to_json(nfa)

    # print the JSON representation
    print(json_data)

if __name__ == "__main__":
    main()
