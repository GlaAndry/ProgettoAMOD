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
#L = 10000
#listOfModules = [1,2,4,8,16,50,100,200,400,500,1000,2000,2500,5000,8710]
#listOfDemands = [12,45,55,33,125,1,15,78,41,45,22,41,56,23,84]
#listOfDemands = [1200, 4500, 5500, 3300, 12500, 100, 1500, 7800, 4100, 4500, 2200, 4100, 5600, 2300, 8400]

#L = 110
#listOfModules = [70,40,55,25,35]
#listOfDemands = [205,2321,143,1089,117]
#listOfDemands = [20500, 232100, 14300, 108900, 11700]

#L = 1500
#listOfModules = [1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 100, 125, 200, 250, 500, 1000]
#listOfDemands = [158,240,7,56,78,65,30,15,550,664,768,255,11,1,1500,12]


#L = 10000
#listOfModules = [4990,4919,4640,4300,4283,4225,4108,4097,4071,3971,3898,3875,3853,3833,3747,3701,3660,3388,3019,2927,2832,2823,2696,2408,1585,1546,1222,1194,1096,1049,958,876,865,835,676,636,613,583,527,515,506,484,478,425,294,186,64]
#listOfDemands = [2,3,2,3,2,3,4,2,4,2,1,5,1,1,2,2,2,1,1,2,1,2,1,2,1,2,3,1,3,1,1,1,1,2,2,1,3,3,2,3,1,5,1,1,1,5,1] ##run1

L = 20
listOfModules = [9,8,7,6]
listOfDemands = [511,301,263,383] ##run1


n = len(listOfModules)


def calculate_solution_add_method_checkPrimal(L, listOfModules, listOdDemands, n):

    print(f"Lunghezza lista dei moduli: {len(listOfModules)}")
    print(f"Lunghezza lista della domanda: {len(listOdDemands)}")

    ##Passo 0: inizializzazione
    B = cs.determineInitialPattern(L,listOfModules)

    ##Passo 1: soluzione del problema primale e duale
    D , Y , C, opt= cs.resolve_primal(listOdDemands, B) ##Del duale prendo solamente gli scarti

    enteringPattern, dualObj = cs.resolve_pricing(L, Y, listOfModules)
    B = cs.updateBase(B, enteringPattern)

    while(True):
        try:
            if opt == 1:
                err_abs = cs.roundUpSolution(C)-p.value(D.objective)
                err_apx = (cs.roundUpSolution(C)-p.value(D.objective))/cs.roundUpSolution(C)
                print("\n\nTrovata la soluzione:\n")
                print(f"Valore soluzione corrente: {p.value(D.objective)}")
                print(f"Valore della soluzione con round-up: {cs.roundUpSolution(C)}")
                print(f"Valore dell'errore Assoluto: {err_abs}")
                print(f"Valore dell'errore Relativo: {err_apx}")
                return dualObj , err_abs, err_apx
            else:
                #####################
                ##Passo 2: Iterazione
                D, Y , C = cs.resolve_primal(listOdDemands, B)
                print(f"Y = {Y}")
                print(f"C = {C}")
                enteringPattern, dualObj = cs.resolve_pricing(L, Y, listOfModules) ##Ricavo il pattern entrante
                
                B = cs.updateBase(B, enteringPattern) ##Aggiorno la matrice aggiungendo il nuovo pattern

        except np.linalg.LinAlgError as err:
            if 'Singular matrix' in str(err):
                print("L'istanza non è corretta.")
                break
            else:
                print(err)
                break


def calculate_solution_add_method_checkDual(L, listOfModules, listOdDemands, n):

    print(f"Lunghezza lista dei moduli: {len(listOfModules)}")
    print(f"Lunghezza lista della domanda: {len(listOdDemands)}")

    counter = 0
    ##Passo 0: inizializzazione
    B = cs.determineInitialPattern(L,listOfModules)

    ##Passo 1: soluzione del problema primale e duale
    D , Y , C, opt= cs.resolve_primal(listOdDemands, B) ##Del duale prendo solamente gli scarti
    ## D rappresenta il problema primale che stiamo risolvendo e viene utilizzato nel calcolo della soluzione.
    ##Opt : intero che rappresenta se il problema primale è ottimo o meno.
    print(f"Y = {Y}") ##Valori del problema DUALE utilizzati all'interno del problema del pricing problem per ricavare il nuovo pattern di taglio, se esiste.
    print(f"C = {C}") ##Valori del problema PRIMALE 

    enteringPattern, dualObj = cs.resolve_pricing(L, Y, listOfModules)
    B = cs.updateBase(B, enteringPattern)

    while(True):
        try:
            if(len(enteringPattern) == 0): ##Controllo se ho ottenuto la soluzione ottima.
                err_abs = cs.roundUpSolution(C)-p.value(D.objective)
                err_apx = (cs.roundUpSolution(C)-p.value(D.objective))/cs.roundUpSolution(C)

                print("\n\nTrovata la soluzione ottima!\n")
                print(f"Valore soluzione corrente: {p.value(D.objective)}")
                print(f"Valore della soluzione con round-up: {cs.roundUpSolution(C)}")
                print(f"Valore dell'errore Assoluto: {err_abs}")
                print(f"Valore dell'errore Relativo: {err_apx}")
                return dualObj , err_abs, err_apx
            else:
                ### Counter per il numero di iterazioni
                ### Nel caso in cui non venga ricavata una
                ### soluzione migliore di quella ottenuta.
                counter += 1
                if counter == 10:
                    print(f"Valore soluzione corrente: {p.value(D.objective)}")
                    print(f"Valore della soluzione con round-up: {cs.roundUpSolution(C)}")
                    return dualObj, 0, 0
                #####################
                ##Passo 2: Iterazione
                D, Y , C, opt = cs.resolve_primal(listOdDemands, B)
                print(f"Y = {Y}")
                print(f"C = {C}")
                enteringPattern, dualObj = cs.resolve_pricing(L, Y, listOfModules) ##Ricavo il pattern entrante
                
                B = cs.updateBase(B, enteringPattern) ##Aggiorno la matrice aggiungendo il nuovo pattern ricavato dal problema di pricing

        except np.linalg.LinAlgError as err:
            if 'Singular matrix' in str(err):
                print("L'istanza non è corretta.")
                break
            else:
                print(err)
                break







def mul100(list1):
    ret = []
    for x in list1:
        ret.append(x*100)
    print(ret)


obj = calculate_solution_add_method_checkDual(L, listOfModules, listOfDemands, n)
#print(obj)
#mul100([12,45,55,33,125,1,15,78,41,45,22,41,56,23,84])
