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


##Specifica del problema:


##MIE
L = 10000
listOfModules = [1,2,4,8,16,50,100,200,400,500,1000,2000,2500,5000,10000]
#listOfDemands = [12,45,55,33,125,1,15,78,41,45,22,41,56,23,84]
listOfDemands = [1200, 4500, 5500, 3300, 12500, 100, 1500, 7800, 4100, 4500, 2200, 4100, 5600, 2300, 8400]

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

            if(len(enteringPattern) == 0): ##Controllo se ho ottenuto la soluzione ottima.
                print("\n\nTrovata la soluzione ottima!\n")
                print(f"Valore soluzione corrente: {p.value(D.objective)}")
                print(f"Valore della soluzione con round-up: {cs.roundUpSolution(p.value(D.objective))}")
                break
            else:
                ### Counter per il numero di iterazioni
                ### Nel caso in cui non venga ricavata una
                ### soluzione migliore di quella ottenuta.
                counter += 1
                if counter == 15:
                    print(f"Valore soluzione corrente: {p.value(D.objective)}")
                    print(f"Valore della soluzione con round-up: {cs.roundUpSolution(p.value(D.objective))}")
                    break
                #####################
                ##Passo 2: Iterazione
                D, Y , C = cs.resolve_primal(listOdDemands, B)
                print(f"Y = {Y}")
                print(f"C = {C}")
                enteringPattern = cs.resolve_pricing(L, Y, listOfModules) ##Ricavo il pattern entrante
                
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


def mul100(list1):
    ret = []
    for x in list1:
        ret.append(x*100)
    print(ret)


#calculate_solution_substitute_method(L, listOfModules, listOdDemands, n)
calculate_solution_add_method(L, listOfModules, listOfDemands, n)
#mul100([12,45,55,33,125,1,15,78,41,45,22,41,56,23,84])
