from Compiler.tokenizer import Tokenizer
from Compiler.AST import BinOp, UnOp, IntVal, Identifier, Block, Assignment, Print, NoOp, While, If, VarDecl, StringVal, SymbolTable, FuncDec, FuncCall, Return, Read
import sys

class Parser:

    def __init__(self, tokenizer : Tokenizer = None):
        self.tokenizer = tokenizer

    def run(self, code : str):
        ''''
        Recebe o código fonte como argumento, inicializa um objeto Tokenizador, 
        posiciona no primeiro token e retorna o resultado do parseExpression().
        Será chamado pelo main(). Ao final, verifica se token = EOF.
        '''
        self.tokenizer = Tokenizer(code, 0, None)
        self.tokenizer.selectNext()
        resultado = self.parseBlock()

        if self.tokenizer.next.type != "EOF":
            sys.stderr.write('[ERRO] Não chegou ao final da String.\n')
            sys.exit()

        ST = SymbolTable()

        return resultado.Evaluate(ST)
    
    def parseExpression(self):
        ''''
        Consome os tokens do Tokenizer e analisa se a sintaxe e
        está aderente à gramática proposta. Retorna o resultado 
        da expressão analisada.
        '''
        resultado = self.parseTerm()
        while self.tokenizer.next.type == "MAIS" or self.tokenizer.next.type == "MENOS" or self.tokenizer.next.type == "OR":
            
            if self.tokenizer.next.type == "MAIS":
                self.tokenizer.selectNext()
                resultado = BinOp('+', [resultado, self.parseTerm()])

            elif self.tokenizer.next.type == "MENOS":
                self.tokenizer.selectNext()
                resultado = BinOp('-', [resultado, self.parseTerm()])
            
            elif self.tokenizer.next.type == "OR":
                self.tokenizer.selectNext()
                resultado = BinOp('ou', [resultado, self.parseTerm()])

        return resultado 

    def parseTerm(self):
        resultado = self.parseFactor()

        while self.tokenizer.next.type == "VEZES" or self.tokenizer.next.type == "DIVIDIDO" or self.tokenizer.next.type == "AND":

            if self.tokenizer.next.type == "VEZES":
                self.tokenizer.selectNext()
                resultado = BinOp('*', [resultado, self.parseFactor()])

            elif self.tokenizer.next.type == "DIVIDIDO":
                self.tokenizer.selectNext()
                resultado = BinOp('/', [resultado, self.parseFactor()])

            elif self.tokenizer.next.type == "AND":
                self.tokenizer.selectNext()
                resultado = BinOp('e', [resultado, self.parseFactor()])
            
            else:
                sys.stderr.write('[ERRO no ParseTerm] Nenhum dos termos "*" ou "/" ou "e" foram detectados.\n')
                sys.exit()
            
        return resultado

    def parseFactor(self):

        if self.tokenizer.next.type == "INT":
            resultado = self.tokenizer.next.value
            resultado = IntVal(resultado, [])
            self.tokenizer.selectNext()
            return resultado
        
        elif self.tokenizer.next.type == "INPUT":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "ABRE_PARENTESES":
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "FECHA_PARENTESES":
                    self.tokenizer.selectNext()
                    return Read()
                else:
                    sys.stderr.write('[ERRO] Parênteses do entrada() não foi fechado.\n')
                    sys.exit()

        
        elif self.tokenizer.next.type == "IDENTIFIER":
            func_name = self.tokenizer.next.value
            resultado = Identifier(func_name, [])
            self.tokenizer.selectNext()

            if self.tokenizer.next.type == "ABRE_PARENTESES":
                args_list = []
                self.tokenizer.selectNext()

                if self.tokenizer.next.type != "FECHA_PARENTESES":
                    args_list.append(self.RelExpr())
                    while self.tokenizer.next.type == "COMMA":
                        self.tokenizer.selectNext()
                        args_list.append(self.RelExpr())
                    
                if self.tokenizer.next.type == "FECHA_PARENTESES":
                    self.tokenizer.selectNext()
                    resultado = FuncCall(func_name, args_list)

                else:
                    sys.stderr.write('[ERRO] Parênteses não foi fechado na chamada de função.\n')
                    sys.exit()

                resultado = FuncCall(func_name, args_list)

            return resultado
        
        elif self.tokenizer.next.type == "STRING":
            resultado = self.tokenizer.next.value
            resultado = StringVal(resultado, [])
            self.tokenizer.selectNext()
            return resultado
        
        elif self.tokenizer.next.type == "MAIS" or self.tokenizer.next.type == "MENOS" or self.tokenizer.next.type == "NOT":

            if self.tokenizer.next.type == "MAIS":
                self.tokenizer.selectNext()
                resultado = self.parseFactor()
                resultado = UnOp('+', [resultado])
                return resultado
            
            elif self.tokenizer.next.type == "MENOS":
                self.tokenizer.selectNext()
                resultado = self.parseFactor()
                resultado = UnOp('-', [resultado])
                return resultado
            
            elif self.tokenizer.next.type == "NOT":
                self.tokenizer.selectNext()
                resultado = self.parseFactor()
                resultado = UnOp('!', [resultado])
                return resultado

        elif self.tokenizer.next.type == "ABRE_PARENTESES":
            self.tokenizer.selectNext()
            resultado = self.RelExpr()
            if self.tokenizer.next.type == "FECHA_PARENTESES":
                self.tokenizer.selectNext()
                return resultado
            else:
                sys.stderr.write('[ERRO] Parênteses não foi fechado.\n')
                sys.exit()
        
        elif self.tokenizer.next.type == "FECHA_PARENTESES":
            sys.stderr.write('[ERRO] Parênteses não foi aberto.\n')
            sys.exit()

        elif self.tokenizer.next.type == "READLINE":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "ABRE_PARENTESES":
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "FECHA_PARENTESES":
                    self.tokenizer.selectNext()
                    return Read()
                else:
                    sys.stderr.write('[ERRO] Parênteses do readline() não foi fechado.\n')
                    sys.exit()
    
        else:
            sys.stderr.write('[ERRO no ParseFactor].\n')
            sys.exit()
        
    def RelExpr(self):
        resultado = self.parseExpression()

        while self.tokenizer.next.type == "IGUAL" or self.tokenizer.next.type == "MENOR" or self.tokenizer.next.type == "MAIOR":

            if self.tokenizer.next.type == "IGUAL":
                self.tokenizer.selectNext()
                resultado = BinOp('==', [resultado, self.parseExpression()])
            elif self.tokenizer.next.type == "MENOR":
                self.tokenizer.selectNext()
                resultado = BinOp('<', [resultado, self.parseExpression()])
            elif self.tokenizer.next.type == "MAIOR":
                self.tokenizer.selectNext()
                resultado = BinOp('>', [resultado, self.parseExpression()])

        return resultado

    def parseBlock(self):
        '''
        Cria um objeto block para adicionar os statements no formato de nodes.
        '''
        nodes = []

        while self.tokenizer.next.type != "EOF":
            nodes.append(self.parseStatement())
            self.tokenizer.selectNext()
            
        self.tokenizer.selectNext()
        return Block(nodes)
    
    def parseStatement(self):
        '''
        Analisa se o statement é uma atribuição ou um println ou uma quebra de linha.
        '''
        if self.tokenizer.next.type == "IDENTIFIER":

            # Nome da variável
            identifier = Identifier(self.tokenizer.next.value, [])

            # Avança para pegar o sinal de atribuição ou declaração
            self.tokenizer.selectNext()

            if self.tokenizer.next.type == "ASSIGNMENT":
                # Avança para pegar o valor da variável
                self.tokenizer.selectNext()
                resultado = Assignment("=" , [identifier, self.RelExpr()])
           
            elif self.tokenizer.next.type == "ABRE_PARENTESES":
                self.tokenizer.selectNext()
                args_list = []

                if self.tokenizer.next.type != "FECHA_PARENTESES":
                    args_list.append(self.RelExpr())
                    print(args_list)
                    while self.tokenizer.next.type == "COMMA":
                        self.tokenizer.selectNext()
                        args_list.append(self.RelExpr())
                    
                if self.tokenizer.next.type == "FECHA_PARENTESES":
                    resultado = FuncCall(identifier.value, args_list)
                    self.tokenizer.selectNext()
                else:
                    sys.stderr.write('[ERRO] Parênteses não foi fechado na chamada de função.\n')
                    sys.exit()

            else: 
                sys.stderr.write('[ERRO] Não foi encontrada atribuição nem declaração ou chamada de função.\n')
                sys.exit()

            if self.tokenizer.next.type == "SEMICOLON":
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "FIM":
                    return resultado
                else:
                    sys.stderr.write('[ERRO] Não encontrou a quebra de linha\n')
                    sys.exit()
            else:
                sys.stderr.write('[ERRO] Não encontrou o ponto e vírgula.\n')
                sys.exit()
        
        elif self.tokenizer.next.type == "PRINTLN":
            self.tokenizer.selectNext()

            if self.tokenizer.next.type == "ABRE_PARENTESES":
                self.tokenizer.selectNext()
                resultado = Print("PRINTLN", [self.RelExpr()])

                if self.tokenizer.next.type == "FECHA_PARENTESES":
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == "SEMICOLON":
                        self.tokenizer.selectNext()
                        if self.tokenizer.next.type == "FIM":
                            return resultado
                        else:
                            sys.stderr.write('[ERRO] Não encontrou a quebra de linha depois do imprime()\n')
                            sys.exit()
                    else:
                        sys.stderr.write('[ERRO] Não encontrou o ponto e vírgula depois do imprime()\n')
                        sys.exit()
                
                else:
                    sys.stderr.write('[ERRO] Parênteses não foi fechado no println.\n')
                    sys.exit()

        elif self.tokenizer.next.type == "WHILE":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "ABRE_PARENTESES":

                self.tokenizer.selectNext()

                condition = self.RelExpr() 

                while_children = []
                
                if self.tokenizer.next.type == "FECHA_PARENTESES":
                    self.tokenizer.selectNext()
                    
                    if self.tokenizer.next.type == "ABRE_CHAVES":
                        self.tokenizer.selectNext()
                        if self.tokenizer.next.type == "FIM":
                            self.tokenizer.selectNext()

                            while self.tokenizer.next.type != "FECHA_CHAVES":
                                while_children.append(self.parseStatement())
                                self.tokenizer.selectNext()

                            while_block = Block(while_children) 
                            
                            if self.tokenizer.next.type == "FECHA_CHAVES":
                                self.tokenizer.selectNext()
                                return While("WHILE", [condition, while_block])
                            else:
                                sys.stderr.write('[ERRO] Não encontrou o "}" do loop while.\n')
                                sys.exit()

                    else:
                        sys.stderr.write('[ERRO] Não encontrou O "{" do loop while.\n')
                        sys.exit()
                else:
                    sys.stderr.write('[ERRO] Não encontrou o ")" do loop while.\n')
                    sys.exit()

        elif self.tokenizer.next.type == "IF":

            self.tokenizer.selectNext()
            condition = self.RelExpr()


            if self.tokenizer.next.type == "ABRE_CHAVES":
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "FIM":
                    
                    if_children = []
                    self.tokenizer.selectNext()

                    while self.tokenizer.next.type != "FECHA_CHAVES" and self.tokenizer.next.type != "ELSE":
                        if_children.append(self.parseStatement())
                        self.tokenizer.selectNext()
                        
                    if_block = Block(if_children)

                    if self.tokenizer.next.type == "FECHA_CHAVES":
                        self.tokenizer.selectNext()

                        if self.tokenizer.next.type == "ELSE":
                            self.tokenizer.selectNext()

                            if self.tokenizer.next.type == "ABRE_CHAVES":
                                self.tokenizer.selectNext()
                                if self.tokenizer.next.type == "FIM":   
                                    
                                    else_children = []
                                    self.tokenizer.selectNext()

                                    while self.tokenizer.next.type != "FECHA_CHAVES":
                                        else_children.append(self.parseStatement())
                                        self.tokenizer.selectNext()

                                    else_block = Block(else_children)

                                    if self.tokenizer.next.type == "FECHA_CHAVES":
                                        self.tokenizer.selectNext()
                                        return If("IF", [condition, if_block, else_block])
                
                                    else:
                                        sys.stderr.write('[ERRO] Não encontrou o } depois do else.\n')
                                        sys.exit()
                            
                        elif self.tokenizer.next.type == "FIM":
                            self.tokenizer.selectNext()
                            return If("IF", [condition, if_block])

                    else:
                        sys.stderr.write('[ERRO] Não encontrou o } depois do if.\n')
                        sys.exit()

            else:
                sys.stderr.write('[ERRO] Não encontrou o { do if.\n')
                sys.exit()

        elif self.tokenizer.next.type == "FUNCTION":
            self.tokenizer.selectNext()

            if self.tokenizer.next.type == "IDENTIFIER":
                func_name = Identifier(self.tokenizer.next.value)
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "ABRE_PARENTESES":
                    self.tokenizer.selectNext()
                    
                    # Função com parâmetros
                    params_list = []
                    if self.tokenizer.next.type == "IDENTIFIER":
                        identifier = Identifier(self.tokenizer.next.value)
                        params_list.append(VarDecl(self.tokenizer.next.value, [identifier, None]))
                        self.tokenizer.selectNext()

                        # Loopa em cima dos parâmetros
                        while self.tokenizer.next.type == "COMMA":
                            self.tokenizer.selectNext()
                            if self.tokenizer.next.type == "IDENTIFIER":
                                identifier = Identifier(self.tokenizer.next.value)
                                params_list.append(VarDecl(self.tokenizer.next.value, [identifier, None]))
                                self.tokenizer.selectNext()
                            else:
                                sys.stderr.write('[ERRO] Identificadores de parâmetros não está adequado.\n')
                                sys.exit()
                                                                
                    # Após pegar os parâmetros, verifica se o parênteses foi fechado
                    # Ou vai direto para cá no caso de uma função sem parâmetros
                    if self.tokenizer.next.type == "FECHA_PARENTESES":
                        self.tokenizer.selectNext()     
                        if self.tokenizer.next.type == "ABRE_CHAVES":
                            self.tokenizer.selectNext()
                            # Verifica a quebra de linha
                            if self.tokenizer.next.type == "FIM":
                                self.tokenizer.selectNext()
                
                                func_instructions = []
                                while self.tokenizer.next.type != "FECHA_CHAVES":
                                    func_instructions.append(self.parseStatement())
                                    self.tokenizer.selectNext()
                                

                                self.tokenizer.selectNext()
                                func_list = [func_name] + params_list + [Block(func_instructions)]
                                return FuncDec(func_list)
                            else:
                                sys.stderr.write('[ERRO] Não encontrou a quebra de linha.\n')
                                sys.exit()
                        else:
                            sys.stderr.write('[ERRO] Não encontrou o { da função.\n')
                            sys.exit()
                    else:
                        sys.stderr.write('[ERRO] Não encontrou o ) da função.\n')
                        sys.exit()         
            else:
                sys.stderr.write('[ERRO] Função sem nome.\n')
                sys.exit()
        
        elif self.tokenizer.next.type == "RETURN":

            self.tokenizer.selectNext()

            return_node = Return("RETURN", [self.RelExpr()])
            
            if self.tokenizer.next.type == "SEMICOLON":
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == "FIM":
                    return return_node
            
                else:
                    sys.stderr.write('[ERRO] Não encontrou a quebra de linha.\n')
                    sys.exit()
            else:
                sys.stderr.write('[ERRO] Não colocou ; depois do return.\n')
                sys.exit()
        
        # Linha vazia
        elif self.tokenizer.next.type == "FIM":
            return NoOp()
        
        else:
            sys.stderr.write('[ERRO] Statement inválido.\n')
            sys.exit()