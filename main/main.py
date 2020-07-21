##main.py
##Mazzola Alessio 0279323

#Import
import cuttingStock as cs


##Variabili del problema:
L = 300
listOfModules = [70,40,55,25,35,58,69,82,95]
listOdDemands = [205,2321,143,1089,117,411,34,411,67]
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