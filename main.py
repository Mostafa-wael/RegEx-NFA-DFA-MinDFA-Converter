from postfix2nfa import NFA
from nfa2dfa import DFA
from dfa2min import MIN_DFA
from regex2postfix import POSTFIX, validateRegex


def main():
    cases = {0: 'ab(b|c)*d+', 1: ' (AB)', 2: '(A|B)', 3: '([A-Z])', 4: '(A)+', 5: '(A)*', 6: '(((AB)((A|B)*))(AB))', 7: '((((AB)|[A-Z])+)([A-Z]*))', 8: '(((((ABE)|C)|((([A-Z])S)*))+)((AB)C))',
             9: '((([a-z_])(([a-z0-9_])*))(([!?])?))', 10: '(A(((B*)|(DA))*))((CG)|(D([DEF])))', 11: '(ab', 12: '(a([b-c))', 13: '((a|b)|)', 14: '(a{3,2})'}
    regex = cases[0]
    # 7

    # regex = input("Enter regular expression: ")
    if not validateRegex(regex):
        return
    try:
        postfix = POSTFIX(regex)
        print("----------------------------------------------------------------")
        print("regex:", regex)
        print("----------------------------------------------------------------")
        print("postfix: ", postfix.get_postfix())
        print("----------------------------------------------------------------")
        nfa = NFA(postfix=postfix.get_postfix())
        print("NFA: ", nfa.toDict())
        nfa.visualize(name='output/nfa.gv', view=False)
        print("----------------------------------------------------------------")
        dfa = DFA(nfa)
        print("DFA: ", dfa.toDict())
        dfa.visualize(name='output/dfa.gv', view=False)
        print("----------------------------------------------------------------")
        minDfa = MIN_DFA(dfa)
        print("Minimized DFA: ", minDfa.toDict())
        minDfa.visualize(name='output/min_dfa.gv', view=False)
    # catch the excpetion anr print it
    except Exception as e:
        print(e)
        print("Your Regex may be invalid")


if __name__ == '__main__':
    main()
