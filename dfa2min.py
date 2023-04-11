def dfa2min(dfa):
    states = dfa.to_dict()
    symbols = dfa.getSymbols()
    # remove the final states from dfa
    states.pop('startingState')
    groups = []
    final_states = []
    non_final_states = []
    # iterate over states keys and values
    for key, value in states.items():
        # print(getTransitionsOnSymbol(getTransitions(key, value), 'a'))
        # the value is a dictionary with the transitions and the isTerminatingState flag
        if value["isTerminatingState"] == True:
            final_states.append({key: value})
        else:
            non_final_states.append({key: value})
    groups.append(final_states)
    groups.append(non_final_states)
    for g in groups:
        print(g)
    print('-------------------------')
    #---------------------------------------------------------------------------
    # for each group in groups, check if there is a state that has a transition to a state in another group
    # if there is, split the group into two groups
    #---------------------------------------------------------------------------
    split = True
    while split:
        split = False # [[{key1: {a: x, b: y}}, {key2: {a: w}}] [{key3: {a: x, b: y}}, {}]]
        for i, group in enumerate(groups): # [{key1: {a: x, b: y}}, {key2: {a: w}}] [{key3: {a: x, b: y}}, {}]
            for j, states in enumerate(group): # [{key1: {a: x, b: y}}, {key2: {a: w}}] 
                for symbol in symbols: # each symbol has a target state
                    targetState = ''
                    for key, value in states.items(): # {key1: {a: x, b: y}}
                        transitions = getTransitions(key, value)
                        if targetState == '':
                            targetState = getTransitionsOnSymbol(transitions, symbol)
                        else:
                            if targetState != getTransitionsOnSymbol(transitions, symbol):
                                print('split group', group)
                                split = True
                                groups.insert(1,groups[i][:j])
                                groups.insert(2,groups[i][j:])
                                groups.pop(i)
                                break
                       
    for g in groups:
        print(g)
    print('-------------------------')
    out = concatenate_states(groups)
    print(out)
    return groups

def concatenate_states(states_list):
    # Concatenate states within the same list
    new_states = {}
    for states_dict in states_list:
        for states, actions in states_dict.items():
            new_state = ''.join(sorted(states.split()))
            new_states[new_state] = actions
    
    # Update references to new states
    for states_dict in states_list:
        for states, actions in states_dict.items():
            new_state = ''.join(sorted(states.split()))
            for symbol, next_states in actions.items():
                next_states = ''.join(sorted(next_states.split()))
                actions[symbol] = new_states[next_states]
    
    # Merge all states into a single dictionary
    merged_states = {}
    for states_dict in states_list:
        merged_states.update(states_dict)
    
    # Replace state names with the concatenated ones
    for old_state, actions in merged_states.items():
        new_state = ''.join(sorted(old_state.split()))
        if new_state != old_state:
            merged_states[new_state] = actions
            del merged_states[old_state]
    
    return merged_states

def getTransitions(key, value):
    transitions = {}
    for symbol, state in value.items():
        if symbol != "isTerminatingState":
            transitions[symbol]= state  
    return transitions

def getTransitionsOnSymbol(dic, symbol):
    if symbol in dic:
        return dic[symbol]
    else:
        return ''

    