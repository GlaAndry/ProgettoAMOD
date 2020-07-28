##main.py
##Mazzola Alessio 0279323

#Import
import cuttingStock as cs
import pulp as p
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
import time

##Variabili del problema:
#L --> int: Lunghezza del Paper Roll
#ListOfModules --> List[]: Rappresenta la lista dei moduli richiesti
#ListOfDemands --> List[]: Rappresenta la lista delle domande associate ai moduli
#n --> int: Rappresenta la lunghezza della lista 
#L = 110
#listOfModules = [70,40,55,25,35]
#listOfDemands = [205,2321,143,1089,117]
#L = 20
#listOfModules = [9,8,7,6]
#listOfDemands = [511,301,263,383]
L = 10000
listOfModules = [2487,2439,2431,2419,2400,2333,2303,2232,2192,2176,2007,1817,1704,1612,1557,1457,1454,1304,1255,1246,1219,1148,1142,1066,1010,987,969,948,923,685,679,663,598,589,548,537,513,385,303,248,106,2]
listOfDemands = [2,1,2,3,2,1,2,2,1,2,2,3,1,3,3,2,3,3,2,1,3,2,1,2,5,2,3,5,3,2,2,3,1,1,4,2,5,4,2,2,4,19] ##run1
##MIE
#L = 320
#listOfModules = [20,60,80,100,160]
#listOfDemands = [12,7,9,45,52]

#L = 1500
#listOfModules = [1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 100, 125, 200, 250, 500, 1000]
#listOfDemands = [158,240,7,56,78,65,30,15,550,664,768,255,11,1,1500,12]


n = len(listOfModules)


def calculate_solution_substitute_method(L, listOfModules, listOdDemands, n):
    """Per andare ad eseguire questa tipologia di algoritmo bisogna andare a 
    modificare il methodo resolve_primal(...) all'interno di 
    cuttingStock.py per abilitare la differente tipologia di diseguaglianze
    del problema."""

    ##Passo 0: inizializzazione
    B = cs.determineInitialPattern(L,listOfModules)

    ##Passo 1: soluzione del problema primale e duale
    D , Y , C= cs.resolve_primal(listOdDemands, B) ##Del duale prendo solamente gli scarti
    print(f"Y = {Y}")
    print(f"C = {C}")

    enteringPattern = cs.resolve_pricing(L, Y, listOfModules)
    exitPattern = cs.determineExitPattern(B, enteringPattern, n)
    print(f"Exit = {exitPattern}")
    positionExit1 = cs.determinePositionExit(exitPattern, C) 
    print(f"Position Exit = {positionExit1}")
    
    B = cs.changeBase(B,positionExit1, enteringPattern)

    while(True):
        try:
            ##Passo 2: Iterazione
            D, Y , C= cs.resolve_primal(listOdDemands, B)
            print(f"Y = {Y}")
            print(f"C = {C}")
            enteringPattern = cs.resolve_pricing(L, Y, listOfModules) ##Ricavo il pattern entrante

            if(len(enteringPattern) == 0):
                print("\n\nTrovata la soluzione ottima!\n")
                print(f"Valore soluzione corrente: {p.value(D.objective)}")
                print(f"Valore della soluzione con round-up: {cs.roundUpSolution(p.value(D.objective))}")
                break
            exitPattern = cs.determineExitPattern(B, enteringPattern, n)
            print(f"Exit = {exitPattern}")
            positionExit2 = cs.determinePositionExit(exitPattern, C) 
            print(f"Position Exit 2 = {positionExit2}")

            if positionExit1 == positionExit2:
                print(f"Valore soluzione corrente: {p.value(D.objective)}")
                print(f"Valore della soluzione con round-up: {cs.roundUpSolution(p.value(D.objective))}")
                break

            B = cs.changeBase(B,positionExit2, enteringPattern)

        except np.linalg.LinAlgError as err:
            if 'Singular matrix' in str(err):
                print("\n\nE' stata ricavata la seguente soluzione:\n")
                print(f"Valore soluzione corrente: {p.value(D.objective)}")
                print(f"Valore della soluzione con round-up: {cs.roundUpSolution(p.value(D.objective))}")
                break
            else:
                print(err)
                break

def calculate_solution_add_method(L, listOfModules, listOdDemands, n):

    print(f"Lunghezza lista dei moduli: {len(listOfModules)}")
    print(f"Lunghezza lista della domanda: {len(listOdDemands)}")

    counter = 0
    ##Passo 0: inizializzazione
    B = cs.determineInitialPattern(L,listOfModules)

    ##Passo 1: soluzione del problema primale e duale
    D , Y , C= cs.resolve_primal(listOdDemands, B) ##Del duale prendo solamente gli scarti

    enteringPattern = cs.resolve_pricing(L, Y, listOfModules)
    B = cs.updateBase(B, enteringPattern)

    while(True):
        try:
            ### Counter per il numero di iterazioni
            ### Nel caso in cui non venga ricavata una
            ### soluzione migliore di quella ottenuta.
            counter += 1
            if counter == 10:
                print(f"Valore soluzione corrente: {p.value(D.objective)}")
                print(f"Valore della soluzione con round-up: {cs.roundUpSolution(p.value(D.objective))}")
                break
            #####################
            ##Passo 2: Iterazione
            D, Y , C = cs.resolve_primal(listOdDemands, B)
            print(f"Y = {Y}")
            print(f"C = {C}")
            enteringPattern = cs.resolve_pricing(L, Y, listOfModules) ##Ricavo il pattern entrante
            if(len(enteringPattern) == 0): ##Controllo se ho ottenuto la soluzione ottima.
                print("\n\nTrovata la soluzione ottima!\n")
                print(f"Valore soluzione corrente: {p.value(D.objective)}")
                print(f"Valore della soluzione con round-up: {cs.roundUpSolution(p.value(D.objective))}")
                break
            B = cs.updateBase(B, enteringPattern) ##Aggiorno la matrice aggiungendo il nuovo pattern

        except np.linalg.LinAlgError as err:
            if 'Singular matrix' in str(err):
                print("\n\nE' stata ricavata la seguente soluzione:\n")
                print(f"Valore soluzione corrente: {p.value(D.objective)}")
                print(f"Valore della soluzione con round-up: {cs.roundUpSolution(p.value(D.objective))}")
                break
            else:
                print(err)
                break


#calculate_solution_substitute_method(L, listOfModules, listOdDemands, n)
calculate_solution_add_method(L, listOfModules, listOfDemands, n)