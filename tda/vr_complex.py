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

    @property
    def boundary_operator_matrix(self, n, assign = False):
        """
        
        Calculate matrix of a n-th boundary operator.

        Parameters:
        -----------
        n : int
            A non-negative integer.
        assign : bool (default False)
            If True method also outputs dictionaries of assignments of row and column to simplices.

        Output:
        -------
        boundary_operator_matrix : list
            Matrix of a n-th boundary operator.
        matrix_rows_dict: dict
            Dictionary of rows of the matrix.
        matrix_columns_dict: dict
            Dictionary of columns of the matrix.

        Notes:
        ------
        The operation of chain group is addition with Z_2 coefficients.

        """

        if n < 0:
            raise ValueError('"n" has to be a non-negative integer.')
        elif assign is not bool:
            raise ValueError('assign is not a bool.')

        higher_dim_simplicies = self.find_faces_with_dim(n+1)
        lower_dim_simplicies = self.find_faces_with_dim(n)

        boundary_operator_matrix = []
        boundary_operator_dict = {}
        existing_lower_dim_simplicies_list = []
        for higher_dim_simplex in higher_dim_simplicies:
            copied_lower_dim_simplicies_list = []
            temporary_lower_dim_simplicies_list = []

            for i in len(higher_dim_simplex):
                copied_simplex = higher_dim_simplex.copy()
                copied_simplex.pop(i)
                copied_lower_dim_simplicies_list.append(copied_simplex)

            for lower_dim_simplex in lower_dim_simplicies:
                if lower_dim_simplex in copied_lower_dim_simplicies_list:
                    temporary_lower_dim_simplicies_list.append(lower_dim_simplex)
                    if lower_dim_simplex not in existing_lower_dim_simplicies_list:
                        existing_lower_dim_simplicies_list.append(lower_dim_simplex)
            
            boundary_operator_dict[higher_dim_simplex] = temporary_lower_dim_simplicies_list

        matrix_rows_dict = {}
        reversed_matrix_rows_dict = {}
        row_index = 0
        for lower_dim_simplex in existing_lower_dim_simplicies_list:
            boundary_operator_matrix.append([])
            matrix_rows_dict[row_index] = lower_dim_simplex
            reversed_matrix_rows_dict[lower_dim_simplex] = row_index
            row_index += 1 

        matrix_columns_dict = {}
        column_index = 0
        for higher_dim_simplex in higher_dim_simplicies:
            for row in boundary_operator_matrix:
                row.append(0)

            list_of_faces = boundary_operator_dict[higher_dim_simplex]
            for face in list_of_faces:
                row_index = reversed_matrix_rows_dict[face]
                boundary_operator_matrix[row_index][column_index] = 1

            matrix_rows_dict[column_index] = higher_dim_simplex
            column_index += 1

        if assign == False:
            return boundary_operator_matrix
        else:
            return boundary_operator_matrix, matrix_rows_dict, matrix_columns_dict

    @property
    def betti_numbers(self, n = None):
        """
        
        Calculate Betti numbers of the Vietoris-Rips complex.

        Parameters:
        -----------
        n : int (default None)
            A non-negative integer.

        Outputs:
        --------
        betti_numbers : list
            List of Betti numbers of a complex.
        betti_number : int 
            n-th Betti number.

        Notes:
        ------
        The operation of chain group is addition with Z_2 coefficients.

        References:
        -----------
        https://en.wikipedia.org/wiki/Betti_number
        https://youtu.be/gVq_xXnwV-4

        """

        raise NotImplementedError()