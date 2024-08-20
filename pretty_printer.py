# pretty_printer.py

from lark import Tree, Token

class SimplePrettyPrinter:
    def __init__(self):
        self.output = ""

    def print_tree(self, tree):
        self.output = self.visit(tree)
        return self.output

    def visit(self, node):
        # print("type of node:", type(node))
        # print("node:", node)
        result = ""
        if isinstance(node, Tree):
            if node.data == "start":
                result += self.visit_start(node)
            if node.data == "function":
                result += self.visit_function(node)
            if (node.data == "args"):
                result += self.visit_args(node)
            elif node.data == "var_declaration":
                result += self.visit_var_declaration(node)
            elif node.data == "return_statement":
                result += self.visit_return_statement(node)
            elif node.data == "body":
                result += self.visit_body(node)
            elif node.data == "statement":
                result += self.visit(node.children[0])  # Visit the actual statement
            elif node.data == "expr":
                result += self.visit_expr(node)
        elif isinstance(node, Token):
            result += str(node)
        return result

    
    def visit_start(self, node):
        return "\n\n".join(self.visit(child) for child in node.children)

    def visit_function(self, node):
        name = self.visit(node.children[0])
        args = self.visit(node.children[1])
        body = self.visit(node.children[2])
        return f"func {name}({args}) {{\n{body}}}\n\n"

    def visit_args(self, node):
        return ", ".join(self.visit(child) for child in node.children)

    def visit_var_declaration(self, node):
        name = self.visit(node.children[0])
        expr = self.visit(node.children[1])
        return f"    var {name} = {expr};\n"

    def visit_return_statement(self, node):
        expr = self.visit(node.children[0])
        return f"    return {expr};\n"


    def visit_body(self, node):
        return "".join(self.visit(child) for child in node.children)
            
    def visit_expr(self, node):
        if len(node.children) == 1:
            return self.visit(node.children[0])
        else:
            left = self.visit(node.children[0])
            right = self.visit(node.children[1])
            return f"{left} {right}"
