# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 07:28:07 2021

@author: ppznp1
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 17:11:28 2021

@author: ppznp1
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 01:54:57 2021

@author: ppznp1
"""

import networkx as nx
#from matplotlib import pyplot as plt


import cirq
import numpy as np
import math
from matplotlib import pyplot as plt
import random
from scipy.optimize import minimize





"""
class Graph:
    def __init__(self, edges_set):
        self.edges_set = edges_set
        self.node_set = []
        for i in edges_set:
            if (i.start_node not in self.node_set):
                self.node_set.append(i.start_node)
            if (i.end_node not in self.node_set):
                self.node_set.append(i.end_node)
"""
class Edge:
    def __init__(self, start_node, end_node, weight):
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight

set_edges = [Edge(0, 1,10), Edge(1, 2,1), Edge(2,3,10), Edge(3,4,5), Edge(4,5,30),Edge(5,6,20),Edge(6,7,5)];
#set_edges = [Edge(0, 1,10), Edge(1, 2,1), Edge(2,3,10)];



num = 8;
depth = 8
rep = 1000
qubits = [cirq.GridQubit(0, i) for i in range(0, num)]

G = nx.Graph()

for z in set_edges:
    G.add_edge(str(z.start_node), str(z.end_node))



nx.draw(G)
plt.savefig('graph.png')
plt.clf()


def initialization(qubits):
    for i in qubits:
        yield cirq.H.on(i)
        
def cost_unitary(qubits, gamma):
    for i in set_edges:
        yield cirq.ZZPowGate(exponent=-1*gamma/math.pi).on(qubits[i.start_node], qubits[i.end_node])
        
def mixer_unitary(qubits, alpha):
    for i in range(0, len(qubits)):
        yield cirq.XPowGate(exponent=-1*alpha/math.pi).on(qubits[i])


"""
init =[float(random.randint(-314, 314))/float(100) for i in range(0, 8)]
params=init;
gamma = [params[0], params[2], params[4], params[6]];
alpha = [params[1], params[3], params[5], params[7]]


#res=cost_unitary(qubits,gamma)

circuit = cirq.Circuit()
circuit.append(initialization(qubits))
for i in range(0, depth):
    circuit.append(cost_unitary(qubits, gamma[i]))
    circuit.append(mixer_unitary(qubits, alpha[i]))
    
circuit.append(cirq.measure(*qubits, key='x'))
print(circuit)

simulator = cirq.Simulator()
results = simulator.run(circuit, repetitions=rep)
#print("Results:")
#print(results)



results = str(results)[2:].split(", ")


new_res = []
for i in range(0, rep):
    hold = []
    for j in range(0, num):
        hold.append(int(results[j][i]))
    new_res.append(hold)


total_cost = 0
for i in range(0, len(new_res)):
    for j in set_edges:
        total_cost += 0.5*j.weight*( ( (1 - 2*new_res[i][j.start_node]) * (1 - 2*new_res[i][j.end_node]) ) - 1)
total_cost = float(total_cost)/rep

print("Cost: "+str(total_cost))
"""

    

# Executes the circuit

def create_circuit(params):

    #gamma = [params[0], params[2], params[4], params[6]]
    #alpha = [params[1], params[3], params[5], params[7]]
    #gamma = [params[0]];
    #alpha = [params[1]];
    
#    gamma = [] 
#    alpha = [] 
#    for i in range(0, len(params)): 
#        if i % 2: 
#            gamma.append(params[i]) 
#        else :
#            alpha.append(params[i]) 
    
#    gamma = params[0:len(params)/2]
#    alpha = params[len(params)/2+1:len(params)]
    
    gamma,alpha=np.array_split(params,2)
    
    circuit = cirq.Circuit()
    circuit.append(initialization(qubits))
    for i in range(0, depth):
        circuit.append(cost_unitary(qubits, gamma[i]))
        circuit.append(mixer_unitary(qubits, alpha[i]))
    circuit.append(cirq.measure(*qubits, key='x'))
    print(circuit)

    simulator = cirq.Simulator()
    results = simulator.run(circuit, repetitions=rep)
    results = str(results)[2:].split(", ")
    new_res = []
    for i in range(0, rep):
        hold = []
        for j in range(0, num):
            hold.append(int(results[j][i]))
        new_res.append(hold)

    return new_res

def cost_function(params):

    av = create_circuit(params)
    total_cost = 0
    for i in range(0, len(av)):
        for j in set_edges:
            total_cost += 0.5*j.weight*( ( (1 - 2*av[i][j.start_node]) * (1 - 2*av[i][j.end_node]) ) - 1)
    total_cost = float(total_cost)/rep

    print("Cost: "+str(total_cost))

    return total_cost

# Defines the optimization method

#init =[float(random.randint(-314, 314))/float(100) for i in range(0, 2*depth)]
step_size   = 0.05;

a_gamma         = np.arange(0, np.pi, step_size)
a_beta          = np.arange(0, np.pi, step_size)
a_gamma, a_beta = np.meshgrid(a_gamma,a_beta)

F1 = 3-(np.sin(2*a_beta)**2*np.sin(2*a_gamma)**2-0.5*np.sin(4*a_beta)*np.sin(4*a_gamma))*(1+np.cos(4*a_gamma)**2)

# Grid search for the minimizing variables
result = np.where(F1 == np.amax(F1))
a      = list(zip(result[0],result[1]))[0]

calcgamma  = a[0]*step_size;
calcbeta   = a[1]*step_size;
#
#init = [calcgamma,calcbeta]
#reqalpha=[0]*depth;
#reqgamma=[0]*depth;
#reqalpha[0]=calcbeta
#reqgamma[0]=calcbeta
#
#for i in range(0,depth):
#    reqalpha[i+1] = ((i-1)/depth)*reqalpha[i-1]+((depth-i+1)/depth)*reqalpha[i]
#    reqgamma[i+1] = ((i-1)/depth)*reqgamma[i-1]+((depth-i+1)/depth)*reqgamma[i]

reqalpha = np.linspace(calcbeta,((depth+1)/depth)*calcbeta,depth)
reqgamma = np.linspace(calcgamma,((depth+1)/depth)*calcgamma,depth)

init=np.concatenate((reqalpha,reqgamma))



out = minimize(cost_function, x0=init, method="COBYLA", options={'maxiter':100})
print(out)

optimal_params = out['x']
f = create_circuit(optimal_params)

# Creates visualization of the optimal state

nums = []
freq = []

for i in range(0, len(f)):
    number = 0
    for j in range(0, len(f[i])):
        number += 2**(len(f[i])-j-1)*f[i][j]
    if (number in nums):
        freq[nums.index(number)] = freq[nums.index(number)] + 1
    else:
        nums.append(number)
        freq.append(1)

freq = [s/sum(freq) for s in freq]

print(nums)
print(freq)

x = range(0, 2**num)
y = []
for i in range(0, len(x)):
    if (i in nums):
        y.append(freq[nums.index(i)])
    else:
        y.append(0)

plt.bar(x, y)
plt.show()



