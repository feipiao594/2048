import threading
import time
import pygame
import random

class QLearningAgent:
    def __init__(self):
        self.Q = {}  # Q-table，用字典表示，状态 -> 动作值
        self.alpha = 0.1  # 学习率
        self.gamma = 0.9  # 折扣因子
        self.epsilon = 0.1  # ε-greedy策略中的ε
        self.result = None
        self.done_event = threading.Event()
        self.thread_release = True

    def get_action_async(self, board_state):
        time.sleep(0.1)
        self.result = random.choice([pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN])
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
