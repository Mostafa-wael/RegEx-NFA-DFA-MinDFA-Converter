# RegEx -> NFA -> DFA -> Min DFA Converter
A simple python utility to convert regular expressions into NFA, DFA, and MinDFA expressions.
```
______           _____           __     _   _ ______ ___        __    ____________ ___        __    ___  ____        ____________ ___   
| ___ \         |  ___|          \ \   | \ | ||  ___/ _ \       \ \   |  _  \  ___/ _ \       \ \   |  \/  (_)       |  _  \  ___/ _ \  
| |_/ /___  __ _| |____  __  _____\ \  |  \| || |_ / /_\ \  _____\ \  | | | | |_ / /_\ \  _____\ \  | .  . |_ _ __   | | | | |_ / /_\ \ 
|    // _ \/ _` |  __\ \/ / |______> > | . ` ||  _||  _  | |______> > | | | |  _||  _  | |______> > | |\/| | | '_ \  | | | |  _||  _  | 
| |\ \  __/ (_| | |___>  <        / /  | |\  || |  | | | |       / /  | |/ /| |  | | | |       / /  | |  | | | | | | | |/ /| |  | | | | 
\_| \_\___|\__, \____/_/\_\      /_/   \_| \_/\_|  \_| |_/      /_/   |___/ \_|  \_| |_/      /_/   \_|  |_/_|_| |_| |___/ \_|  \_| |_/ 
            __/ |                                                                                                                       
           |___/                                                                                                                        
 _____                           _                                                                                                      
/  __ \                         | |                                                                                                     
| /  \/ ___  _ ____   _____ _ __| |_ ___ _ __                                                                                           
| |    / _ \| '_ \ \ / / _ \ '__| __/ _ \ '__|                                                                                          
| \__/\ (_) | | | \ V /  __/ |  | ||  __/ |                                                                                             
 \____/\___/|_| |_|\_/ \___|_|   \__\___|_|    
 ```
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
