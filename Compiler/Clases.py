from dataclasses import dataclass, field
from typing import List
from copy import deepcopy

#########################     Hoja     ############################
class Hoja:
    def __init__ (self, padre, valor):
        self.valor = valor
        self.padre = padre
        self.hijos = list()
        if self.padre == None:
            self.nivel=0
        else:
            self.nivel = self.padre.nivel+1
    def anhadeHijo(self,nodo):
        self.hijos.append(nodo)
		
#########################     Árbol     ############################
class Arbol():
    def __init__ (self, raiz):
         self.raiz = Hoja(None,raiz)
         self.tamano = 1
    def buscaAux(self,valor,origen):
        if self.tamano == 1:
            if self.raiz.valor==valor:
                return self.raiz
            else:
                return None
        if origen.valor == valor:
            return origen
        if len(origen.hijos)==0:
            return None
        for nodo in origen.hijos:
            n = self.buscaAux(valor,nodo)
            if n is not None and self.buscaAux(valor,nodo).valor == valor:
                return self.buscaAux(valor,nodo)
        return None
    def buscaNodo(self,valor):
        return self.buscaAux(valor,self.raiz)
    def mca(self,a,b):
        nodoA = self.buscaNodo(a)
        nodoB = self.buscaNodo(b)
        if nodoA == None or nodoB == None:
            raise Exception(f'No existe padre {a} {b}')
        if nodoA.valor==nodoB.valor:
            return nodoA.valor
        elif nodoA.nivel > nodoB.nivel:
            return self.mca(nodoA.padre.valor,b)
        else:
            return self.mca(a,nodoB.padre.valor)
    def subtipo(self,hijo,padre):
        if self.buscaNodo(padre) == None:
            return False
        if hijo == padre:
            return True
        return self.subtipoAUX(hijo,self.buscaNodo(padre))
    def subtipoAUX(self,hijo,padre):
        for h in padre.hijos:
            if h.valor == hijo:
                return True
            else:
                if self.subtipoAUX(hijo,h):
                    return True
        return False
    def anhade(self,padre,valor):
        p = self.buscaNodo(padre)
        if p==None:
            raise Exception(f'No existe padre {padre}')
        anade = True
        for h in p.hijos:
            if h.valor == valor:
                anade = False
        if anade:
            p.anhadeHijo(Hoja(p,valor))
            self.tamano = self.tamano + 1
    def recorreAux(self,origen,resultado):
        if len(origen.hijos)==0:
            return resultado
        for nodo in origen.hijos:
            resultado+=[(origen.valor,nodo.valor)]
        for nodo in origen.hijos:
            self.recorreAux(nodo,resultado)
        return resultado
    def recorre(self):
        return self.recorreAux(self.raiz,[])

#########################     Nodos     ############################  
@dataclass
class Nodo:
    linea: int

    def str(self, n):
        return f'{n*" "}#{self.linea}\n'

class Expresion(Nodo):
    cast: str 

#########################     Tipos     ############################
@dataclass
class Formal(Expresion):
    nombre_variable: str
    tipo: str
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_formal\n'
        resultado += f'{(n+2)*" "}{self.nombre_variable}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        return resultado
    def calculaTipo(self, ambito, arbol_clases, diccionario_metodos):
        self.cast = self.tipo
        return []

#########################     Asignaciones     ############################
@dataclass
class Asignacion(Expresion):
    nombre: str
    cuerpo: Expresion

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_assign\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self, ambito, arbol_clases, diccionario_metodos):
        Error = []
        Error += self.cuerpo.calculaTipo(ambito, arbol_clases, diccionario_metodos)
        if self.nombre == 'self':
            self.cast = ambito["SELF_TYPE"]
            Error += [f"{self.linea}: Cannot assign to 'self'."]
            return Error
        if self.nombre in ambito:
            cast_nombre = ambito[self.nombre]
            
        else:
            cast_nombre = 'Object'
            Error += ["Error 25"]
        
        if arbol_clases.subtipo(self.cuerpo.cast,cast_nombre):
            self.cast = cast_nombre
        else:
            self.cast = 'Object'
            if cast_nombre != "SELF_TYPE":
                Error += [f"{self.linea}: Type {self.cuerpo.cast} of assigned expression does not conform to declared type {cast_nombre} of identifier {self.nombre}."]
        return Error

#########################     Llamada Metodo Estatico     ############################
@dataclass
class LlamadaMetodoEstatico(Expresion):
    cuerpo: Expresion
    clase: str
    nombre_metodo: str
    argumentos: List[Expresion]

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_static_dispatch\n'
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n+2)*" "}{self.clase}\n'
        resultado += f'{(n+2)*" "}{self.nombre_metodo}\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += ''.join([c.str(n+2) for c in self.argumentos])
        resultado += f'{(n+2)*" "})\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def calculaTipo(self, ambito, arbol_clases, diccionario_metodos):
        Error = []
        Error +=  self.cuerpo.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        for e in self.argumentos:
            Error +=  e.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        if not arbol_clases.subtipo(self.cuerpo.cast, self.clase):
            self.cast="Object"
            Error += [f"{self.linea}: Expression type {self.cuerpo.cast} does not conform to declared static dispatch type {self.clase}."]
            return Error
            

        if (self.clase,self.nombre_metodo) in diccionario_metodos:
            argumentosT, retorno = diccionario_metodos[(self.clase,self.nombre_metodo)]    
        if len(argumentosT) != len(self.argumentos):
            self.cast = 'Object'
            Error += ["Error 4"]
        else:
            for i in range(len(self.argumentos)):
                self.argumentos[i].calculaTipo(ambito,arbol_clases,diccionario_metodos)
                if self.argumentos[i].cast != argumentosT[i].tipo:
                    if type(self.argumentos[i]) == Objeto and self.argumentos[i].nombre != 'self':
                        pass
                    elif type(self.argumentos[i]) == Objeto and self.argumentos[i].nombre == 'self':
                        Error += [f"{self.linea}: In call of method {self.nombre_metodo}, type SELF_TYPE of parameter {argumentosT[i].nombre_variable} does not conform to declared type {argumentosT[i].tipo}."]
                    else:
                        Error += [f"{self.linea}: In call of method {self.nombre_metodo}, type {self.argumentos[i].cast} of parameter {argumentosT[i].nombre_variable} does not conform to declared type {argumentosT[i].tipo}."]
        
        
        if retorno == "SELF_TYPE":
            self.cast=ambito["SELF_TYPE"]
        else:
            self.cast=retorno
        return Error

#########################     Llamada Metodo     ############################
@dataclass
class LlamadaMetodo(Expresion):
    cuerpo: Expresion
    nombre_metodo: str
    argumentos: List[Expresion]

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_dispatch\n'
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n+2)*" "}{self.nombre_metodo}\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += ''.join([c.str(n+2) for c in self.argumentos])
        resultado += f'{(n+2)*" "})\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        Error = []
        Error +=  self.cuerpo.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        for e in self.argumentos:
            Error +=  e.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        aux = self.cuerpo.cast
        if self.cuerpo.cast == "SELF_TYPE":
            aux = ambito["SELF_TYPE"]
        if (aux,self.nombre_metodo) in diccionario_metodos:
            argumentosT, retorno = diccionario_metodos[(aux,self.nombre_metodo)]
        else:
            self.cast="Object"
            Error += [f"{self.linea}: Dispatch to undefined method {self.nombre_metodo}."]
            return Error
        if len(argumentosT) != len(self.argumentos):
            Error += ["Error 4"]
        else:
            for i in range(len(self.argumentos)):
                self.argumentos[i].calculaTipo(ambito,arbol_clases,diccionario_metodos)
                if self.argumentos[i].cast != argumentosT[i].tipo:
                    if type(self.argumentos[i]) == Objeto and self.argumentos[i].nombre != 'self':
                        pass
                    elif type(self.argumentos[i]) == Objeto and self.argumentos[i].nombre == 'self':
                        if argumentosT[i].tipo != ambito["SELF_TYPE"]:
                            Error += [f"{self.linea}: In call of method {self.nombre_metodo}, type SELF_TYPE of parameter {argumentosT[i].nombre_variable} does not conform to declared type {argumentosT[i].tipo}."]
                    else:
                        if(self.argumentos[i].cast != "SELF_TYPE"):
                            Error += [f"{self.linea}: In call of method {self.nombre_metodo}, type {self.argumentos[i].cast} of parameter {argumentosT[i].nombre_variable} does not conform to declared type {argumentosT[i].tipo}."]
                
        if retorno == "SELF_TYPE":
            self.cast=self.cuerpo.cast
        else:
            self.cast=retorno
        return Error

#########################     Condicionales     ############################
@dataclass
class Condicional(Expresion):
    condicion: Expresion
    verdadero: Expresion
    falso: Expresion

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_cond\n'
        resultado += self.condicion.str(n+2)
        resultado += self.verdadero.str(n+2)
        resultado += self.falso.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        Error = []
        Error +=  self.condicion.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        Error +=  self.verdadero.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        Error +=  self.falso.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        if self.condicion.cast != 'Bool':
            Error += ["Errror 1324"]
        aux1 = self.verdadero.cast
        aux2 = self.falso.cast
        if self.verdadero.cast == "SELF_TYPE":
            aux1=ambito["SELF_TYPE"]
        if self.falso.cast == "SELF_TYPE":
            aux2=ambito["SELF_TYPE"]
        self.cast=arbol_clases.mca(aux1,aux2)
        return Error

#########################     Bucles     ############################
@dataclass
class Bucle(Expresion):
    condicion: Expresion
    cuerpo: Expresion

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_loop\n'
        resultado += self.condicion.str(n+2)
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        Error = []
        Error += self.condicion.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        Error += self.cuerpo.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        if self.condicion.cast != 'Bool':
            Error += [f"{self.linea}: Loop condition does not have type Bool."]
        self.cast="Object"
        return Error

#########################     Let     ############################
@dataclass
class Let(Expresion):
    nombre: str
    tipo: str
    inicializacion: Expresion
    cuerpo: Expresion

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_let\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.inicializacion.str(n+2)
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def calculaTipo(self, ambito, arbol_clases, diccionario_metodos):
        Error = []
        nuevo_ambito = deepcopy(ambito)
        if self.nombre == "self":
            Error+=[f"{self.linea}: 'self' cannot be bound in a 'let' expression."]
        nuevo_ambito[self.nombre] = self.tipo
        Error +=  self.cuerpo.calculaTipo(nuevo_ambito,arbol_clases,diccionario_metodos) 
        Error +=  self.inicializacion.calculaTipo(nuevo_ambito,arbol_clases,diccionario_metodos) 
        if not arbol_clases.subtipo(self.inicializacion.cast,self.tipo) and self.inicializacion.cast != "SELF_TYPE" and self.inicializacion.cast != "_no_type" and self.tipo != "SELF_TYPE":
            Error += [f"{self.linea}: Inferred type {self.inicializacion.cast} of initialization of {self.nombre} does not conform to identifier's declared type {self.tipo}."]
        self.cast = self.cuerpo.cast

        return Error

#########################     Bloques     ############################
@dataclass
class Bloque(Expresion):
    expresiones: List[Expresion]

    def str(self, n):
        resultado = super().str(n)
        resultado = f'{n*" "}_block\n'
        resultado += ''.join([e.str(n+2) for e in self.expresiones])
        resultado += f'{(n)*" "}: {self.cast}\n'
        resultado += '\n'
        return resultado
    def calculaTipo(self, ambito, arbol_clases, diccionario_metodos):
        Error = []
        for e in self.expresiones:
            Error +=  e.calculaTipo(ambito, arbol_clases, diccionario_metodos) 
        self.cast = self.expresiones[-1].cast
        return Error

#########################     RamaCase     ############################
@dataclass
class RamaCase(Expresion):
    nombre_variable: str
    tipo: str
    cuerpo: Expresion

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_branch\n'
        resultado += f'{(n+2)*" "}{self.nombre_variable}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        Error = []
        Error +=  self.cuerpo.calculaTipo(ambito, arbol_clases, diccionario_metodos) 
        if type(self.cuerpo) == Objeto:
            self.cuerpo.cast = self.tipo
        self.cast = self.tipo
        return Error

#########################     Switch     ############################
@dataclass
class Swicht(Expresion):
    expr: Expresion
    casos: List[RamaCase]

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_typcase\n'
        resultado += self.expr.str(n+2)
        resultado += ''.join([c.str(n+2) for c in self.casos])
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        Error = []
        Error += self.expr.calculaTipo(ambito,arbol_clases,diccionario_metodos) 
        for r in self.casos:
            r.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        Aux = []
        for r in self.casos:
            if r.tipo in Aux:
                Error += [f"{self.linea}: Duplicate branch {r.tipo} in case statement."]
            else:
                Aux += [r.tipo]
        tipoRC = self.casos[0].cuerpo.cast
        for rc in self.casos[1:]:
            tipoRC = arbol_clases.mca(rc.cuerpo.cast,tipoRC)
        self.cast = tipoRC
        return Error

#########################     NEW     ############################
@dataclass
class Nueva(Expresion):
    tipo: str
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_new\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        Error = []
        aux = self.tipo
        if self.tipo == "SELF_TYPE":
            aux = ambito["SELF_TYPE"]
        if arbol_clases.buscaNodo(aux)==None:
            Error += [f"{self.linea}: 'new' used with undefined class {aux}."]
        self.cast = self.tipo
        return Error

#########################     Operación Binaria     ############################ 
@dataclass
class OperacionBinaria(Expresion):
    izquierda: Expresion
    derecha: Expresion
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        Error=[]
        Error += self.izquierda.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        Error += self.derecha.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        if arbol_clases.subtipo(self.izquierda.cast,"Int") and arbol_clases.subtipo(self.derecha.cast,"Int"):
            self.cast = arbol_clases.mca(self.izquierda.cast,self.derecha.cast)
        else:
            self.cast = "Object"
            Error += [f"{self.linea}: non-Int arguments: {self.izquierda.cast} + {self.derecha.cast}"]
        return Error

#########################     Suma     ############################
@dataclass
class Suma(OperacionBinaria):
    operando: str = '+'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_plus\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

#########################     Resta     ############################
@dataclass
class Resta(OperacionBinaria):
    operando: str = '-'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_sub\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

#########################     Multiplicación     ############################
@dataclass
class Multiplicacion(OperacionBinaria):
    operando: str = '*'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_mul\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado


#########################     División     ############################
@dataclass
class Division(OperacionBinaria):
    operando: str = '/'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_divide\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

#########################     Menor     ############################
@dataclass
class Menor(OperacionBinaria):
    operando: str = '<'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_lt\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        Error = []
        Error += self.izquierda.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        Error +=  self.derecha.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        if arbol_clases.subtipo(self.izquierda.cast,"Int") and arbol_clases.subtipo(self.derecha.cast,"Int"):
            self.cast = "Bool"
        else:
            self.cast = "Object"
            Error += ["Error 3"]
        return Error

#########################     Menos o igual     ############################
@dataclass
class LeIgual(OperacionBinaria):
    operando: str = '<='

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_leq\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        Error = []
        Error += self.izquierda.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        Error +=  self.derecha.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        if arbol_clases.subtipo(self.izquierda.cast,"Int") and arbol_clases.subtipo(self.derecha.cast,"Int"):
            self.cast = "Bool"
        else:
            self.cast = "Object"
            Error += ["Error 3"]
        return Error

#########################     Igual     ############################
@dataclass
class Igual(OperacionBinaria):
    operando: str = '='

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_eq\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        Error = []
        Error += self.izquierda.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        Error +=  self.derecha.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        if self.izquierda.cast == self.derecha.cast:
            self.cast = "Bool"
        else:
            if (self.izquierda.cast=='Bool' or self.izquierda.cast=='String' or self.izquierda.cast=='Int') and (self.derecha.cast=='Bool' or self.derecha.cast=='String' or self.derecha.cast=='Int'):
                self.cast = "Object"
                Error += [f"{self.linea}: Illegal comparison with a basic type."]
            else:
                self.cast = "Bool"
        return Error

#########################     Negación     ############################
@dataclass
class Neg(Expresion):
    expr: Expresion
    operador: str = '~'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_neg\n'
        resultado += self.expr.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        Error = []
        Error += self.expr.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        self.cast = self.expr.cast
        return Error

#########################     Not     ############################
@dataclass
class Not(Expresion):
    expr: Expresion
    operador: str = 'NOT'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_comp\n'
        resultado += self.expr.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        Error = []
        Error += self.expr.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        self.cast = "Bool"
        return Error

#########################     Es nulo     ############################
@dataclass
class EsNulo(Expresion):
    expr: Expresion

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_isvoid\n'
        resultado += self.expr.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def calculaTipo(self, ambito, arbol_clases, diccionario_metodos):
        Error = []
        Error += self.expr.calculaTipo(ambito,arbol_clases,diccionario_metodos)
        self.cast = self.expr.cast
        return Error


#########################     Objetos     ############################
@dataclass
class Objeto(Expresion):
    nombre: str

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_object\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        Error = []
        if self.nombre in ambito:
            self.cast = ambito[self.nombre]
        else:
            self.cast = "Object"
            Error+=[f"{self.linea}: Undeclared identifier {self.nombre}."]
        return Error


#########################     No type     ############################
@dataclass
class NoExpr(Expresion):
    nombre: str = ''

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_no_expr\n'
        resultado += f'{(n)*" "}: _no_type\n'
        return resultado

    def calculaTipo(self, ambito, arbol_clases, diccionario_metodos):
        self.cast = "_no_type"
        return []

#########################     Enteros     ############################
@dataclass
class Entero(Expresion):
    valor: int

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_int\n'
        resultado += f'{(n+2)*" "}{self.valor}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        self.cast = "Int"
        return []

#########################     Strings     ############################
@dataclass
class String(Expresion):
    valor: str

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_string\n'
        resultado += f'{(n+2)*" "}{self.valor}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        self.cast = "String"
        return []

#########################     Booleanos     ############################
@dataclass
class Booleano(Expresion):
    valor: bool

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_bool\n'
        resultado += f'{(n+2)*" "}{1 if self.valor else 0}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def calculaTipo(self,ambito,arbol_clases,diccionario_metodos):
        self.cast = "Bool"
        return []
		

#########################     IterableNodo     ############################
@dataclass
class IterableNodo(Nodo):
    secuencia: List = field(default_factory=List)


class Programa(IterableNodo):
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{" "*n}_program\n'
        resultado += ''.join([c.str(n+2) for c in self.secuencia])
        return resultado
    
    def calculaTipos(self):
        ambito = dict()
        arbol_clases = Arbol("Object")
        diccionario_metodos = dict()
        diccionario_atributos = dict()
        error = []
        encontrado = False
        for s in self.secuencia:
            if s.nombre == "Main":
                encontrado = True
        if not encontrado:
            return [f"Class Main is not defined."]
        arbol_clases.anhade("Object","Int")
        arbol_clases.anhade("Object","Bool")
        arbol_clases.anhade("Object","String")
        arbol_clases.anhade("Object","IO")
        diccionario_metodos[("Object", "abort")] = ([],"Object")
        diccionario_metodos[("Object", "type_name")] = ([],"String")
        diccionario_metodos[("Object", "copy")] = ([],"SELF_TYPE")
        diccionario_metodos[("IO", "out_string")] = ([Formal(0,"out_string","String")],"SELF_TYPE")
        diccionario_metodos[("IO", "out_int")] = ([Formal(0,"out_int","Int")],"SELF_TYPE")
        diccionario_metodos[("IO", "in_string")] = ([],"String")
        diccionario_metodos[("IO", "in_int")] = ([],"Int")
        diccionario_metodos[("String", "length")] = ([],"Int")
        diccionario_metodos[("String", "concat")] = ([Formal(0,"concat","String")],"String")
        diccionario_metodos[("String", "substr")] = ([Formal(0,"substr","Int"), Formal(0,"substr","Int")],"String")
        for s in self.secuencia:
            s.calculaMetodosAtributos(diccionario_metodos,diccionario_atributos)
        aux = []
        for s in self.secuencia:
            if s.nombre in aux:
                error += [f"{self.linea}: Class {s.nombre} was previously defined."]
            else:
                aux.append(s.nombre)
        repetir = False
        for s in self.secuencia:
            if arbol_clases.buscaNodo(s.padre) == None:
                repetir+=1
            else:
                arbol_clases.anhade(s.padre,s.nombre)
        while repetir!=0:
            for s in self.secuencia:
                if arbol_clases.buscaNodo(s.padre) != None:
                        arbol_clases.anhade(s.padre,s.nombre)
            repetir-=1
        for s in arbol_clases.recorre():
            p,n = s
            propaga(p,n,diccionario_metodos,diccionario_atributos)
        for s in self.secuencia:
            error += s.calculaTipo(ambito,arbol_clases,diccionario_metodos,diccionario_atributos)


        return error
        

#########################     Características     ############################
@dataclass
class Caracteristica(Expresion):
    nombre: str
    tipo: str
    cuerpo: Expresion
            

#########################     Clases     ############################
@dataclass
class Clase(Nodo):
    nombre: str
    padre: str
    nombre_fichero: str
    caracteristicas: List[Caracteristica] = field(default_factory=list)


    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_class\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.padre}\n'
        resultado += f'{(n+2)*" "}"{self.nombre_fichero}"\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += ''.join([c.str(n+2) for c in self.caracteristicas])
        resultado += '\n'
        resultado += f'{(n+2)*" "})\n'
        return resultado

    def calculaTipo(self, ambito, arbol_clases, diccionario_metodos,diccionario_atributos):
        Error = []

        if self.nombre == 'Int' or self.nombre == 'String' or self.nombre == 'Bool' or self.nombre == 'IO' or self.nombre == 'Object' or self.nombre == 'SELF_TYPE':
            Error += [f"{self.linea}: Redefinition of basic class {self.nombre}."]
            return Error
        if self.padre == "SELF_TYPE":
            Error += [f"{self.linea}: Class {self.nombre} cannot inherit class SELF_TYPE."]
            return Error
        if arbol_clases.buscaNodo(self.padre) == None:
            Error += [f"{self.linea}: Class {self.nombre} inherits from an undefined class {self.padre}."]
            return Error
        if self.padre == 'Int' or self.padre == 'String' or self.padre == 'Bool':
            Error += [f"{self.linea}: Class {self.nombre} cannot inherit class {self.padre}."]
            return Error
        nuevo_ambito = deepcopy(ambito)
        nuevo_ambito["SELF_TYPE"]=self.nombre
        nuevo_ambito["self"]="SELF_TYPE"
        for p,a in diccionario_atributos:
            if p==self.padre:
                nuevo_ambito[a] = diccionario_atributos[p,a]
        for c in self.caracteristicas:
            if type(c) == Metodo:
                if (self.padre,c.nombre) not in diccionario_metodos:
                    if arbol_clases.buscaNodo(c.tipo)==None and c.tipo!="SELF_TYPE":
                        Error+=[f"{self.linea}: Undefined return type {c.tipo} in method {c.nombre}."]
                    else:
                        diccionario_metodos[(self.nombre,c.nombre)]=(c.formales,c.tipo)
                else:
                    if len(c.formales)==len(diccionario_metodos[(self.padre,c.nombre)][0]):
                        distintos = False
                        for i in range(len(c.formales)):
                            if c.formales[i].tipo != diccionario_metodos[(self.padre,c.nombre)][0][i].tipo:
                                distintos = True
                                Error += [f"{self.linea}: In redefined method {c.nombre}, parameter type {c.formales[i].tipo} is different from original type {diccionario_metodos[(self.padre,c.nombre)][0][i].tipo}"]
                        if not distintos:
                            diccionario_metodos[(self.nombre,c.nombre)]=(c.formales,c.tipo)
                    else:
                        Error += [f"{self.linea}: Incompatible number of formal parameters in redefined method {c.nombre}."]
            else:
                if (self.padre,c.nombre) not in diccionario_atributos:
                    nuevo_ambito[c.nombre] = c.tipo
                else: 
                    Error += [f"{self.linea}: Attribute {c.nombre} is an attribute of an inherited class."]
        for c in self.caracteristicas:
            Error += c.calculaTipo(nuevo_ambito,arbol_clases,diccionario_metodos)
        return Error
            
    def calculaMetodosAtributos(self,diccionario_metodos,diccionario_atributos):
         for c in self.caracteristicas:
            if type(c) == Metodo:
                diccionario_metodos[(self.nombre,c.nombre)]=(c.formales,c.tipo)
            else:
                diccionario_atributos[(self.nombre,c.nombre)] = c.tipo
def propaga(padre, hijo,diccionario_metodos,diccionario_atributos):
    for p,m in list(diccionario_metodos):
        if p == padre:
            diccionario_metodos[(hijo,m)]=diccionario_metodos[(p,m)]
    for p,m in list(diccionario_atributos):
        if p == padre:
            diccionario_atributos[(hijo,m)]=diccionario_atributos[(p,m)]
			
			
#########################     Métodos     ############################
@dataclass
class Metodo(Caracteristica):
    formales: List[Formal]

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_method\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += ''.join([c.str(n+2) for c in self.formales])
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)
        return resultado
    def calculaTipo(self, ambito, arbol_clases, diccionario_metodos):
        nuevo_ambito = deepcopy(ambito)
        Error = []
        aux = []
        for e in self.formales:
            if e.nombre_variable in aux:
                Error += [f"{self.linea}: Formal parameter {e.nombre_variable} is multiply defined."]
            else:
                aux.append(e.nombre_variable)
        for e in self.formales:
            if e.nombre_variable == "self":
                Error += [f"{self.linea}: 'self' cannot be the name of a formal parameter."]
            if e.tipo == "SELF_TYPE":
                Error += [f"{self.linea}: Formal parameter {e.nombre_variable} cannot have type SELF_TYPE."]
        for e in self.formales:
            nuevo_ambito[e.nombre_variable] = e.tipo
        Error += self.cuerpo.calculaTipo(nuevo_ambito,arbol_clases,diccionario_metodos)
        self.cast = self.tipo
        aux =self.cuerpo.cast
        if self.cuerpo.cast == "SELF_TYPE":
            aux = ambito["SELF_TYPE"]
        aux2 = self.cast
        if self.tipo == "SELF_TYPE" and self.cuerpo.cast != "SELF_TYPE":
                Error += [f"{self.linea}: Inferred return type {self.cuerpo.cast} of method foo does not conform to declared return type {self.tipo}."]
        if self.cast == "SELF_TYPE":
            aux2 = ambito["SELF_TYPE"]
        if not arbol_clases.subtipo(aux,aux2) and not arbol_clases.buscaNodo(aux)==None:
            Error += [f"{self.linea}: Inferred return type {aux} of method {self.nombre} does not conform to declared return type {aux2}."]
        return Error


#########################     Atributos     ############################
@dataclass
class Atributo(Caracteristica):

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_attr\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)
        return resultado
    def calculaTipo(self, ambito, arbol_clases, diccionario_metodos):
        Error = []
        if self.nombre == "self":
            Error += [f"{self.linea}: 'self' cannot be the name of an attribute."]
        
        Error +=  self.cuerpo.calculaTipo(ambito, arbol_clases, diccionario_metodos)
        if self.cuerpo.cast != '_no_type':
            if arbol_clases.subtipo(self.cuerpo.cast,self.tipo):
                self.cast = self.tipo
        else:
            self.cast = self.tipo
        return Error
