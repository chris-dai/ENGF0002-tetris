from board import Direction, Rotation
from random import Random


class Player:
    def choose_action(self, board):
        raise NotImplementedError


class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def choose_action(self, board):
        return self.random.choice([
            Direction.Left,
            Direction.Right,
            Direction.Down,
            Rotation.Anticlockwise,
            Rotation.Clockwise,
            Direction.Drop
        ])

a = -0.510066 # agg_height
b = 0.760666 # complete_lines
c = -0.35663 # holes
d = -0.184483 # bumpiness

class Chris:

    def choose_action(self,board):
        final_move = []
        rot, pos = self.choose_best_move(board)
        for i in range(rot):
            final_move.append(Rotation.Clockwise)
        if pos < 0:
            for i in range(abs(pos)):
                final_move.append(Direction.Left)
        if pos > 0:
            for i in range(pos):
                final_move.append(Direction.Right)
        final_move.append(Direction.Drop)
        return final_move
    
    def best_score(self, board, rotation, x):
        game_copy = board.clone()
        old_score = game_copy.score
        for i in range (rotation):
            game_copy.rotate(Rotation.Clockwise)
        if x < 0:
            for i in range(abs(x)):
                game_copy.move(Direction.Left)
        if x > 0:
            for i in range(x):
                game_copy.move(Direction.Right)
        game_copy.move(Direction.Drop)

        agg_height_score = self.agg_height(game_copy)
        holes_score = self.holes(game_copy)
        bum_score = self.bumpiness(game_copy)
        complete_lines_score = self.complete_lines(game_copy.score - old_score)
        score = agg_height_score + holes_score + bum_score + complete_lines_score # heuristic score
        return score, game_copy

    def choose_best_move(self,board):
        ''' clone the board and do test move before real move - we try 40 possibilities'''
        max_score = -1000000
        try:
            for rotation in range(4): 
                for pos in range(-5,5):
                    score_current, new_board = self.best_score(board, rotation, pos)
                    lookahead_score = -1000000
                    for rotation2 in range(4): 
                        for pos2 in range(-5,5):
                            lookahead_score = max(lookahead_score, self.best_score(new_board, rotation2, pos2)[0])
                    score = score_current + lookahead_score
                    if score > max_score:
                        max_score = score
                        best_rot = rotation
                        best_pos = pos
        except Exception:
            best_rot = 0
            best_pos = 0
        return best_rot, best_pos

    def holes(self,board): 
        total_holes = 0
        for x in range (board.width):
            for y in range(board.height):
                if (x,y) in board.cells and (x,y+1) not in board.cells:
                    total_holes += 1
        holes_score = total_holes * c
        return holes_score

    def column_height(self,board):
        column_height = []  # [0,0,0,0,0,0,0,0,0,0]
        for x in range(board.width):
            for y in range(board.height):
                if (x,y) in board.cells:
                    column_height.append(board.height-y)  # column_height[x] = board.height - y
                    break
                if y == board.height-1:
                    column_height.append(0)
        return column_height

    def agg_height(self,board):
        return sum(self.column_height(board)) * a 
                
    def bumpiness(self, board):
        bump = 0            # adjacent column diff 
        heights = self.column_height(board)
        for x in range(0,9):
            bump += abs(heights[x] - heights[x+1])
        return bump * d



    def complete_lines(self,diff):
        if 100 < diff < 125:
            result = 1
        elif 400 < diff < 425:
            result = 2
        elif 800 < diff < 825:
            result = 3
        elif 1600 < diff < 1625:
            result = 4
        else:
            return 0
        
        return result * b

SelectedPlayer = Chris
