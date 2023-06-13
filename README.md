# APS - Uma Linguagem de Programação

**Aluno:** Luca Coutinho Melão

Repositório para a entrega da APS da disciplina Lógica da Computação (2023.1). Consiste na criação de uma linguagem de programação própria.

## 1. Introdução

A linguagem de programação criada é uma linguagem simples, com palavras reservadas em português, com o intuito de ser uma ferramenta didática e de fácil aprendizado para novos programadores brasileiros. Ela possui uma seleção de palavras reservadas intuitiva e também é pouco tipada, para que seja possível o aprendizado da lógica de programação sem grandes preocupações com a sua sintaxe. Acesse a apresentação com [slides](SimpleLanguage.pdf) para ter uma visão geral da linguagem.

Abaixo, segue a estrutura do repositório:

```bash
APS-LOGCOMP-LUCA
│
├── Compiler
│   ├── tokenizer.py
│   ├── parse.py
│   └── AST.py
│
├── Flex and Bison
│   ├── exec
│   ├── lexer.c
│   ├── lexer.l
│   ├── parser.c
│   ├── parser.h
│   └── parser.y
│
├── README.md
├── testes.txt
└── SimpleLanguage.pdf

```

`Compiler`: Pasta com o compilador da linguagem, feito em Python. Nela, cada arquivo tem uma responsabilidade específica:

- `tokenizer.py`: Análise léxica da linguagem, transformando o código em uma lista de tokens.
- `parse.py`: Análise sintática da linguagem, transformando a lista de tokens em uma árvore sintática abstrata.
- `AST.py`: Análise semântica da linguagem, transformando a árvore sintática abstrata em uma árvore semântica abstrata.

`Flex and Bison`: Pasta com os arquivos do Flex e do Bison, que foram utilizados para a entrega da tarefa 2.

`testes.txt`: Arquivo com testes que demonstram as características da Linguagem. (Tarefa 4)

`SimpleLanguage.pdf`: Apresentação com slides da Linguagem. (Tarefa 5)

## 2. Linguagem estruturada - Padrão EBNF

```` py

BLOCO          =  {COMANDO} ;
 
COMANDO        =  ( λ | ATRIBUICAO | IMPRESSAO | ENQUANTO | SE | FUNCAO | RETORNA | CHAMADA), ";", "\n" ;
 
ATRIBUICAO     =  IDENTIFICADOR,(["=",RELEXPR] |"=", RELEXPR );

IMPRESSAO      =  "imprime", "(" RELEXPR ")" ;
 
SE             =  "se", "(", RELEXPR, ")", "{", COMANDO, "}", ["senao", "{", COMANDO, "}"] ;
 
ENQUANTO       =  "enquanto", "(", RELEXPR, ")", "{", COMANDO,"}" ;
  
FUNCAO         =  "funcao", IDENTIFICADOR, "(", [PARAMETRO], ")", "{", "\n", {BLOCO}, "}" ;

PARAMETRO      =  IDENTIFICADOR, {",", IDENTIFICADOR} ;

CHAMADA        = IDENTIFICADOR, "(", [RELEXPR, {",", RELEXPR}] ,")";
 
RETORNA        =  "retorna", RELEXPR;

RELEXPR        =  EXPRESSAO, { ("<" | ">" | "==" ), EXPRESSAO } ;
 
EXPRESSAO      =  TERMO {("+" | "-", "ou") TERMO} ;
 
TERMO          =  FATOR {("*" | "/" | "e"), FATOR} ;
 
FATOR          = (NÚMERO | STRING | IDENTIFICADOR, ["(", [RELEXPR, {",", RELEXPR}] ,")"] | ("+" | "-" | "!"), FACTOR) | "(", RELEXPR, ")" ;
 
CHAMADAFUNCAO  =  IDENTIFICADOR "(" [EXPRESSAO {"," EXPRESSAO}] ")" ;
 
IDENTIFICADOR  =  LETRA, {LETRA | DIGITO | "_"} ;
 
NÚMERO         =  DIGITO, { DIGITO } ;
 
STRING         =  '"' {LETRA} '"' ;

LETRA          =  ( a | ... | z | A | ... | Z ) ;
 
DIGITO         =  ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;

````

## 3. Exemplos de código e programas

**3.1.** Atribuição e impressão de valores

```py
x = 5;
y = 3;
imprime(x + y);
```

**3.2.** Estrutura condicional (se-senao)

```py
x = 10;
y = 20;

se (x > y) {
    imprime(x);
} senao {
    imprime(y);
}
```

**3.3.** Laço enquanto

```py
x = 0;

enquanto (x < 5) {
    imprime(x);
    x = x + 1;
}
```

**3.4.** Declaração de função e chamada de função

```py
funcao subtracao(a, b) {
    retorna a - b;
}

x = 5;
y = 3;

resultado = subtracao(x, y);
imprime(resultado);
```

**3.5.** Condicional com E

```py
x = 10;
y = 20;
z = 30;

se (x < y e y < z) {
    imprime("x é menor que y e y é menor que z");
}
```

**3.6.** Condicional com OU

```py
temperatura = 25;

se (temperatura < 20 ou temperatura > 30) {
    imprime("A temperatura está fora do intervalo confortável");
} senao {
    imprime("A temperatura está dentro do intervalo confortável");
}
```

**3.7.** Condicional com E e OU

```py
idade = 25;
temCarteira = 1; // 1 representa verdadeiro, 0 representa falso

se ((idade > 17 e idade < 66) e temCarteira == 1) {
    imprime("A pessoa pode dirigir");
} senao {
    imprime("A pessoa não pode dirigir");
}
```

**3.8.** Condicional com múltiplas condições lógicas

```py
nota1 = 7;
nota2 = 9;
nota3 = 6;
media = (nota1 + nota2 + nota3) / 3;

se (media > 5 e (nota1 > 5 e nota2 > 5 e nota3 > 5)) {
    imprime("Aprovado");
} senao {
    imprime("Reprovado");
}
```

**3.9.** Função com condicionais que recebe entrada via terminal

```py
funcao ePar(n) {
    se (n / 2 * 2 == n) {
        resultado = 1;
    } senao {
        resultado = 0;
    }
    retorna resultado;
}

imprime("Digite um número: ");
x = entrada();
se (ePar(x) == 1) {
    imprime("O número digitado é par");
} senao {
    imprime("O número digitado é ímpar");
}
```

**3.10.** Função recursiva

```py
funcao fatorial(n) {
    se ((n == 0) ou (n == 1)) {
        resultado = 1;
    } senao {
        resultado = n * fatorial(n - 1);
    }
    retorna resultado;
}

x = 5;
resultado = fatorial(x);
imprime(resultado);
```

## 4. Execução do compilador

Depois de clonar o repositório, acesse o diretório pelo terminal e execute o seguinte comando para rodar o exemplo de testes:

```shell
python3 main.py testes.txt
```
