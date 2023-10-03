from enum import Enum
from gettext import translation
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

    def evaluate(self, input_string):
        input_symbols = list(input_string)
        current_state = None
        for symbol in input_symbols:
            if current_state is None:
                current_state = self.starting_state
            next_state = self.transition_table[current_state][symbol]
        return next_state in self.finishing_states

class Identifier_DFA(DFA):
    alphabet = [x for x in string.ascii_letters] + [str(x) for x in range(1, 10)]
    states = ["q0", "q1"]
    starting_state = "q0"
    finishing_states = ["q1"]
    transition_table = {
        "q0": { },
        "q1": { }
    }
    for char in alphabet:
        if char.isnumeric():
            transition_table["q0"][char] = "q0"
            transition_table["q1"][char] = "q0"
        else: 
            transition_table["q0"][char] = "q1"
            transition_table["q1"][char] = "q1"
    def prt(self):
        print(self.transition_table)
    
    def __init__(self):
        super().__init__(self.alphabet, self.states, self.starting_state, self.finishing_states, self.transition_table)

class Real_DFA(DFA):
    alphabet = [str(x) for x in range(1, 10)]
    states = ["q0"]
    starting_state = "q0"
    finishing_states = ["q0"]
    transition_table = {
        "q0": { }
    }
    for char in alphabet:
        transition_table["q0"][char] = "q0"
    
    def prt(self):
        print(self.transition_table)

    def __init__(self):
        super().__init__(self.alphabet, self.states, self.starting_state, self.finishing_states, self.transition_table)

    
class FileReader():
    def __init__(self, path):
        self.path = path

class Lexer():
    # "while (t < upper) s = 22.00;" 
    keywords = ["while", "if"]
    separators = ["(", ")", ";"]
    identifiers = []
    operators = ["<", ">", "="]
    curr_index = 0
    def __init__(self, source_string):
        self.source_string = source_string

    
    def is_keyword(self, stream):
        return self.get_keyword(stream)

    def get_keyword(self, stream):
        for index, keyword in enumerate(self.keywords):
            # Make the if also capable of checking for separators in addition to spaces
            if stream.startswith(keyword) and stream[len(keyword):][0] == " ":
               return (len(keyword), keyword)
            else:
                return None 


    # Return token
    def lexer(self):
        stream = self.source_string[self.curr_index:]
        id_DFA = Identifier_DFA()
        real_DFA = Real_DFA()
        # for char in stream:
        # while self.curr_index < len(stream):
        #     print(stream)
        #     if stream[index].isspace():
        #         index += 1
        #         stream = stream[index:]
        #         continue
        #     elif stream[index] in self.operators: # Fix == operator 
        #         self.curr_index += index + 1
        #         return Token(TokenType.OPERATOR, stream[index])
        #     elif stream[index] in self.separators:
        #         self.curr_index += index + 1
        #         return Token(TokenType.SEPARATOR, stream[index])
        #     elif self.is_keyword(stream) is not None:
        #         (keyword_length, keyword) = self.get_keyword(stream)
        #         self.curr_index += keyword_length
        #         return Token(TokenType.KEYWORD, keyword)
        #     elif stream[index] in real_DFA.alphabet:
        #         if stream[index + 1] in real_DFA.alphabet:
        #             index += 1
        #             continue 
        #         else:
        #             if real_DFA.evaluate(stream[:index + 1]):
        #                 self.curr_index += index + 1
        #                 return Token(TokenType.REAL, stream[:index + 1])
        #     index += 1

            # if stream[index].isspace():
            #     stream = stream[index:]
            #     index += 1
            #     continue
        index = self.curr_index
        if stream[index] in self.operators:
            self.curr_index += 1
            return Token(TokenType.OPERATOR, stream[index])
        elif stream[index] in self.separators:
            self.curr_index += index + 1
            return Token(TokenType.SEPARATOR, stream[index])
        elif self.is_keyword(stream) is not None:
                (keyword_length, keyword) = self.get_keyword(stream)
                self.curr_index += keyword_length 
                return Token(TokenType.KEYWORD, keyword)


def main():
    # myToken = Token(TokenType.IDENTIFIER, "myVar")
    alphabet = ["0", "1"]
    states = ["q0", "q1"]
    starting_state = "q0"
    finishing_states = ["q1"]
    transition_table = { 
        "q0": {"0": "q0", "1": "q1"},
        "q1": {"0": "q0", "1": "q1"} 
    }

    ends_with_one = DFA(alphabet, states, starting_state, finishing_states, transition_table)
    input = "0101010101"
    val = ends_with_one.evaluate(input)
    print(f"Ends with 1: {input} = {val}")
    print(ends_with_one.evaluate("0101010101"))

    lexer = Lexer("while (x == 55) y = 2;")
    print(lexer.lexer())
    print(lexer.lexer())
    print(lexer.lexer())
    print(lexer.lexer())
    print(lexer.lexer())
    print(lexer.lexer())
    print(lexer.lexer())

if __name__ == "__main__":
    main()