"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    pass


def custom_score(game, player):
    return float(len(game.get_legal_moves(player))-len(game.get_legal_moves(game.get_opponent(player))))  
    

def custom_score_2(game, player):
##partitioning checker
    
   (x1,y1)=game.get_player_location(player)
   (x2,y2)=game.get_player_location(game.get_opponent(player))
   part = False
   
   if(abs(x1-x2)>1):
       moves=[m for m in game.get_blank_spaces() if (m[1]>min(x1,x2) and m[1]<max(x1,x2))]
       for x in range(min(x1,x2)+1,max(x1,x2)):
           if(part):
               break
           else:
               for y in range(0,game.height+1):
                   if((y,x) in moves):
                       part=False
                       break
                   else:
                       part=True

   if(part==False):               
       if(abs(y1-y2)>1):
           moves=[m for m in game.get_blank_spaces() if (m[0]>min(y1,y2) and m[0]<max(y1,y2))]
           for y in range(min(y1,y2)+1,max(y1,y2)):
               if(part):
                   break
               else:
                   for x in range(0,game.width+1):
                       if((y,x) in moves):
                           part=False
                           break
                       else:
                           part=True
   if(part==True):
       return float(2*(len(game.get_legal_moves(player))-len(game.get_legal_moves(game.get_opponent(player)))))
   else:
       return float(len(game.get_legal_moves(player))-len(game.get_legal_moves(game.get_opponent(player))))


def custom_score_3(game, player):

    (x1,y1)=game.get_player_location(player)
    (x2,y2)=game.get_player_location(game.get_opponent(player))
    
    Cy=game.height/2
    Cx=game.width/2
    
    dist1=((x1-Cx)**2+(y1-Cy)**2)**(1/2)
    dist2=((x2-Cx)**2+(y2-Cy)**2)**(1/2)
    
    return float(len(game.get_legal_moves(player))-len(game.get_legal_moves(game.get_opponent(player))) - 0.5*(dist1-dist2))

class IsolationPlayer:

    def __init__(self, search_depth=3, score_fn=custom_score_3, timeout=10.):
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
        
        if self.time_left()< self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        if self.terminal_test(game,game.active_player):
            return (-1,-1) # No valid Moves            
        else:
            for m in game.get_legal_moves(game.active_player):
                v = self.min_value(game.forecast_move(m), search_depth - 1)
                if v > best_score:
                    best_score = v
                    best_move = m
        return best_move
    
    
    def min_value(self,game,search_depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        if self.terminal_test(game,game.active_player):
            return float("inf")  # win
        
        v = float("inf")           
        if search_depth<=0:
            return self.score(game,self)

        else:                
            for m in game.get_legal_moves(game.active_player):
                v = min(v, self.max_value(game.forecast_move(m),search_depth-1))
        return v
    
    
    def max_value(self,game,search_depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        if self.terminal_test(game,game.active_player):
            return float("-inf")  # loss
        
        v = float("-inf")          
        if search_depth<=0:
            return self.score(game,self)

        else:           
            for m in game.get_legal_moves(game.active_player):
                v = max(v, self.min_value(game.forecast_move(m),search_depth-1))
        return v



class AlphaBetaPlayer(IsolationPlayer):
    
    def terminal_test(self,game,player):

        return not bool(game.get_legal_moves(player))

    def get_move(self, game, time_left):
  
        self.time_left = time_left
        best_move = (-1, -1)
        search_depth=1
        
        
        try:
            while(1):
                best_move=self.alphabeta(game, search_depth)
                search_depth+=1
                    
        except SearchTimeout:
            return best_move

        return best_move
    
    
    def alphabeta(self, game, search_depth, alpha=float("-inf"), beta=float("inf")):

        best_score = float("-inf")
        best_move = (-1,-1)
        
        if self.time_left()< self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        if self.terminal_test(game,game.active_player):
            return best_move  # no valid moves
                   
        else:
            
            for m in game.get_legal_moves(game.active_player):
                #max->min
                v = self.min_value(game.forecast_move(m), search_depth - 1,alpha,beta)
                if v > best_score:
                    best_score = v
                    best_move = m
                alpha = max(alpha, v)
                if best_score >= beta:
                    return best_move
        return best_move
        
    def min_value(self,game,search_depth,alpha,beta):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        if self.terminal_test(game,game.active_player):
            return float("inf")  # win
        
        v = float("inf")           
        if search_depth<=0:
            return self.score(game,self)
        

        else:                
            for m in game.get_legal_moves(game.active_player):
                v = min(v, self.max_value(game.forecast_move(m),search_depth-1,alpha,beta))               
                if v<=alpha:
                    return v
                beta=min(v,beta)                           

        return v
    
    def max_value(self,game,search_depth,alpha,beta):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        if self.terminal_test(game,game.active_player):
            return float("-inf")  # loss
        
        v = float("-inf")          
        if search_depth<=0:
            return self.score(game,self)
        
        else:           
            for m in game.get_legal_moves(game.active_player):
                v = max(v, self.min_value(game.forecast_move(m),search_depth-1,alpha,beta))               
                if v>=beta:
                    return v
                alpha=max(alpha,v)
        return v    
    
    

        
    

