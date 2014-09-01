"""
This is a docstring for the module:

Assignment 1 for Algorithmic Thinking course
"""

EX_GRAPH0 = {0:set([1,2]),1:set(),2:set()}
EX_GRAPH1 = {0:set([1,4,5]),
            1: set ([2, 6]),
            2: set ([3]),
            3: set ([0]),
            4: set ([1]),
            5: set ([2]),
            6: set ()}
EX_GRAPH2 = {0: set ([1, 4, 5]),
            1: set ([2, 6]),
            2: set ([3, 7]),
            3: set ([7]),
            4: set ([1]),
            5: set ([2]),
            6: set (),
            7: set ([3]),
            8: set ([1, 2]),
            9: set ([0, 4, 5, 6, 7, 3])
            }

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
    
def compute_in_degrees(digraph):
    """
    This is a docstring for a function:
    
    compute in - degree for all nodes of a directed graph
    """
    res = {}
    for key in digraph.keys ():
        res [key] = 0
    for key in digraph.keys ():
        nodes = digraph [key]
        for node in nodes:
            if node in res.keys ():
                res [node] += 1
            else:
                res [node] = 1
    return res  

def in_degree_distribution(digraph):
    """
    This is a docstring for a function:
    
    compute in - degree distribution of a directed graph
    """
    in_degrees = compute_in_degrees (digraph)
    res = {}
    for key in in_degrees.keys ():
        in_degree = in_degrees [key]
        if in_degree in res.keys ():
            res [in_degree] += 1
        else:
            res [in_degree] = 1
    return res
    
    