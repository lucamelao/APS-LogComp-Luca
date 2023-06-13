%{
#include <stdio.h>
#include <string.h>
#include "parser.h"
%}

%option noyywrap

%%

[ \t\n]                 ;

\"[^"]*\"               return STRING;

"e"                     return AND;
"ou"                    return OR;
"imprime"               return PRINT;
"se"                    return IF;
"senao"                 return ELSE;
"enquanto"              return WHILE;
"funcao"                return FUNCTION;
"retorna"               return RETURN;

[a-zA-Z][a-zA-Z0-9_]*   return IDENTIFIER;
"[a-zA-Z][a-zA-Z0-9_]"  return STRING;
[0-9]+"."[0-9]+         return DOUBLE;
[0-9]+                  return INT;

"="                     return EQUAL;
"+"                     return PLUS;
"-"                     return MINUS;
"*"                     return MULTIPLY;
"/"                     return DIVIDE;
"("                     return LPAR;
")"                     return RPAR;
";"                     return SEMICOLON;
","                     return COMMA;
"{"                     return LBRACE;
"}"                     return RBRACE;
"=="                    return EQ;
"!="                    return NE;
"<"                     return LT;
">"                     return GT;

.                       printf("Token desconhecido\n"); yyterminate();

%%