import re
def validateRegex(regex):
    try:
        re.compile(regex)
    except re.error:
        print(f"Invalid regular expression: {regex}")
        return False
    return True
class POSTFIX:
    def __init__(self, regex):
        self.regex = regex
        self.postfix = self.shunt_yard(regex)
    def get_postfix(self):
        return self.postfix
    def shunt_yard(self, regex):
        # Map each operator to its precedence level.
        # The operators supported by this code are * (kleene star), + (one or more), ? (zero or one), . (concatenation), and | (alternation).
        operators = {'*': 5, '+': 4, '?': 3, '.': 2, '|': 1}
        # postfix will eventually store the postfix notation of the input regular expression,.
        # stack is used as an intermediate stack in the Shunting Yard algorithm.
        postfix, stack = "", ""
        # Check if the regular expression contains any character classes (denoted by square brackets).
        # If a character class is found, the function converts it to an alternation between the characters inside the class.
        # For example, the character class [abc] would be converted to the regular expression (a|b|c).
        # This is done using a while loop that iterates over the characters of the regular expression, finds the opening and closing brackets of the character class, and replaces the contents of the class with an alternation.
        for i in range(len(regex)):
            c = regex[i]
            if c == '[':
                j = i + 1
                while regex[j] != ']':
                    if regex[j].isalnum() and regex[j + 1].isalnum():
                        regex = regex[:j + 1] + '|' + regex[j + 1:]
                    j += 1

        # Replace all remaining square brackets with parentheses.
        # This is done because parentheses are used to group sub-expressions in regular expressions
        regex = regex.replace('[', '(')
        regex = regex.replace(']', ')')

        print("postfix1: ", regex)

        # Replace any hyphen character (-) in the regular expression with an alternation between the characters on either side of the hyphen.
        # For example, the expression a-z would be converted to (a|b|c|...|y|z).
        # This is done using another for loop that iterates over the characters of the regular expression, finds the hyphen character, and replaces it with an alternation.
        hyphen_count = regex.count('-')
        for i in range(hyphen_count):
            for j in range(len(regex)):
                c = regex[j]
                if c == '-':
                    final = regex[j + 1]
                    first = regex[j - 1]
                    temp_list = ''
                    for k in range(int(ord(final) - ord(first))):
                        temp_list = temp_list + '|'
                        char = chr(ord(first) + k + 1)
                        temp_list = temp_list + char
                    regex = regex[0: j] + temp_list + regex[j + 2:]
                    break
        print("postfix2: ", regex)
        # Insert a concatenation operator (.) between any two adjacent characters(characters that are not operators), unless the characters are already separated by an operator, or the second character is an opening parenthesis.
        dotIndices = []
        for i in range(len(regex) - 1):
            startOps = [')', "*","+", "*"]
            endOps = ["*", "+", ".", "|", ")"]
            if regex[i] in startOps and regex[i+1] not in endOps:
                dotIndices.append(i)
            elif regex[i].isalnum() and (regex[i+1].isalnum() or regex[i+1] == '('):
                dotIndices.append(i)
        
        for i in range(len(dotIndices)):
            regex = regex[:dotIndices[i] + 1 + i] + '.' + regex[dotIndices[i] + 1 + i:]
        print("postfix3: ", regex)
        # Iterate over each character of the regular expression and performs the Shunting Yard algorithm.
        for i in range(len(regex)):
            c = regex[i]
            # If the character is an opening parenthesis, push it onto the stack.
            if c == '(':
                stack = stack + c
            # If the character is a closing parenthesis, pop operators off the stack and append them to the postfix string until an opening parenthesis is found. Then pop the opening parenthesis from the stack.
            elif c == ')':
                while stack[-1] != '(':
                    # places the character at the end of the stack in the postfix expression
                    postfix = postfix + stack[-1]
                    # [:-1] denotes up to or including the last character
                    stack = stack[:-1]
                stack = stack[:-1]  # removes the open bracket in the stack

            # If the character is an operator, pop operators off the stack and append them to the postfix string as long as they have higher or equal precedence to the current operator. Then push the current operator onto the stack.
            elif c in operators:
                while stack and operators.get(c, 0) <= operators.get(stack[-1], 0):
                    postfix, stack = postfix + stack[-1], stack[:-1]
                stack = stack + c

            # If the character is a operand (i.e. not an operator or parenthesis), append it to the postfix string.
            else:
                postfix = postfix + c
            print("postfix4: ", regex)
        # After iterating over all characters of the regular expression, the function pops any remaining operators off the stack and appends them to the postfix string.
        while stack:
            postfix, stack = postfix + stack[-1], stack[:-1]
        print("postfix5: ", regex)

        # Finally, the function returns the postfix notation of the input regular expression.
        return postfix