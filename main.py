from regex2nfa import NFA, validate_regex, shunt_yard, postfix_to_nfa
from nfa2dfa import DFA
from dfa2min import dfa2min
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
    nfa.visualize(name='output/nfa.gv', view=False)
    print("----------------------------------------------------------------")
    dfa = DFA(nfa)
    print("DFA: ", dfa.to_dict())
    dfa.visualize(name='output/dfa.gv', view=False)
    print("----------------------------------------------------------------")
    min_dfa = dfa2min(dfa)

    


if __name__ == '__main__':
    main()