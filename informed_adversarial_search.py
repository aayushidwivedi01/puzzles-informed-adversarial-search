############################################################
# CIS 521: Homework 3
############################################################

student_name = "Aayushi Dwivedi"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random
import  copy 
from Queue import PriorityQueue

############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    return TilePuzzle([[(r*cols) + c +1 if (r*cols) + c +1 < rows*cols \
                     else 0 for c in xrange(cols)] for r in xrange(rows)]);
    


class TilePuzzle(object):
    
    # Required
    def __init__(self, board):
        self.board = board;
        self.rows = len(board);
        self.cols = len(board[0]);
        self.goal = [[(r*self.cols) + c +1 if (r*self.cols) + c +1 < self.rows*self.cols \
                    else 0 for c in xrange(self.cols)] for r in xrange(self.rows)];

        for i in xrange(self.rows):
          for j in xrange(self.cols):
            if self.board[i][j] == 0:
              (self.i, self.j) = i,j;

    def get_board(self):
        return self.board;

    def perform_move(self, direction):
        if direction == "up":
            if  self.i - 1 >=0:
                (self.board[self.i - 1][self.j], self.board[self.i][self.j])=\
                    (self.board[self.i][self.j], self.board[self.i - 1][self.j]);
                self.i = self.i - 1;
                return True;
            else:
                return False;
       
        if direction == "down":
            if  self.i + 1 < self.rows:
                (self.board[self.i + 1][self.j], self.board[self.i][self.j])=\
                    (self.board[self.i][self.j], self.board[self.i + 1][self.j]);
                self.i = self.i + 1;
                return True;
            else:
                return False;

        if direction == "right":
            if  self.j + 1 < self.cols:
                (self.board[self.i][self.j + 1], self.board[self.i][self.j ])=\
                    (self.board[self.i][self.j], self.board[self.i ][self.j + 1]);
                self.j = self.j + 1;
                return True;
            else:
                return False;

        if direction == "left":
            if  self.j - 1 >= 0:
                (self.board[self.i][self.j - 1], self.board[self.i][self.j])=\
                    (self.board[self.i][self.j], self.board[self.i][self.j - 1]);
                self.j = self.j - 1;
                return True;
            else:
                return False;
           

    def scramble(self, num_moves):
        seq = ["up", "down", "right", "left"];
        for i in xrange(num_moves):
            self.perform_move(random.choice(seq));
    
    def get_goal(self):
        return self.goal;
    def is_solved(self):
        if self.board == self.goal:
            return True;
        else:
            return False;
    
    def copy(self):
        return TilePuzzle(copy.deepcopy(self.get_board()));
    
    def successors(self):
        new_board = self.copy();
        if new_board.perform_move("up"):
            yield ("up", new_board);
        
        new_board = self.copy();
        if new_board.perform_move("down"):
            yield ("down", new_board);
        
        new_board = self.copy();
        if new_board.perform_move("right"):
            yield ("right", new_board);

        new_board = self.copy();
        if new_board.perform_move("left"):
            yield ("left", new_board);


    def iddfs_helper(self, limit, moves):
        if limit == len(moves):
            yield (moves, self);
        else:
            for (direction, new_board) in self.successors():
                if (new_board.is_solved()):
                    yield (moves + [direction], new_board);
                else:
                    for (updated_moves, config) in  new_board.iddfs_helper(limit, moves + [direction]):
                        yield (updated_moves, config);

    # Required
    def find_solutions_iddfs(self):
        limit = 0;
        found = False
        while not found:
            for (moves, config) in self.iddfs_helper(limit, []):
                if config.is_solved():
                    yield moves;
                    found = True;        
            limit += 1;
    
    def create_goal_indicies(self):
        self.goal_indices = dict((self.goal[i][j],(i,j)) for i in xrange(self.rows) for j in xrange(self.cols));

    def manhattan_distance(self, board):
        distance = 0;
        for r1 in xrange(self.rows):
            for c1 in xrange(self.cols):
                (r2, c2) = self.goal_indices[board[r1][c1]]
                distance += (abs(r1-r2) + abs(c1 -c2));       
        return distance
    # Required
    def find_solution_a_star(self):
        if (self.is_solved()):
            return [];
        self.create_goal_indicies();        
        frontier = PriorityQueue();
        frontier.put((self.manhattan_distance(self.board), ([],self)));
        explored = set();
        explored.add( tuple (tuple(row) for row in self.get_board()))
        while not frontier.empty():
            (distance, (moves, config)) = frontier.get();
            for (new_move, new_config) in config.successors():
                solution = moves + [new_move];
                if new_config.is_solved():
                    return solution;
                state = (solution, new_config);
                new_board = tuple(tuple(row) for row in new_config.get_board());
                if new_board not in explored:
                    frontier.put((self.manhattan_distance(new_config.get_board())\
                                    +len(solution),state));
                    explored.add(new_board);

############################################################
# Section 2: Grid Navigation
############################################################

def valid_successors(row, col, scene):
    #up
    if row - 1 >= 0 and not scene[row -1][col]:
        yield (row -1, col);
    #down
    if row + 1 < len(scene) and not scene[row + 1][col]:
        yield (row + 1, col);
    #left
    if col - 1 >= 0 and not scene[row][col - 1]:
        yield (row, col - 1);
    #right
    if col + 1 < len(scene[0]) and not scene[row][col + 1]:
        yield (row, col + 1);
    #up-left
    if col - 1 >= 0 and row - 1 >= 0 and not scene[row-1][col - 1]:
        yield (row -1, col - 1);
    #up-right
    if col + 1 < len(scene[0]) and row - 1 >=0 and not scene[row - 1][col + 1]:
        yield (row - 1, col + 1);
    #down-left
    if col - 1 >= 0 and row + 1 < len(scene) and not scene[row + 1][col - 1]:
        yield (row + 1, col - 1);
    #down-right
    if col + 1 < len(scene[0]) and row + 1 < len(scene) and not scene[row + 1][col + 1]:
        yield (row + 1, col + 1);

def euclidean_distance(start, goal):
    return ((start[0] - goal[0])**(2) + (start[1] - goal[1])**(2))**(0.5) 

def find_path(start, goal, scene):
    if (start == goal):
        return [];
    if (scene[start[0]][start[1]] or scene[goal[0]][goal[1]]):
        return None;
    frontier = PriorityQueue();
    frontier.put((euclidean_distance(start, goal), ([start], start,0)));
    explored = set();
    configs_in_frontier = dict();
    configs_in_frontier[start] = 0; 
    while not frontier.empty():
        (distance, (moves, curr_pos, g)) = frontier.get();
        explored.add(curr_pos);
        for new_move in valid_successors(curr_pos[0], curr_pos[1], scene):
            solution = moves + [new_move];
            if new_move == goal:
                return solution;
            new_g =  g + euclidean_distance(curr_pos, new_move)
            state = (solution, new_move, new_g);
            if new_move not in explored:
                if new_move not in configs_in_frontier or\
                (new_move in configs_in_frontier and\
                new_g < configs_in_frontier[new_move]):
                    frontier.put((euclidean_distance(new_move, goal) + state[2], state));
                    configs_in_frontier[new_move] = new_g;
    return None

############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

def create_distinct_disks(l, n):
    return [ i + 1  if i < n else 0 for i in xrange(l)];

def distinct_successors(puzzle, length):
    for loc in xrange(length):
        if  not puzzle[loc]:
            continue;
        old_puzzle = puzzle[:];
        if loc + 1 < length and old_puzzle[loc +1] \
            and loc + 2 < length and not old_puzzle[loc + 2]:
            old_puzzle[loc], old_puzzle[loc + 2] = old_puzzle[loc + 2], old_puzzle[loc]
            yield ( (loc, loc + 2), old_puzzle);
            old_puzzle = puzzle[:]

        if loc + 1 < length and not old_puzzle[loc + 1] :
            old_puzzle[loc], old_puzzle[loc +1] = old_puzzle[loc +1], old_puzzle[loc]
            yield ( (loc, loc +1), old_puzzle);
            old_puzzle = puzzle[:]

        if loc - 1 >= 0 and old_puzzle[loc - 1] \
            and loc -  2 >= 0 and  not old_puzzle[loc - 2]:
            old_puzzle[loc - 2], old_puzzle[loc] = old_puzzle[loc], old_puzzle[loc - 2]
            yield ( (loc, loc -  2), old_puzzle);
            old_puzzle = puzzle[:]

        if loc - 1 >= 0 and not old_puzzle[loc - 1] :
            old_puzzle[loc - 1], old_puzzle[loc] = old_puzzle[loc], old_puzzle[loc - 1]
            yield ( (loc, loc - 1), old_puzzle);
            old_puzzle = puzzle[:]

def distance(puzzle):
    l = len(puzzle)
    return sum([ (abs(l - val - i))/2 + abs( (l - val - i)) % 2\
             for (i, val) in enumerate(puzzle) if val > 0]);


def solve_distinct_disks(length, n):
    puzzle = [ i + 1  if i < n else 0 for i in xrange(length)];
    goal = [ 0 if i < length - n else length - i  for i in xrange(length)];
    if length == 0 or puzzle == goal:
        return [];
    frontier = PriorityQueue();
    frontier.put((distance(puzzle), ([],puzzle)));
    explored = set();
    while not frontier.empty():
        (future_cost, (move, config)) = frontier.get();
        explored.add(tuple(config));
        for (new_move, new_config) in distinct_successors(config, length):
            solution = move + [new_move]
            if (new_config == goal):
                return solution;
            state = (solution, new_config);

            if tuple(new_config) not in explored:
                frontier.put((distance(new_config) + len(solution), state));
    return None
    

############################################################
# Section 4: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    return DominoesGame([[False] * cols for r in xrange(rows)])

class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = board;
        self.rows = len(board);
        self.cols = len(board[0]);
    def get_board(self):
        return self.board;

    def reset(self):
        self.board = [[False] * self.cols for r in xrange(self.rows)]; 

    def is_legal_move(self, row, col, vertical):
        if row < 0 or row >= self.rows \
        or col < 0 or col >= self.cols \
        or self.board[row][col]:
            return False;
        if vertical:
            if row + 1 < self.rows and not self.board[row +1][col]:
                return True;
            else:
                return False;
        else:
            if col + 1 < self.cols and not self.board[row][col +1]:
                return True;
            else:
                return False;

    def legal_moves(self, vertical):
        for row in xrange(self.rows):
            for col in xrange(self.cols):
                if self.is_legal_move(row, col, vertical):
                    yield (row, col);
        


    def perform_move(self, row, col, vertical):
        seq = [1,0];
        if not vertical:
            seq =[0,1];
        self.board[row][col] = True;
        self.board[row+seq[0]][col + seq[1]] = True;
        

    def game_over(self, vertical):
        moves = list(self.legal_moves(vertical));
        if len(moves) == 0:
            return True;
        else:
            return False;

    def copy(self):
        new_board = copy.deepcopy(self.board);
        return DominoesGame(new_board);

    def successors(self, vertical):
        for (row, col) in self.legal_moves(vertical):
            new_game = self.copy();
            new_game.perform_move(row, col, vertical);
            yield ((row, col), new_game);

    def get_random_move(self, vertical):
        moves = list(self.legal_moves(vertical));
        return random.choice(moves);
    
    def evaluate(self, vertical):
        v = list(self.legal_moves(vertical));
        s = list(self.legal_moves(not vertical));
        return  len(v) - len(s);

    def max_value(self, vertical, limit, alpha, beta):
        if limit ==  0 or self.game_over(vertical):
            return (None, self.evaluate(vertical), 1);
        
        v = -float('inf');
        num_leaves = 0;
        best_move = [-1, -1]
        for ((row, col), new_game) in self.successors(vertical):
            (child_move,s, leaves) =  new_game.min_value(not vertical, limit - 1, alpha, beta);
            if v < s:
                best_move = [row, col];
                v = s;
            num_leaves += leaves;
            if  v >= beta:
                return (tuple(best_move), v, num_leaves);
            alpha = max(alpha, v);
        return (tuple(best_move), v, num_leaves);

    def min_value(self, vertical, limit, alpha, beta):
        if limit == 0 or self.game_over(vertical):
            return (None, self.evaluate(not vertical), 1);
        v = float('inf');
        num_leaves = 0;
        for ((row,col), new_game) in self.successors(vertical):
            (child_move, s, leaves) = new_game.max_value(not vertical, limit - 1, alpha, beta);
            v = min(v, s);
            num_leaves += leaves;
            if v <= alpha:
                return ((), v, num_leaves);
            beta = min(beta, v);
        return ((), v, num_leaves);
            
        
    # Required
    def get_best_move(self, vertical, limit):
        return self.max_value(vertical, limit, -float('inf'), float('inf'))

############################################################
# Section 5: Feedback
############################################################

feedback_question_1 = """
20 hrs
"""

feedback_question_2 = """
Optimizing Grid navigation.
Took a while to figure out heuristics fuction for
linear disk movements. 
"""

feedback_question_3 = """
I liked problem 3 because it gave a comparision
between something I had previously implemented.
No, I wouldn't change anything about this assignment.
"""
