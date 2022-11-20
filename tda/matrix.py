from copy import copy, deepcopy
from itertools import chain


class Matrix(object):
    """

    Representation of matrices.

    """

    def __init__(self, entries, int_check=True):
        """

        Parameters:
        -----------
        entries: list
            Two dimensional list of entries.
        int_check: bool
            Check if entries are integers.

        Notes:
        ------
        Entries have to be integers due to modulo 2 operations.

        """

        if int_check is True:
            for i in range(len(entries)):
                if type(entries[i]) is not int:
                    raise ValueError('Entries have to be integers')

        self.entries = entries
        self.num_rows = len(entries)
        self.num_cols = len(entries[0])

    def check_row_index(self, row_index):
        """

        Check if row_index has a correct value.

        Parameters:
        -----------
        row_index: int
            Index of a row.

        """

        if row_index < 0:
            raise ValueError('Row index cannot be negative.')
        elif row_index >= self.num_rows:
            raise ValueError('Row index out of range.')

    def check_col_index(self, col_index):
        """

        Check if row_index has a correct value.

        Parameters:
        -----------
        col_index: int
            Index of a col.

        """

        if col_index < 0:
            raise ValueError('Col index cannot be negative.')
        elif col_index >= self.num_cols:
            raise ValueError('Col index out of range.')

    def get_row(self, row_index, index_check=True):
        """

        Get a row from matrix.

        Parameters:
        -----------
        row_index: int
            Index of a row.
        index_check: bool
            If true then check if row_index is correct.

        Output:
        -------
        row: list
            A row.

        """

        if index_check is True:
            self.check_row_index(row_index)

        return self.entries[row_index]

    def get_col(self, col_index, index_check=True):
        """

        Get a column from matrix.

        Parameters:
        -----------
        col_index: int
            Index of a column.
        index_check: bool
            If true check if col_index is correct.

        Output:
        -------
        col: list
            A column.

        """

        if index_check is True:
            self.check_col_index(col_index)

        col = []
        for row in self.entries:
            col.append(row[col_index])
        return col

    def change_row(self, row_index, new_entries, index_check=True,
                   new_entries_check=True):
        """

        Return a matrix with changed values of row.

        Parameters:
        -----------
        row_index: int
            Index of a row.
        new_entries: list
            A list with desired values of row.
        index_check: bool
            If true then check if row_index is correct.
        new_entries_check: bool
            If true then check if length of new_entries is correct.

        Output:
        -------
        entries: list
            Entries of a matrix with changed values.

        """

        if index_check is True:
            self.check_row_index(row_index)

        if new_entries_check is True:
            if len(new_entries) is not len(self.entries):
                raise ValueError('Incorrect length of new_entries.')

        self.entries[row_index] = new_entries
        return self.entries

    def change_col(self, col_index, new_entries, index_check=True,
                   new_entries_check=True):
        """

        Return a matrix with changed values of column.

        Parameters:
        -----------
        col_index: int
            Index of a column.
        values: list
            A list with desired values of column.
        index_check: bool
            If true then check if col_index is correct.
        new_entries_check: bool
            If true then check if length of new_entries is correct.

        Output:
        -------
        entries: list
            Entries of a matrix with changed values.

        """

        if index_check is True:
            self.check_col_index(col_index)

        if new_entries_check is True:
            if len(new_entries) is not len(self.entries):
                raise ValueError('Incorrect length of new_entries.')

        for row_index in range(self.num_rows):
            self.entries[row_index][col_index] = new_entries[col_index]
        return self.entries

    def add_rows(self, row_target_index, row_add_index, index_check=True):
        """

        Add one row to another.

        Parameters:
        -----------
        row_target_index: int
            Index of changed row.
        row_add_index: int
            Index of added row to another.
        index_check: bool
            If true then check if row_target_index
            and row_add_index are correct.

        Notes:
        ------
        This method uses modulo 2 addition of entries.

        """

        if index_check is True:
            self.check_row_index(row_target_index)
            self.check_row_index(row_add_index)

        row_target = self.get_row(row_target_index)
        row_add = self.get_row(row_add_index)
        summed_row = []
        for i in range(self.num_cols):
            summed_entries = (row_target[i] + row_add[i]) % 2
            summed_row.append(summed_entries)
        self.change_row(row_target_index, summed_row)

    def add_cols(self, col_target_index, col_add_index, index_check):
        """

        Add one col to another.

        Parameters:
        -----------
        col_target_index: int
            Index of changed col.
        col_add_index: int
            Index of added col to another.
        index_check: bool
            If true then check if col_target_index
            and col_add_index are correct.

        Notes:
        ------
        The method uses modulo 2 addition of entries.

        """

        if index_check is True:
            self.check_col_index(col_target_index)
            self.check_col_index(col_add_index)

        col_target = self.get_col(col_target_index)
        col_add = self.get_col(col_add_index)
        summed_col = []
        for i in range(self.num_rows):
            summed_entries = (col_target[i] + col_add[i]) % 2
            summed_col.append(summed_entries)
        self.change_row(col_target_index, summed_col)

    def non_zero(self, entry_index, index_check=True):
        """

        Arranges rows and cols so that specified entry on diagonal is non zero.

        Parameters:
        -----------
        entry_index: int
            Index of a row (and column) that contains the entry.
        index_check: bool

        Output:
        -------
        value_check: bool
            Boolean that tells whether the entry is not zero.

        Notes:
        ------
        Intended to use only in smith_normal_form method due to algorithm
        optimizations.

        It will move a row, if non zero entry is on the same column as the
        desired place.

        It will move a columns, if non zero entry is on the right side of
        the desired place.

        """

        if index_check is True:
            self.check_row_index(entry_index)
            self.check_col_index(entry_index)

        zero_row = True
        for i in range(self.num_cols):
            if self.entries[entry_index][i] != 0:
                zero_row = False
        if zero_row is True:
            return False

        if self.entries[entry_index][entry_index] != 0:
            return True

        for row_index in chain(range(entry_index),
                               range(entry_index+1, self.num_rows)):

            if self.entries[row_index][entry_index] != 0:
                copied_row = copy(self.get_row(row_index))
                copied_entry_row = copy(self.get_row(entry_index))

                self.change_row(entry_index, copied_row)
                self.change_row(row_index, copied_entry_row)

                return True

        for col_index in chain(range(entry_index),
                               range(entry_index+1, self.num_cols)):
            if self.entries[entry_index][col_index] != 0:
                copied_col = copy(self.get_col(col_index))
                copied_entry_col = copy(self.get_col(entry_index))

                self.change_col(entry_index, copied_col)
                self.change_col(col_index, copied_entry_col)

                return True

        return False

    def snf(self):
        """

        Calculate Smith normal form of a matrix.

        Output:
        -------
        snf: matrix
            Smith normal form of a matrix.

        Notes:
        ------
        The method uses modulo 2 addition.

        The method is not consistent with theory, but it is good enough
        for getting rank of a matrix.

        """

        snf = deepcopy(self)
        max_dim = min(snf.num_rows, snf.num_cols)

        for dim in range(max_dim):
            value_check = snf.non_zero(dim)

            if value_check is True:
                for row_index in chain(range(dim), range(dim+1, snf.num_rows)):
                    if snf.entries[row_index][dim] == 1:
                        snf.add_rows(row_index, dim)

        return snf

    def snf_rank(self):
        """

        Calculate rank of Smith normal form of a matrix.

        Output:
        -------
        snf_rank: int
            Rank of Smith normal form of a matrix.

        Notes:
        ------
        The method uses modulo 2 addition, with exception of calculating rank
        itself.

        """

        snf = self.snf()
        max_dim = min(snf.num_rows, snf.num_cols)

        snf_rank = 0
        for i in range(max_dim):
            snf_rank += snf.entries[i][i]

        return snf_rank
