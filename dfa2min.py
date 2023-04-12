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
        split = False # [[{key1: {a: key1, b: key2}}, {key2: {a: w}}] [{key3: {a: key1, b: key2}}, {}]]
        for i, group in enumerate(groups): # [{key1: {a: key1, b: key2}}, {key2: {a: key3}}] [{key3: {a: key1, b: key2}}, {}]
            targetGroups = {}
            first_state = next(iter(group)) # {key1: {a: key1, b: key2}}
            for key, value in first_state.items():
                for symbol in symbols:
                    if symbol in value:
                        targetGroups[symbol] = [j for j, group in enumerate(groups) if value[symbol] in getGroupKeys(group)][0] # {key1, key2}
            splitted_states = []
            for k, state in enumerate(group):
                outputGroups = {}
                for key, value in state.items():
                    for symbol in symbols:
                        if symbol in value:
                            List = [j for j, group in enumerate(groups) if value[symbol] in getGroupKeys(group)]
                            outputGroups[symbol] = List[0]
                if outputGroups != targetGroups:
                    split = True
                    splitted_states.append(state)
            if len(splitted_states) > 0:
                groups.insert(i+1, list(splitted_states))
                groups[i] = [state for state in group if state not in splitted_states]        
    newGroups = concat_states(groups)
    return newGroups

def concat_states(groups):
    # result = {'startingState': groups[0][0].keys()}
    # for g, group in enumerate(groups):
    #     # for all the states in the group, rename them to the group number
    #     for state in group:
    #         for key, value in state.items():
    #             result[g] = value
        
    # return result
        
def getGroupKeys(group):
    keys = []
    for state in group:
        for key, value in state.items():
            keys.append(key)
    return keys


