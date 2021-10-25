from itertools import combinations, product
import networkx as nx
from copy import copy


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
        -----------
        points: list
            A list of `Point` objects.
        epsilon: float
            A positive real number.
        metric: callable
            A function that calculates distance between `Point` objects.

        """

        if epsilon < 0:
            raise ValueError('Epsilon has to be greater than 0.')

        if len(points) < 1:
            raise ValueError('List of points cannot be empty')

        self.points = points
        self.epsilon = epsilon
        self.metric = metric
        self.n_points = len(points)

        self.graph = None
        self.n_edges = None
        self.faces = None
        self.simplices = None
        self.max_dim = None

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

        Add edges to the graph.

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

        Output:
        -------
        simplices : tuple
            Tuple of maximal simplices in the complex.

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
        self.simplices = tuple(simplices)
        return self.simplices

    def find_faces(self):
        """

        Find faces.

        Output:
        -------
        faces : tuple
            Tuple of faces.

        References:
        -----------
        https://en.wikipedia.org/wiki/Clique_(graph_theory)
        https://en.wikipedia.org/wiki/Simplex

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

        Output:
        -------
        faces : tuple
            Tuple of faces of the given dimension.

        References:
        -----------
        https://en.wikipedia.org/wiki/Clique_(graph_theory)
        https://en.wikipedia.org/wiki/Simplex

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

        Calculate the dimension of the simplicial complex.

        Output:
        -------
        max_dim : int
            Dimension of the simplicial complex

        """

        self.max_dim = 0
        for s in self.simplices:
            self.max_dim = max(self.max_dim, len(s) - 1)
        return self.max_dim

    def check_nesting(self, higher_simplices, lower_simplices):
        """

        Find which simplices are nested in others.

        Parameters:
        -----------
        higher_simplices : tuple
            A tuple of simplices of higher dimension.
        lower_simplices : tuple
            A tuple of simplices of lower dimension.

        Output:
        -------
        nested_simplices : dict
            A dictionary of nested simplices.
        present_lower_simplices : list
            A list of simplices that are present as values in dictionary.

        Notes:
        ------
        Simplices have to be of one higher dimension that the others.

        """

        nested_simplices = {}
        present_lower_simplices = []
        for higher_simplex in higher_simplices:
            copied_lower_simplices = []
            temporary_lower_simplices = []

            for point_index in range(len(higher_simplex)):
                copied_simplex = list(copy(higher_simplex))
                copied_simplex.pop(point_index)
                copied_lower_simplices.append(tuple(copied_simplex))

            for lower_simplex in lower_simplices:
                if lower_simplex in copied_lower_simplices:
                    temporary_lower_simplices.append(lower_simplex)
                    if lower_simplex not in present_lower_simplices:
                        present_lower_simplices.append(lower_simplex)

            nested_simplices[higher_simplex] = temporary_lower_simplices

        return nested_simplices, present_lower_simplices

    def boundary_operator_matrix(self, n):
        """

        Calculate matrix of a n-th boundary operator.

        Parameters:
        -----------
        n : int
            A non-negative integer.

        Output:
        -------
        boundary_matrix : list
            Matrix of a n-th boundary operator.
        matrix_rows: dict
            Dictionary of rows of the matrix.
        matrix_cols: dict
            Dictionary of columns of the matrix.

        Notes:
        ------
        The operation of chain group is addition with Z_2 coefficients.

        """

        if n < 0:
            raise ValueError('"n" has to be a non-negative integer.')

        higher_simplices = self.find_faces_with_dim(n+1)
        lower_simplices = self.find_faces_with_dim(n)

        boundary_dict, present_lower_simplices = self.check_nesting(
            higher_simplices, lower_simplices)

        boundary_matrix = []
        matrix_rows = {}
        reversed_matrix_rows = {}
        row_index = 0
        for lower_simplex in present_lower_simplices:
            boundary_matrix.append([])
            matrix_rows[row_index] = lower_simplex
            reversed_matrix_rows[lower_simplex] = row_index
            row_index += 1

        matrix_cols = {}
        col_index = 0
        for higher_simplex in higher_simplices:
            for row in boundary_matrix:
                row.append(0)

            list_of_faces = boundary_dict[higher_simplex]
            for face in list_of_faces:
                row_index = reversed_matrix_rows[face]
                boundary_matrix[row_index][col_index] = 1

            matrix_cols[col_index] = higher_simplex
            col_index += 1

        return boundary_matrix, matrix_rows, matrix_cols

    def betti_numbers(self):
        """

        Calculate Betti numbers of the Vietoris-Rips complex.

        Outputs:
        --------
        betti_numbers : list
            List of Betti numbers of a complex.

        Notes:
        ------
        The operation of chain group is addition with Z_2 coefficients.

        References:
        -----------
        https://en.wikipedia.org/wiki/Betti_number
        https://youtu.be/gVq_xXnwV-4

        """

        raise NotImplementedError()

    def nth_betti_number(self, n):
        """

        Calculate n-th Betti number of the Vietoris-Rips complex.

        Outputs:
        --------
        nth-betti_number : int
            N-th Betti number of a complex.

        Notes:
        ------
        The operation of chain group is addition with Z_2 coefficients.

        References:
        -----------
        https://en.wikipedia.org/wiki/Betti_number
        https://youtu.be/gVq_xXnwV-4

        """

        raise NotImplementedError()
