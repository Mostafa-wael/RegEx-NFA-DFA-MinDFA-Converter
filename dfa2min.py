import graphviz


class MIN_DFA:
    def __init__(self, dfa):
        self.dfa = dfa
        self.states = self.dfa2min(dfa)
    # Utility functions
    def getGroupKeys(self, group):
        keys = []
        for state in group:
            for key, value in state.items():
                keys.append(key)
        return keys
    # COnversion from DFA to Minimized DFA
    def dfa2min(self, dfa):
        states = dfa.toDict()
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
                            targetGroups[symbol] = [j for j, group in enumerate(groups) if value[symbol] in self.getGroupKeys(group)][0] # {key1, key2}
                splitted_states = []
                for k, state in enumerate(group):
                    outputGroups = {}
                    for key, value in state.items():
                        for symbol in symbols:
                            if symbol in value:
                                List = [j for j, group in enumerate(groups) if value[symbol] in self.getGroupKeys(group)]
                                outputGroups[symbol] = List[0]
                    if outputGroups != targetGroups:
                        split = True
                        splitted_states.append(state)
                if len(splitted_states) > 0:
                    groups.insert(i+1, list(splitted_states))
                    groups[i] = [state for state in group if state not in splitted_states]        
        newGroups = self.concatStates(groups)
        return newGroups
    def concatStates(self, groups):
        # create a hashtable for the states with the group number as the key
        hashTable = {}
        for g, group in enumerate(groups):
            # for all the states in the group, rename them to the group number
            for state in group:
                for key, value in state.items():
                    hashTable[key] = str(g)
        # Create a new dictionary for the new groups
        newGroups = {'startingState':0}
        groupCopy = groups.copy()
        # iterate over the groups
        for g, group in enumerate(groupCopy):
            # iterate over the states in the group
            for state in group:
                # iterate over the states in the group
                for key, value in state.items():
                    # iterate over the transitions in the state
                    for symbol, next_state in value.items():
                        # if the next state is in another group, replace it with the group number
                        if next_state in hashTable:
                            value[symbol] = str(hashTable[next_state])
                            newGroups[str(g)] = value
        return newGroups
    # For exporting the minimized DFA
    def toDict(self):
        return self.states
    def visualize(self, name='output/min.gv', view=False):
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
        graph.render("output/min", view=False)

            


