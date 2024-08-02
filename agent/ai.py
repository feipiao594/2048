import copy
import threading
import time
import numpy as np
import pygame
import random

class QLearningAgent:
    def __init__(self):
        self.Q = {}  # Q表：状态 -> 动作 -> Q值
        self.alpha = 0.1  # 学习率
        self.gamma = 0.9  # 折扣因子
        self.epsilon = 0.1  # 探索率
        self.last_env = None
        self.last_state = None
        self.last_action = None
        self.result = None
        self.done_event = threading.Event()
        self.thread_release = True
        self.reward_sum = 0
        self.times = 0

    def flatten_state(self, board):
        # 将棋盘状态展平成元组或适合Q-learning的其他格式
        return tuple(board.flatten())

    def get_action_async(self, board_state):
        # time.sleep(0.5)
        if self.result:
            reward = self.reward(board_state)
            self.update(reward, board_state)
        state = self.flatten_state(board_state.board)  # 将棋盘状态转换成适合的格式
        if state not in self.Q:
            self.Q[state] = {action: 0 for action in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]}
        
        if random.random() < self.epsilon:
            action = random.choice([pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN])
        else:
            action = max(self.Q[state], key=self.Q[state].get)
        
        self.last_env = copy.deepcopy(board_state)
        self.last_state = state
        self.last_action = action
        self.result = action
        self.done_event.set()


    def get_action(self, board_state):   
        if self.thread_release:
            self.thread = threading.Thread(target=self.get_action_async, args=(board_state,))
            self.thread.start()
            self.thread_release = False
            return None
        elif self.done_event.is_set():
            self.thread_release = True
            self.done_event.clear()
            return self.result
        else:
            return None

    def reset(self):
        self.last_env = None
        self.last_state = None
        self.last_action = None
        self.result = None
        self.reward_sum = 0
        
    def update(self, reward, next_board_state):
        next_state = self.flatten_state(next_board_state.board)
        if next_state not in self.Q:
            self.Q[next_state] = {action: 0 for action in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]}
        
        max_next_Q = max(self.Q[next_state].values()) if next_state in self.Q else 0
        current_Q = self.Q[self.last_state][self.last_action]
        self.Q[self.last_state][self.last_action] = (1 - self.alpha) * current_Q + self.alpha * (reward + self.gamma * max_next_Q)

    def reward(self, board_state):
        reward_temp = 0
        if board_state.fail:
            self.times += 1
            print(f"Times: {self.times}, Reward: {self.reward_sum}, Score: {board_state.score}")
            reward_temp += -1000
            return reward_temp 
        
        if (board_state.board == self.last_env.board).all():
            # print(f"Reward_temp: -1")
            return -1
        
        max_tile = np.max(board_state.board)
        max_tile_last = np.max(self.last_env.board)
        
        temp_1 = board_state.score
        temp_2 = self.last_env.score
        reward_temp += temp_1 - temp_2
        
        if max_tile_last < max_tile:
            reward_temp += 10 * max_tile
        
        # print(f"Reward_temp: {reward_temp}")
        self.reward_sum += reward_temp
        return reward_temp


