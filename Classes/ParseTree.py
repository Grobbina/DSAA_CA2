import regex as re

class ParseTree():
    def __init__(self, expression):
        self.expression = expression
        self.tokens = re.findall(r'\d+|\+|\-|\*|\/|\*\*|\(|\)', expression)
        self.current_index = 0

    def BuildTree(self):
        return self.Expression()
