import pygame
import time
from board import Board
from ai_versions import AIVersions
from errors import TooManyMoves, AIDoesNotExist

class Chess():
    """ A class to represent a Chess game.
    
    Methods
    -------
    board_layer()
        returns the base surface for the pygame screen
    highlighting()
        updates the visual with identifying move outlines
    chess_game()
        runs the game loop and AIs
    """

    def __init__(self):
        self.size = 800     #Size of the board
        self.space = 100    #Size of the checker spaces
        self.screen = pygame.display.set_mode((self.size, self.size))
        self.colors = [(232, 235, 239), (125, 135, 150)]    #Colors for checkerboard

        self.game = Board(self.screen)  #instance of a Board
        self.smart = AIVersions()   #instance of an AI

    def board_layer(self):
        """ Create the base pygame surface for the chessboard. 
        
        Returns
        -------
        pygame.Surface
            base surface of the game 

        """
        board_layer = pygame.Surface((self.size, self.size))

        for y in range(8):
            color_idx = y % 2   #To alternate staring color of row
            for x in range(8):
                rect = pygame.Rect(x*self.space, y*self.space, self.space, self.space)
                pygame.draw.rect(board_layer, self.colors[color_idx], rect)
                color_idx = (color_idx + 1) % 2     #To alternate colors
        
        return board_layer  #The completed base layer

    def highlighting(self, best_move, turn):
        """ Updates the visual with identifying move outlines.

        Outlines the current and new position in black. Draws a
        green line when not attacking. Draws a red line and red 
        shade when attacking a piece. 
        
        Parameters
        ----------
        best_move : list
            a list of the piece object and the location tuple
        turn : boolean
            if the player is White (True) or black (False)
        """

        piece, space = best_move
        ox, oy = piece.location
        nx, ny = space

        #Creating rectangles to outline the spots
        curr_spot = pygame.Rect(ox * self.space, oy * self.space, self.space, self.space)
        new_spot = pygame.Rect(nx * self.space, ny * self.space, self.space, self.space)

        pygame.draw.rect(self.screen, (0, 0, 0), curr_spot, 5)  #Current spot outline

        #Changes line color and shades sopt red if piece is attacking
        if self.game.board[ny][nx] is None:
            pygame.draw.rect(self.screen, (0, 0, 0), new_spot, 5)   #New spot outline
            pygame.draw.line(self.screen, (144, 238, 144), curr_spot.center, new_spot.center, 10)   #Green line
        else:
            #Red shade for capturing a piece
            new_shade = pygame.Surface((self.space, self.space))
            new_shade.set_alpha(120)
            new_shade.fill((255, 0, 0))
            self.screen.blit(new_shade, (nx * self.space, ny * self.space))

            pygame.draw.rect(self.screen, (0, 0, 0), new_spot, 5)   #New spot outline

            pygame.draw.line(self.screen, (255, 0, 0), curr_spot.center, new_spot.center, 10)   #Red line

        pygame.display.update()     #update the visual

    def chess_game(self, ai=2, moves_ahead=3, player=True, delay=500):
        """ Runs the game loop and with the selected AI.

        Parameters
        ----------
        ai : int, optional
            the AI that is being used (default is aplha beta pruning)
        moves_ahead : int, optional
            the number of moves the AI is looking ahead (default is 3)
        player : bool, optional
            which player gets to go first (default is True)
        delay : int, optional
            number of milliseconds before updating the screen (default is 500ms)
        
        Raises
        ------
        AIDoesNotExist
            There are only two AIs to select from, so the ai parameter must
            be either 1 or 2
        TooManyMoves
            The game runs too slow if the AI is looking too many moves ahead,
            so only a certain number is allowed for each AI
        """

        try:   
            #Ensure that an AI is seleceted
            if ai != 1 and ai != 2:
                raise AIDoesNotExist

            #Ensure that the game is not too slow
            if (ai == 1 and moves_ahead) > 3 \
                or (ai == 2 and moves_ahead > 5):
                raise TooManyMoves

            pygame.display.set_caption('AI Chess')  #Name game
            board_layer = self.board_layer()

            #Initial board display
            self.screen.fill(pygame.Color('grey'))
            self.screen.blit(board_layer, (0, 0))
            self.game.update_board()            #ensures that the board object is correct
            pygame.display.flip()   #The image can be displayed

            can_play = True
            #-----------------------
            moves = 0
            total_time = 0
            #Game loop
            while can_play:
                ev = pygame.event.get()    #all events in list

                for e in ev:
                    if e.type == pygame.QUIT:  #closed window?
                        return
                
                #This is a minimax AI
                if ai == 1:
                    #-------------------------------
                    start = time.time()
                    #-------------------------------
                    self.smart.minimax(player, moves_ahead, self.game)    #minimax
                    #-------------------------------
                    elapsed = time.time() - start
                    moves += 1
                    total_time += elapsed
                    print(total_time/moves)
                    #-------------------------------

                #This is a alpha beta pruning AI
                elif ai == 2:
                    #-------------------------------
                    start = time.time()
                    #-------------------------------
                    self.smart.alpha_beta_pruning(player, moves_ahead, self.game)   #alpha beta pruning
                    #-------------------------------
                    elapsed = time.time()- start
                    moves += 1
                    total_time += elapsed
                    print(total_time/moves)
                    #-------------------------------

                #To highlight where the piece is moving from and to
                #--------------------------------------------------
                self.highlighting(self.smart.best_move, player)
                pygame.time.wait(delay)  #delay to see highlights (default 500)
                #--------------------------------------------------

                self.smart.make_best_move(self.game)    #makes the best move on the board

                #Gets the state of the game
                if self.game.get_game_status():
                    print("Winner is {}".format("White" if player else "Black"))
                    pygame.time.wait(5000)  #As of now will pause for 5 seconds before closing game
                    return

                self.screen.fill(pygame.Color('grey'))  #Color over current board
                self.screen.blit(board_layer, (0, 0))
                self.game.update_board()            #ensures that the board object is correct
                pygame.display.flip()   #The image can be displayed

                player = not player     #switches players

            pygame.quit()

        #Tell user the appropriate options if not provided
        except AIDoesNotExist:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("There are only two AI options:")
            print("    Input number 1 for minimax AI.")
            print("    Input number 2 for alpha-beta pruning AI.")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        #Tell user the appropriate number of moves allowed
        except TooManyMoves:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("For reliable performance:")
            print("    Minimax (1) should look 3 or less moves ahead.")
            print("    Alpha-beta pruning (2) should look 5 or less moves ahead.")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
