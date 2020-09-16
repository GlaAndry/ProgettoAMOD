##cuttingStock.py
##Mazzola Alessio 0279323

#Import
import pulp as p
import numpy as np
import collections
from numpy.linalg import inv
import math

""" Dobbiamo necessariamente andare a considerare il problema rilassato di CSP
in quanto non si conosce ancora un algoritmo per determinare una soluzione ottima
del problema intero """

"""Possiamo dividere l'algoritmo implementativo nei seguenti passaggi:
    1) Determinazione delle modalità di taglio iniziali, quindi si prendono
    gli oggetti da tagliare uno alla volta e si determina quale sia la migliore
    modalità di taglio solamente andando a considerare quell'oggetto.
    2) Risoluzione del problema primale e del duale associato, cioè il problema
    di pricing (Problema di Knapsack) per 
    determinare modalità di taglio migliori di quelle già presenti, se possibile.
    In caso se ne trovino di migliori, allora allora la modalità di taglio viene aggiunta
    al problema rilassato.
    3) Iterare il procedimento fino a ricavare la soluzione cercata. """



def determineInitialPattern(L, listOfModule):
    ##Questo metodo serve per inizializzare la matrice B delle modalità
    ##di taglio possibili data la lunghezza L del paper Roll e 
    ##la lista di tutti i moduli.

    ##Inizialmente andiamo a considerare solamente tutt

    #L: int --> Lunghezza del paperRoll
    #listOfModule: list --> [Lunghezze di tutti i moduli del problema]
    #return B --> matrince nxn di tutti i moduli di taglio

    n = len(listOfModule)
    initialLenght = L

    ##Liste di appoggio per il metodo.
    B = []
    A = []

    counter = 0

    for y in range(0, n):
        while L - listOfModule[y] >= 0:
            L = L - listOfModule[y]
            counter += 1
        for x in range (0, n):
            if x == y:
                A.append(counter)
            else:
                A.append(0)
        #print(A)
        B.append(A)
        A = []
        counter = 0
        L = initialLenght
            
    return B


def resolve_primal(listOfDemand, cutScheme):
    """Questo metodo va a risolvere il problema primale. In particolare da questo 
    andiamo a ritornare i seguenti elementi:
    
    Lp_prob : Permette di ricavare la soluzione ottima del problema
    B : Lista di elementi utilizzata come funzione obiettivo nel problema duale
    C : Vettore dei costi associati al problema, utilizzata per la determinazione 
        della posizione nel metodo determinePositionExit(...)

    """
    ## Liste di appoggio per il metodo.
    B = []
    C = []
    reduced_cost = []
    isOpt = 0

    #Creazione del problema di programmazione lineare intera
    Lp_prob = p.LpProblem('Primal_Problem', p.LpMinimize)  

    ##Creazione delle variabili
    xs = [p.LpVariable("x{}".format(i), lowBound = 0, cat='Continuous') for i in range(len(cutScheme))]

    ##Funzione obiettivo:
    total_prof = sum(x for x in xs)
    Lp_prob += total_prof
    
    ##Diseguaglianze del problema:

    ####################################
    #for z in range (len(cutScheme)):
    #    Lp_prob += sum (h * cut[z] for h ,cut in zip(xs, cutScheme)) >= listOfDemand[z] ##Questo funziona per il metodo sostitutivo
    ###################################
    #counter = 0
    for x in range(len(cutScheme[0])):
        Lp_prob += sum (h * cut[x] for h ,cut in zip(xs, cutScheme)) >= listOfDemand[x] ##Questo funziona per il metodo add
    #    counter += 1

    #Solver
    print("Problema")
    print(Lp_prob)

    status = Lp_prob.solve()
    print(p.LpStatus[status])
    print("Objective value:", p.value(Lp_prob.objective))
    print ('\nThe values of the variables : \n')
    ##Valore primale delle variabili e vettore dei costi ridotti.
    for v in Lp_prob.variables():
        reduced_cost.append(v.dj)
        C.append(v.varValue)
        print(v.name, "=", v.varValue)

    ##Valore duale delle variabili
    for name, c in list(Lp_prob.constraints.items()):
        B.append(c.pi)
    ##controllo se la soluzione del primale è ottima tramite il vettore dei costi ridotti.
    if(min(reduced_cost) >= 0):
        isOpt = 1
        return Lp_prob, B , C , isOpt

    return Lp_prob, B , C , isOpt


def resolve_pricing(L, listObjectiveFunction, listInequity):
    ##Questo metodo va a risolvere il sottoproblema di knapsack 
    ##derivante dal CSP rilassato, andando a restituire la modalità
    ##di taglio che deve entrare in base.
    ##Un pattern entra in base solamente se il valore della sua
    ##funzione obiettivo e > 1.

    #L --> int: Lunghezza del Roll
    #listObjectiveFunction: --> list: [valori della funzione obiettivo] --> i valori sono individuati dai valori del problema duale
    #listInequity --> list: [valori della diseguaglianza]
    ##return A --> list: [Nuova Cutting pattern]

    ##Creazione della lista per la nuova base.
    A = []

    #Creazione del problema di programmazione lineare intera
    Lp_prob = p.LpProblem('Pricing Problem', p.LpMaximize)  

    ##Creazione delle variabili
    xs = [p.LpVariable("x{}".format(i), lowBound = 0, cat='Integer') for i in range(len(listObjectiveFunction))]

    ##Funzione obiettivo:
    total_prof = sum(x * obj for x,obj in zip(xs, listObjectiveFunction))
    Lp_prob += total_prof
    
    ##Diseguaglianze del problema:
    total_weight = sum(x * w for x,w in zip(xs, listInequity))
    Lp_prob += total_weight <= L

    #Solver
    status = Lp_prob.solve()
    print(p.LpStatus[status])
    print("Objective value:", p.value(Lp_prob.objective))
    print ('\nThe values of the variables : \n')
    for v in Lp_prob.variables():
        print(v.name, "=", v.varValue)

    ##Verifico se il valore della funzione obiettivo è maggiore di 1,
    ##In questo caso la lista A diventerà la nuova base da aggiungere 
    ##Al problema.
    if p.value(Lp_prob.objective) > 1:
        for v in Lp_prob.variables():
            A.append(int(v.varValue))

    return A, p.value(Lp_prob.objective)

def determineExitPattern(B, enteringPattern, n):
    ##Attraverso questo metodo andiamo a determinare quale pattern 
    ##deve uscire dalla base per fare spazio al nuovo pattern 
    ##di taglio ricavato.

    ##In particolare possiamo scrivere BP_j = P_i
    ##P_J = pattern Uscente
    ##P_i = pattern entrante
    ##B matrice nxn

    exitPattern = []
    value = 0

    P_i = np.matrix(enteringPattern)
    B_np = np.matrix(B)
    ePattern = np.divide(P_i, B_np)
    ePatternList = ePattern.tolist()

    for x in range(n):
        for y in range(n):
            if(x == y):
                value += ePatternList[x][y]
        exitPattern.append(value)
        value = 0

    return exitPattern


def determinePositionExit(exitPattern, costVector):
    ##questo metodo permette di ritrovare il corrispondente 
    ##thetha associato al pattern uscente, in modo tale da ritornare la 
    ##posizione in B del pattern uscente per far posto a quello entrante.

    ##return pos --> int: Posizione del pattern uscente in B

    thetha = 0
    newTheta = 10000000 #valore molto grande (BIG_M)
    pos = 0

    for x in range(0,len(exitPattern)):
        if(exitPattern[x] == 0):
            continue
        else: ##255.5 - x*theta >= 0 --> 255.5 >= x*theta --> tetha = 255.5/x
            thetha = costVector[x]/exitPattern[x]
            if(thetha < newTheta):
                newTheta = thetha
                pos = x    
            
    return pos + 1



def updateBase(oldBase, enteringPattern):
    """Questo metodo si occupa di andare ad aggiornare la base B
    del problema primale, andando quindi ad aggiungere la modalità
    di taglio ricavata precedentemente per andare poi a ripetere
    i passi dell'algoritmo
    
    oldBase --> list[][] : Rappresenta la base non aggiornata del problema
    enteringPattern --> list[]: Rappresenta una lista contenente il pattern 
                                da aggiungere alla nuova base.
    """

    oldBase.append(enteringPattern)
    return oldBase

    

def changeBase(B, pos, enteringPattern):
    """Metodo utilizzato per la versione dell'algoritmo con
    sostituzione."""
    ##Questo metodo restituisce la nuova base sulla quale andare
    ##nuovamente a calcolare il problema.

    #B: matrix nxn --> vecchia base del problema
    #pos: int --> determinato tramite determinePositionExit

    ##return B_new: matrix nxn --> nuova base del problema.

    B_new = []
    counter = 1

    for x in B:
        if(counter == pos):
            B_new.append(enteringPattern)
        else:
            B_new.append(x)
        counter +=1

    #print(np.matrix(B_new).transpose())

    return B_new


def roundUpSolution(solutionList):
    ##Questo metodo si occupa di eseguire il rounding 
    ##up della solzione se questa non dovesse essere 
    ##intera.

    ##solutionList: list[] --> lista di valori della soluzione (interi e non)
    ##return: IntSolution --> valore della solzione intera.
    solValue = 0
    for x in solutionList:
        solValue += math.ceil(x)

    return solValue


