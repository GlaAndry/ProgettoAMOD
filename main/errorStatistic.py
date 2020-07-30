"""Questo modulo python è adibito al calcolo delle diverse statistiche
come il tempo medio di completamento e l'allontanamento medio dalla 
soluzione ottima delle diverse istanze dei problemi.
"""

import main as m

##def varibili
dualVal = 0
err_abs = 0
err_apx = 0


if __name__ == "__main__":
    # write data in a file. 
    file = open("stat/errorAllInstances.csv","a")  ##a necessario altrimenti si ha l'overwrite degli elementi già scritti.
    file.write("assoluto, relativo \n")

    L = 20
    listOfModules = [9,8,7,6]
    listOfDemands = [511,301,263,383] ##run1
    n = len(listOfModules)
    dualVal, err_abs, err_apx = m.calculate_solution_add_method(L, listOfModules, listOfDemands, n)
    file.write("%s,%s \n" %(str(err_abs),str(err_apx)))
    L = 20
    listOfModules = [9,8,7,6]
    listOfDemands = [51100, 30100, 26300, 38300] ##run2
    n = len(listOfModules)
    dualVal, err_abs, err_apx = m.calculate_solution_add_method(L, listOfModules, listOfDemands, n)
    file.write("%s,%s \n" %(str(err_abs),str(err_apx)))
    L = 110
    listOfModules = [70,40,55,25,35]
    listOfDemands = [20500, 232100, 14300, 108900, 11700]
    n = len(listOfModules)
    dualVal, err_abs, err_apx = m.calculate_solution_add_method(L, listOfModules, listOfDemands, n)
    file.write("%s,%s \n" %(str(err_abs),str(err_apx)))
    L = 320
    listOfModules = [20,60,80,100,160]
    listOfDemands = [12,7,9,45,52]
    n = len(listOfModules)
    dualVal, err_abs, err_apx = m.calculate_solution_add_method(L, listOfModules, listOfDemands, n)
    file.write("%s,%s \n" %(str(err_abs),str(err_apx)))
    L = 320
    listOfModules = [20,60,80,100,160]
    listOfDemands = [1200, 700, 900, 4500, 5200]
    n = len(listOfModules)
    dualVal, err_abs, err_apx = m.calculate_solution_add_method(L, listOfModules, listOfDemands, n)
    file.write("%s,%s \n" %(str(err_abs),str(err_apx)))
    L = 1500
    listOfModules = [25,50,75,100,300]
    listOfDemands = [12,7,9,45,52]
    n = len(listOfModules)
    dualVal, err_abs, err_apx = m.calculate_solution_add_method(L, listOfModules, listOfDemands, n)
    file.write("%s,%s \n" %(str(err_abs),str(err_apx)))
    L = 1500
    listOfModules = [25,50,75,100,300]
    listOfDemands = [1200, 700, 900, 4500, 5200]
    n = len(listOfModules)
    dualVal, err_abs, err_apx = m.calculate_solution_add_method(L, listOfModules, listOfDemands, n)
    file.write("%s,%s \n" %(str(err_abs),str(err_apx)))
    L = 1500
    listOfModules = [25,50,75,100,300, 500, 750, 1500]
    listOfDemands = [12,7,9,45,52,98,66,22,75]
    n = len(listOfModules)
    dualVal, err_abs, err_apx = m.calculate_solution_add_method(L, listOfModules, listOfDemands, n)
    file.write("%s,%s \n" %(str(err_abs),str(err_apx)))
    L = 1500
    listOfModules = [25,50,75,100,300, 500, 750, 1500]
    listOfDemands = [1200, 700, 900, 4500, 5200, 9800, 6600, 2200, 7500]
    n = len(listOfModules)
    dualVal, err_abs, err_apx = m.calculate_solution_add_method(L, listOfModules, listOfDemands, n)
    file.write("%s,%s \n" %(str(err_abs),str(err_apx)))
    L = 10000
    listOfModules = [1,2,4,8,16,50,100,200,400,500,1000,2000,2500,5000,10000]
    listOfDemands = [12,45,55,33,125,1,15,78,41,45,22,41,56,23,84]
    n = len(listOfModules)
    dualVal, err_abs, err_apx = m.calculate_solution_add_method(L, listOfModules, listOfDemands, n)
    file.write("%s,%s \n" %(str(err_abs),str(err_apx)))
    L = 10000
    listOfModules = [1,2,4,8,16,50,100,200,400,500,1000,2000,2500,5000,10000]
    listOfDemands = [1200, 4500, 5500, 3300, 12500, 100, 1500, 7800, 4100, 4500, 2200, 4100, 5600, 2300, 8400]
    n = len(listOfModules)
    dualVal, err_abs, err_apx = m.calculate_solution_add_method(L, listOfModules, listOfDemands, n)
    file.write("%s,%s \n" %(str(err_abs),str(err_apx)))
    file.close()