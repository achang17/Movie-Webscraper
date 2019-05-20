class Node:

    '''
    type holds a string (either "ACTOR" or "MOVIE")
    edges holds a list of edges that are connected to this node
    neighbors holds a list of neighboring nodes
    '''
    def __init__(self, group, name, edges, year):
        self.group = group
        self.name = name
        self.edges = edges
        self.year = year
