# coding: utf-8

from Lexer import CoolLexer
from sly import Parser
import sys
import os
from Clases import *
DIRECTORIO = os.path.join("C:/Users/green/Desktop/Progr/LPROGRAMACION/compiler")


sys.path.append(DIRECTORIO)

GRADING = os.path.join(DIRECTORIO, 'grading')
FICHEROS = os.listdir(GRADING)

TESTS = [fich for fich in FICHEROS
         if os.path.isfile(os.path.join(GRADING, fich))
         and fich.endswith(".test")]

#TESTS=["casemultiplebranch.test"]

class CoolParser(Parser):
    tokens = CoolLexer.tokens
    precedence = (
        ('left', 'IN','LET'),
        ('right', 'ASSIGN'),
        ('right', 'NOT'),
        ('nonassoc', '<','LE','='),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'ISVOID'),
        ('left', '@'),
        ('left', '.'),
        ('right', '~')
    )

    #Lista de clases (Programa)
    @_('l_class')
    def program(self, p):
        return Programa(p.l_class[-1].linea,p.l_class)

    #Definicion de la clase
    #nombre del fichero,caracteristicas...
    @_('CLASS TYPEID herencia "{" l_feature "}"')
    def clase(self, p): 
        return Clase(p.lineno,p.TYPEID,p.herencia,self.nombre_fichero,p.l_feature)

    #Contenido de cada una de las clases
    @_('clase ";"')
    def l_class(self, p):
        return [p.clase]

    #Caso en el que de dispone de varias clases separadas por punto y coma
    @_('clase ";" l_class')
    def l_class(self, p):
        return  [p.clase] + p.l_class




    ##################         Formal         ######################
    
    @_('formal')
    def l_formal(self,p):
        return [p.formal]

    #primera y siguientes variables
    @_('l_formal "," formal')
    def l_formal(self,p):
        return p.l_formal + [p.formal]

    #nombre variable y tipo, separados por ":"
    @_('OBJECTID ":" TYPEID')
    def formal(self,p):
        return Formal(p.lineno, p.OBJECTID, p.TYPEID)

    ##################################################################

    
    #herencia de otra clase
    @_('INHERITS TYPEID')
    def herencia(self, p):
        return p.TYPEID

    #Caracteristicas 
    @_('OBJECTID "(" l_formal ")" ":" TYPEID "{" expr "}" ')
    def feature(self, p):
        return Metodo(p.lineno,p.OBJECTID,p.TYPEID,p.expr, p.l_formal)
 
    #Caracteristicas de la linea hasta el ";"
    @_('l_feature feature ";"')
    def l_feature(self, p):
        return p.l_feature + [p.feature]

    #Asignacion de valor mediante una expresion
    @_('ASSIGN expr')
    def inicializador(self, p):
        return p.expr


    #asignacion a una expresion
    @_('OBJECTID ASSIGN expr')
    def expr(self, p):
        return Asignacion(p.lineno, p.OBJECTID, p.expr)
 
    #objeto y su asignacion
    @_('OBJECTID ":" TYPEID inicializador')
    def feature(self, p):
        return Atributo(p.lineno,p.OBJECTID,p.TYPEID,p.inicializador)

   
   

    #########################     Argumentos     ############################

    #argumentos de metodos
    @_('expr')
    def lista_argumentos(self, p):
        return [p.expr]

    #lista argumentos separados por ","
    @_('lista_argumentos "," expr')
    def lista_argumentos(self, p):
        return p.lista_argumentos + [p.expr]

    #lista de argumentos
    @_('lista_argumentos')
    def s_expr(self, p):
        return p.lista_argumentos

    ####################################################################################
    




    #########################     Llamadas a metodos     ############################
     
    @_('expr "." OBJECTID "(" s_expr ")" ')
    def expr(self, p):
        return LlamadaMetodo(p.lineno, p.expr, p.OBJECTID, p.s_expr)

    #llamada a metodo estatico
    @_('expr "@" TYPEID "." OBJECTID "(" s_expr ")" ')
    def expr(self, p):
        return LlamadaMetodoEstatico(p.lineno, p.expr, p.TYPEID, p.OBJECTID, p.s_expr)

    #llamada a metodo
    @_('OBJECTID "(" s_expr ")"')
    def expr(self, p):
        return LlamadaMetodo(p.lineno, Objeto(p.lineno,"self"),p.OBJECTID, p.s_expr)

    ####################################################################################


 
    

    #######################   declaracion de variables     ############################

    @_('decl')
    def l_decl(self,p):
        return [p.decl]
 
    @_('l_decl "," decl')
    def l_decl(self,p):
        return   p.l_decl + [p.decl] 


    @_('OBJECTID ":" TYPEID inicializador')
    def decl(self,p):
        return (p.OBJECTID,p.TYPEID,p.inicializador)

    ####################################################################################




    #########################  Casos de elementos vacios    ###########################

    #Regla 'empty' propiamente dicha
    @_('')
    def empty(self, p):
        pass
    
    #Caso 'l_feature' vacio
    @_('empty')
    def l_feature(self, p): 
        return []

    #Caso 'l_formal' vacio
    @_('empty')
    def l_formal(self,p): 
        return []
    
    #Caso 's_expr' vacio
    @_('empty') 
    def s_expr(self, p): 
        return []

    #Caso 'l_expr' vacio
    @_('empty')
    def l_expr(self,p): 
        return []

    #Caso 'herencia' vacio
    @_('empty')
    def herencia(self, p): 
        return "Object"
    
    #Caso 'inicializador' vacio
    @_('empty')
    def inicializador(self, p): 
        return NoExpr(-1)

    ########################################################################


 
      
    ######  Gestion de las distintas expresiones contenidas en el codigo   ######## 
 
    #Nuevo tipo
    @_('NEW TYPEID')
    def expr(self, p): 
        return Nueva(p.lineno,p.TYPEID)

    #Comprobar nulidad de la expresion
    @_('ISVOID expr')
    def expr(self, p): 
        return EsNulo(p.lineno,p.expr)

    #Suma de dos expresiones
    @_('expr "+" expr')
    def expr(self, p):
        return Suma(p.lineno,p.expr0,p.expr1)

    #Resta de dos expresiones
    @_('expr "-" expr')
    def expr(self, p): 
        return Resta(p.lineno,p.expr0,p.expr1)

    #Multiplicacion de dos expresiones
    @_('expr "*" expr')
    def expr(self, p): 
        return Multiplicacion(p.lineno,p.expr0,p.expr1)

    #Comparacion LE de dos expresiones
    @_('expr LE expr')
    def expr(self, p): 
        return LeIgual(p.lineno,p.expr0,p.expr1)

    #Comparacion < de dos expresiones
    @_('expr "<" expr')
    def expr(self, p): 
        return Menor(p.lineno,p.expr0,p.expr1)

    #Division de dos expresiones
    @_('expr "/" expr')
    def expr(self, p): 
        return Division(p.lineno,p.expr0,p.expr1)

    #Negacion de una expresion
    @_('"~" expr')
    def expr(self, p): 
        return Neg(p.lineno,p.expr)

    #Igualdad entre dos expresiones
    @_('expr "=" expr')
    def expr(self, p): 
        return Igual(p.lineno,p.expr0,p.expr1)

    #NOT de una expresion
    @_('NOT expr')
    def expr(self, p): 
        return Not(p.lineno,p.expr)

    #Expresiones encapsuladas entre parentesis
    @_('"(" expr ")"')
    def expr(self, p): 
        return p.expr

    #expresiones separadas por ;(atoi)
    @_(' expr ";" l_expr')
    def l_expr(self,p): 
        return  [p.expr] + p.l_expr

    #expresiones entre "{}" separadas por ;
    @_('"{" expr ";" l_expr "}"')
    def expr(self, p): 
        return Bloque(p.lineno, [p.expr] + p.l_expr )
 
    #Condicional if/else con expresiones
    @_('IF expr THEN expr ELSE expr FI')
    def expr(self, p): 
        return Condicional(p.lineno,p.expr0,p.expr1,p.expr2)
    
    #Expresion contenida en un elemento case
    @_('CASE expr OF l_ramacase ESAC ')
    def expr(self, p): 
        return Swicht(p.lineno,p.expr,p.l_ramacase)

    #Bucle while
    @_('WHILE expr LOOP expr POOL')
    def expr(self, p): 
        return Bucle(p.lineno,p.expr0,p.expr1)

    #Expresion de tipo "let"
    @_('LET l_decl IN expr ')
    def expr(self, p):
        lets = p.expr
        for i in reversed(p.l_decl):
            lets = Let(p.expr.linea, *i, lets)
        return lets
    
    #############################################################################
    


    
    ######  Los siguientes cuatro metodos definen nuestros tipos de datos  ######

    #Aparicion de elementos de tipo Int 
    @_('OBJECTID') 
    def expr(self, p):
        return Objeto(p.lineno,p.OBJECTID)
 
    #Aparicion de elementos de tipo Int 
    @_('INT_CONST')
    def expr(self, p): 
        return Entero(p.lineno,p.INT_CONST)

    #Aparicion de elementos de tipo String
    @_('STR_CONST')
    def expr(self, p): 
        return String(p.lineno,p.STR_CONST)

    #Aparicion de elementos de tipo Bool 
    @_('BOOL_CONST')
    def expr(self, p): 
        return Booleano(p.lineno,p.BOOL_CONST)
    ############################################################################### 




    ######  Conjunto que define a forma de actuar las ramas case en el codigo   ######
    
    #El ramacase define el caso en el que aparece el case con la funcion ARROW y 
    #los otros dos,definen los casos de 'ramacase' individual o 'l_ramacase ramacase'
    @_('OBJECTID  ":" TYPEID DARROW expr ";"')
    def ramacase(self, p): 
        return RamaCase(p.lineno,p.OBJECTID,p.TYPEID,p.expr)

    @_('ramacase')
    def l_ramacase(self, p):     
        return [p.ramacase]

    @_('l_ramacase ramacase')
    def l_ramacase(self, p): 
        return p.l_ramacase + [p.ramacase]
    ###################################################################################    





    ######  Gestion de los distintos errores que pueden aparecer en el codigo   ######

    #Caso en el cual aparece un error antes de ";"
    @_('error ";"')
    def l_feature(self, p):  
       return []

    #Error dentro del metodo
    @_('OBJECTID "(" l_formal ")" ":" TYPEID "{" error "}" ')
    def feature(self, p): 
        return Nodo(p.lineno)

    #Error antes de una definicion 
    @_('error ";" formal')
    def l_formal(self,p): 
        return [Nodo(p.lineno)]

    #Error antes de una expresion
    @_(' error ";" l_expr')
    def l_expr(self,p): 
        return  [Nodo(p.lineno)]

    #Error entre "{}" y antes de ";"
    @_('"{" error ";" l_expr "}"')
    def expr(self, p): 
        return [Nodo(p.lineno)]

    #Error en la declaracion
    @_('error "," decl')
    def l_decl(self,p): 
        return [Nodo(p.lineno)]
    
    #Definicion de error
    def error(self, p): 
        if p!= None:
            temp = f'"{self.nombre_fichero}", line {p.lineno}: syntax error at or near '
            if p.type in {'IF', 'FI','OF', 'ELSE', 'POOL', 'LOOP', 'LE','DARROW' }:
                temp += f'{p.type}'
            elif p.type in CoolLexer.tokens:
                temp += f'{p.type} = {p.value}'
            elif p.type in CoolLexer.literals:
                temp += f"'{p.type}'"
        else:
            temp = '"emptyprogram.test", line 0: syntax error at or near EOF'
        
        self.errores.append(temp)
    ################################################################################### 


Pasados=0
NoPasados=0
 
for fich in TESTS:

    f = open(os.path.join(GRADING, fich), 'r')
    g = open(os.path.join(GRADING, fich + '.out'), 'r')
    lexer = CoolLexer()
    lexer1 = CoolLexer()
    parser = CoolParser()
    parser.nombre_fichero = fich
    parser.errores = []
    bien = ''.join([c for c in g.readlines() if c and '#' not in c])
    entrada = f.read()
    j = parser.parse(lexer.tokenize(entrada))
  
    parser.errores += j.calculaTipos()
   
    for t0 in lexer1.tokenize(entrada):
        pass
    if j and not parser.errores:
        resultado = '\n'.join([c for c in j.str(0).split('\n')
                               if c and '#' not in c])
    else:
        for i in range(len(parser.errores)):
            parser.errores[i]=fich+":"+parser.errores[i]
            
        resultado = '\n'.join(parser.errores)
        resultado += '\n' + "Compilation halted due to static semantic errors."
    f.close(), g.close()
    if resultado.lower().strip().split() != bien.lower().strip().split():
        print(f"Revisa el fichero {fich}")
        NoPasados+=1
        f = open(os.path.join(GRADING, fich)+'.nuestro', 'w')
        g = open(os.path.join(GRADING, fich)+'.bien', 'w')
        f.write(resultado.strip())
        g.write(bien.strip())
        f.close()
        g.close()
    else:
        Pasados+=1
        print(f"test: {fich}    --> OK")
   

print(f"\n\n\nTest pasados: {Pasados}    \nTest no pasados:  {NoPasados}")


    


