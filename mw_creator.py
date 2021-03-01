import numpy as np
from random import randrange

class Minesweper:
    def __init__(self,size,num_mine):
        """
        Creates a square board of Minesweper of a given size and
        number of mines. The conventions for the board is as follows:
        Any integer >= 0 is a number and mines are encoded as -1
        """
        self.size = size
        self.num_mine = num_mine
        self._board = None
        self._zeros = None

    def __repr__(self):
        return self.board.__repr__()

        

    @property
    def board(self):            # creates the board once and for all
        if self._board is None:
            self._board = self.minesweper(self.size,self.num_mine)
            return self._board
        return self._board


    def add_nghb(self,row,col,mines):
        """
        Given a mine position updates its neighbors so that the
        numbers on the board are created and are correct
        """
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
        """
        The main function that creates the board given a size and
        number of mines
        """
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
        This is the class to "play" the game. It takes a Minesweper board
        as the only argument. The conventions are as follows:
        The board is stored as a string array.
        - denotes an unopened cell
        x denotes a flagged cell
        ? denotes a question-flagged cell
        We further count the number of moves that the player plays
        this includes opening 0 cells. So a player who wins the game will have
        done at least size**2 moves. 
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
        """ Open the cell row,col """
        size = self.size
        if self.board[row,col] in self.playable:
            self.num_moves += 1
            self.tot_moves += 1
            
            val = self.mw.board[row,col]
            if val == -1:
                return(self.num_moves)
            self.board[row,col] = str(val)
            
            if self.mw.board[row,col] == 0:
                # When you open an empty cell
                # all the neighboring cells should be opened
                # this is probably not the most efficient way of doing this
                # but for a smaller board sizes it should be just fine
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
        """ Flag the cell as a mine """ 
        self.tot_moves += 1
        if self.board[row,col] in self.playable:

            self.num_mine_left -= 1
            self.board[row,col] = 'x'
        return self.board

    def flag_q(self,row,col):
        """ Flags it as a question mark """
        self.tot_moves += 1
        if self.board[row,col] in self.playable:
            self.board[row,col] = '?'
        return self.board

    def unflag(self,row,col):
        """ Unflags the cell """ 
        self.tot_moves += 1
        if self.board[row,col] in ['x','?']:
            self.board[row,col] = '-'
        return self.board
        
    




m = Minesweper(5,4)
p=Player(m)
