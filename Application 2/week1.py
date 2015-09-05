"""
Algorithmic Thinking - Week 1 - Assignment
"""

EX_GRAPH0 = {
    0: set([1, 2]),
    1: set([]),
    2: set([])
}

EX_GRAPH1 = {
    0: set([1, 4, 5]),
    1: set([2, 6]),
    2: set([3]),
    3: set([0]),
    4: set([1]),
    5: set([2]),
    6: set([])
}

EX_GRAPH2 = {
    0: set([1, 4, 5]),
    1: set([2, 6]),
    2: set([3, 7]),
    3: set([7]),
    4: set([1]),
    5: set([2]),
    6: set([]),
    7: set([3]),
    8: set([1, 2]),
    9: set([0, 3, 4, 5, 6, 7])
}


def make_complete_graph(num_nodes):
    """Returns a complete directed graph with the given number of nodes.

    >>> make_complete_graph(1)
    {0: set([])}

    >>> make_complete_graph(2)
    {0: set([1]), 1: set([0])}

    >>> make_complete_graph(4)
    {0: set([1, 2, 3]), 1: set([0, 2, 3]), 2: set([0, 1, 3]), 3: set([0, 1, 2])}

    >>> make_complete_graph(0)
    {}

    >>> make_complete_graph(-1)
    {}
    """
    return dict((i, set(range(num_nodes)) - set([i]))
                for i in range(num_nodes))


def out_edges(digraph):
    """Returns a flattened list of out-edges for the given graph.

    >>> out_edges(EX_GRAPH0)
    [1, 2]
    """
    return [subitems for items in digraph.values() for subitems in items]


def compute_in_degrees(digraph):
    """Computes the in-degrees for the nodes in the given graph.

    >>> compute_in_degrees(EX_GRAPH0)
    {0: 0, 1: 1, 2: 1}

    >>> compute_in_degrees(EX_GRAPH1)
    {0: 1, 1: 2, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1}

    >>> compute_in_degrees(EX_GRAPH2)
    {0: 1, 1: 3, 2: 3, 3: 3, 4: 2, 5: 2, 6: 2, 7: 3, 8: 0, 9: 0}
    """
    return dict({(node, out_edges(digraph).count(node)) for node in
                 digraph.keys()})


def in_degree_distribution(digraph):
    """Computes the in-degree distribution for the given graph.

    >>> in_degree_distribution(EX_GRAPH0)
    {0: 1, 1: 2}

    >>> in_degree_distribution(EX_GRAPH1)
    {1: 5, 2: 2}

    >>> in_degree_distribution(EX_GRAPH2)
    {0: 2, 1: 1, 2: 3, 3: 4}
    """
    in_degrees = compute_in_degrees(digraph).values()
    return dict((in_degree, in_degrees.count(in_degree))
                for in_degree in in_degrees)