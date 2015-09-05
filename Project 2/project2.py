"""
implement bfs_visited, which gives the set of nodes visited by bfs
on an undirected graph starting from a specified node.

The check for whether a node has already been visited might affect
the complexity of the problem. If its O(1), its all good. Otherwise,
that complexity will be a multiple of that. i.e if its O(logn), then
time complexity of bfs will be O(nlogn).
"""

from collections import deque
#import unittest

# class TestAlg(unittest.TestCase):

    # def test_1(self):
        # EX_GRAPH2 = {
             # 0: set([1]),
             # 1: set([2, 0, 3]),
             # 2: set([3, 1]),
             # 3: set([1, 2, 4, 5]),
             # 4: set([3]),
             # 5: set([3]),
             # 6: set([7, 8]),
             # 7: set([8, 6]),
             # 8: set([6, 7]),
             # 9: set([])
        # }
        # self.assertEqual(set(range(6)), bfs_visited(EX_GRAPH2, 0))
        # self.assertEqual(set([9]), bfs_visited(EX_GRAPH2, 9))
        # self.assertEqual(set(range(6,9)), bfs_visited(EX_GRAPH2, 8))
        # self.assertEqual(largest_cc_size(EX_GRAPH2), 6)
        # self.assertEqual(compute_resilience(EX_GRAPH2, range(10)),
                         # [6, 5, 4, 3, 3, 3, 3, 2, 1, 1, 0])


def bfs_visited(ugraph, start_node):
    """compute set of all node visited by bfs traversal of graph"""
    neighbors = deque([start_node])
    visited = set()

    while neighbors:
        node = neighbors.popleft()
        visited.add(node)
        for item in ugraph[node]:
            if item not in visited:
                neighbors.append(item)

    return visited


def cc_visited(ugraph):
    """compute connected components of graph"""
    connected_components = []
    allnodes = set(ugraph.keys())

    while allnodes:
        node = allnodes.pop()
        visited = bfs_visited(ugraph, node)
        allnodes -= visited
        connected_components.append(visited)

    return connected_components


def largest_cc_size(ugraph):
    """compute the size of the largest connected component"""

    connected_components = cc_visited(ugraph)
    if connected_components:
        return max(list(map(len, connected_components)))
    else:
        return 0


def compute_resilience(ugraph, attack_order):
    """compute the resilience of the graph given attack order"""
    resilience = [largest_cc_size(ugraph)]

    for node in attack_order:
        remove_node(ugraph, node)
        resilience.append(largest_cc_size(ugraph))

    return resilience


def remove_node(ugraph, node):
    """remove node from graph"""

    neighbors = ugraph[node]
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    del ugraph[node]


# if __name__ == "__main__":
    # unittest.main()