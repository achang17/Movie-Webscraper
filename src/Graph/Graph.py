from src.Graph import Node
from src.Graph import Edge

from src.Scraper.Scraper import read_from_json

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, group, name, edges, year):
        node = Node(group, name, edges, year)
        self.nodes.append(node)

    def add_edge(self, actor, movie, weight):
        edge = Edge(actor, movie, weight)
        self.edges.append(edge)

    def data_to_graph(self, data):
        for d in data:
            if (data[d]['json_class'] == 'Movie'):
                group = "Movie"
                name = data[d]['name']
                box_office = data[d]['box_office'] if data[d]['box_office'] is not None else 1000000
                edges = self.get_movie_edges(name, data[d]['actors'], box_office)
                year = data[d]['year']
                node = Node(group, name, edges, year)
                #self.nodes[name] = node
                self.nodes.append(node)

            else:
                group = "Actor"
                name = data[d]['name']
                edges = self.get_actor_edges(name, self.edges)
                year = 2013
                node = Node(group, name, edges, year)
                self.nodes.append(node)

    def get_list_of_movies_from_actor(self, actor):
        movies = []
        for edge in self.edges:
            if edge.actor == actor:
                movies.append(edge.movie)

        return movies

    def get_movie_gross(self, movie):
        total_gross = 0

        for edge in self.edges:
            if edge.movie == movie:
                total_gross += edge.weight

        return total_gross

    def get_list_of_actors_from_movie(self, movie):
        actors = []
        for edge in self.edges:
            if edge.movie == movie:
                actors.append(edge.actor)
        return actors

    def weight_sum_helper(self, n):
        sum = 0
        for i in range(n+1):
            sum += i
        return sum

    def get_actor_edges(self, actor, graph_edges):
        actor_edges = []

        for edge in graph_edges:
            if edge.actor == actor:
                actor_edges.append(edge)

        return actor_edges

    def get_movie_edges(self, movie, neighbors, box_office):
        edges = []
        n = len(neighbors)
        weight = self.weight_sum_helper(n)

        for actor in neighbors:
            edge = Edge.Edge(actor, movie, n*int(box_office/weight))
            print(edge.actor)
            print(edge.movie)
            print(edge.weight)
            n -= 1
            edges.append(edge)

        return edges

if __name__ == "__main__":
    graph = Graph()
    data = read_from_json('../data_small.json')

    for d in data:
        if data[d]['json_class'] == 'Movie':
            group = "Movie"
            name = data[d]['name']
            box_office = data[d]['box_office'] if data[d]['box_office'] is not None else 1000000
            edges = graph.get_movie_edges(name, data[d]['actors'], box_office)
            print(edges)
            year = data[d]['year']
            node = Node.Node(group, name, edges, year)
            print(node.group)
            print(node.name)
            print(node.year)
            # self.nodes[name] = node
            graph.nodes.append(node)
            graph.edges += edges
            print(graph.nodes)

        else:
            group = "Actor"
            name = data[d]['name']
            edges = graph.get_actor_edges(name, graph.edges)
            print(edges)
            year = 2013
            node = Node.Node(group, name, edges, year)
            graph.nodes.append(node)
            print(graph.nodes)
            # self.nodes[name] = node
            # print(data[d]['movies'])

    query = graph.get_list_of_movies_from_actor("Tom Holland")
    print("query")
    print(query)

