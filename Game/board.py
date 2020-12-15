from king import King
from queen import Queen
from bishop import Bishop
from knight import Knight
from rook import Rook
from pawn import Pawn
import random

class Board():
    """ A class to represent a Board for a chessgame.
    
    Attributes
    ----------
    chessboard : pygame.Surface
        the current pygame surface being used

    Methods
    -------
    add_pieces()
        appends the proper pieces and locations to each team list
    clone_move(piece_newl)
        returns the moving piece, piece being captured (if applicable), and copy object
    get_idx_piece(piece)
        returns the list the piece is in and the index
    reset_lists(involved)
        resets the lists and matricies to have the initial pieces
    update_board()
        updates the display and the matrix
    display_pieces()
        decides which piece images should be displayed on the screen
    create_matrix()
        makes the board matrix
    turn_moves_b()
        gets the possible moves for the black player
    turn_moves_w()
        gets the possible moves for the white player
    pieces_left()
        returns True if both players have pieces left
    in_check(max_turn)
        returns True and the possible moves if the King is in check
    king_captured()
        returns True if the King is captured
    get_game_status()
        returns True if one of the end conditions is True
    evaluate_score()
        returns the current score of the game
    """

    def __init__(self, chessboard):
        self.wp = []    #White pieces
        self.bp = []    #Black pieces
        self.add_pieces()

        self.board = [[None for i in range(8)] for j in range(8)]
        self.create_matrix()
        
        self.chessboard = chessboard    #Surface

        self.score = 0
        self.game_over = False

    def add_pieces(self):
        """ Appends the proper pieces and locations to each team list.
        
        Team lists are used to get the possible moves and easily
        check the capture status of a piece.
        """

        self.wp.append(King(4, 7, True))
        self.wp.append(Queen(3, 7, True))
        self.wp.append(Rook(0, 7, True))
        self.wp.append(Rook(7, 7, True))
        self.wp.append(Knight(1, 7, True))
        self.wp.append(Knight(6, 7, True))
        self.wp.append(Bishop(2, 7, True))
        self.wp.append(Bishop(5, 7, True))
        for i in range(8):
            self.wp.append(Pawn(i, 6, True))

        self.bp.append(King(4, 0, False))
        self.bp.append(Queen(3, 0, False))
        self.bp.append(Rook(0, 0, False))
        self.bp.append(Rook(7, 0, False))
        self.bp.append(Knight(1, 0, False))
        self.bp.append(Knight(6, 0, False))
        self.bp.append(Bishop(2, 0, False))
        self.bp.append(Bishop(5, 0, False))
        for i in range(8):
            self.bp.append(Pawn(i, 1, False))

    def clone_move(self, piece_newl):
        """ Clones pieces and temporarily moves the piece in the matrix and list.
        
        Clones the pieces that will be involved with the move,
        moves the clone piece, and updates the matrix for future moves.
        Original piece objects and locations will be returned in a list.
        The copied piece object is also returned.

        Parameters
        ----------
        piece_newl : list
            list of original piece object and the new location

        Returns
        -------
        tuple
            list of the pieces involved and the copy of the piece
        """

        org_p, new_location = piece_newl    #piece and space to move
        x, y = new_location

        copy_p = org_p.clone()    #copy of the original piece

        #stores the index of the piece in the corresponding piece list
        in_list, org_idx = self.get_idx_piece(org_p)

        #change the piece in the list
        in_list[org_idx] = copy_p

        #If the new space has a piece it needs to be copied
        if self.board[y][x] is not None:
            occ_p = self.board[y][x]
            
            copy_occ_p = occ_p.clone()

            #gets the index of the piece in the corresponding piece list
            in_list, occ_idx = self.get_idx_piece(occ_p)

            #change the occupied piece in the list
            in_list[occ_idx] = copy_occ_p

        self.create_matrix()   #update the matrix

        copy_p.update_clone(x, y, self)   #move the piece

        #copy_p.update_clone(x, y, self)   #move the piece
        
        self.create_matrix()    #update the matrix

        #Depends if two pieces were involved or not
        try:
            return [org_p, org_idx, occ_p, occ_idx], copy_p
        except UnboundLocalError:
            return [org_p, org_idx], copy_p

    def get_idx_piece(self, piece):
        """ Gets the team that the piece is on and the index where the piece is.

        Parameters
        ----------
        piece : obj (depends on the child class)
            list of original piece object and the new location

        Returns
        -------
        tuple
            the list for the team and index in that list
        """

        #choose which list to alter
        in_list = self.wp if piece.white else self.bp

        #get index in list of original piece
        for idx in range(len(in_list)):
            if in_list[idx] is piece:
                return in_list, idx       #index in pieces list

    def reset_lists(self, involved):
        """ Resets the game state before attempting to find the best move.

        Used to ensure that the board has no lingering copies or any 
        unwanted images being displayed.

        Parameters
        ----------
        involved : list
            a list of the piece and the new location
        """

        indices = involved[0]
        cx, cy = involved[1].location

        involved[1].captured = True #ensure that the piece is gone
        
        self.board[cy][cx] = None
        #Piece and index next to each other
        for i in range(0, len(indices), 2):
            #Which list was the piece in
            in_list = self.wp if indices[i].white else self.bp
            in_list[indices[i+1]] = indices[i]  #Replace the copied piece
        
        self.create_matrix()    #Update the matrix

    def display_pieces(self):
        """ Display the non-captured pieces on the pygame surface. """

        for i in range(len(self.wp)):
            if not self.wp[i].captured:
                self.wp[i].show_image(self.chessboard)
        
        for i in range(len(self.bp)):
            if not self.bp[i].captured:
                self.bp[i].show_image(self.chessboard)

    def create_matrix(self):
        """ Creates a matrix that has the non-captured pieces. """

        #Placing the white team
        for i in range(len(self.wp)):
            if not self.wp[i].captured:
                x, y = self.wp[i].location
                self.board[y][x] = self.wp[i]

        #Placing the black team
        for i in range(len(self.bp)):
            if not self.bp[i].captured:
                x, y = self.bp[i].location
                self.board[y][x] = self.bp[i] 

    def update_board(self):
        """ Runs the method to display pieces and create a matrix. """

        self.display_pieces()
        self.create_matrix()

    def turn_moves_b(self):
        """ Gets the possible moves for the black player.

        Returns
        -------
        list
            list that contains piece object with possible locations

        Raises
        ------
        TypeError
            If there are not any moves, the move list is empty.
        """

        game_boards = []

        #For each of the pieces in black pieces
        for i in self.bp[1:]:
            #If the piece is still playable
            if not i.captured:
                piece_states = i.turn_moves(self.board)
                for j in piece_states:
                    game_boards.append([i, j])  #{Old location, new location}
        
        #Shuffle the list so the same move is not chosen on ties
        try:
            random.shuffle(game_boards)
        except TypeError:
            pass
        
        return game_boards

    def turn_moves_w(self):
        """ Gets the possible moves for the white player.

        Returns
        -------
        list
            list that contains piece object with possible locations

        Raises
        ------
        TypeError
            If there are not any moves, the move list is empty.
        """

        game_boards = []

        #For each of the pieces in white pieces
        for i in self.wp:
            #If the piece is still playable
            if not i.captured:
                piece_states = i.turn_moves(self.board)
                for j in piece_states:
                    game_boards.append([i, j])  #{Old location, new location}
        
        #Shuffle the list so the same move is not chosen on ties
        try:
            random.shuffle(game_boards)
        except TypeError:
            pass
        
        return game_boards
        
    def pieces_left(self):
        """ Checks to see if both teams still have at least one piece left.
        
        Returns
        -------
        bool
            True if both teams have a piece left, False if one/both teams
            have no pieces remaining
        """

        w_moves = False
        b_moves = False

        #Both look for at least one playable piece
        for w in self.wp:
            if not w.captured:
                w_moves = True
                break
        
        for b in self.bp:
            if not b.captured:
                b_moves = True
                break
        
        #Returns True if both players have a piece left
        return w_moves and b_moves 

    def in_check(self, max_turn):
        """ Checks to see if the current player King is in check.
        
        Parameters
        ----------
        max_turn : bool
            True for max player, False for min player

        Returns
        -------
        tuple
            (True, possible moves) if the King is in check
            (False, None) if the King is not in check
        """

        white = self.turn_moves_w()
        black = self.turn_moves_b()

        #White turn check if black can capture next move
        if max_turn:
            king_space = self.wp[0].location    #Store King spots

            for b in black:
                if b[1] == king_space:

                    #----- Valid spots to move -----
                    #Valid spots to move
                    get_out = self.wp[0].turn_moves(self.board)
                    for b in black:
                        if b[1] in get_out:
                            get_out.remove(b[1])
                    #-------------------------------
                    return True, get_out    #True if a spot matches

        #Black turn check if white can capture next move
        else:
            king_space = self.bp[0].location

            #Cross-checking same spots
            for w in white:
                if w[1] == king_space:
                    #----- Valid spots to move -----
                    #Valid spots to move
                    get_out = self.bp[0].turn_moves(self.board)
                    for w in white:
                        if w[1] in get_out:
                            get_out.remove(w[1])
                    #-------------------------------
                    return True, get_out     #True if a spot matches
        
        return False, None    #The King is not in check

    def king_captured(self):
        """ Checks if either King has been captured.
        
        Returns
        -------
        bool
            True if a King has been captured, otherwise False
        """

        if self.wp[0].captured or self.bp[0].captured:
            return True

        return False

    def get_game_status(self):
        """ Checks both end game conditions.
        
        Returns
        -------
        bool
            True if a either condition met, False if both
            are not met
        """

        if not self.pieces_left() or self.king_captured():
            self.game_over = True
        
        return self.game_over

    def evaluate_score(self):
        """ Calculates the score of the current board.
        
        Returns
        -------
        int
            the calculated score of the board
        """
        
        score = 0

        #Add the scores of the white player (MAX)
        for w in self.wp:
            if not w.captured:
                score += w.value

        #Subtract the scores of the black player (MIN)
        for b in self.bp:
            if not b.captured:
                score -= b.value

        return score
