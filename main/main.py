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
    rilassato.
    4) Determinare nuovamente la soluzione del problmea con le nuove modalità di taglio aggiunte.
    5) Se il problema duale non presenta delle modalità di taglio migliori, allora STOP """

cuttingAndDemand = {"l_i": 2 , "d_i": 5} ##Dizionario contenente il modulo di taglio l_i e la sua domanda d_i 
             ##la lunghezza L ed il numero di pezzi da produrre R (cioè la domanda)

L = 10



  
# Create a LP Minimization problem 
Lp_prob = p.LpProblem('CPS Continuo', p.LpMinimize)  
  
# Create problem Variables  
x = p.LpVariable("x", lowBound = 0, cat='Integer')   # Create a variable x >= 0 
#y = p.LpVariable("y", lowBound = 0)   # Create a variable y >= 0 
  
# Objective Function 
Lp_prob += x   
  
# Constraints: 
Lp_prob += 2 * x >= cuttingAndDemand.get('d_i')
  
# Display the problem 
print(Lp_prob) 

print(cuttingAndDemand.get('d_i'))
  
status = Lp_prob.solve()   # Solver 
print(p.LpStatus[status])   # The solution status 
  
# Printing the final solution 
print(p.value(x),p.value(Lp_prob.objective))   