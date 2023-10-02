from enum import Enum
from gettext import translation

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

def main():
    myToken = Token(TokenType.IDENTIFIER, "myVar")
    alphabet = ["0", "1"]
    states = ["q0", "q1"]
    starting_state = "q0"
    finishing_states = ["q1"]
    transition_table = { 
        "q0": {"0": "q0", "1": "q1"},
        "q1": {"0": "q0", "1": "q1"} 
    }

    ends_with_one = DFA(alphabet, states, starting_state, finishing_states, transition_table)
    print(ends_with_one.evaluate("0101010101"))

if __name__ == "__main__":
    main()