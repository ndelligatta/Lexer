from enum import Enum
import string

class TokenType(Enum):
    KEYWORD = 0
    SEPARATOR = 1
    IDENTIFIER = 2
    OPERATOR = 3
    REAL = 4

    def __str__(self):
        return self.name

class Token():
    def __init__(self, type, lexeme):
        self.type = type
        self.lexeme = lexeme

    def __str__(self):
        return f"{self.type} | {self.lexeme}"

class DFA():
    def __init__(self, alphabet, states, starting_state, finishing_states, transition_table):
        self.alphabet = alphabet
        self.states = states 
        self.starting_state = starting_state
        self.finishing_states = finishing_states
        self.transition_table = transition_table
    
    def in_alphabet(self, char):
        return char in self.alphabet

    def evaluate(self, input_string):
        input_symbols = list(input_string)
        current_state = None
        for symbol in input_symbols:
            if current_state is None:
                current_state = self.starting_state
            else:
                current_state = next_state
            next_state = self.transition_table[current_state][symbol]
            #print(f"{symbol} => {current_state} -> {next_state}")
        return next_state in self.finishing_states

class Identifier_DFA(DFA):
    alphabet = set([x for x in string.ascii_letters] + [str(x) for x in range(1, 10)])
    states = ["q0", "q1", "q2"]
    starting_state = "q0"
    finishing_states = ["q1"]
    transition_table = {
        "q0": { },
        "q1": { },
        "q2": { },
    }
    
    for char in alphabet:
        if char.isnumeric():
            transition_table["q0"][char] = "q2"
            transition_table["q1"][char] = "q1"
            transition_table["q2"][char] = "q2"
        else: 
            transition_table["q0"][char] = "q1"
            transition_table["q1"][char] = "q1"
            transition_table["q2"][char] = "q2"
    
    def __init__(self):
        super().__init__(self.alphabet, self.states, self.starting_state, self.finishing_states, self.transition_table)

class Real_DFA(DFA): 
    alphabet = set([str(x) for x in range(0,10)] + ["."])
    states = ["q0", "q1", "q2", "q3", "q4"]
    starting_state = "q0"
    finishing_states = ["q3"]
    # Refactor for loop to automatically create
    # transition table from the states 
    transition_table = {
        "q0": { },
        "q1": { },
        "q2": { },
        "q3": { },
        "q4": { }
    }
    
    for char in alphabet:
        if char.isnumeric():
            transition_table["q0"][char] = "q1"
            transition_table["q1"][char] = "q1"
            transition_table["q2"][char] = "q3"
            transition_table["q3"][char] = "q3"
            transition_table["q4"][char] = "q4"
        elif char == ".":
            transition_table["q0"][char] = "q4"
            transition_table["q1"][char] = "q2"
            transition_table["q2"][char] = "q4"
            transition_table["q3"][char] = "q4"
            transition_table["q4"][char] = "q4"
    
    def __init__(self):
        super().__init__(self.alphabet, self.states, self.starting_state, self.finishing_states, self.transition_table)

class FileIO():
    def read_file(file_name):
        with open(file_name, 'r') as file:
            data = file.read().replace('\n', '')
        return data
    


class Lexer():
    keywords = {"while", "if"}
    separators = {"(", ")", ";"}
    identifiers = set()
    operators = {"<", ">", "="}
    
    def __init__(self, source_string):
        self.source_string = source_string
        self.stream = self.source_string.split()
        self.curr_index = 0
    
    def lexer(self):
        #print(self.stream)
        if len(self.stream) > 0:
            block = str(self.stream[0])
            token_length, token = self.parse(block)
            if(len(block) > token_length):
                self.stream[0] = self.stream[0][token_length:]
                #print(self.stream)
                return token
            elif(len(block) == token_length):
                del self.stream[0]
                #print(self.stream)
                return token

    def parse(self, block):
        operator = next((operator for operator in self.operators if block.startswith(operator)), None)
        separator = next((separator for separator in self.separators if block.startswith(separator)), None)
        keyword = next((keyword for keyword in self.keywords if block.startswith(keyword)), None)      
        
        results = [(TokenType.OPERATOR, operator), (TokenType.SEPARATOR, separator), (TokenType.KEYWORD, keyword)]
        
        for result in results:
            if result[1] is not None:
                token_length = len(result[1])
                return (token_length, Token(result[0], result[1]))
        
        id_DFA = Identifier_DFA()
        real_DFA = Real_DFA()
        flag = True
        id_flag = True 
        real_flag = True
        alphabet = set()
        
        for i, char in enumerate(block):
            if char not in Identifier_DFA.alphabet:
                id_flag = False
            if char not in Real_DFA.alphabet:
                real_flag = False
            if char in self.operators or char in self.keywords or char in self.separators:
                token_length = i
                flag = False
                break
            else:
                alphabet.add(char)
        
        if flag:
            token_length = len(block)
        current_string = block[:token_length]
        if id_flag:
            # for i, char in enumerate(block):
            if id_DFA.evaluate(block[:token_length]):
                return (token_length, Token(TokenType.IDENTIFIER, current_string))
        else:
            id_flag = True
            for i, char in enumerate(block[:token_length]):
                if char not in Identifier_DFA.alphabet:
                    id_flag = False
            if id_flag:
                if id_DFA.evaluate(block[:token_length]):
                    return (token_length, Token(TokenType.IDENTIFIER, current_string))
        if real_flag:
            if real_DFA.evaluate(block[:token_length]):
                return (token_length, Token(TokenType.REAL, current_string))
        else:
            real_flag = True
            for i, char in enumerate(block[:token_length]):
                if char not in Real_DFA.alphabet:
                    real_flag = False
            if real_flag:
                if real_DFA.evaluate(block[:token_length]):
                    return (token_length, Token(TokenType.REAL, current_string))
        return (0, Token(None, current_string))


def main():
    source = FileIO.read_file("input_scode.txt")
    lexer = Lexer(source)

    tokens = []
    for i in range(1, 11):
        tokens.append(lexer.lexer())
    x = 0
    while x < len(tokens):
        print(tokens[x])
        x += 1

if __name__ == "__main__":
    main()