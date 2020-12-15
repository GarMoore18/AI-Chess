from piece import Piece
from queen import Queen

#Constructor and method docstrings are in the parent class
class Pawn(Piece):
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
            self.image = "white_pawn.svg.png"
        else:
            self.image = "black_pawn.svg.png"
        super().__init__(x, y, white, self.image)

        self.value = 100
        self.first_move = True  #Can move differently on first move

    def promotion(self, board_obj):
        """ Checks if a Pawn has reached the opponents side of the board.

        The promotion for a Pawn will result in a Queen object taking the
        the Pawn's spot in the game.
        
        Parameters
        ----------
        board_obj : board.Board
            the board object that was created
        """

        x, y = self.location

        #Where, in which list, is this Pawn object stored
        in_list = self.wp if self.white else self.bp
        for idx in len(in_list):
            if in_list[idx] is self:
                p_idx = idx
                break

        if y == 0 and self.white:
            queen_prom = Queen(x, y, True)
            #self.captured = True
            board_obj.board[y][x] = queen_prom
            board_obj.wp[idx] = queen_prom

        if y == 7 and not self.white:
            queen_prom = Queen(x, y, False)
            #self.captured = True
            board_obj.board[y][x] = queen_prom
            board_obj.bp[idx] = queen_prom 

    def can_move(self, x, y, board):
        #The space is a valid spot
        if not self.valid_spot:
            return False

        #Check to see if the Pawn is attacking a team piece
        if self.same_team(x, y, board):
            return False

        #----- Horizontal Move -----
        if x != self.location[0]:
            return False

        #----- Diagonal Attack -----
        if board[y][x] is not None:
            if abs(x - self.location[0]) == abs(y - self.location[1]) and \
               ((self.white and y - self.location[1] == -1) or \
                   (not self.white and y - self.location[1] == 1)):
                
                self.first_move = False     #Pawn can move, the first move is done

                return True
            return False    

        #---------- Vertical Moves ----------
        #----- First Move -----
        #Pawns can move two spaces on first move
        if (self.first_move and ((self.white and y - self.location[1] == -2) or \
             (not self.white and y - self.matrixPlacement[1] == 2))):
            
            if self.blocked(x, y, board):   #Check to see if the Pawn is blocked
                return False

            self.first_move = False     #Pawn can move, the first move is done

            return True

        #----- Not First Move -----
        #White pieces can move up one (neg direction) and the black pieces can move down one (positve direction)
        if (self.white and y - self.location[1] == -1) or \
             (not self.white and y - self.location[1] == 1):

            if self.blocked(x, y, board):   #Check to see if the Pawn is blocked
                return False

            self.first_move = False     #Pawn can move, the first move is done

            return True

        return False    #The Pawn cannot move there

    def turn_moves(self, board):
        can_move = []

        #Checks for attacking opportunities
        for xm in range(-1, 2, 2):
            x = self.location[0] + xm
            if self.white:
                y = self.location[1] - 1
            else:
                y = self.location[1] + 1

            if self.valid_spot(x, y):
                attacked_piece = board[y][x]
                if attacked_piece is not None and \
                    not self.same_team(x, y, board):
                    can_move.append((x, y))
        
        #Pawn can move one space
        x = self.location[0]
        if self.white:
            y = self.location[1] - 1
        else:
            y = self.location[1] + 1
        if self.valid_spot(x, y) and \
            board[y][x] is None :
            can_move.append((x, y))

        #Pawn can move two spaces on first turn
        if self.first_move:
            if self.white:
                y = self.location[1] - 2
            else:
                y = self.location[1] + 2
            if self.valid_spot(x, y) and \
                board[y][x] is None and \
                not self.blocked(x, y, board):
                can_move.append((x, y))

        return can_move   #List of valid moves
