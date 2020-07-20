##cuttingStock.py
##Mazzola Alessio 0279323

#Import
import pulp as p
import numpy as np
import collections

##variabili del problema
#L --> Lunghezza del Roll
#l_i --> moduli di taglio
#d_i --> domanda per il singolo modulo

""" Dobbiamo necessariamente andare a considerare il problema rilassato di CSP
in quanto non si conosce ancora un algoritmo per determinare una soluzione ottima
del problema intero """

"""Possiamo dividere l'algoritmo implementativo nei seguenti passaggi:
    1) Determinazione delle modalità di taglio iniziali, quindi si prendono
    gli oggetti da tagliare uno alla volta e si determina quale sia la migliore
    modalità di taglio solamente andando a considerare quell'oggetto.
    2) Soluzione del problema rilassato con le modalità di taglio trovate.
    3) Determinazione del problema duale di pricing (Problema di Knapsack) per 
    determinare se qualche modalità di taglio sia migliore delle altre. In caso
    se ne trovino di migliori, allora aggiungere la modalità di taglio al problema
    rilassato. Nell'aggiunta della modalità di taglio dovremo andare a determinare quale 
    modulo dovrà essere scartato andando a risolvere un ulteriore problema.
    4) Determinare nuovamente la soluzione del problema con le nuove modalità di taglio.
    5) Se il problema duale non presenta delle modalità di taglio migliori, allora STOP """

#cuttingAndDemand = {"l_i": 2 , "d_i": 5} ##Dizionario contenente il modulo di taglio l_i e la sua domanda d_i 
             ##la lunghezza L ed il numero di pezzi da produrre R (cioè la domanda)

#L = 10

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

#print(determineInitialPattern(20, [10,2,3,4]))
#print(determineInitialPattern(20, [9,8,7,6]))

def numeroTagliDataDomanda(B, listOfDemand):
    ##Questo metodo ritorna una lista che identifica il numero minimo di
    ##tagli da effettuare data la matrice B e le rispettive domande
    ##di prodotto.

    #B: matrice nxn di tutti i tagli
    #listOfDemanda: list --> lista di tutte le domande dei prodotti
    #return C: list --> Lista dei tagli effettuati

    C=[]
    pos = 0
    for list in B:
            cuts =  listOfDemand[pos] / list[pos]
            pos += 1
            C.append(cuts)
    return C

#print(numeroTagliDataDomanda(determineInitialPattern(20, [9,8,7,6]), [511,301,263,383]))

def totalRolls(C):
    ##Questo metodo restituisce il numero totale di Roll da tagliare
    ##Data la lista C dei tagli effettuati

    #return numberOfRoll: float

    numberOfRoll = 0

    for num in C:
        numberOfRoll = numberOfRoll + num
    return numberOfRoll

#print(totalRolls(numeroTagliDataDomanda(determineInitialPattern(20, [9,8,7,6]), [511,301,263,383])))


#def checkIfOpt():
    ##La soluzione risulta essere ottima soilamente se C_j - Z_j per tutti 
    ##i pattern di tagli fuori dalla base

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
    B_np = np.matrix(B)
    Y = np.true_divide(C_b, B_np)
    Ylist = Y.tolist()

    ##Rendiamo la matrice una lista di valori
    ##in modo tale da eliminare quelli che non sono
    ##di nostro interesse
    value = 0
    for x in Ylist:
        for y in range(n):
            if(x[y] != np.Infinity):
                value += x[y]
        Yret.append(value)
        value = 0
    return Yret

#print(determinDualValue(determineInitialPattern(20, [9,8,7,6]), 4))


def resolve_pricing(L, listObjectiveFunction, listInequity):
    ##Questo metodo va a risolvere il sottoproblema di knapsack 
    ##derivante dal CSP rilassato, andando a restituire la modalità
    ##di taglio che deve entrare in base.
    ##Un pattern entra in base solamente se il valore della sua
    ##funzione obiettivo e > 1.

    #L --> int: Lunghezza del Roll
    #listObjectiveFunction: --> list: [valori della funzione obiettivo] --> i valori sono individuati dai valori del problema duale
    #listInequity --> list: [valori della diseguaglianza]
    ##return A --> list: [Nuova base]

    ##Creazione della lista per la nuova base.
    A = []

    #Creazione del problema di programmazione lineare intera
    Lp_prob = p.LpProblem('Pricing Problem', p.LpMaximize)  

    ##Creazione delle variabili
    xs = [p.LpVariable("x{}".format(i+1), lowBound = 0, cat='Integer') for i in range(len(listObjectiveFunction))]

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
            A.append(v.varValue)

    return A


#print('Primo problema \n\n')
#print(resolve_pricing(20, determinDualValue(determineInitialPattern(20, [9,8,7,6]), 4), [9,8,7,6]))


def determineExitPattern():
    ##Attraverso questo metodo andiamo a determinare quale pattern 
    ##deve uscire dalla base per fare spazio al nuovo pattern 
    ##di taglio ricavato.
    return None

#print('\n\nSecondo problema\n\n')
#print(resolve_pricing(20, [1/2, 1/2, 1/3, 1/3], [9,8,7,6]))