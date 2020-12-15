from board import Board
import random

class AIVersions():
    """ A class to represent AIs for a chessgame.

    Methods
    -------
    choice() --> !!!NO LONGER SUPPORTED!!!
        makes a random move for a player
    minimax(max_turn, max_depth, board, depth=0)
        returns best score for a player and updates teh best move instance variable
    get_idx_piece(piece)
        returns the list the piece is in and the index
    """

    def __init__(self):
        self.best_move = None

    def choice(self, player, board):
        """ Makes a random move from the possible moves list.

        !!!NO LONGER SUPPORTED!!!

        Parameters
        ----------
        player : bool
            list of original piece object and the new location
        board : board.Board
            the Board object that stores the matrix for the game
        """

        #White player and black player turns
        if player:
            choices = board.turn_moves_w()

        else:
            choices = board.turn_moves_b()

        self.best_move = random.choice(choices)     #random move choice

        #If the move involves a pawn, ensure that the first move is declared
        if type(self.best_move[0]).__name__ == 'Pawn':
            if self.best_move[0].first_move:
                self.best_move[0].first_move = False

        #Updates the piece location and the board
        self.best_move[0].update(self.best_move[1][0], self.best_move[1][1], board)
    
    def minimax(self, max_turn, max_depth, board, depth=0):
        """ Chooses the best move to make with the Minimax algorithm.
            
        Parameters
        ----------
        max_turn : bool
            True for the max player, False for the min player
        max_depth : int
            how many moves the AI will look ahead
        board : board.Board
            the Board object that stores the matrix for the game
        depth : int, optional
            the starting depth (default is 0)

        Returns
        -------
        int
            the best score that the player can achieve
        """

        #The max look ahead depth is reached, return the score
        if depth == max_depth:
            return board.evaluate_score()

        #If max player turn (TRUE BOOLEAN)
        elif max_turn:
            best_score = float('-inf')

            #----- Check for King in check -----
            check, safe = board.in_check(max_turn)
            if check:
                choices = [[board.wp[0], sm] for sm in safe]
            else:
                choices = board.turn_moves_w()
            #------------------------------------

            for idx in range(len(choices)):
                #call to clone pieces and make a move
                real = board.clone_move(choices[idx])

                #store the score from the recursive call
                possible_score = self.minimax(False, max_depth, board, depth + 1)
                
                #store the score and move_idx if it is more than the best score
                if possible_score > best_score:
                    best_score = possible_score

                    #Only update the best move if it is white turn
                    if depth == 0:
                        self.best_move = choices[idx]

                board.reset_lists(real)     #undo the move

        #else: min player turn (FALSE BOOLEAN)
        else:
            best_score = float('inf')

            #----- Check for King in check -----
            check, safe = board.in_check(max_turn)
            if check:
                choices = [[board.bp[0], sm] for sm in safe]
            else:
                choices = board.turn_moves_b()
            #------------------------------------

            for idx in range(len(choices)):
                #call to clone pieces and make a move
                real = board.clone_move(choices[idx])

                #store the score from the recursive call
                possible_score = self.minimax(True, max_depth, board, depth + 1)
                
                #store the score and move_idx if it is less than the best score
                if possible_score < best_score:
                    best_score = possible_score

                    #Only update the best move if it is black turn
                    if depth == 0:
                        self.best_move = choices[idx]

                board.reset_lists(real)     #undo the move
        
        return best_score   #Best score for that board

    def make_best_move(self, board):
        """ Makes the best move found by the AI.

        Parameters
        ----------
        board : board.Board
            the Board object that stores the matrix for the game
        """

        piece, spot = self.best_move

        #Print the move in the console
        print('{} {} will move from {} to {}' \
                .format("White" if piece.white else "Black", \
                type(piece).__name__, \
                piece.location, spot))

        #If the move involves a pawn, ensure that the first move is declared
        if type(piece).__name__ == 'Pawn':
            if piece.first_move:
                piece.first_move = False

        #Updates the piece location and the board
        piece.update(spot[0], spot[1], board)

    def alpha_beta_pruning(self, max_turn, max_depth, board, alpha=float('-inf'), beta=float('inf'), depth=0):
        """ Chooses the best move to make with the addition of alph-beta pruning.
            
        Parameters
        ----------
        max_turn : bool
            True for the max player, False for the min player
        max_depth : int
            how many moves the AI will look ahead
        board : board.Board
            the Board object that stores the matrix for the game
        alpha : int, optional
            used to prune (default is -inf)
        beta : int, optional
            used to prune (default is inf)            
        depth : int, optional
            the starting depth (default is 0)

        Returns
        -------
        int
            the best score that the player can achieve
        """
            
        #The max look ahead depth is reached, return the score
        if depth == max_depth:
            return board.evaluate_score()

        #If max player turn (TRUE BOOLEAN)
        elif max_turn:
            best_score = float('-inf')

            #----- Check for King in check -----
            check, safe = board.in_check(max_turn)
            if check:
                choices = [[board.wp[0], sm] for sm in safe]
            else:
                choices = board.turn_moves_w()
            #------------------------------------

            for idx in range(len(choices)):
                #call to clone pieces and make a move
                real = board.clone_move(choices[idx])

                #store the score from the recursive call
                possible_score = self.alpha_beta_pruning(False, max_depth, board, alpha, beta, depth + 1)
                
                #store the score and move_idx if it is more than the best score
                if possible_score > best_score:
                    best_score = possible_score

                    #Only update the best move if it is white turn
                    if depth == 0:
                        self.best_move = choices[idx]

                #if higher score, best alpha is now best
                if best_score > alpha:
                    alpha = best_score

                board.reset_lists(real) #undo the move

                #there is already a better move
                if beta <= alpha:
                    break

        #else: min player turn (FALSE BOOLEAN)
        else:
            best_score = float('inf')

            #----- Check for King in check -----
            check, safe = board.in_check(max_turn)
            if check:
                choices = [[board.bp[0], sm] for sm in safe]
            else:
                choices = board.turn_moves_b()
            #------------------------------------

            for idx in range(len(choices)):
                #call to clone pieces and make a move
                real = board.clone_move(choices[idx])

                #store the score from the recursive call
                possible_score = self.alpha_beta_pruning(True, max_depth, board, alpha, beta, depth + 1)
                
                #store the score and move_idx if it is less than the best score
                if possible_score < best_score:
                    best_score = possible_score

                    #Only update the best move if it is black turn
                    if depth == 0:
                        self.best_move = choices[idx]

                #if lower score, best beta is now best
                if best_score < beta:
                    beta = best_score

                board.reset_lists(real) #undo the move

                #there is already a better move
                if beta <= alpha:
                    break
        
        return best_score   #Best score for that board
    