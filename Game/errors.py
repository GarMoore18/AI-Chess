class AIDoesNotExist(Exception):
    """ Custom exception for AI selection. 
    
    There are only two AIs, so the user must
    select a valid number.
    """
    pass

class TooManyMoves(Exception):
    """ Custom exception for AI move depth. 
    
    The AIs become too slow to play if the
    look ahead depth is set too high.
    """
    pass
