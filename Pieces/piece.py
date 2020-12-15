import pygame
from pygame import Color
import copy
from abc import ABC, abstractmethod

class Piece(ABC):
    """ A class to represent a piece on a chessboard. 

        Attributes
        ----------
        x : int
            x position of a piece
        y : int
            y position of a piece
        white : bool
            color of the piece
        image : str
            image for the piece

        Methods
        -------
        get_image_rect()
            returns image converted to pygame surface
        show_image(screen)
            displays image on pygame surface
        update(x, y, board_obj)
            moves the piece for matrix and screen locations
        update_clone(x, y, board_obj)
            moves piece location for temporary boards
        get_type()
            returns the name of the piece
        clone()
            returns a shallow copy of a piece
        blocked(x, y, board)
            returns True if the piece is not blocked
        valid_spot(x, y)
            returns True if the spot is on the board
        same_team(x, y, board)
            returns True if the pieces are on the same team
        can_move(x, y, board)
            abstract method
        turn_moves(board)
            abstract method
        """

    def __init__(self, x, y, white, image):
        """
        Parameters
        ----------
        x : int
            x position of a piece
        y : int
            y position of a piece
        white : bool
            color of the piece
        image : str
            image for the piece
        """

        self.location = (x, y)      #where the piece is on the board
        self.white = white          #if the color is white (True) or black (False)
        self.value = 0              #default point value of any piece is 0
        self.captured = False       #when the game starts, the piece is not captured

        self.image = image          #image to use in pygame
        self.converted = self.get_image_rect()  #The image as a transparent rectangle
        self.screen_placement = (x*100, y*100)  #Only works for 800px X 800px board
    
    def get_image_rect(self):
        """ Converts an image into a pygame surface.

        Returns
        -------
        pygame.Surface
            image converted to pygame surface 
        """

        load_image = pygame.image.load(self.image)  #Load the image as a surface
        scale_image = pygame.transform.scale(load_image, (100,100))   #Rescale the iamge to fit in the spac
        return scale_image.convert_alpha()  #The image as a transparent rectangle
        
    def show_image(self, screen):
        """ Displays the converted image on the base pygame surface. 
        
        Parameters
        ----------
        screen : pygame.Surface
            base pygame layer for the chessboard images
        """

        screen.blit(self.converted, self.screen_placement)

    def update(self, x, y, board_obj):
        """ Moves the piece for matrix and screen locations.

        In addition to moving the selected piece, if a piece
        is attacked the captured status is updated. 

        Parameters
        ----------
        x : int
            new x location
        y : int
            new y location
        board_obj : board.Board
            the board object that was created
        """
        old = board_obj.board[y][x]
        moved_from = copy.copy(self.location)

        #The desired spot has a piece there
        if old is not None:
            old.converted.fill(Color(0,0,0,0))    #Clear the piece
            old.captured = True                   #set capture status to True
            #Print the piece that captured another piece
            print("{} {} captured {} {}".format('White' if self.white else 'Black', \
                    type(self).__name__, 'White' if old.white else 'Black', type(old).__name__))
        
        self.location = (x, y)
        self.screen_placement = (x*100, y*100)   #The screen coordinates 

        board_obj.board[moved_from[1]][moved_from[0]] = None      #old spot is now None

        """ #Promotion only works for pawns
        try:
            self.promotion(board_obj)
        except AttributeError:
            pass """

    def update_clone(self, x, y, board_obj):
        """ Moves the piece matrix location for temporary boards.

        To utilize recursion effectively for minimax/alpha beta pruning,
        this method utlizes cloned pieces that can be replaced with the
        original once the board score is calculated.

        Parameters
        ----------
        x : int
            new x location
        y : int
            new y location
        board_obj : board.Board
            the board object that was created
        """

        old = board_obj.board[y][x]
        mfx, mfy = copy.copy(self.location)

        #The desired spot has a piece there
        if old is not None:
            old.captured = True   #set capture status to True

        self.location = (x, y)

        board_obj.board[mfy][mfx] = None      #old spot is now None

        """ #Promotion only works for pawns
        try:
            self.promotion(board_obj)
        except AttributeError:
            pass """

    def get_type(self):
        """ Gets the name of the piece.
        
        Returns
        -------
        str
            the name of the object
        """

        return type(self).__name__

    def clone(self):
        """ Shallow copy of a piece.

        Returns
        -------
        obj (depends on the child class)
            a copy of the piece 
        """

        return copy.copy(self)   #copy of original piece

    def blocked(self, x, y, board):
        """ Checks to see if a piece is blocked by another piece.
        
        Parameters
        ----------
        x : int
            x location
        y : int
            y location
        board : list
            the matrix storage of the chessboard

        Returns
        -------
        bool
            True if the piece is blocked, False if the piece is
            not blocked.
        """

        #----- Which direction -----
        xd = x - self.location[0]
        yd = y - self.location[1]

        #x and y direction to check spots in corresponding direction
        xd = 1 if xd > 0 else -1 if xd < 0 else 0
        yd = 1 if yd > 0 else -1 if yd < 0 else 0

        #----- Start checking the spots to the new location -----
        amx, amy = self.location
        amx += xd
        amy += yd

        #Each spot from the old space to the new space must be checked
        while amx != x or amy != y:

            if board[amy][amx] is not None:
                return True     #Piece is blocked and cannot move

            #Increment to next spot
            amx += xd
            amy += yd

        return False    #Piece is not blocked and can move

    def valid_spot(self, x, y):
        """ Checks to make sure the spot is on the board.
        
        Parameters
        ----------
        x : int
            new x location
        y : int
            new y location

        Returns
        -------
        bool
            True if the spot is on the board, False if the spot is
            not on the board.
        """

        #x and y need to be a number 0 to 7
        if 0 <= x < 8 and 0 <= y < 8:
            return True

        return False    #Not a valid spot

    def same_team(self, x, y, board):
        """ Checks to see if two pieces are on the same team.
        
        Parameters
        ----------
        x : int
            new x location
        y : int
            new y location
        board : list
            the matrix storage of the chessboard

        Returns
        -------
        bool
            True if the pieces are on the same team, False if 
            the pieces are not on the same team.
        """

        att_spot = board[y][x]    #Where the piece is trying to be moved

        #There is already a piece at the desired space
        if att_spot is not None:
            
            #Checks to see if the pieces are on the same team
            if att_spot.white == self.white:
                return True     #True if on same team

        return False    #False if not on same team

    @abstractmethod
    def can_move(self, x, y, board):
        """ Checks if the desired spot is a legal move.

        Parameters
        ----------
        x : int
            x location
        y : int
            y location
        board : list
            the matrix storage of the chessboard

        Returns
        -------
        bool
            True if the desired spot is legal, False if the spot
            is an illegal move
        """
        pass

    @abstractmethod
    def turn_moves(self, board):
        """ Gets all of the legal moves a piece can make.

        Parameters
        ----------
        board : list
            the matrix storage of the chessboard

        Returns
        -------
        list
            a list of all of the possible moves a specific piece
            can make for the current turn
        """
        pass
    