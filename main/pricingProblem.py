##cuttingStock.py
##Mazzola Alessio 0279323

#Import
import pulp as p

##variabili del problema
#L --> Lunghezza del Roll
#l_i --> moduli di taglio
#d_i --> domanda per il singolo modulo


objects = {} ##Dizionario degli oggetti, contiene l'oggetto stesso, 
             ##la lunghezza L ed il numero di pezzi da produrre d (cioè la domanda)
cuttingPattern = [] ##Lista di pattern di taglio per ottenere oggetti 
                    ##dall'insieme di una lunghezza l_i



  
# Create a LP Minimization problem 
Lp_prob = p.LpProblem('Pricing Problem - Knapsack from youtube', p.LpMaximize)  
  
# Create problem Variables  
a = p.LpVariable("a", lowBound = 0, cat='Integer')   # Create a variable a >= 0 
b = p.LpVariable("b", lowBound = 0, cat='Integer')   # Create a variable b >= 0 
c = p.LpVariable("c", lowBound = 0, cat='Integer')   # Create a variable c >= 0 
d = p.LpVariable("d", lowBound = 0, cat='Integer')   # Create a variable d >= 0 


  
# Objective Function 
Lp_prob += (1/2) * a + (1/2) * b + (1/2) * c + (1/3) * d    
  
# Constraints: 
Lp_prob += 9 * a + 8 * b + 7 * c + 6 * d <= 20
  
# Display the problem 
print(Lp_prob) 
  
status = Lp_prob.solve()   # Solver 
print(p.LpStatus[status])   # The solution status 
  
# Printing the final solution 
print(p.value(a), p.value(b), p.value(c), p.value(d), p.value(Lp_prob.objective))  