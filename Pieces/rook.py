from piece import Piece

#Constructor and method docstrings are in the parent class
class Rook(Piece):
    """ A class to represent a Rook on a chessboard.

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
        returns a list of all valid moves for a Rook
    """

    def __init__(self, x, y, white):
        if white:
            self.image = "white_rook.svg.png"
        else:
            self.image = "black_rook.svg.png"
        super().__init__(x, y, white, self.image)
        self.value = 500

    def can_move(self, x, y, board):
        #The space is a valid spot
        if not self.valid_spot:
            return False

        #Check to see if the Rook is attacking a team piece
        if self.same_team(x, y, board):
            return False

        #Vetical and horizonatl movement of the Rook
        if x == self.location[0] or y == self.location[1]:
            if self.blocked(x, y, board):   #Check to see if the Rook is blocked
                return False
            return True

        return False    #The Rook cannot move there

    def turn_moves(self, board):
        can_move = []

        #Horizontal movement
        for xm in range(8):
            x = xm
            y = self.location[1]
            if x != self.location[0] and \
                not self.same_team(x, y, board) and \
                not self.blocked(x, y, board):
                can_move.append((x, y))
        
        #Vertical movement
        for ym in range(8):
            x = self.location[0]
            y = ym
            if y != self.location[1] and \
                not self.same_team(x, y, board) and \
                not self.blocked(x, y, board):
                can_move.append((x, y))

        return can_move    #List of valid moves
        