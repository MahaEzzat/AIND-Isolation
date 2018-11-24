"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    print("TimeOut")
    pass


def custom_score(game, player):
    return len(game.get_legal_moves(player))/(81.0)   
    

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    raise NotImplementedError


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    raise NotImplementedError


class IsolationPlayer:

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=30.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


    
class MinimaxPlayer(IsolationPlayer):

    def terminal_test(self,game,player):

        return not bool(game.get_legal_moves(player))
    
    def get_move(self, game, time_left):
  
        self.time_left = time_left
        best_move = (-1, -1)
        
        try:
            return self.minimax(game, self.search_depth)
        
        except SearchTimeout:
            return best_move

        return best_move
    
    
    def minimax(self,game, search_depth):

        best_score = float("-inf")
        best_move = (-1,-1)
        player=game._active_player
        
        if self.time_left< self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        else:
            for m in game.get_legal_moves(game.active_player):
                v = self.min_value(game.forecast_move(m), search_depth - 1,player)
                if v > best_score:
                    best_score = v
                    best_move = m
                if self.time_left < self.TIMER_THRESHOLD:
                    raise SearchTimeout()
        return best_move
    
    
    def min_value(self,game,search_depth,player):

        if self.terminal_test(game,game.active_player):
            return 1  # win
        
        v = float("inf")           
        if search_depth<=0:
            return self.score(game,player)
        
        if self.time_left < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        else:                
            for m in game.get_legal_moves(game.active_player):
                v = min(v, self.max_value(game.forecast_move(m),search_depth-1,player))
                if self.time_left < self.TIMER_THRESHOLD:
                    raise SearchTimeout()
        return v
    
    
    def max_value(self,game,search_depth,player):
        
        if self.terminal_test(game,game.active_player):
            return -1  # loss
        
        v = float("-inf")          
        if search_depth<=0:
            return self.score(game,player)
        
        if self.time_left < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        else:           
            for m in game.get_legal_moves(game.active_player):
                v = max(v, self.min_value(game.forecast_move(m),search_depth-1,player))
                if self.time_left < self.TIMER_THRESHOLD:
                    raise SearchTimeout()
        return v



class AlphaBetaPlayer(IsolationPlayer):
    
    def terminal_test(self,game,player):

        return not bool(game.get_legal_moves(player))
    
    
    def max_value(self,game,search_depth,player,alpha_beta):
        
        if self.terminal_test(game,game.active_player):
            return -1  # loss
        
        v = float("-inf")          
        if search_depth<=0:
            return self.score(game,player)
        
        if self.time_left < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        else:           
            for m in game.get_legal_moves(game.active_player):
                v = max(v, self.min_value(game.forecast_move(m),search_depth-1,player,alpha_beta))

                if alpha_beta[0] == float("-inf"):
                    alpha_beta[0]=v
                else:
                    if v>=alpha_beta[1]:
                        return v
                    alpha_beta[0]=max(alpha_beta[0],v)   
                print("Max_value: ",alpha_beta)
                if self.time_left < self.TIMER_THRESHOLD:
                    raise SearchTimeout()                

                
        return v    
    
    
    def min_value(self,game,search_depth,player,alpha_beta):

        if self.terminal_test(game,game.active_player):
            return 1  # win
        
        v = float("inf")           
        if search_depth<=0:
            return self.score(game,player)
        
        if self.time_left < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        else:                
            for m in game.get_legal_moves(game.active_player):
                v = min(v, self.max_value(game.forecast_move(m),search_depth-1,player,alpha_beta))
                if alpha_beta[1] == float("inf"):
                    alpha_beta[1]=v
                else:  
                    if v<=alpha_beta[0]:
                        return v
                    alpha_beta[1]=min(v,alpha_beta[1])
                if self.time_left < self.TIMER_THRESHOLD:
                    raise SearchTimeout()               
                print("Min_value: ",alpha_beta)
                
        return v
        
    
    def get_move(self, game, time_left):
  
        self.time_left = time_left
        best_move = (-1, -1)
        search_depth=1
        
        while(1):
            try:
                best_move=self.alphabeta(game, search_depth)
                print("Search_depth: ",search_depth)
                search_depth+=1
                    
            except SearchTimeout:
                return best_move

        return best_move
    
    
    def alphabeta(self, game, search_depth, alpha=float("-inf"), beta=float("inf")):

        best_score = float("-inf")
        best_move = (-1,-1)
        player=game._active_player
        alpha_beta=[0]*2
        alpha_beta[0]=alpha
        alpha_beta[1]=beta
        
        if self.time_left< self.TIMER_THRESHOLD:
            raise SearchTimeout()
        else:
            for m in game.get_legal_moves(game.active_player):
                #max->min
                print("alphabeta: ",alpha_beta)
                v = self.min_value(game.forecast_move(m), search_depth - 1,player,alpha_beta)
                if v > best_score:
                    best_score = v
                    best_move = m
                if self.time_left < self.TIMER_THRESHOLD:
                    raise SearchTimeout()
        return best_move
    
