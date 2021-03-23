from enum import Enum

"""
Base exception thrown for tokenizer errors
"""
class TokenizerException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
    
    def __str__(self):
        return f"TokenizerExceptionn:  {self.message}"

"""
Exception thrown when an operator is not on available_operations map
"""
class InvaidOperationException(TokenizerException):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
    
    def __str__(self):
        return f"InvaidOperatioException:  {self.message}"

"""
Exception thrown when a token does not fit on Keywords class
"""
class UnkonwnTokenException(TokenizerException):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
    
    def __str__(self):
        return f"UnknownTokenException:  {self.message}"

"""
Every type of token the program is able to accept
"""
class Keywords(Enum):
    EOF = "<EOF>"
    INT = "INT"
    PLUS = "PLUS"
    MINUS = "MINUS"
    DIVIDE = "DIVIDE"
    MULTIPLY = "MULTIPLY"
    MODULUS = "MODULUS"
    SPACE = "SPACE"

"""
Rules to filter wich type of token a certain character is
"""
class TokenCategories():
    is_int = staticmethod(lambda c: c.isdigit())
    is_plus = staticmethod(lambda c: c == "+")
    is_minus = staticmethod(lambda c: c == "-")
    is_divide = staticmethod(lambda c: c == "/")
    is_multiply = staticmethod(lambda c: c == "*")
    is_modulus = staticmethod(lambda c: c == "%")
    is_whitespace = staticmethod(lambda c: c.isspace())
    is_comment_start = staticmethod(lambda c: c == "#")
    is_comment_end = staticmethod(lambda c: c == "\n")


"""
Stores a character in memory as a token
"""
class Token():
    def __init__(self, category, value, position):
        self.category = category
        self.position = position
        self.value = value
    
    def __str__(self):
        return f"Token({self.category}, {self.position}"
    
    def __repr__(self):
        return f"Token({self.category}, {self.position}, {self.value}"

"""
Recieves a single line string containing a command to be executed,
in this case will be an arithmetic operation comprised of two single
digit integers, and any of the four basic operations, plus modulus
"""
class TokenParser():
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.curent_token = None
    
    def step_position(self):
        self.position += 1
    
    """
    Categorizes every character received as a type of token until EOF
    """
    def next_token(self):
        if self.position + 1 >  len(self.code):
            return Token(Keywords.EOF, None, self.position)

        character = self.code[self.position]

        token_indentifier_fns = {
            Keywords.DIVIDE:  TokenCategories.is_divide,
            Keywords.MULTIPLY:  TokenCategories.is_multiply,
            Keywords.PLUS:  TokenCategories.is_plus,
            Keywords.MINUS:  TokenCategories.is_minus,
            Keywords.MODULUS:  TokenCategories.is_modulus,
            Keywords.INT:  TokenCategories.is_int,
            Keywords.SPACE:  TokenCategories.is_whitespace,
        }

        for keyword, function in token_indentifier_fns.items():
            if function(character):
                token = Token(keyword, character, self.position)
                self.step_position()
                return token
                
        raise UnknownTokenException(f"This program does not support the token {character}")


    """
    Applies the corresponding operation to `first` and `last` integers, based on the
    type of token received as `operation`
    """
    def execute_operation(self, operation: Keywords, first: int, last:int):
        available_operations = {
            Keywords.PLUS : (lambda x,y: x + y),
            Keywords.MINUS : (lambda x,y: x - y),
            Keywords.MULTIPLY : (lambda x,y: x * y),
            Keywords.DIVIDE : (lambda x,y: x / y),
            Keywords.MODULUS : (lambda x,y: x % y)
        }

        operation_function = available_operations.get(operation)
        if operation_function:
            return operation_function(first, last)
        
        raise InvaidOperation(f"Unexpected operator {operation}")
    
    """
    Verifies if the token is the same category as expected before asking for the next token
    """
    def store_or_fail(self, category):
        if self.current_token.category == category:
            self.current_token = self.next_token()
        else:
            raise InvalidTokenSequenceException(f"Token of {category} expected at position \
             {self.position}, instead found {self.current_token}")
    
    """
    Uses arithmetic operations with the input tokens. It might be userful to split every token
    using regex instead of walking into every character, to allow using multiple digit tokens
    """
    def expr(self):
        self.current_token = self.next_token()

        previous = self.current_token
        self.store_or_fail(Keywords.INT)

        op = self.current_token
        self.store_or_fail(op.category)
        
        next = self.current_token
        self.store_or_fail(Keywords.INT)

        return self.execute_operation(op.category, int(previous.value), int(next.value))
        
        
import sys

"""
Interactive terminal to calculate numbers
"""
arguments = sys.argv[1:]

if arguments == []:
    while True:
        try:
            code = input('>>> ')
        except EOFError:
            break
        if not code:
            continue
        parser = TokenParser(code)
        result = parser.expr()
        print(result)

else:
    for filename in arguments.split(" "):
        with open(filename, "r") as code_file:
            parser = TokenParser("".join(code_file.readlines()))
            result = parser.expr()
            print(result)
