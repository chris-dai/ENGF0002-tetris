from board import Direction, Rotation, Shape
from board import Position, Bitmap, Block
from random import random

a = -0.510066 # agg_height
b = 0.760666 # complete_lines
c = -0.35663 # holes
d = -0.184483 # bumpiness

class Player:

    # board.falling.move
    def choose_action(self,board):
        rot, pos = self.choose_best_move(board)
        final_move = [Rotation.Anticlockwise]*rot
        if pos < 0:
            final_move += [Direction.Left]*abs(pos)
        if pos > 0:
            final_move += [Direction.Right]*abs(pos)
        final_move.append(Direction.Drop)
        return final_move

    def game_copy(self,board):
        game_copy = board.clone()
        falling = board.falling.clone()
        rotate = board.rotate.clone()

    def choose_best_move(self,board):
        ''' clone the board and do test move before real move - we try 40 possibilities'''
        max_score = -1000000
        for rotation in range(4): 
            for x in range(-5,4): 
                game_copy = board.clone()
                old_score = game_copy.score
                for _ in range (rotation):
                    game_copy.move(Rotation.Anticlockwise)

                if x < 0:
                    for _ in range(abs(x)):
                        game_copy.move(Direction.Left)
                if x > 0:
                    for _ in range(x):
                        game_copy.move(Direction.Right)
                game_copy.move(Direction.Drop)

                agg_height_score = self.agg_height(game_copy)
                holes_score = self.holes(game_copy)
                bum_score = self.bumpiness(game_copy)
                complete_lines_score = self.complete_lines(game_copy.score - old_score)
                score = agg_height_score + holes_score + bum_score + complete_lines_score # heuristic score
                
                if score > max_score:
                    max_score = score
                    best_rot = rotation
                    best_x = x
        return best_rot, best_x
        
    def agg_height(self,board):
        total_height = 0
        for x in range (0, 9):
            for y in range(0, 24):
                if (x,y) in board.cells:
                    single_height = 24 - y
                    break
        total_height += single_height
        return total_height * a

    def holes(self,board): 
        total_holes = 0
        for x in range (0, 9):
            for y in range(0, 24):
                if (x,y) in board.cells and (x,y+1) not in board.cells:
                    total_holes += 1
        holes_score = total_holes * c
        return holes_score

    def column_height(self,board,x):
        column_height = [0,0,0,0,0,0,0,0,0,0]
        for y in range(0,24):
            for x in range(0,9):
                if (x,y) in board.cells:
                    column_height[x] = 24 - y
                    break
        return column_height
                
    def bumpiness(self,column_height):
        bump = 0            # adjacent column diff 
        for x in range(0,9):
            bump += abs(column_height[x] - column_height[x+1])
        bum_score = bump * d
        return bum_score

    # def column_height(self,board,x)
    #     column_height = 0
    #     for y in range(0,24):
    #         if (x,y) in board.cells:
    #             column_height = 24 - y
    #             break
    #     return column_height
    
    # def bumpiness(self,column_height):



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



    def score(self, board): # heuristic score
        score = 0
        agg_height_score = self.agg_height(board)
        bum_score = self.bumpiness(board)
        holes_score = self.holes(board)
        complete_lines_score = self.complete_lines(board)
        score = agg_height_score + bum_score + holes_score + complete_lines_score
        return score


SelectedPlayer = Player

# class RandomPlayer(Player):
#     def __init__(self, seed=None):
#         self.random = Random(seed)

#     def choose_action(self, board):
#         return self.random.choice([
#             Direction.Left,
#             Direction.Right,
#             Direction.Down,
#             Rotation.Anticlockwise,
#             Rotation.Clockwise,
#         ])
