%{
#include <stdio.h>
int yylex();
void yyerror(const char *s) { printf("ERRO: %s\n", s); }
%}

%token IDENTIFIER INT DOUBLE STRING
%token EQUAL PLUS MINUS MULTIPLY DIVIDE
%token LPAR RPAR SEMICOLON COMMA LBRACE RBRACE
%token EQ NE LT GT AND OR
%token PRINT IF ELSE WHILE FUNCTION RETURN

%start program

%%

program : stmts
        ;

stmts : stmt
      | stmts stmt
      ;

stmt : assignment
     | print_statement
     | if_statement
     | while_statement
     | function_declaration
     | return_statement
     ;

assignment : IDENTIFIER EQUAL expression SEMICOLON
           ;

print_statement : PRINT LPAR expression RPAR SEMICOLON
                ;

if_statement : IF LPAR condition RPAR LBRACE stmts RBRACE
             | IF LPAR condition RPAR LBRACE stmts RBRACE ELSE LBRACE stmts RBRACE
             ;

while_statement : WHILE LPAR condition RPAR LBRACE stmts RBRACE
                ;

function_declaration : FUNCTION IDENTIFIER LPAR parameter_list RPAR LBRACE stmts RBRACE
                     ;

return_statement : RETURN expression SEMICOLON
                 | RETURN SEMICOLON
                 ;

parameter_list : IDENTIFIER
               | parameter_list COMMA IDENTIFIER
               | /* empty */
               ;

expression : expression PLUS term
           | expression MINUS term
           | term
           ;

term : term MULTIPLY factor
     | term DIVIDE factor
     | factor
     ;

factor : INT
       | DOUBLE
       | STRING
       | IDENTIFIER
       | LPAR expression RPAR
       | function_call
       ;

function_call : IDENTIFIER LPAR expression_list RPAR
              ;

expression_list : expression
                | expression_list COMMA expression
                | /* empty */
                ;

condition : condition_logical
          | condition AND condition_logical
          | condition OR condition_logical
          ;

condition_logical : expression EQ expression
                  | expression NE expression
                  | expression LT expression
                  | expression GT expression
                  ;

%%

int main(){
  yyparse();
  return 0;
}
