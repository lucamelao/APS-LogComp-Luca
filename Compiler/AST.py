import sys

class Node:
    def __init__(self, value : str, children : list = []):
        self.value = value 
        self.children = children 

    def Evaluate(self, ST) -> int:
        pass 
    
class BinOp(Node):
    '''
    Binary Operation, 2 children
    '''
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, ST):

        left_value = self.children[0].Evaluate(ST)
        right_value = self.children[1].Evaluate(ST)

        if self.value == '+':
            return left_value + right_value
        elif self.value == '-':
            return left_value - right_value
        elif self.value == '*':
            return left_value * right_value
        elif self.value == '/':
            return left_value // right_value
        elif self.value == '==':
            return left_value == right_value
        elif self.value == '<':
            return left_value < right_value
        elif self.value == '>':
            return left_value > right_value
        elif self.value == 'e':
            return left_value and right_value
        elif self.value == 'ou':
            return left_value or right_value
        else:
            sys.stderr.write('[ERRO] Operador inválido.\n')
            sys.exit()

class UnOp(Node):
    '''
    Unary Operation, 1 child
    '''
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, ST):

        # value, type = self.children[0].Evaluate(ST)
        value = self.children[0].Evaluate(ST)

        # if type == 'Int':
        if self.value == '-':
            return -value
        elif self.value == '!':
            return not value
        else:
            return value

class IntVal(Node):

    ''''
    Integer Value, 0 children
    '''
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, ST):
        return int(self.value)

class NoOp(Node):
    '''
    No Operation, 0 children
    '''
    def __init__(self):
        super().__init__(0, [])
    
    def Evaluate(self, ST):
        return 0
    
class SymbolTable:
    ''''
    Existe durante a execucão da AST.
    Armazena os valores de cada variável.
    '''
    
    def __init__(self):
        self.table = {}

    def setter(self, key, value):
        self.table[key] = value
    
    def getter(self, key):
        if key in self.table.keys():
            return self.table[key]
        else:
            sys.stderr.write('[ERRO] A variável buscada não foi declarada.\n')
            sys.exit()

class Identifier(Node):
    '''
    Identifier, 0 children.
    value : name
    '''
    def __init__(self, value : str, children : list = []):
        super().__init__(value, children)

    def Evaluate(self, ST):
        return ST.getter(self.value)
    
class Assignment(Node): 
    '''
    Assignment, 2 children.
    children[0] : Identifier
    children[1] : Expression -> faz o Evaluate(ST)
    '''
    def __init__(self, value : str, children : list = []):
        super().__init__(value, children)

    def Evaluate(self, ST):
        value = self.children[1].Evaluate(ST)
        ST.setter(self.children[0].value, value)
    
class Block(Node):
    ''''
    Avalia todas as expressões dentro do bloco.
    '''
    def __init__(self, children : list = []):
        super().__init__("", children)

    def Evaluate(self, ST):
        for child in self.children:
            res = child.Evaluate(ST)
            if isinstance(child, Return):
                return res

class Print(Node):
    ''''
    Print, 1 child.
    Imprime o valor da expressão (Evaluate do children[0])
    '''
    def __init__(self, value : str, children : list = []):
        super().__init__(value, children)

    def Evaluate(self, ST):
        print(self.children[0].Evaluate(ST))
    
class While(Node):
    ''''
    While, 2 children.
    children[0] : Condição -> faz o Evaluate(ST)
    O valor é o elemento 0 da tupla retornada pelo Evaluate(ST)
    children[1] : Block while True
    '''
    def __init__(self, value : str, children : list = []):
        super().__init__(value, children)

    def Evaluate(self, ST):
        while self.children[0].Evaluate(ST):
            self.children[1].Evaluate(ST)
          
class If(Node):
    ''''
    If, 3 children.
    children[0] : Condição -> faz o Evaluate(ST)
    O valor é o elemento 0 da tupla retornada pelo Evaluate(ST)
    children[1] : Block if True
    children[2] : Block if False
    '''
    def __init__(self, value : str, children : list = []):
        super().__init__(value, children)

    def Evaluate(self, ST):
        conditional = self.children[0].Evaluate(ST)
        if conditional:
            self.children[1].Evaluate(ST)
        else:
            if len(self.children) == 3:
                self.children[2].Evaluate(ST)

class Read(Node):

    def __init__(self, value : str = None, children : list = []):
        super().__init__(value, children)

    def Evaluate(self, ST):
        return (input())
    
class VarDecl(Node):
    ''''
    Declaração de variável, 0 children.
    Pelo menos dois nós

    Primeiro nó: identifier
    Segundo nó: Resultado do RelExpr ou valor default
    Inteiro eh zero, string eh vazia
    '''
    
    def __init__(self, value : str, children : list):
        super().__init__(value, children)

    def Evaluate(self, ST):
        identifier = self.children[0]
        value = self.children[1]

        # Extraindo o valor do object no caso de um nó
        if isinstance(value, Node):
            value = value.Evaluate(ST)[0]

        ST.declarator(identifier.value, value)

class StringVal(Node):

    ''''
    String Value, 0 children
    '''
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, ST):
        return str(self.value)
    
# -- Novas classes v2.4 -- #

class FuncDec(Node):
    '''
    Declaração de função
    '''
    def __init__(self, children):
        super().__init__(None, children)

    def Evaluate(self, ST):
        FuncTable.declarator(self.children[0].value, self)

class FuncCall(Node):
    '''
    Chamada de função, n children
    '''
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, ST):
        # Recupera o nó da função na FuncTable
        funcNode = FuncTable.getter(self.value)

        # Cria uma nova SymbolTable para a função (dinâmica)
        funcST = SymbolTable()

        # Verificando se o número de argumentos é adequado
        if len(self.children) != (len(funcNode.children) - 2):
            sys.stderr.write('[ERRO] Número de argumentos inválido.\n')
            sys.exit()

        n_args = len(self.children)

        for i in range(n_args):
            key = funcNode.children[i+1].value
            value = self.children[i].Evaluate(ST)
            funcST.setter(key, value)

        # Executando o bloco da função
        retorno = funcNode.children[-1].Evaluate(funcST)
        
        # Retorna o valor de retorno da função
        return retorno
    
class Return(Node):
    '''
    Retorno de função, 1 child
    '''
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, ST):
        return self.children[0].Evaluate(ST)
    

class FuncTable:
    ''''
    Existe durante a execucão da AST.
    Armazena os valores de cada variável.
    '''
    table = {}

    @staticmethod
    def declarator(key, value):
        FuncTable.table[key] = value
    
    @staticmethod
    def getter(key):
        if key in FuncTable.table.keys():
            return FuncTable.table[key]
        else:
            sys.stderr.write(f'\n[ERRO NA FUNCTABLE] A variável buscada [{key}] não foi declarada.\n\n')
            sys.exit()
