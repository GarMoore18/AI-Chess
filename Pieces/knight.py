from piece import Piece

#Constructor and method docstrings are in the parent class
class Knight(Piece):
    """ A class to represent a Knight on a chessboard.

    Attributes
    ----------
    x : int
        x position of a piece
    y : int
        y position of a piece
    white : bool
        color of the piece

    Methods
    -------
    can_move(x, y, board)
        returns True for a legal move, False if illegal
    turn_moves(board)
        returns a list of all valid moves for a Knight
    """

    def __init__(self, x, y, white):
        if white:
            self.image = "white_knight.svg.png"
        else:
            self.image = "black_knight.svg.png"
        super().__init__(x, y, white, self.image)
        self.value = 300

    def can_move(self, x, y, board):
        #The space is a valid spot
        if not self.valid_spot:
            return False

        #Check to see if the Knight is attacking a team piece
        if self.same_team(x, y, board):
            return False

        #Special 1 by 2 movement of the Knight
        if (abs(x - self.location[0]) == 2 and \
                abs(y - self.location[1]) == 1) \
                or \
            (abs(x - self.location[0]) == 1 and \
                abs(y - self.location[1]) == 2):
            return True

        return False    #The Knight cannot move there

    def turn_moves(self, board):
        can_move = []

        #Left and right movement
        for xm in range(-2, 3, 4):
            for ym in range(-1, 2, 2):
                x = xm + self.location[0]
                y = ym + self.location[1]
                if self.valid_spot(x, y) and \
                    not self.same_team(x, y, board):
                    can_move.append((x, y))

        #Up and down movement
        for xm in range(-1, 2, 2):
            for ym in range(-2, 3, 4):
                x = xm + self.location[0]
                y = ym + self.location[1]
                if self.valid_spot(x, y) and \
                    not self.same_team(x, y, board):
                    can_move.append((x, y))

        return can_move  #List of valid moves
        