from src.Graph.Graph import Graph

import unittest

from src.Graph.Edge import Edge
from src.Graph.Node import Node


class TestGraph(unittest.TestCase):
    #def add_node(self, group, edges, year):
    #     def __init__(self, group, name, edges, year):
    #         def __init__(self, actor, movie, weight):

    def test_add_node_to_graph(self):
        graph = Graph()

        graph.add_node("Actor", "Ann Hathaway", [], 2019)
        self.assertEqual(len(graph.nodes), 1)
        self.assertEqual(graph.nodes[0].group, "Actor")
        self.assertEqual(graph.nodes[0].name, "Ann Hathaway")
        self.assertEqual(graph.nodes[0].year, 2019)

    def test_add_node_to_graph(self):
        graph = Graph()

        graph.add_node("Movie", "Princess Diaries", [], 2019)
        self.assertEqual(len(graph.nodes), 1)
        self.assertEqual(graph.nodes[0].group, "Movie")
        self.assertEqual(graph.nodes[0].name, "Princess Diaries")
        self.assertEqual(graph.nodes[0].year, 2019)

    def test_weight_sum_helper(self):
        graph = Graph()
        n = graph.weight_sum_helper(10)
        self.assertEqual(n, 55)


    def test_add_edge_to_graph(self):
        graph = Graph()

        graph.add_edge("Ann Hathaway", "Princess Diaries", 100)
        self.assertEqual(len(graph.edges), 1)
        self.assertEqual(graph.edges[0].movie, "Princess Diaries")
        self.assertEqual(graph.edges[0].actor, "Ann Hathaway")
        self.assertEqual(graph.edges[0].weight, 100)

    def test_query_1(self):
        graph = Graph()

        edges = []
        edge = graph.add_edge("Ann Hathaway", "Princess Diaries", 100)
        edges.append(edge)
        graph.add_node("Movie", "Princess Diaries", edges, 2019)

        self.assertEqual(len(graph.edges), 1)
        self.assertEqual(len(graph.nodes[0].edges), 1)
        self.assertEqual(graph.get_list_of_movies_from_actor("Ann Hathaway")[0], "Princess Diaries")

    def test_query_2(self):
        graph = Graph()

        edges = []
        edge = graph.add_edge("Ann Hathaway", "Princess Diaries", 100)
        edges.append(edge)
        graph.add_node("Movie", "Princess Diaries", edges, 2019)

        self.assertEqual(len(graph.edges), 1)
        self.assertEqual(graph.edges[0].weight, 100)
        self.assertEqual(graph.get_movie_gross("Princess Diaries"), 100)


    def test_query_3(self):
        graph = Graph()

        edges = []
        edge = graph.add_edge("Ann Hathaway", "Princess Diaries", 100)
        edges.append(edge)
        graph.add_node("Movie", "Princess Diaries", edges, 2019)

        self.assertEqual(len(graph.get_list_of_movies_from_actor("Ann Hathaway")), 1)
        self.assertEqual(graph.get_list_of_movies_from_actor("Ann Hathaway")[0], "Princess Diaries")