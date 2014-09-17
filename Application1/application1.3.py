"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2
#import simpleplot
import math
import pylab
import matplotlib.pyplot as plt
import random

# Plot options
STANDARD = True
LOGLOG = True

NUM_NODES = 28000
NUM_INIT = 100
p = 0.5

def make_complete_graph(num_nodes):
    """
    This is a docstring for a function:
    
    make a complete graph
    """
    if num_nodes <= 0:
        return {}
    res = {}
    for node in range (num_nodes):
        keys = range (0, num_nodes)
        keys.remove (node)
        res[node] = set (keys)
    return res
    
"""
Provided code for application portion of module 1

Helper class for implementing efficient version
of DPA algorithm
"""
class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors


        
def load_graph(num_nodes):
    """
    Load DPA graph
    Returns a dictionary that models a graph
    """
    dpa = DPATrial (NUM_INIT)        
    cur_num_nodes = NUM_INIT
    res = {}
    
    res = make_complete_graph (NUM_INIT)
    
    for node in range (NUM_INIT, NUM_NODES):
        keys = dpa.run_trial (cur_num_nodes)
        res [node] = keys
        cur_num_nodes += 1
    return res

def compute_in_degrees(digraph):
    """
    This is a docstring for a function:
    
    compute in - degree for all nodes of a directed graph
    """
    res = {}
    for key in digraph.keys ():
        res [key] = 0
    cnt = 0
    for key in digraph.keys ():
        cnt += 1
        print 'cnt: ' + str (cnt)
        nodes = digraph [key]
        for node in nodes:
            if node in res.keys ():
                res [node] += 1
            else:
                res [node] = 1
    print 'Finish calcualting in degree'    
    return res
    
def in_degree_distribution(digraph):
    """
    This is a docstring for a function:
    
    compute in - degree distribution of a directed graph
    """
    in_degrees = compute_in_degrees (digraph)
    res = {}
    cnt = 0
    for key in in_degrees.keys ():
        cnt += 1
        print 'dist: ' + str (cnt)
        in_degree = in_degrees [key]
        if in_degree in res.keys ():
            res [in_degree] += 1
        else:
            res [in_degree] = 1
    sum = 352807
    for key in res.keys ():
        res [key] = float (res[key]) / sum
    print 'finish distribution'
    return res

citation_graph = load_graph(NUM_NODES)

print len (citation_graph.keys ())

#in_degrees = compute_in_degrees (citation_graph)

dist = in_degree_distribution (citation_graph)

###############################################
# plottting code
plot_type = STANDARD
plot_size = 40

# Pass name of mystery function in as a parameter
# simpleplot.plot_bars ('Citation distribution', 400, 300, 'Cited','Distribution', dist)

plt.bar(range(len(dist)), dist.values(), align='center', log=True)
plt.xticks(range(len(dist)), dist.keys())

plt.show()




