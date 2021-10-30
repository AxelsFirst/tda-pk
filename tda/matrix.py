from copy import copy, deepcopy


class Matrix(object):
    """

    Representation of matrices.

    """

    def __new__(cls, entries):
        """

        Check whether entries can create a matrix.

        Parameters:
        -----------
        entries: list
            Two dimensional list of entries.

        Notes:
        ------
        Entries have to be integers.

        """

        desired_length = len(entries[0])
        for row in entries:
            if desired_length != len(row):
                raise ValueError(
                    'Each row has to have exact amount of entries!')

        return super(Matrix, cls).__new__(cls, entries)

    def __init__(self, entries):
        """

        Parameters:
        -----------
        entries: list
            Two dimensional list of entries.

        Notes:
        ------
        Entries have to be integers.

        """

        self.entries = entries
        self.num_rows = len(entries)
        self.num_cols = len(entries[0])

    def get_row(self, row_index):
        """

        Get a row from matrix.

        Parameters:
        -----------
        row_index: int
            Index of a row.

        Output:
        -------
        row: list
            A row.

        """

        return self.entries[row_index]

    def get_col(self, col_index):
        """

        Get a column from matrix.

        Parameters:
        -----------
        col_index: int
            Index of a column.

        Output:
        -------
        col: list
            A column.

        """

        col = []
        for row in self.entries:
            col.append(row[col_index])
        return col

    def change_row(self, row_index, values):
        """

        Return a matrix with changed values of row.

        Parameters:
        -----------
        matrix: list
            A matrix.
        row_index: int
            Index of a row.
        values: list
            A list with desired values of row.

        Output:
        -------
        matrix: list
            A matrix with changed rows.

        """

        self.entries[row_index] = values
        return self.entries

    def change_col(self, col_index, values):
        """

        Return a matrix with changed values of column.

        Parameters:
        -----------
        col_index: int
            Index of a column.
        values: list
            A list with desired values of column.

        Output:
        -------
        entries: list
            A entries of a matrix with changed values.

        """

        for row_index in range(self.num_rows):
            self.entries[row_index][col_index] = values[col_index]
        return self.entries

    def add_rows(self, index_row_to_change, index_row_to_add):
        """

        Add one row to another.

        Parameters:
        -----------
        index_row_to_change: int
            Index of changed row.
        index_row_to_add: int
            Index of added row to another.

        Notes:
        ------
        The method uses modulo 2 addition of entries.

        """

        row_to_change = self.get_row(index_row_to_change)
        row_to_add = self.get_row(index_row_to_add)
        summed_row = []
        for i in self.num_cols:
            summed_entries = (row_to_change(i) + row_to_add(i)) % 2
            summed_row.append(summed_entries)
        self.change_row(summed_row)

    def add_cols(self, index_col_to_change, index_col_to_add):
        """

        Add one col to another.

        Parameters:
        -----------
        index_col_to_change: int
            Index of changed col.
        index_col_to_add: int
            Index of added col to another.

        Notes:
        ------
        The method uses modulo 2 addition of entries.

        """

        col_to_change = self.get_col(index_col_to_change)
        col_to_add = self.get_col(index_col_to_add)
        summed_col = []
        for i in self.num_rows:
            summed_entries = (col_to_change(i) + col_to_add(i)) % 2
            summed_col.append(summed_entries)
        self.change_row(summed_col)

    def make_non_zero_diagonal_entry(self, entry_index):
        """

        Arranges rows and cols so that specified entry on diagonal is non zero.

        Parameters:
        -----------
        entry_index: int
            Index of a row (and column) that contains the entry.

        Output:
        -------
        value_check: bool
            Boolean that tells whether the entry is not zero.

        Notes:
        ------
        It will move rows, if non zero entry is below the desired place.
        It will move columns, if non zero entry is right of the desired place.

        """

        for row_index in range(entry_index, self.num_rows):
            if self.entries[row_index][entry_index] != 0:
                if row_index != entry_index:
                    copied_row = copy(self.get_row(row_index))
                    copied_entry_row = copy(self.get_row(entry_index))
                    self.change_row(entry_index, copied_row)
                    self.change_row(row_index, copied_entry_row)
                return True

        for col_index in range(entry_index, self.num_cols):
            if self.entries[entry_index][col_index] != 0:
                if col_index != entry_index:
                    copied_col = copy(self.get_col(col_index))
                    copied_entry_col = copy(self.get_col(entry_index))
                    self.change_col(entry_index, copied_col)
                    self.change_col(col_index, copied_entry_col)
                return True

        return False

    def smith_normal_form(self):
        """

        Calculate Smith normal form of a matrix.

        Output:
        -------
        snf: matrix
            Smith normal form of a matrix.

        Notes:
        ------
        The method uses modulo 2 addition.
        Entries of the matrix have to be 0 or 1.

        """

        snf = deepcopy(self)
        max_dim = min(snf.num_rows, snf.num_cols)

        for current_dim in range(max_dim):
            value_check = snf.make_non_zero_diagonal_entry(current_dim)

            if value_check is True:
                for row_index in range(current_dim+1, snf.num_rows):
                    if snf.entries[row_index][current_dim] == 1:
                        snf.add_rows(row_index, current_dim)

                for col_index in range(current_dim+1, snf.num_cols):
                    if snf.entries[current_dim][col_index] == 1:
                        snf.add_cols(col_index, current_dim)

        return snf

    def smith_normal_form_rank(self):
        """

        Calculate rank of Smith normal form of a matrix.

        Output:
        -------
        snf_rank: int
            Rank of Smith normal form of a matrix.

        Notes:
        ------
        The method uses modulo 2 addition.
        Entries of the matrix have to be 0 or 1.

        """

        snf = self.smith_normal_form_rank()
        max_dim = min(snf.num_rows, snf.num_cols)

        snf_rank = 0
        for i in range(max_dim):
            if snf.entries[i][i] == 1:
                snf_rank += 1

        return snf_rank
