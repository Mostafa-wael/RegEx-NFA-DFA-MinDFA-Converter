from postfix2nfa import NFA
from nfa2dfa import DFA
from dfa2min import MIN_DFA
from regex2postfix import POSTFIX, validate_regex
def main():
    cases = ["([A-Ea-c]+.1)|(2.[0-9]*.K?.[ABC].A.B.C)", "([A-Ea-c]+1)|(2[0-9]*K?[ABC]ABC)", "ab(b|c)*d+"]
    regex = cases[2]
    # regex = input("Enter regular expression: ")
    if not validate_regex(regex):
        return
    print("regex:", regex)
    postfix = POSTFIX(regex)
    print("postfix: ", postfix.get_postfix())
    print("----------------------------------------------------------------")
    nfa  = NFA(postfix=postfix.get_postfix())
    print("NFA: ", nfa.toDict())
    nfa.visualize(name='output/nfa.gv', view=False)
    print("----------------------------------------------------------------")
    dfa = DFA(nfa)
    print("DFA: ", dfa.toDict())
    dfa.visualize(name='output/dfa.gv', view=False)
    print("----------------------------------------------------------------")
    min_dfa = MIN_DFA(dfa)
    print("Minimized DFA: ", min_dfa.toDict())
    min_dfa.visualize(name='output/min_dfa.gv', view=False)


    


if __name__ == '__main__':
    main()