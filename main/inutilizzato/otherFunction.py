#Import
import pulp as p
import numpy as np
import collections
from numpy.linalg import inv
import math


def numeroTagliDataDomanda(B, listOfDemand):
    ##Questo metodo ritorna una lista che identifica il numero minimo di
    ##tagli da effettuare data la matrice B e le rispettive domande
    ##di prodotto.

    #B: matrice nxn di tutti i tagli
    #listOfDemanda: list --> lista di tutte le domande dei prodotti
    #return returnCuts: list --> Lista dei tagli effettuati

    returnCuts = []

    C=[]
    
    B_np = np.matrix(B).transpose() ##Traspongo la matrice
    B_inverse = inv(B_np) ##rendo inversa la matrice
    demand_np = np.array(listOfDemand)

    C = np.multiply(demand_np, B_inverse) ##Eseguo la moltiplicazione con
    ##La matrice inversa

    ##Determino la lista finale dei tagli.
    valore = 0
    pos = 0
    for x in C.tolist():
        for y in range(len(listOfDemand)):
            valore += x[y]
            pos += 1
        returnCuts.append(valore)
        pos = 0
        valore = 0

    return returnCuts


def totalRolls(C):
    ##Questo metodo restituisce il numero totale di Roll da tagliare
    ##Data la lista C dei tagli effettuati

    #return numberOfRoll: float

    numberOfRoll = 0

    for num in C:
        numberOfRoll = numberOfRoll + num
    return numberOfRoll


def determinDualValue(B, n):
    ##Questo metodo va a determianare le variabili duali y per 
    ##La ricerca di un nuovo pattern
    ##In particolare per il duale si avrà YB = C_b = [1...1]

    #B: matrix nxn --> Matrice di base del problema
    #n: int --> dimensione della matrice e lunghezza di Y
    #Yret --> Ritorno dei valori della funzione obiettivo del problema duale di pricing

    Yret = []

    ##Numpy function per eseguire la divisione
    Y = np.ones(n)
    C_b = np.ones(n)
    B_np = np.matrix(B).transpose()
    B_inverse = inv(B_np)
    Y = np.multiply(C_b, B_inverse)
    Ylist = Y.tolist()

    ##Rendiamo la matrice una lista di valori
    ##in modo tale da eliminare quelli che non sono
    ##di nostro interesse
    ##Determino la lista finale dei tagli.
    valore = 0
    pos = 0
    
    for y in range(n):
        for x in Ylist:
            valore += x[y]
            pos += 1
        Yret.append(valore)
        pos = 0
        valore = 0

    return Yret



def determinPosEx(exitPattern, costVector):

    pos = 0

    #Creazione del problema di programmazione lineare intera
    Lp_prob = p.LpProblem('PositionProblem', p.LpMaximize)  

    ##Creazione delle variabili
    x = p.LpVariable("x", lowBound = 0, cat='Continuous')

    ##Funzione obiettivo:
    #total_prof = xs
    Lp_prob += x
    
    ##Diseguaglianze del problema:
    ##Diseguaglianze del problema:
    for z in range (len(exitPattern)):
        if not exitPattern[z] == 0:
            #Lp_prob += costVector[z] - x * exitPattern[z] >= 0
            Lp_prob += x >= costVector[z] / exitPattern[z]

        else:
            Lp_prob += x >= 1000

    #total_weight = sum(float(cost) - x * float(ex) for cost,ex in zip(costVector, exitPattern))
    #Lp_prob += total_weight <= 0

    #Solver
    print(Lp_prob)
    status = Lp_prob.solve()
    print(p.LpStatus[status])
    print("Objective value:", p.value(Lp_prob.objective))

    for x in range(len(exitPattern)):
        if costVector[x] == p.value(Lp_prob.objective):
            pos = x
    
    return pos +1
        

    ##Verifico se il valore della funzione obiettivo è maggiore di 1,
    ##In questo caso la lista A diventerà la nuova base da aggiungere 
    ##Al problema.
    #if p.value(Lp_prob.objective) > 1:
    #    for v in Lp_prob.variables():
    #        A.append(int(v.varValue))


def changeBase2(B, enteringPattern):
   
    enteringPattern.append(0) ##aggiungo 0 per rendere la matrice quadrata
    ##Inoltre scelgo 0 proprio perché non previsto a priori come taglio.
    for x in B:
        x.append(0)
    B.append(enteringPattern)
    return B


def updateDemand(listOfDemand, position):
    value = listOfDemand[position]
    listOfDemand.append(value)
    return listOfDemand

