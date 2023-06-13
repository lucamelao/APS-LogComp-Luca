import sys

reserved_words = ["imprime", "se", "senao", "enquanto", "retorna", "funcao", "e", "ou", "entrada"]

class Token:
    def __init__(self, type : str , value : int):
        self.type = type
        self.value = value

class Tokenizer:
    '''
    Análise Léxica
    Separação da string em tokens
    Cada token é um número ou um sinal, objeto da classe Token
    '''
    def __init__(self, source : str, position : int, next : Token):
        ''''
        Inicializa o Tokenizer
        Atributo 1: .source - string a ser tokenizada
        Atributo 2: .position - posição atual na string sendo separada pelo tokenizador
        Atributo 3: .next - último token separado
        Método: selectNext() - lê o próximo token e atualiza next
        '''
        self.source = source
        self.position = 0 
        self.next = None 
        
    def selectNext(self):
        '''
        Lê o próximo token da string e o armazena em self.next
        '''

        # Ignora espaços em branco
        while self.position < len(self.source) and self.source[self.position] == " ":
            self.position += 1
            
        # Verifica se chegou ao fim do arquivo
        if self.position >= len(self.source):
            self.next = Token("EOF", None)
            return

        # Verifica se o próximo token é um número
        elif self.source[self.position].isdigit():
            token = self.source[self.position]
            i = 1
            while token.isdigit():
                i += 1
                if self.position + i > len(self.source):
                    break
                token = self.source[self.position : self.position + i]

            self.next = Token("INT", int(self.source[self.position : self.position + i - 1]))
            self.position += i - 1
        
        # Verifica se o próximo token é um sinal de operação +
        elif self.source[self.position] == "+":
            self.next = Token("MAIS", "+")
            self.position += 1
        
        # Verifica se o próximo token é um sinal de operação -
        elif self.source[self.position] == "-":
            self.next = Token("MENOS", "-")
            self.position += 1

        # Verifica se o próximo token é um sinal de operação /
        elif self.source[self.position] == "/":
            self.next = Token("DIVIDIDO", "/")
            self.position += 1
        
        # Verifica se o próximo token é um sinal de operação *
        elif self.source[self.position] == "*":
            self.next = Token("VEZES", "*")
            self.position += 1

        # Verifica se o próximo token é um sinal de operação (
        elif self.source[self.position] == "(":
            self.next = Token("ABRE_PARENTESES", "(")
            self.position += 1

        # Verifica se o próximo token é um sinal de operação )
        elif self.source[self.position] == ")":
            self.next = Token("FECHA_PARENTESES", ")")
            self.position += 1

        # Verifica se o próximo token é um sinal de operação {
        elif self.source[self.position] == "{":
            self.next = Token("ABRE_CHAVES", "{")
            self.position += 1
        
        # Verifica se o próximo token é um sinal de operação }
        elif self.source[self.position] == "}":
            self.next = Token("FECHA_CHAVES", "}")
            self.position += 1

        # Verifica se o próximo token é um sinal de operação ;
        elif self.source[self.position] == ";":
            self.next = Token("SEMICOLON", ";")
            self.position += 1

        # Verifica se o próximo token é um sinal de operação =
        elif self.source[self.position] == "=":

            # Verifica se o próximo token é um sinal de operação ==
            if self.source[self.position + 1] == "=":
                self.next = Token("IGUAL", "==")
                self.position += 2
            else:
                self.next = Token("ASSIGNMENT", "=")
                self.position += 1
        
        # Verifica se o próximo token é um sinal de fim de linha \n
        elif self.source[self.position] == "\n":
            self.next = Token("FIM", "\n")
            self.position += 1

        # Verifica se o próximo token é um sinal de operação >
        elif self.source[self.position] == ">":
            self.next = Token("MAIOR", ">") 
            self.position += 1
        
        # Verifica se o próximo token é um sinal de operação <
        elif self.source[self.position] == "<":
            self.next = Token("MENOR", "<")
            self.position += 1

        # Verifica se o próximo token é um sinal de operação !
        elif self.source[self.position] == "!":
            self.next = Token("NOT", "!")
            self.position += 1

        # Verifica se o próximo token é um sinal de separador de parâmetros
        elif self.source[self.position] == ",":
            self.next = Token("COMMA", ",")
            self.position += 1

        # Verifica se o próximo token é um sinal de string
        elif self.source[self.position] == "\"":
            token = self.source[self.position]
            i = 1
            while self.position + i < len(self.source) and self.source[self.position + i] != "\"":
                i += 1
                token = self.source[self.position : self.position + i]

            # Verifica se a string foi finalizada corretamente
            if self.position + i >= len(self.source):
                sys.stderr.write('[ERRO] Erro léxico: string não fechada\n')
                sys.exit()

            self.next = Token("STRING", self.source[self.position + 1 : self.position + i])
            self.position += i + 1

        # Verifica se o próximo token é uma palavra/variável declarada
        elif self.source[self.position].isalnum() or self.source[self.position] == "_":

            token = self.source[self.position]
            i = 1
            while self.position + i < len(self.source) and (self.source[self.position + i].isalnum() or self.source[self.position + i] == "_"):
                i += 1
                token = self.source[self.position : self.position + i]

            self.next = Token("IDENTIFIER", token)
            self.position += i

            if self.next.value in reserved_words:
                if self.next.value == "imprime":
                    self.next = Token("PRINTLN", self.next.value)
        
                elif self.next.value == "se":
                    self.next = Token("IF", self.next.value)
                
                elif self.next.value == "senao":
                    self.next = Token("ELSE", self.next.value)
                
                elif self.next.value == "enquanto":
                    self.next = Token("WHILE", self.next.value)
                
                elif self.next.value == "funcao":
                    self.next = Token("FUNCTION", self.next.value)

                elif self.next.value == "retorna":
                    self.next = Token("RETURN", self.next.value)

                elif self.next.value == "e":
                    self.next = Token("AND", self.next.value)
                
                elif self.next.value == "ou":
                    self.next = Token("OR", self.next.value)
                
                elif self.next.value == "entrada":
                    self.next = Token("INPUT", self.next.value)

        else:
            sys.stderr.write('[ERRO] Token desconhecido pelo compilador.\n')
            sys.exit()