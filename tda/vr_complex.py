from itertools import combinations, product
import networkx as nx


class VietorisRipsComplex(object):
    """

    Representation of the Vietoris-Rips complex.

    References:
    -----------
    https://en.wikipedia.org/wiki/Vietoris%E2%80%93Rips_complex

    """

    def __init__(self, points, epsilon, metric):
        """

        Parameters:
        ----------
        points: list
            A list of `Point` objects.
        epsilon: float
            A positive real number.
        metric: callable
            A function that calculates distance between `Point` objects.

        """

        if epsilon <= 0:
            raise ValueError('Epsilon has to be greater than 0.')

        if not points:
            raise ValueError('List of points cannot be empty.')

        self.points = points
        self.epsilon = epsilon
        self.metric = metric
        self.n_points = len(points)

        self.graph = None
        self.n_edges = None
        self.faces = None
        self.simplices = None

    def create_graph(self):
        """

        Create a graph from points.

        """

        self.graph = nx.Graph()
        self._add_vertices()
        self._add_edges()

    def _add_vertices(self):
        """

        Add vertices to the graph.

        """

        self.graph.add_nodes_from(self.points)

    def _add_edges(self):
        """

        Add edges to the graph

        """

        self.n_edges = 0
        for p1, p2 in product(self.points, self.points):
            if p1 != p2 and self.metric(p1, p2) < self.epsilon:
                self.graph.add_edge(p1, p2)
                self.n_edges += 1

    def _remove_edges(self):
        """

        Remove edges from graph.

        """

        for p1, p2 in product(self.points, self.points):
            if p1 != p2:
                try:
                    self.graph.remove_edge(p1, p2)
                except nx.exception.NetworkXError:
                    pass

    def find_simplices(self):
        """

        Find simplices in graph.

        Notes:
        ------
        This function will not list simplices that are contained in other
        simplices.

        References:
        -----------
        https://en.wikipedia.org/wiki/Clique_(graph_theory)
        https://en.wikipedia.org/wiki/Simplex

        """

        simplices = tuple(nx.find_cliques(self.graph))
        simplices = list(map(lambda s: tuple(s), simplices))
        self.simplices = simplices
        return tuple(simplices)

    def find_faces(self):
        """

        Find faces.

        """

        faces = set()
        for s in self.simplices:
            n_edges = len(s)
            for face_dim in range(n_edges, 0, -1):
                for f in combinations(s, face_dim):
                    faces.add(f)
        self.faces = tuple(faces)
        return self.faces

    def find_faces_with_dim(self, dim):
        """

        Find faces of a given dimension.

        Parameters:
        -----------
        dim : int
            A non-negative integer.

        """

        if dim < 0:
            raise ValueError('A non-negative dimension was expected.')

        self.faces = self.find_faces()
        return tuple(filter(lambda f: len(f) == dim + 1, self.faces))

    def change_epsilon(self, epsilon):
        """

        Change epsilon.

        Parameters:
        -----------
        epsilon: float
            A positive float.

        """

        if epsilon <= 0:
            raise ValueError('Epsilon has to be greater than 0.')

        self.simplices = None
        self.epsilon = epsilon
        self._remove_edges()
        self._add_edges()

    @property
    def complex_dimension(self):
        """

        Calculate the dimension of the complex.

        """

        max_dim = 0
        for s in self.simplices:
            max_dim = max(max_dim, len(s) - 1)
        return max_dim

    @property
    def zeroth_betti_number_graph(self):
        """

        Calculate the zeroth Betti number of the graph.

        References:
        -----------
        https://en.wikipedia.org/wiki/Betti_number

        """

        return nx.number_connected_components(self.graph)

    @property
    def first_betti_number_graph(self):
        """

        Calculate the first Betti number of the graph.

        References:
        -----------
        https://en.wikipedia.org/wiki/Betti_number

        """

        return self.zeroth_betti_number_graph + self.n_edges - self.n_points

    @property
    def betti_number_complex(self):
        raise NotImplementedError()

    @property
    def cyclomatic_number(self):
        raise NotImplementedError()
