from reasoner.patterns import TokenType

class AkomaBuilder():
    def __init__(self, akomaroot):
        self.akomaroot = akomaroot


    def add_token(self, token, identification):
        print(token.name, identification, token.value)
