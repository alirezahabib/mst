import sys

from graphviz import Digraph
from graphviz import Graph as Graphviz

from src import edge
from src import vertex

DIRECTED = "DIRECTED"


def parse_graph(file):
    with open(file, 'r') as handle:
        start = int(handle.readline())
        matrix = [list(map(int, line.strip().split(' '))) for line in handle]

    n = len(matrix)
    #      starting vertex is invalid                input matrix is not square
    if start < 0 or start >= n or not all(len(row) == n for row in matrix):
        raise ValueError('Input file is broken.')

    g = Graph()

    for i in range(n):
        g.add_vertex(vertex.Vertex(i))

    print(f'Starting vertex is {start}')
    print(f'Input matrix: ')
    for i, row in enumerate(matrix):
        for j, weight in enumerate(row):
            print(weight, end=', ')
            g.add_edge(edge.Edge(i, j, {"WEIGHT": weight}))
        print()

    return start, g


class Graph:
    def __init__(self, vertices=None, edges=None, attr=None):
        """
            stores vertices and edges
            param vertices: Dictionary with vertices
            param edges:    Dictionary with edges
            param attr:     Properties of graph
        """
        if attr is None:
            attr = {}
        if vertices is None:
            vertices = {}
        self.vertices = vertices

        if edges is None:
            edges = {}
        self.edges = edges

        self.attr = attr

    def add_vertex(self, vertex):
        if vertex.id not in self.vertices.keys():
            self.vertices[vertex.id] = vertex

    def get_vertices(self):
        return self.vertices

    def add_edge(self, edge, directed=False, auto=False):
        """
            Add edge to source edges if there is no other edge with same source and target
            :param edge: edge to insert
            :param directed: enable graph directed
            :param auto: allow loops
        """
        (v1, v2) = edge.get_id()
        if v1 in self.vertices.keys() and v2 in self.vertices.keys():
            if directed:
                if auto:
                    self.edges[edge.get_id()] = edge
                else:
                    if v1 != v2:
                        self.edges[edge.get_id()] = edge
            else:
                if self.edges.get((v2, v1)) is None:
                    if auto:
                        self.edges[edge.get_id()] = edge
                    else:
                        if v1 != v2:
                            self.edges[edge.get_id()] = edge

    def get_edges(self):
        edges = []
        for (key, target) in self.edges.keys():
            edges.append((key, target))
        return edges

    def get_edge(self, id, directed=False):
        """
            Get edge by specific id
            param id: Tupla identifier of edge
            param directed: Filter to find edge directed
        """
        (u, v) = id
        for (source, target) in self.edges.keys():
            if directed:
                if (source, target) == (u, v):
                    return self.edges[(source, target)]
            else:
                if (source, target) == (u, v) or (source, target) == (v, u):
                    return self.edges[(source, target)]
        return None

    def get_adjacent_vertices_by_vertex(self, id, type=None):
        """
            Get adjacent vertex of specific vertex
            param id: Vertex identifier in the graph
            param type: Filter
                None - All adjacent vertices
                +    - Output adjacent vertices
                -    - Input adjacent vertices
        """
        vertex = []
        for (source, target) in self.edges.keys():
            if type is None:
                if source == id:
                    vertex.append(target)
                elif target == id:
                    vertex.append(source)
            elif type == '+':
                if source == id:
                    vertex.append(target)
            elif type == '-':
                if target == id:
                    vertex.append(source)

        return vertex

    def create_graphviz(self, attr_label_vertex=None, source=None,
                        attr_label_edge=None):
        dot = Graphviz()

        # Review attribute directed of graph
        if DIRECTED in self.attr:
            if self.attr[DIRECTED]:
                dot = Digraph()
            else:
                dot = Graphviz()
        if attr_label_vertex is None:
            # Map the graph to graphviz structure
            for n in list(self.vertices.keys()):
                dot.node(str(n), str(n))
        else:
            # Map the graph to graphviz structure and add vertex attribute
            for n in list(self.vertices.keys()):
                label = "Node: " + str(n)
                source_label = "Node source: " + str(
                    source) if source is not None else ""
                label = label + "\n" + source_label
                label = label + "\n" + attr_label_vertex + " (" + str(
                    self.vertices[n].attributes[attr_label_vertex]) + ")"
                dot.node(str(n), label)

        if attr_label_edge is None:
            for e in self.get_edges():
                (s, t) = e
                dot.edge(str(s), str(t))
        else:
            for e in self.get_edges():
                (s, t) = e
                label_edge = self.edges[(s, t)].attr["WEIGHT"]
                dot.edge(str(s), str(t), label=str(label_edge))

        return dot

    def find(self, parent, i):
        """
        find is a utility function to find set of an element i
        :param parent: parent node source
        :param i: node source
        """
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def kruskal(self):
        """
        a function based on Kruskal's algorithm to find a minimum spanning tree of an undirected edge-weighted graph.
        :return g graph representing minimum spanning tree
        """
        g = Graph(attr={DIRECTED: False})
        # Create set for each v of V[G]
        parent = []
        rank = []
        for v in self.get_vertices():
            parent.append(v)
            rank.append(0)

        # Sort edges by weight
        q = sorted(self.edges.items(), key=lambda x: x[1].attr["WEIGHT"])
        for e in q:
            (u, v) = e[0]
            v1 = self.find(parent, u)
            v2 = self.find(parent, v)
            if v1 != v2:
                g.add_vertex(vertex.Vertex(u))
                g.add_vertex(vertex.Vertex(v))
                g.add_edge(edge.Edge(u, v, {"WEIGHT": e[1].attr["WEIGHT"]}))
                if rank[v1] < rank[v2]:
                    parent[v1] = v2
                    rank[v2] += 1
                else:
                    parent[v2] = v1
                    rank[v1] += 1
        return g

    def prim(self, start):
        """
            Prim is a function based on Prim algorithm
            to find a minimum spanning tree of an undirected edge-weighted graph.
            :return g graph representing the minimum spanning tree
        """
        g = Graph(attr={DIRECTED: False})
        distance = [sys.maxsize] * len(self.vertices)
        parent = [None] * len(self.vertices)
        set = [False] * len(self.vertices)

        distance[start] = 0
        parent[start] = -1

        for _ in self.vertices:
            # Search vertex with minimum distance
            min_index = 0
            min_vert = sys.maxsize
            for v in self.vertices:
                if distance[v] < min_vert and set[v] is False:
                    min_vert = distance[v]
                    min_index = v
            u = min_index

            # Add u vertex in set to not use it in other iteration 
            set[u] = True
            g.add_vertex(vertex.Vertex(u))

            # Iterate all adjacent vertices of u vertex and update distance 
            for v in self.get_adjacent_vertices_by_vertex(u):
                if set[v] is False and distance[v] > \
                        self.get_edge((u, v)).attr["WEIGHT"]:
                    distance[v] = self.get_edge((u, v)).attr["WEIGHT"]
                    parent[v] = u

        for i in self.vertices:
            if i == start:
                continue
            if parent[i] is not None:
                g.add_edge(edge.Edge(parent[i], i, {"WEIGHT": self.get_edge((parent[i], i)).attr["WEIGHT"]}))

        return g
