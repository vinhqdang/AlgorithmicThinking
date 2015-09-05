"""
Algorithmic Thinking - Application 1
"""

import itertools
import random
import urllib2
from collections import defaultdict
import matplotlib.pyplot as plt
from week1 import make_complete_graph

CITATION_URL = \
    "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"


class DPATrial(object):

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
        self._node_numbers = [node for node in range(num_nodes)
                              for dummy_idx in range(num_nodes)]

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


def flatten_edges(graph):
    """
    Returns a flat list with all the edges in the given graph
    """
    return [subitems for items in graph.values() for subitems in items]


def count_occurrences(items):
    """
    Counts how many times an item is present in a list (faster than list.count)
    """
    occurrences = defaultdict(int)
    for item in items:
        occurrences[item] += 1
    return occurrences


def normalize_distribution(distribution, total_occurrences):
    """
    Normalizes a distribution
    """
    return {count: distribution[count] / float(total_occurrences)
            for count in distribution.keys()}


def save_distribution(graph, filename):
    """
    Saves the in-degree distribution for a given graph as a JPG image
    """
    citations = count_occurrences(flatten_edges(graph))
    distribution = count_occurrences(citations.values())
    normalized = normalize_distribution(distribution, len(graph.keys()))

    plt.title('In-degree distribution')
    plt.xlabel('in-degree')
    plt.ylabel('probability')
    plt.loglog(
        normalized.keys(),
        normalized.values(),
        marker='o',
        linestyle='')
    plt.savefig(filename)


def generate_random_graph(num_nodes, probability):
    """
    Generates a random graph with a given number of nodes
    """
    graph = {node: [] for node in range(num_nodes)}
    for i, j in itertools.permutations(range(num_nodes), 2):
        if i == j or random.random() > probability:
            continue
        graph[i].append(j)
    return graph


def dpa(arg_n, arg_m):
    """
    Generates a graph according to the DPA algorithm (own implementation)
    """
    graph = make_complete_graph(arg_m)
    in_degrees = count_occurrences(flatten_edges(graph))
    total_in_degrees = sum(in_degrees.keys())
    for i in range(arg_m, arg_n):
        out_edges = []
        while len(out_edges) < arg_m:
            random_node = graph.keys()[random.randint(0, len(graph) - 1)]
            probability = (in_degrees[random_node] + 1) / \
                float(total_in_degrees + len(graph))
            if random.random() > probability:
                out_edges.append(random_node)

        graph[i] = set(out_edges)
        total_in_degrees += len(graph[i])
        for j in graph[i]:
            in_degrees[j] += 1
    return graph


def dpa2(arg_n, arg_m):
    """
    Generates a graph according to the DPA algorithm (using provided code for
    running DPA trials)
    """
    graph = make_complete_graph(arg_m)
    dpa_trial = DPATrial(arg_m)
    for i in range(arg_m, arg_n):
        graph[i] = dpa_trial.run_trial(arg_m)
    return graph


def answer_q1():
    """
    Answers Q1
    """
    save_distribution(load_graph(CITATION_URL), 'q1.jpg')


def answer_q2():
    """
    Answers Q2
    """
    graph = generate_random_graph(10000, 0.4)
    save_distribution(graph, 'q2.jpg')


def answer_q3():
    """
    Answers Q3
    """
    citation_graph = load_graph(CITATION_URL)
    avg_degree = len(flatten_edges(citation_graph)) / len(citation_graph)
    dpa_graph = dpa2(len(citation_graph), avg_degree)
    save_distribution(dpa_graph, 'q3.jpg')

if __name__ == '__main__':
    # answer_q1()
    # answer_q2()
    answer_q3()