class ChessBoard:
    """Finds all unique configurations of a set of normal chess pieces
    on a chess board with dimensions width×height where none of the pieces
    is in a position to take any of the others

    width, height - int dimensions
    pieces - list with pieces
    """
    PIECES = ('Q', 'R', 'B', 'K', 'N')
    PIECES_MAP = dict(zip(PIECES, range(5, 0, -1)))

    def __init__(self, width, height, pieces, verbose=False):
        self.width, self.height, self.pieces = width, height, pieces
        self.verbose = verbose
        self.__unique_comb_hashes = set()

    def __is_cell_cannot_be_taken(self, cell, cells_map):
        return cell in cells_map and cells_map[cell] in ChessBoard.PIECES_MAP

    def check_board_for_k(self, y, x, cells_map):
        """Marks cells which can take King if they are not taken by other piece
        If King on this cell can take another piece - return

        y, x - int coordinates
        width, height - board parameters, passed to keep their calculation in one place
        board - 2-dimension listwith current board
        """

        new_hit_cells = set()
        # just move 1 step around current cell
        for i in range(-1, 2):
            for j in range(-1, 2):
                _x, _y = x + j, y + i
                if (i or j) and (0 <= _x < self.width and 0 <= _y < self.height):
                    cell = (_y, _x)
                    if self.__is_cell_cannot_be_taken(cell, cells_map):
                        return None
                    if cell not in cells_map:
                        new_hit_cells.add(cell)
        return new_hit_cells

    def check_board_for_r(self, y, x, cells_map):
        """Marks cells which can take Rook if they are not taken by other piece
        If Rook on this cell can take another piece - return

        y, x - int coordinates
        width, height - board parameters, passed to keep their calculation in one place
        board - 2-dimension listwith current board
        """

        new_hit_cells = set()
        # move horizontaly
        for i in range(self.width):
            if i == x:
                continue
            cell = (y, i)
            if self.__is_cell_cannot_be_taken(cell, cells_map):
                return None
            if cell not in cells_map:
                new_hit_cells.add(cell)
        # and vertically
        for i in range(self.height):
            if i == y:
                continue
            cell = (i, x)
            if self.__is_cell_cannot_be_taken(cell, cells_map):
                return None
            if cell not in cells_map:
                new_hit_cells.add(cell)
        return new_hit_cells

    def check_board_for_b(self, y, x, cells_map):
        """Marks cells which can take Bishop if they are not taken by other piece
        If Bishop on this cell can take another piece - return

        y, x - int coordinates
        width, height - board parameters, passed to keep their calculation in one place
        board - 2-dimension listwith current board
        """

        new_hit_cells = set()
        for i in range(self.width):
            if i == x:
                continue

            _y = y + abs(x - i)
            if _y < self.height:
                cell = (_y, i)
                if self.__is_cell_cannot_be_taken(cell, cells_map):
                    return None
                if cell not in cells_map:
                    new_hit_cells.add(cell)

            _y = y - abs(x - i)
            if _y >= 0:
                cell = (_y, i)
                if self.__is_cell_cannot_be_taken(cell, cells_map):
                    return None
                if cell not in cells_map:
                    new_hit_cells.add(cell)
        return new_hit_cells

    def check_board_for_q(self, y, x, cells_map):
        """Marks cells which can take Queen if they are not taken by other piece
        If Queen on this cell can take another piece - return

        y, x - int coordinates
        width, height - board parameters, passed to keep their calculation in one place
        board - 2-dimension listwith current board
        """

        # since queen is intersection of bishop and rook...
        cells_r = self.check_board_for_r(y, x, cells_map)
        if cells_r is None:
            return cells_r
        cells_b = self.check_board_for_b(y, x, cells_map)
        if cells_b is None:
            return cells_b
        return cells_r.union(cells_b)

    def check_board_for_n(self, y, x, cells_map):
        """Marks cells which can take Knight if they are not taken by other piece
        If Knight on this cell can take another piece - return

        y, x - int coordinates
        width, height - board parameters, passed to keep their calculation in one place
        board - 2-dimension listwith current board
        """

        new_hit_cells = set()
        # very naive solve for knights
        for i, j in ((-2, 1), (-1, 2), (1, 2), (2, 1)):
            _x = x + i
            if not (_x < self.width and _x >= 0):
                continue

            _y = y + j
            if _y < self.height:
                cell = (_y, _x)
                if self.__is_cell_cannot_be_taken(cell, cells_map):
                    return None
                if cell not in cells_map:
                    new_hit_cells.add(cell)

            _y = y - j
            if _y >= 0:
                cell = (_y, _x)
                if self.__is_cell_cannot_be_taken(cell, cells_map):
                    return None
                if cell not in cells_map:
                    new_hit_cells.add(cell)
        return new_hit_cells

    def check_board(self, y, x, cells_map, piece):
        """Upper level function which takes function respective to piece and checks board
        """

        return {
            'K': self.check_board_for_k,
            'R': self.check_board_for_r,
            'Q': self.check_board_for_q,
            'B': self.check_board_for_b,
            'N': self.check_board_for_n,
        }[piece](y, x, cells_map)

    def get_combinations_number(self):
        return len(self.__unique_comb_hashes)

    def new_board(self):
        row = lambda x: list(0 for _ in range(x))
        return list(row(self.width) for _ in range(self.height))

    def find_combinations(self):
        self.place_pieces({}, self.pieces)

    def place_pieces(self, _cells_map, pieces):
        for i in range(self.height):
            for j in range(self.width):
                # if this place is already under attack or this place taken
                if (i, j) in _cells_map:
                    continue

                piece = pieces[0]
                # or current piece on this place will attack other pieces
                cells_to_mark = self.check_board(i, j, _cells_map, piece)
                # just continue
                if cells_to_mark is None:
                    continue
                # if ok - make copy of current taken cells
                cells_map = dict(_cells_map)
                cells_map[(i, j)] = piece
                # add cells taken by current piece
                for coords in cells_to_mark:
                    cells_map[coords] = None
                # if its last piece we need to store combination hash and continue
                # (and print if required)
                if len(pieces) == 1:
                    # yeah, maybe its worst hash that You've seen
                    _h = hash(tuple(sorted(cells_map.items())))
                    if _h not in self.__unique_comb_hashes:
                        self.__unique_comb_hashes.add(_h)
                        if self.verbose:
                            print(self.prettyfie_board(cells_map))
                    return
                # if not - go deeper
                self.place_pieces(cells_map, pieces[1:])

    def prettyfie_board(self, cells):
        board = self.new_board()
        for cell, v in cells.items():
            y, x = cell
            board[y][x] = v or '-'
        width, delimeter = len(board[0]), '   '
        board = '\n'.join(delimeter.join(str(cell) for cell in row) for row in board)
        line = '-' * (len(delimeter) * (width - 1) + width)
        return '{0}\n{1}'.format(line, board)
