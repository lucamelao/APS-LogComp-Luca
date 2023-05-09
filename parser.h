/* A Bison parser, made by GNU Bison 2.3.  */

/* Skeleton interface for Bison's Yacc-like parsers in C

   Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006
   Free Software Foundation, Inc.

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2, or (at your option)
   any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor,
   Boston, MA 02110-1301, USA.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     IDENTIFIER = 258,
     INT = 259,
     DOUBLE = 260,
     STRING = 261,
     EQUAL = 262,
     PLUS = 263,
     MINUS = 264,
     MULTIPLY = 265,
     DIVIDE = 266,
     LPAR = 267,
     RPAR = 268,
     SEMICOLON = 269,
     COMMA = 270,
     LBRACE = 271,
     RBRACE = 272,
     EQ = 273,
     NE = 274,
     LT = 275,
     GT = 276,
     AND = 277,
     OR = 278,
     PRINT = 279,
     IF = 280,
     ELSE = 281,
     WHILE = 282,
     FUNCTION = 283,
     RETURN = 284
   };
#endif
/* Tokens.  */
#define IDENTIFIER 258
#define INT 259
#define DOUBLE 260
#define STRING 261
#define EQUAL 262
#define PLUS 263
#define MINUS 264
#define MULTIPLY 265
#define DIVIDE 266
#define LPAR 267
#define RPAR 268
#define SEMICOLON 269
#define COMMA 270
#define LBRACE 271
#define RBRACE 272
#define EQ 273
#define NE 274
#define LT 275
#define GT 276
#define AND 277
#define OR 278
#define PRINT 279
#define IF 280
#define ELSE 281
#define WHILE 282
#define FUNCTION 283
#define RETURN 284




#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef int YYSTYPE;
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
# define YYSTYPE_IS_TRIVIAL 1
#endif

extern YYSTYPE yylval;

