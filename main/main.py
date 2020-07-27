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
L = 110
listOfModules = [70,40,55,25,35]
listOdDemands = [205,2321,143,1089,117]
#L = 20
#listOfModules = [9,8,7,6]
#listOdDemands = [511,301,263,383]
#L = 10000
#listOfModules = [4990,4919,4640,4300,4283,4225,4108,4097,4071,3971,3898,3875,3853,3833,3747,3701,3660,3388,3019,2927,2832,2823,2696,2408,1585,1546,1222,1194,1096,1049,958,876,865,835,676,636,613,583,527,515,506,484,478,425,294,186,64]
#listOdDemands = [2,3,2,3,2,3,4,2,4,2,1,5,1,1,2,2,2,1,1,2,1,2,1,2,1,2,3,1,3,1,1,1,1,2,2,1,3,3,2,3,1,5,1,1,1,5,1] ##run1
#listOdDemands = [200,300,200,300,200,300,400,200,400,200,100,500,100,100,200,200,200,100,100,200,100,200,100,200,100,200,300,100,300,100,100,100,100,200,200,100,300,300,200,300,100,500,100,100,100,500,100] ##run2
#L = 10000
#listOfModules = [4964,4950,4826,4816,4808,4682,4663,4631,4451,4387,4233,4127,3992,3968,3858,3698,3672,3565,3387,3336,3309,3118,3078,2988,2870,2862,2847,2735,2716,2652,2631,2553,2496,2406,2125,2017,1939,1848,1832,1672,1624,1593,1436,1225,1212,1060,943,763,733,583,476,462,278,246,80,74,40]
#listOdDemands = [3,1,1,1,1,1,4,1,1,2,1,1,2,1,1,2,4,1,3,3,1,3,4,1,1,2,2,2,3,1,3,2,3,1,2,1,3,4,1,2,1,1,4,2,3,4,2,1,4,1,1,2,3,1,3,2,2]
#L = 10000
#listOfModules = [4990,4919,4640,4300,4283,4225,4108,4097,4071,3971,3898,3875,3853,3833,3747,3701,3660,3388,3019,2927,2832,2823,2696,2408,1585,1546,1222,1194,1096,1049,958,876,865,835,676,636,613,583,527,515,506,484,478,425,294,186,64]
#listOdDemands = [2,3,2,3,2,3,4,2,4,2,1,5,1,1,2,2,2,1,1,2,1,2,1,2,1,2,3,1,3,1,1,1,1,2,2,1,3,3,2,3,1,5,1,1,1,5,1]

##MIE
#L = 320
#listOfModules = [20,60,80,100,160]
#listOdDemands = [12,7,9,45,52]

#L = 1500
#listOfModules = [1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 100, 125, 200, 250, 500, 1000]
#listOdDemands = [158,240,7,56,78,65,30,15,550,664,768,255,11,1,1500,12]


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
calculate_solution_add_method(L, listOfModules, listOdDemands, n)