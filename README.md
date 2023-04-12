# RegEx -> NFA -> DFA -> Min DFA Converter
A simple python utility to convert regular expressions into NFA, DFA, and MinDFA expressions.

## To convert -infix-regular expressions into  postfix-expressions
```python
postfix = POSTFIX(regex)
```
## To convert postfix-expressions into NFA
```python
nfa = NFA(postfix=postfix.get_postfix())
print("NFA: ", nfa.toDict())
nfa.visualize(name='output/nfa.gv', view=False)
```
## To convert NFA into DFA
```python
dfa = DFA(nfa)
print("DFA: ", dfa.toDict())
dfa.visualize(name='output/dfa.gv', view=False)
```
## To convert DFA into MinDFA
```python
minDfa = MIN_DFA(dfa)
print("Minimized DFA: ", minDfa.toDict())
minDfa.visualize(name='output/min_dfa.gv', view=False)
```