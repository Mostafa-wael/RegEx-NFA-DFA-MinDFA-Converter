from regex2nfa import NFA, validate_regex, shunt_yard, postfix_to_nfa
from nfa2dfa import DFA
from dfa2min import MIN_DFA
def main():
    # regex = "([A-Ea-c]+.1)|(2.[0-9]*.K?.[ABC].A.B.C)"
    regex = "([A-Ea-c]+1)|(2[0-9]*K?[ABC]ABC)"
    # regex = "ab(b|c)*d+"
    regex = "ab(b|c)*d+"
    # regex = input("Enter regular expression: ")
    if not validate_regex(regex):
        return
    print("regex:", regex)
    postfix = shunt_yard(regex)
    print("postfix:", postfix)
    # print("expected:", "A|B|C|D|E|a|b|c1+20|1|2|3|4|5|6|7|8|9K*A|B|CABC?|")

    print("----------------------------------------------------------------")
    nfa = postfix_to_nfa(postfix)
    print("NFA: ", nfa.to_dict())
    nfa.visualize(name='output/nfa.gv', view=False)
    print("----------------------------------------------------------------")
    dfa = DFA(nfa)
    print("DFA: ", dfa.to_dict())
    dfa.visualize(name='output/dfa.gv', view=False)
    print("----------------------------------------------------------------")
    min_dfa = MIN_DFA(dfa)
    print("Minimized DFA: ", min_dfa.to_dict())
    min_dfa.visualize(name='output/min_dfa.gv', view=False)


    


if __name__ == '__main__':
    main()