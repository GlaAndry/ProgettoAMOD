##main.py
##Mazzola Alessio 0279323

#Import
import pulp as p

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

cuttingAndDemand = {"l_i": 2 , "d_i": 5} ##Dizionario contenente il modulo di taglio l_i e la sua domanda d_i 
             ##la lunghezza L ed il numero di pezzi da produrre R (cioè la domanda)

L = 10


def resolve_pricing(L, listObjectiveFunction, listInequity):
    ##Questo metodo va a risolvere il sottoproblema di knapsack 
    ##derivante dal CSP rilassato, andando a restituire la modalità
    ##di taglio che deve entrare in base.
    ##Un pattern entra in base solamente se il valore della sua
    ##funzione obiettivo e > 1.

    #L --> int: Lunghezza del Roll
    #listObjectiveFunction: --> list: [valori della funzione obiettivo]
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


print('Primo problema \n\n')
print(resolve_pricing(20, [1/2, 1/2, 3/8, 1/4], [9,8,7,6]))

print('\n\nSecondo problema\n\n')
print(resolve_pricing(20, [1/2, 1/2, 1/3, 1/3], [9,8,7,6]))