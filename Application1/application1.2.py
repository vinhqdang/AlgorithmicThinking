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

# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(30)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    num_nodes = 1000
    p = 0.5
    res = {}
    for node in range (num_nodes):
        keys = range (0, num_nodes)
        keys.remove (node)
        for key in keys:
            prob = random.uniform (0, 1)
            if (prob > p):
                keys.remove (key)
        res[node] = set (keys)
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

citation_graph = load_graph(CITATION_URL)

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




