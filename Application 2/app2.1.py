"""
Algorithmic Thinking - Application 1
"""

from collections import deque, defaultdict
import itertools
import random
import urllib2
import time


def bfs_visited(ugraph, start_node):
    """
    Returns a set with all nodes visited by a breadth-first search that starts
    at the given start node.
    """
    if start_node not in ugraph:
        raise ValueError("invalid start node")

    queue = deque([start_node])
    visited = deque([start_node])
    while len(queue) > 0:
        for neighbor in ugraph[queue.popleft()]:
            if neighbor in visited:
                continue
            visited.append(neighbor)
            queue.append(neighbor)
    return set(visited)


def cc_visited(ugraph):
    """
    Returns a list of sets representing the connected components of the given
    undirected graph.
    """
    remaining_nodes = set(ugraph.keys())
    components = []
    while len(remaining_nodes) > 0:
        visited = bfs_visited(ugraph, remaining_nodes.pop())
        remaining_nodes = remaining_nodes - visited
        components.append(visited)
    return components


def largest_cc_size(ugraph):
    """
    Returns the size of the largest connected component in the given undirected
    graph.
    """
    if len(ugraph) == 0:
        return 0
    return max([len(component) for component in cc_visited(ugraph)])


def compute_resilience(ugraph, attack_order):
    """
    Returns a list whose k + 1th entry is the size of the largest connected
    component in the given graph after the removal of the first k elements in
    the given attack order.
    """
    graph = copy_graph(ugraph)
    attack_order = list(attack_order)
    resilience = [largest_cc_size(graph)]
    while len(attack_order) > 0:
        removed_node = attack_order.pop(0)
        graph.pop(removed_node)
        for node in graph:
            graph[node] = graph[node] - set([removed_node])
        resilience.append(largest_cc_size(graph))
    return resilience


class UPATrial:

    """
    Simple class to encapsulate optimizated trials for the UPA algorithm

    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities

    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a
        complete graph with num_nodes nodes

        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes)
                              for dummy_idx in range(num_nodes)]

    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers

        Updates the list of node numbers so that each node number
        appears in correct ratio

        Returns:
        Set of nodes
        """

        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))

        # update the list of node numbers so that each node number
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))

        # update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph

    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[: -1]

    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1: -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph


def generate_random_ugraph(num_nodes, probability):
    """
    Generates a random undirected graph with the given number of nodes.
    """
    graph = {node: set([]) for node in range(num_nodes)}
    for i, j in itertools.permutations(range(num_nodes), 2):
        if i == j or random.random() > probability:
            continue
        graph[i].update([j])
        graph[j].update([i])
    return graph


def calculate_p(num_nodes, num_edges):
    """
    Calculates the probability p to be used when generating a random undirected
    graph in order to get a graph with the given number of nodes and
    approximately the given number of edges.
    """
    return num_edges / float(num_nodes * (num_nodes - 1))


def random_order(graph):
    """
    Returns the list of nodes in the given graph in random order.
    """
    nodes = graph.keys()
    random.shuffle(nodes)
    return nodes


def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph


def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree. (provided code)

    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)

    order = []
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node

        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order


def fast_targeted_order(ugraph):
    """
    Computes a targeted attack order consisting of nodes of maximal degree (own
    implementation).
    """
    graph = copy_graph(ugraph)
    degree_sets = defaultdict(set)
    for node in graph:
        degree_sets[len(graph[node])].update([node])

    attack_order = []
    for k in reversed(range(len(graph))):
        while len(degree_sets[k]) > 0:
            u = degree_sets[k].pop()
            for v in graph[u]:
                d = len(graph[v])
                degree_sets[d].remove(v)
                degree_sets[d - 1].update([v])
            attack_order.append(u)
            for node in graph.pop(u):
                if u in graph[node]:
                    graph[node].remove(u)

    return attack_order


def upa(arg_n, arg_m):
    """
    Generates a graph according to the UPA algorithm.
    """
    graph = generate_random_ugraph(arg_m, 1)
    upa_trial = UPATrial(arg_m)
    for i in range(arg_m, arg_n):
        graph[i] = set(upa_trial.run_trial(arg_m))
        for neighbor in graph[i]:
            graph[neighbor].update([i])
    return graph


def compare_resiliences(attack_order, title):
    """
    Compares the resilience of three differente graphs (complete random, UPA
    and provided computer network graph) to a given attack model.
    """
    from application1 import flatten_edges
    import matplotlib.pyplot as plt

    NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"

    network_graph = load_graph(NETWORK_URL)
    num_nodes = len(network_graph)
    num_edges = len(flatten_edges(network_graph)) / 2.0

    p = calculate_p(num_nodes, num_edges)
    random_graph = generate_random_ugraph(num_nodes, p)

    m = int(num_edges / num_nodes)
    upa_graph = upa(num_nodes, m)

    print 'network graph:', num_nodes, 'nodes and', num_edges * 2, 'edges'
    print 'random graph:', len(random_graph), 'nodes and', len(flatten_edges(random_graph)), 'edges'
    print 'upa graph:', len(upa_graph), 'nodes and', len(flatten_edges(upa_graph)), 'edges'

    plt.plot(range(num_nodes + 1),
             compute_resilience(random_graph, attack_order(random_graph)),
             '-b',
             label='random graph (p = %f)' % p)

    plt.plot(range(num_nodes + 1),
             compute_resilience(upa_graph, attack_order(upa_graph)),
             '-r',
             label='upa graph (m = %d)' % m)

    plt.plot(range(num_nodes + 1),
             compute_resilience(network_graph, attack_order(network_graph)),
             '-g',
             label='network graph')

    plt.title(title)
    plt.xlabel('nodes removed')
    plt.ylabel('largest connected component')
    plt.legend()
    plt.show()


def answer_q1():
    """
    Answers Q1.
    """
    compare_resiliences(random_order, 'Resilience under random attack')


def answer_q3():
    """
    Answers Q3.
    """
    import matplotlib.pyplot as plt

    graphs = []
    m = 5
    for n in range(10, 1000, 10):
        graphs.append(upa(n, m))

    normal_running_times = []
    fast_running_times = []
    for graph in graphs:
        start = time.time()
        targeted_order(graph)
        normal_running_times.append(time.time() - start)

        start = time.time()
        fast_targeted_order(graph)
        fast_running_times.append(time.time() - start)

    plt.plot(range(10, 1000, 10),
             normal_running_times,
             '-r',
             label='targeted_order')

    plt.plot(range(10, 1000, 10),
             fast_running_times,
             '-g',
             label='fast_targeted_order')

    plt.title('Targeted order algorithms comparison (desktop Python)')
    plt.xlabel('input size (number of nodes)')
    plt.ylabel('time (seconds)')
    plt.legend()
    plt.show()


def answer_q4():
    """
    Answers Q4.
    """
    compare_resiliences(fast_targeted_order, 'Resilience under ordered attack')

if __name__ == '__main__':
    #answer_q1()
    #answer_q3()
    answer_q4()