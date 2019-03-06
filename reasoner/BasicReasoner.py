from reasoner.patterns import recognize_pattern, TokenType

class BasicReasoner():
    def __init__(self, htmlroot, akomabuilder):
        self.htmlroot = htmlroot
        self.akomabuilder = akomabuilder
        self.current_token = False
        self.generator = None
        self.current_hierarchy = {
            TokenType.GLAVA: 0,
            TokenType.ODELJAK: 0,
            TokenType.PODODELJAK: 0,
            TokenType.CLAN: 0,
            TokenType.STAV: 0,
            TokenType.TACKA: 0,
            TokenType.PODTACKA: 0,
            TokenType.ALINEJA: 0}

    def token_generator(self):
        for child in self.htmlroot:

            self.current_token = recognize_pattern(child)
           # print(self.current_token.type,self.current_token.value)
            yield self.current_token

    def get_next_token(self):
        if self.generator is None:
            self.generator = self.token_generator()
        try:
            return next(self.generator)
        except StopIteration:
            self.current_token = None
            return None

    def start(self):
        body = False
        while self.current_token is not None:
            self.get_next_token()
            if(self.current_token is None):
                break
            if self.current_token.type <= TokenType.CLAN:
                body = True
            if body:
                self.reason()

    def reason(self):
        if self.current_token is None:
            return
        if self.current_token.type == TokenType.GLAVA and self.current_token.value == None:
            self.glava_find_title()
        elif self.current_token.type == TokenType.STAV and self.current_token.value[-1:] != "." and self.current_token.value[-1:] != ":"and self.current_token.value[-1:] != ",":
            self.title_find_clan()
        else:
            self.akomabuilder.add_token(self.current_token, self.get_identification(self.current_token))
            if self.current_token.type == TokenType.STAV and self.current_token.value[-1:] == ":":
                self.expect_tacke()

    def glava_find_title(self):
        glava = self.current_token
        self.get_next_token()
        if (self.current_token.type != TokenType.STAV):
            print("WARNING - GLAVA NEMA NASLOV")
        elif (self.current_token.value[-1:] == "."):
            print("WARNING - NASLOV GLAVE NE SME DA IMA TACKU NA KRAJU")
        glava.text = self.current_token.value
        return glava

    def title_find_clan(self):
        naslov = self.current_token
        self.get_next_token()
        if self.current_token is None:
            return
        if self.current_token.type != TokenType.CLAN:
            print("WARNING - NEMA CLANA ISPOD NASLOVA")
            #self.akomabuilder.add_token(naslov, self.get_identification(self.current_token))
            self.reason() # deal with this unknown element
        else:
            self.current_token.value = naslov.value
            self.akomabuilder.add_token(self.current_token, self.get_identification(self.current_token))

    def expect_tacke(self):
        #print("TACKA?")
        while self.current_token is not None:
            self.get_next_token()
            if(self.current_token is None):
                break
            elif self.current_token.type == TokenType.ODELJAK:
                if (self.current_token.type == TokenType.ODELJAK):
                    self.current_token.type = TokenType.TACKA
                    self.current_token.name = "тачка"
                self.reason()
            elif self.current_token.type <= TokenType.STAV:
                break
            else:
                self.reason()

    def get_identification(self, token):
        if token.number is None:
            self.current_hierarchy[token.type] += 1
        elif token.number2 is not None :
            self.current_hierarchy[token.type] = token.number2
        else:
            self.current_hierarchy[token.type] = token.number

        for i in range(TokenType.ALINEJA, token.type, -1):
            if i == TokenType.CLAN:
                continue
            self.current_hierarchy[i] = 0

        #if token.type+1 != TokenType.CLAN and token.type != TokenType.ALINEJA:
         #   self.current_hierarchy[token.type+1] = 0

        values = ["gla", "od", "podod", "clan", "stav", "tac", "podtac", "ali"]
        retval = ""
        for i in range(TokenType.GLAVA, TokenType.ALINEJA+1):
            if token.type < i:
                break
            if self.current_hierarchy[i] == 0:
                continue

            retval += values[i-1] + str(self.current_hierarchy[i]) + "_"

        return retval[:-1]

