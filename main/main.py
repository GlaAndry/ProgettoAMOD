##main.py
##Mazzola Alessio 0279323

#Import
import cuttingStock as cs

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
    rilassato.
    4) Determinare nuovamente la soluzione del problmea con le nuove modalità di taglio aggiunte.
    5) Se il problema duale non presenta delle modalità di taglio migliori, allora STOP """


##Variabili del problema:
L = 20
listOfModules = [9,8,7,6]
listOdDemands = [511,301,263,383]
n = len(listOfModules)


def calculate_solution():

    B = cs.determineInitialPattern(L,listOfModules)
    C = cs.numeroTagliDataDomanda(B, listOdDemands)
    Optm = cs.totalRolls(C)
    print("Numero Di tagli data la domanda per questo pattern: ", C)
    print("Valore soluzione corrente: ", Optm)
    print("Valore della soluzione con roundUp: ", cs.roundUpSolution(Optm))

    Y = cs.determinDualValue(B, n)
    enteringPattern = cs.resolve_pricing(L, Y, listOfModules)
    exitPattern = cs.determineExitPattern(B, enteringPattern, n)
    positionExit = cs.determinePositionExit(exitPattern, C)
    B = cs.changeBase(B, positionExit, enteringPattern)

    while(True):
        
        C = cs.numeroTagliDataDomanda(B, listOdDemands)
        Optm = cs.totalRolls(C)
        print("Numero Di tagli data la domanda per questo pattern: ", C)
        print("Valore soluzione corrente: ", Optm)
        print("Valore della soluzione con roundUp: ", cs.roundUpSolution(Optm))

        Y = cs.determinDualValue(B, n)
        enteringPattern = cs.resolve_pricing(L, Y, listOfModules)
        if(len(enteringPattern) == 0):
            print("\n\nTrovata la soluzione ottima!\n")
            print("Numero Di tagli data la domanda per questo pattern: ", C)
            print("Valore soluzione corrente: ", Optm)
            print("Valore della soluzione con roundUp: ", cs.roundUpSolution(Optm))
            break
        exitPattern = cs.determineExitPattern(B, enteringPattern, n)
        positionExit = cs.determinePositionExit(exitPattern, C)
        print(positionExit)

        B = cs.changeBase(B, positionExit, enteringPattern)

    

calculate_solution()