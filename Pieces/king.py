from piece import Piece

#Constructor and method docstrings are in the parent class
class King(Piece):
    """ A class to represent a King on a chessboard.

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
            returns a list of all valid moves for a King
        """

    def __init__(self, x, y, white):
        if white:
            self.image = "white_king.svg.png"
        else:
            self.image = "black_king.svg.png"
        super().__init__(x, y, white, self.image)
        self.value = 10000    #The King has the highest value

    def can_move(self, x, y, board):
        inspect.getdoc(Piece.can_move)
        #The space is a valid spot
        if not self.valid_spot:
            return False

       #Check to see if the King is attacking a team piece
        if self.same_team(x, y, board):
            return False

        #King can move 1 space in any direction
        if abs(x - self.location[0]) <= 1 and \
            abs(y - self.location[1]) <= 1:
            return True
        
        return False    #The King cannot move there

    def turn_moves(self, board):
        can_move = []

        #Can move (+/0/-) in x position
        for xm in range(-1, 2):

            #For each x possibility, there is a y possibility
            for ym in range(-1, 2):

                #If both are 0, the piece did not move go to next
                if ym == 0 and xm == 0:
                    continue

                #The new x and y positions
                x = self.location[0] + xm
                y = self.location[1] + ym

                #A valid move in terms of what a piece can do
                if self.valid_spot(x, y) and not self.same_team(x, y, board):
                    can_move.append((x, y))    #Valid move added

        return can_move   #List of valid moves
