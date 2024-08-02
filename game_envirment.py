import pygame
import numpy as np
import random

from tools import display_data

class game_envirment:
    def __init__(self):
        self.board = np.zeros((display_data.GRID_SIZE, display_data.GRID_SIZE), dtype=int)
        self.add_random_tile()
        self.add_random_tile()
        self.success = False
        self.fail = False
    
    def reset(self):
        self.board = np.zeros((display_data.GRID_SIZE, display_data.GRID_SIZE), dtype=int)
        self.add_random_tile()
        self.add_random_tile()
        self.success = False
        self.fail = False
    
    # 添加随机方块
    def add_random_tile(self):
    # 找到所有空白格子的位置
        empty_cells = [(row, col) for row in range(display_data.GRID_SIZE) for col in range(display_data.GRID_SIZE) if self.board[row, col] == 0]
        if empty_cells:
            # 在随机位置生成一个2或者4
            row, col = random.choice(empty_cells)
            self.board[row, col] = random.choice([2 ,2 ,2 ,2 ,4]) # 2的概率是80%，4的概率是20%
    
    # 处理移动和合并逻辑
    def slide(self, row):
        # 将非零元素滑向一侧，合并相同元素
        non_zero_tiles = [tile for tile in row if tile != 0]
        new_row = []
        i = 0
        while i < len(non_zero_tiles):
            if i + 1 < len(non_zero_tiles) and non_zero_tiles[i] == non_zero_tiles[i + 1]:
                new_row.append(non_zero_tiles[i] * 2)
                i += 2
            else:
                if(non_zero_tiles[i] >= 2048):
                    self.success = True
                new_row.append(non_zero_tiles[i])
                i += 1
        # 补充空白
        new_row += [0] * (display_data.GRID_SIZE - len(new_row))
        return new_row
    
    def move(self, direction):
        board_changed = []
        if direction == pygame.K_LEFT:
            board_changed = np.array([self.slide(row) for row in self.board])
        elif direction == pygame.K_RIGHT:
            board_changed = np.array([self.slide(row[::-1])[::-1] for row in self.board])
        elif direction == pygame.K_UP:
            board_changed = np.transpose([self.slide(col) for col in np.transpose(self.board)])
        elif direction == pygame.K_DOWN:
            board_changed = np.transpose([self.slide(col[::-1])[::-1] for col in np.transpose(self.board)])
        if(self.board != board_changed).any():
            self.board = board_changed
            self.add_random_tile()
            
                
                
    def check_can_move(self):
        board_changed_left = np.array([self.slide(row) for row in self.board])
        board_changed_right = np.array([self.slide(row[::-1])[::-1] for row in self.board])
        board_changed_up = np.transpose([self.slide(col) for col in np.transpose(self.board)])
        board_changed_down = np.transpose([self.slide(col[::-1])[::-1] for col in np.transpose(self.board)])
        if(board_changed_left == self.board).all() and (board_changed_right == self.board).all() and (board_changed_up == self.board).all() and (board_changed_down == self.board).all():
                self.fail = True