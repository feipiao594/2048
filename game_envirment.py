import pygame
import numpy as np
import random

from tools import display_data


class game_envirment:
    def __init__(self):
        self.board = np.zeros(
            (display_data.GRID_SIZE, display_data.GRID_SIZE), dtype=int)
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()
        self.success = False
        self.fail = False
        self.score = 0

    def reset(self):
        self.__init__()

    def add_random_tile(self):
        '''
            在空白格子中随机生成一个 2 或者 4.
        '''
        empty_cells = [(row, col) for row in range(display_data.GRID_SIZE)
                       for col in range(display_data.GRID_SIZE) if self.board[row, col] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row, col] = random.choice(
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 4])  # 2的概率是80%，4的概率是20%

    def slide(self, row: list, validate=False) -> list:
        '''
            处理单行滑动逻辑, 将非零元素滑向左侧, 合并相同元素.
            返回滑动后新的行.

            :param row: 待处理的行.
            :param validate: 是否仅验证可移动, 不执行计算得分.

            >>> self.slide([0, 0, 2, 2])
            [4, 0, 0, 0]
        '''
        non_zero_tiles = [tile for tile in row if tile != 0]
        new_row = []

        i = 0
        while i < len(non_zero_tiles):
            # 合并
            if i + 1 < len(non_zero_tiles) and non_zero_tiles[i] == non_zero_tiles[i + 1]:
                new_row.append(non_zero_tiles[i] * 2)
                if not validate:
                    self.score += non_zero_tiles[i] * 2
                i += 2
            else:
                if non_zero_tiles[i] >= 2048:
                    self.success = True
                new_row.append(non_zero_tiles[i])
                i += 1
        # 补充空白
        new_row += [0] * (display_data.GRID_SIZE - len(new_row))
        return new_row

    def move(self, direction: int):
        '''
            给定方向, 移动整个棋盘.
        '''
        new_board = None

        if direction == pygame.K_LEFT:
            new_board = np.array([self.slide(row) for row in self.board])
        elif direction == pygame.K_RIGHT:
            new_board = np.array(
                [self.slide(row[::-1])[::-1] for row in self.board])
        elif direction == pygame.K_UP:
            new_board = np.transpose(
                [self.slide(col) for col in np.transpose(self.board)])
        elif direction == pygame.K_DOWN:
            new_board = np.transpose(
                [self.slide(col[::-1])[::-1] for col in np.transpose(self.board)])

        if (self.board != new_board).any():
            self.board = new_board
            self.add_random_tile()

    def check_can_move(self):
        '''
            检查是否可以移动.
        '''
        board_changed_left = np.array(
            [self.slide(row, validate=True) for row in self.board])
        board_changed_right = np.array(
            [self.slide(row[::-1], validate=True)[::-1] for row in self.board])
        board_changed_up = np.transpose(
            [self.slide(col, validate=True) for col in np.transpose(self.board)])
        board_changed_down = np.transpose(
            [self.slide(col[::-1], validate=True)[::-1] for col in np.transpose(self.board)])
        # 枚举四个方向移动后相同
        if (board_changed_left == self.board).all() and (board_changed_right == self.board).all() and (board_changed_up == self.board).all() and (board_changed_down == self.board).all():
            self.fail = True
