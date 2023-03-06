class RepositoryException(Exception):
    pass


class BoardRepository:
    def __init__(self):
        # Initializes the board as an empty 6 rows x 7 columns list of lists matrix
        self._data = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]

    def get_slot_status(self, x, y):
        # Gets the status of a slot in the board
        return self._data[x][y]

    def update_board(self, x, y, fill):
        # Updates a slot in the board and also checks if the human player is able to put one more disc into a column and
        # raises an exception if not
        if x < 0:
            raise RepositoryException("Cannot insert discs in that column anymore!")
        self._data[x][y] = fill

    def get_board(self):
        # Returns the entire board's matrix
        return self._data
