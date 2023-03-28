# APS - Uma Linguagem de Programação

**Aluno:** Luca Coutinho Melão

Repositório para a entrega da APS da disciplina Lógica da Computação (2023.1). Consiste na criação de uma linguagem de programação própria.

## 1. Introdução

A linguagem de programação criada é uma linguagem simples, com palavras reservadas em português, com o intuito de ser uma ferramenta didática e de fácil aprendizado para novos programadores brasileiros. Ela possui poucas palavras reservadas e também é pouco tipada, para que seja possível o aprendizado da lógica de programação sem grandes preocupações com a sintaxe da linguagem.

## 2. Linguagem estruturada - Padrão EBNF

```` py
SimpleLanguage =  {COMANDO} ;
 
COMANDO        =  ATRIBUICAO | IMPRESSAO | CONDICIONAL | LACOENQUANTO | LACOPARACADA | DECLARAFUNCAO | RETORNA VALOR ;
 
ATRIBUICAO     =  IDENTIFICADOR '=' EXPRESSAO ';' ;
 
IMPRESSAO      =  'imprime' '(' EXPRESSAO ')' ';' ;
 
CONDICIONAL    =  'se' '(' CONDICAO ')' '{' {COMANDO} '}' ['senao' '{' {COMANDO} '}'] ;
 
LACOENQUANTO   =  'enquanto' '(' CONDICAO ')' '{' {COMANDO} '}' ;
 
LACOPARACADA   =  'paraCada' '(' ATRIBUICAO ';' CONDICAO ';' ATRIBUICAO ')' '{' {COMANDO} '}' ;
 
DECLARAFUNCAO  =  'funcao' IDENTIFICADOR '(' [IDENTIFICADOR {',' IDENTIFICADOR}] ')' '{' {COMANDO} '}' ;
 
RETORNA VALOR  =  'retorna' [EXPRESSAO] ';' ;
 
EXPRESSAO      =  TERMO {('+' | '-') TERMO} ;
 
TERMO          =  FATOR {('*' | '/') FATOR} ;
 
FATOR          =  NÚMERO | IDENTIFICADOR | '(' EXPRESSAO ')' | CHAMADAFUNCAO ;
 
CHAMADAFUNCAO  =  IDENTIFICADOR '(' [EXPRESSAO {',' EXPRESSAO}] ')' ;
 
CONDICAO       =  CONDICAOLOGICA {('e' | 'ou')} CONDICAOLOGICA ;
 
CONDICAOLOGICA =  EXPRESSAO ('==' | '!=' | '<' | '>' | '<=' | '>=') EXPRESSAO ;
 
IDENTIFICADOR  =  LETRA {LETRA | DIGITO} ;
 
NÚMERO         =  DIGITO {DIGITO} ['.' DIGITO {DIGITO}] ;
 
LETRA          =  ( a | ... | z | A | ... | Z ) ;
 
DIGITO         =  ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;

````

## 3. Exemplos de código

```` py
// Exemplo 1: Atribuição e impressão de valores
x = 5;
y = 3;
imprime(x + y);

// Exemplo 2: Estrutura condicional (se-senao)
x = 10;
y = 20;

se (x > y) {
    imprime(x);
} senao {
    imprime(y);
}

// Exemplo 3: Laço enquanto
x = 0;

enquanto (x < 5) {
    imprime(x);
    x = x + 1;
}

// Exemplo 4: Laço paraCada
paraCada (i = 0; i < 10; i = i + 1) {
    imprime(i);
}

// Exemplo 5: Declaração de função e chamada de função
funcao subtracao(a, b) {
    retorna a - b;
}

x = 5;
y = 3;

resultado = subtracao(x, y);
imprime(resultado);

// Exemplo 6: Condicional com E
x = 10;
y = 20;
z = 30;

se (x < y e y < z) {
    imprime("x é menor que y e y é menor que z");
}

// Exemplo 7: Condicional com OU
temperatura = 25;

se (temperatura < 20 ou temperatura > 30) {
    imprime("A temperatura está fora do intervalo confortável");
} senao {
    imprime("A temperatura está dentro do intervalo confortável");
}

// Exemplo 8: Condicional com E e OU
idade = 25;
temCarteira = 1; // 1 representa verdadeiro, 0 representa falso

se ((idade >= 18 e idade <= 65) e temCarteira == 1) {
    imprime("A pessoa pode dirigir");
} senão {
    imprime("A pessoa não pode dirigir");
}

// Exemplo 9: Condicional com múltiplas condições lógicas
nota1 = 7;
nota2 = 9;
nota3 = 6;
media = (nota1 + nota2 + nota3) / 3;

se (media >= 6 e (nota1 >= 6 e nota2 >= 6 e nota3 >= 6)) {
    imprime("Aprovado");
} senão {
    imprime("Reprovado");
}

//Exemplo 10: Condicional com aninhamento
x = 5;
y = 10;
z = 15;

se (x < y e y < z) {
    imprime("x é menor que y e y é menor que z");
    se (x * 2 < z ou y * 2 > z) {
        imprime("x * 2 é menor que z ou y * 2 é maior que z");
    }
}
````
