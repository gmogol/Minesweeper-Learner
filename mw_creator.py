import numpy as np
from random import randrange

class Minesweper:
    def __init__(self,size,num_mine):
        """
        Creates a square board of Minesweper of a given size and
        number of mines
        """
        self.size = size
        self.num_mine = num_mine
        self._board = None
        self._zeros = None

    def __repr__(self):
        return self.board.__repr__()

        

    @property
    def board(self):
        if self._board is None:
            self._board = self.minesweper(self.size,self.num_mine)
            return self._board
        return self._board


    def add_nghb(self,row,col,mines):
        size = self.size
        prev_row = max(0,row-1)
        prev_col = max(0,col-1)
        next_row = min(size-1, row+1)+1
        next_col = min(size-1,col+1)+1
        nghb = mines[prev_row:next_row , prev_col:next_col]
        nghb_mask = (nghb != -1)
        nghb = nghb + nghb_mask
        mines[prev_row:next_row , prev_col:next_col] = nghb
        return mines
        

    def minesweper(self,size,num_mine):
        if num_mine > size**2:
            raise Exception('Too many mines')
        mines = np.zeros([size,size],dtype = int)
        mine_loc = []
        while num_mine != 0:
            row = randrange(size)
            col = randrange(size)
                
            while mines[row,col] == -1:
                row = randrange(size)
                col = randrange(size)


            mines[row,col] = -1
            mine_loc.append((row,col))
            num_mine -= 1
            mines = self.add_nghb(row,col,mines)
        return mines

    
class Player():
    def __init__(self,mw):
        """

        """
        self.mw = mw
        size = mw.size
        self.size = size
        self.num_mine = mw.num_mine
        self.num_mine_left = mw.num_mine
        self.num_moves = 0
        self.tot_moves = 0
        board = np.empty([size,size],dtype = str)

        
        self.playable = ['-','?']
        board[:] = '-'
        
        self.board = board

        
        
    def open(self,row,col):
        size = self.size
        if self.board[row,col] in self.playable:
            self.num_moves += 1
            self.tot_moves += 1
            
            val = self.mw.board[row,col]
            if val == -1:
                return(self.num_moves)
            self.board[row,col] = str(val)
            
            if self.mw.board[row,col] == 0:
                
                prev_row = max(0,row-1)
                prev_col = max(0,col-1)
                next_row = min(size-1, row+1)
                next_col = min(size-1,col+1)
                
                self.open(prev_row,col)
                self.open(prev_row,prev_col)
                self.open(prev_row,next_col)
                
                self.open(row,prev_col)
                self.open(row,next_col)
                
                self.open(next_row,col)
                self.open(next_row,next_col)
                self.open(next_row,prev_col)
        return self.board
            

    def flag(self,row,col):
        self.tot_moves += 1
        if self.board[row,col] in self.playable:

            self.num_mine_left -= 1
            self.board[row,col] = 'x'
        return self.board

    def flag_q(self,row,col):
        self.tot_moves += 1
        if self.board[row,col] in self.playable:
            self.board[row,col] = '?'
        return self.board

    def unflag(self,row,col):
        self.tot_moves += 1
        if self.board[row,col] in ['x','?']:
            self.board[row,col] = '-'
        return self.board
        
    




m = Minesweper(5,4)
p=Player(m)
