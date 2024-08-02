import game_envirment
import pygame

from agent import Agent
from tools import display_data

running = True
pygame.init()
WINDOW_SIZE = (display_data.GRID_SIZE * display_data.CELL_SIZE + (display_data.GRID_SIZE+ 1) * display_data.MARGIN, display_data.GRID_SIZE * display_data.CELL_SIZE +(display_data.GRID_SIZE + 1) * display_data.MARGIN)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("2048 Game")
game_env = game_envirment.game_envirment()

def restart_game():
    global running
    global game_env
    game_env.reset()
    running = True
    cycle(game_env)

def success_window():
    # 游戏胜利窗口
    global WINDOW_SIZE
    
    transparent_surface = pygame.Surface(WINDOW_SIZE)
    transparent_surface.set_alpha(128)  # 设置透明度，0-255之间，255为不透明
    transparent_surface.fill(display_data.WHITE)
    
    screen.blit(transparent_surface, (0, 0))
    font = pygame.font.Font(None, 100)
    text = font.render("You Win!", True, display_data.RED)
    text_rect = text.get_rect(center=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    button_font = pygame.font.Font(None, 50)
    button_text = button_font.render("Restart", True, display_data.BLACK)
    button_rect = button_text.get_rect(center=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 + 100))
    pygame.draw.rect(screen, display_data.GRAY, button_rect.inflate(20, 10))
    screen.blit(button_text, button_rect)
    
    pygame.display.flip()
    
    # 处理事件
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    restart_game()
                    return
        
    
def fail_window():
    # 游戏失败窗口
    global WINDOW_SIZE
    
    transparent_surface = pygame.Surface(WINDOW_SIZE)
    transparent_surface.set_alpha(128)  # 设置透明度，0-255之间，255为不透明
    transparent_surface.fill(display_data.WHITE)
    
    screen.blit(transparent_surface, (0, 0))
    font = pygame.font.Font(None, 100)
    text = font.render("Game Over!", True, display_data.RED)
    text_rect = text.get_rect(center=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    button_font = pygame.font.Font(None, 50)
    button_text = button_font.render("Restart", True, display_data.BLACK)
    button_rect = button_text.get_rect(center=(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2 + 100))
    pygame.draw.rect(screen, display_data.GRAY, button_rect.inflate(20, 10))
    screen.blit(button_text, button_rect)
    
    pygame.display.flip()
    
    # 处理事件
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    restart_game()
                    return



def cycle(game_env):
    # 游戏主循环
    global running
    while running:
        # 处理事件
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    game_env.move(event.key)
                    game_env.check_can_move()
        # 清空屏幕
        screen.fill(display_data.DARK_GRAY)
        # 绘制游戏板
        for row in range(display_data.GRID_SIZE):
            for col in range(display_data.GRID_SIZE):
                # 计算每个格子的位置
                x = display_data.MARGIN + col * (display_data.CELL_SIZE + display_data.MARGIN)
                y = display_data.MARGIN + row * (display_data.CELL_SIZE + display_data.MARGIN)
                # 绘制格子的背景
                pygame.draw.rect(screen, display_data.TILE_COLORS[game_env.board[row, col]], (x, y, display_data.CELL_SIZE, display_data.CELL_SIZE))
                # 绘制格子中的数字（如果有）
                if game_env.board[row, col] != 0:
                    font = pygame.font.Font(None, 80)
                    text = font.render(str(game_env.board[row, col]), True, display_data.NUMBER_BROWN)
                    text_rect = text.get_rect(center=(x + display_data.CELL_SIZE / 2, y + display_data.CELL_SIZE / 2))
                    screen.blit(text, text_rect)
        # 更新屏幕显示True
        pygame.display.flip()
        if game_env.success:
            running = False
            success_window()
        elif game_env.fail:
            running = False
            fail_window()
            
if __name__ == "__main__":
    restart_game()