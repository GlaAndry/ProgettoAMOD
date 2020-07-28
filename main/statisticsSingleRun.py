"""Questo modulo python è adibito al calcolo delle diverse statistiche
come il tempo medio di completamento e l'allontanamento medio dalla 
soluzione ottima delle diverse istanze dei problemi.
"""

import main as m
import time ##import per la misura dei tempi di esecuzione.

L = 10000
listOfModules = [1,2,4,8,16,50,100,200,400,500,1000,2000,2500,5000,10000]
listOfDemands = [12,45,55,33,125,1,15,78,41,45,22,41,56,23,84]
#listOfDemands = [1200, 4500, 5500, 3300, 12500, 100, 1500, 7800, 4100, 4500, 2200, 4100, 5600, 2300, 8400]
n = len(listOfModules)


if __name__ == "__main__":
    start_time = time.time()
    m.calculate_solution_add_method(L, listOfModules, listOfDemands, n)
    print("--- %s seconds ---" % (time.time() - start_time))


