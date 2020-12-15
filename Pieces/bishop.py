from piece import Piece

# Constructor and method docstrings are in the parent class
class Bishop(Piece):
    """ A class to represent a Bishop on a chessboard.

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
        returns a list of all valid moves for a Bishop
    """

    def __init__(self, x, y, white):
        if white:
            self.image = "white_bishop.svg.png"
        else:
            self.image = "black_bishop.svg.png"
        super().__init__(x, y, white, self.image)
        self.value = 300

    def can_move(self, x, y, board):
        #The space is a valid spot
        if not self.valid_spot:
            return False

        #Check to see if the Bishop is attacking a team piece
        if self.same_team(x, y, board):
            return False

        #Vetical and horizontal movement of the Bishop
        if abs(x - self.location[0]) == abs(y - self.location[1]):
            if self.blocked(x, y, board):   #Check to see if the Bishop is blocked
                return False
            return True

        return False    #The Bishop cannot move there

    def turn_moves(self, board):
        can_move = []

        # - Top right to bottom left
        for xm in range(8):
            x = xm
            y = self.location[1] - (self.location[0] - xm)
            if x != self.location[0] and \
                self.valid_spot(x, y) and \
                not self.same_team(x, y, board) and \
                not self.blocked(x, y, board):
                can_move.append((x, y))

        # - Top left to bottom right
        for ym in range(8):
            x = self.location[0] + (self.location[1] - ym)
            y = ym
            if x != self.location[0]:
                if self.valid_spot(x, y) and \
                    not self.same_team(x, y, board) and \
                    not self.blocked(x, y, board):
                    can_move.append((x, y))
        
        return can_move   #List of valid moves
        