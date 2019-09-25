#!/usr/bin/env python3

'''
By: Brandon Beckwith, Diep Nguyen
'''

from functools import total_ordering
from math import floor
from copy import deepcopy
from queue import PriorityQueue
import argparse

'''
Calculates the manhatten distance between tiles on two boards
'''
def manhatten_distance(board, goal, xdim):
    total = 0

    # Create two hashes that map the tile number to it's position
    bord = {board[i]: (floor(i % xdim), floor(i/xdim)) for i in range(0, len(board))}
    gord = {goal[i]: (floor(i % xdim), floor(i/xdim)) for i in range(0, len(goal))}

    # Use a lookup to find the manhatten distance between two tiles
    for k,b in bord.items():
        g = gord[k]

        total += abs(g[0] - b[0]) + abs(g[1] - b[1])

    return total

'''
Returns the number of tiles that aren't in the correct spot
'''
def in_correct_spot(board, goal, xdim):
    return sum([1 for i in range(0, len(board)) if board[i] != goal[i]])

'''
A board class used to store the various board states

Total_ordering is used to implement comparison operations
'''
@total_ordering
class Board:

    HEUR_FUNC = in_correct_spot
    GOAL_BOARD = [1,2,3,4,5,6,7,8,0]
    X_DIM = 3
    Y_DIM = 3
    BLANK = 0

    def __init__(self, board, parent):
        self.board = board
        self.g = 0
        self.parent = None

        if parent != None:
            self.parent = parent
            self.g = parent.g + 1

        self.h = Board.HEUR_FUNC(board, Board.GOAL_BOARD, Board.X_DIM)
        self.f = self.g + self.h
        pass

    '''
    Checks to see if the x/y coordinate is valid
    '''
    def is_bad(self, x, y):
        return x < 0 or x >= Board.X_DIM or y < 0 or y >= Board.Y_DIM

    '''
    Gets the square level at the x/y
    '''
    def get(self, x, y):
        if self.is_bad(x,y):
            return -1

        return self.board[x + y * Board.X_DIM]

    '''
    Finds the blank tile's x/y and returns them
    '''
    def get_blank_index(self):
        tmp = self.board.index(Board.BLANK)
        return (floor(tmp % Board.X_DIM), floor(tmp / Board.X_DIM))

    '''
    Sets a tile to a new value
    '''
    def set(self, x, y, val):
        if self.is_bad(x,y):
            return False
        
        self.board[x + y * Board.X_DIM] = val
        return True

    '''
    Swaps two tiles based on x/y coordinates
    '''
    def swap(self, x1, y1, x2, y2):
        if self.is_bad(x1,y1) or self.is_bad(x2, y2):
            return False
        
        tmp = self.get(x1, y1)

        if not self.set(x1, y1, self.get(x2, y2)):
            return False

        if not self.set(x2, y2, tmp):
            return False

        self.h = Board.HEUR_FUNC(self.board, Board.GOAL_BOARD, Board.X_DIM)

        self.f = self.g + self.h
        return True

    '''
    Get a list of valid child boards
    '''
    def get_children(self):
        (x,y) = self.get_blank_index()
        out = []

        for (nx, ny) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:

            if self.is_bad(x + nx, y + ny):
                continue

            child = Board(deepcopy(self.board), self)
            child.swap(x, y, x + nx, y + ny)
            out.append(child)

        return out

    '''
    A recursive method used to print the path
    '''
    def print_path(self):
        total = 1
        if not self.parent == None:
            total += self.parent.print_path()
        
        print(self)
        print("g: %d, h: %d, f(x): %d" % (self.g, self.h, self.f))
        print("-----------------------------------")
        return total

    '''
    Goal test, returns true if goal
    '''
    def is_goal(self):
        return self.board == Board.GOAL_BOARD

    '''
    A static method used to check to see if the board is valid
    '''
    @staticmethod
    def verify(board):
        return len(board) == Board.X_DIM * Board.Y_DIM

    '''
    Essentially too string
    '''
    def __str__(self):
        out = "+-----+\n"
        for y in range(0, Board.Y_DIM):
            for x in range(0, Board.X_DIM):
                out += "|" + str(self.get(x,y))
            out += "|\n" 
        out += "+-----+"
        return out

    '''
    Allows the object be printed from the interactive terminal
    '''
    def __repr__(self):
        return self.__str__()

    '''
    Override the equal-to comparison operator
    Allows us to use the built in priority queue
    '''
    def __eq__(self, other):
        try:
            return self.f == other.f
        except AttributeError:
            return NotImplemented
        except:
            raise

    '''
    Override the less-than comparison operator.
    Allows us to use the built in priority queue
    '''
    def __lt__(self, other):
        try:
            return self.f < other.f
        except AttributeError:
            return NotImplemented
        except:
            raise

'''
A simple A* algorthm wrapped in a class
'''
class AStar:

    '''
    Initialize the AStar class
    start = starting board
    goal = desired board state
    heuristic = heuristic function
    '''
    MAX_ITERATIONS = 500000

    def __init__(self, start, goal, heuristic):
        Board.GOAL_BOARD = goal
        Board.HEUR_FUNC = heuristic

        self.frontier = PriorityQueue()
        self.seen = {tuple(start): True}
        self.start = Board(start, None)

        self.frontier.put(self.start)
        self.end = self.start
        self.iterations = 0
        self.generated = 0
    
    '''
    Runs the a start and attempts to figure out a path
    '''
    def find_goal(self):

        while not self.frontier.empty():
            self.end = self.frontier.get()

            if self.end.is_goal():
                return True

            for child in self.end.get_children():
                if not tuple(child.board) in self.seen:
                    self.seen[tuple(child.board)] = True
                    self.frontier.put(child)
                    self.generated += 1

            self.iterations += 1

            if self.iterations >= AStar.MAX_ITERATIONS:
                return False

        return False

    '''
    Prints the path from start to finish along with the number of moves and iterations
    '''
    def print_path(self):
        total = self.end.print_path()
        print("Number of moves: %d" % (total))
        print("Iterations needed: %d" % (self.iterations))
        print("Nodes Generated: %d" % (self.generated))
    
    def __str__(self):
        pass


def main():

    #Parse user input
    parser = argparse.ArgumentParser(description="Runs the A* algorithm")
    parser.add_argument('-s', '--start', type=str, help='The tiles for the initial state')
    parser.add_argument('-g', '--goal', type=str, help='The tiles for the goal state')
    parser.add_argument('-p', '--position', action='store_true', help='Use position correctness for the heuristic, instead of Manhatten Distance')
    args = parser.parse_args()

    #Check user input
    if args.start == None or args.goal == None:
        desc = '''
        Runs A* on a given set of boards.

        Boards are input as a string of numbers read from left to right, top to bottom.
        +-----+
        |1|2|3|
        |4|5|6| -> 123456780
        |7|8|0|
        +-----+
        '''
        print(desc)
        parser.print_help()
        return -1

    #Verify the board is eligable
    if not Board.verify(args.start) or not Board.verify(args.goal):
        print("A board doesn't contain the right number of elements!")
        return -1

    #Convert the input to numerical arrays
    start = [int(c) for c in args.start]
    goal = [int(c) for c in args.goal]
    
    #Run A* using the given heuristic
    star = None
    if args.position:
        star = AStar(start, goal, in_correct_spot)
    else:
        star = AStar(start, goal, manhatten_distance)

    #Print the path
    if star.find_goal():
        star.print_path()
        return 0

    if (star.iterations >= star.MAX_ITERATIONS):
        print("Max number of iterations exceeded")

    print("Path couldn't be found :(")
    return -1

if __name__ == "__main__":
    main()
