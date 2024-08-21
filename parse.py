from lark import Lark, Transformer, v_args, Tree, Token
import random
from pretty_printer import SimplePrettyPrinter  # Import the PrettyPrinter class

# Define a simple language grammar
simple_grammar = r"""
start: (function)+

function: "func" NAME "(" args ")" "{" body "}"

args: (NAME ("," NAME)*)?

body: (statement)*

statement: var_declaration | return_statement

var_declaration: "var" NAME "=" expr ";"
return_statement: "return" expr ";"

expr: NAME | NUMBER | expr "*" expr

NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
NUMBER: /\d+/

%ignore /\s+/   
%ignore /\/\/[^\n]*/   
"""
parser = Lark(simple_grammar, start='start', parser='lalr')

# Transformer to scramble the names
@v_args(inline=True)
class SimpleTransformer(Transformer):
    def __init__(self):
        self.name_mapping = {}
    
    def generate_random_name(self, length=2):
        return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=length))
    
    def NAME(self, name):
        scrambled_name = Token('NAME', self.name_mapping.get(name, self.generate_random_name()))
        self.name_mapping[name] = scrambled_name
        return scrambled_name
    
    def function(self, name, args, body):
        return Tree('function', [name, args, body])

    def var_declaration(self, name, expr):
        return Tree('var_declaration', [name, expr])

    def return_statement(self, expr):
        return Tree('return_statement', [expr])

    def expr(self, *args):
        return Tree('expr', list(args))

    def NUMBER(self, n):
        return Token('NUMBER', n)

# Example code in the simple language
simple_code = """
func add(a, b, c) {
    var result = a * b * c;
    return result;
}

func multiply(x, y) {
    var product = x * y;
    return product;
}
"""

# Parse and transform the code
parsed_tree = parser.parse(simple_code)
transformer = SimpleTransformer()
transformed_tree = transformer.transform(parsed_tree)

# Print the transformed tree structure for inspection
# print(transformed_tree.pretty())


pretty_printer = SimplePrettyPrinter()
print(pretty_printer.print_tree(transformed_tree))
