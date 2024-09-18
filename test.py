import pygame
from pygame import mixer
import random
import time
import os
from PIL import Image

# 初始化 Pygame
pygame.init()
mixer.init()

# 当前工作目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 定义常量
WIDTH, HEIGHT = 600, 600
TILE_SIZE_NORMAL = 100
TILE_SIZE_HARD = 75
ROWS_NORMAL, COLS_NORMAL = 6, 6
ROWS_HARD, COLS_HARD = 8, 8
FPS = 30
FONT_SIZE = 40
COUNTDOWN_TIME_NORMAL = 30
COUNTDOWN_TIME_HARD = 20
MUSIC_VOLUME = 0.5

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("羊了个羊小游戏")

# 加载背景图片
background_path = os.path.join(current_dir, "background.png")
if not os.path.exists(background_path):
    raise FileNotFoundError(f"背景图片 {background_path} 不存在.")
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# 加载背景音乐
music_path = os.path.join(current_dir, "backgroundm.mp3")
if not os.path.exists(music_path):
    raise FileNotFoundError(f"背景音乐 {music_path} 不存在.")
mixer.music.load(music_path)
mixer.music.set_volume(MUSIC_VOLUME)
mixer.music.play(-1)  # -1 表示无限循环播放

# 加载图案图片
def load_patterns(tile_size):
    pattern_files = [f for f in os.listdir(current_dir) if f.endswith('.png')]
    patterns = []
    for file_path in pattern_files:
        img = Image.open(os.path.join(current_dir, file_path))
        img.thumbnail((tile_size, tile_size), Image.Resampling.LANCZOS)
        pattern = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
        patterns.append(pattern)
    return patterns

# 字体
font = pygame.font.SysFont('Microsoft YaHei UI', FONT_SIZE, bold=True)

# 绘制文本
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# 绘制棋盘
def draw_board(board, tile_size):
    for row in range(len(board)):
        for col in range(len(board[row])):
            tile = board[row][col]
            if tile is not None:
                screen.blit(tile, (col * tile_size, row * tile_size))

# 检查匹配
def check_match(selected, board):
    if len(selected) == 2:
        r1, c1 = selected[0]
        r2, c2 = selected[1]
        if 0 <= r1 < len(board) and 0 <= c1 < len(board[0]) and 0 <= r2 < len(board) and 0 <= c2 < len(board[0]):
            if board[r1][c1] == board[r2][c2]:
                board[r1][c1] = None
                board[r2][c2] = None
                if all(tile is None for row in board for tile in row):
                    return True
                return True
    return False

# 重置游戏状态
def reset_game_state(mode):
    global board, selected, clicked_positions, clock, all_cleared, start_time
    if mode == "hard":
        tile_size = TILE_SIZE_HARD
        rows, cols = ROWS_HARD, COLS_HARD
    else:
        tile_size = TILE_SIZE_NORMAL
        rows, cols = ROWS_NORMAL, COLS_NORMAL
    board = prepare_board(rows, cols, tile_size)
    selected = []
    clicked_positions = set()
    clock = pygame.time.Clock()
    all_cleared = False
    start_time = time.time()

# 准备棋盘
def prepare_board(rows, cols, tile_size):
    num_patterns_needed = (rows * cols) // 2
    pattern_indices = [i for i in range(num_patterns_needed) for _ in range(2)]
    random.shuffle(pattern_indices)
    patterns = load_patterns(tile_size)
    board = [[patterns[idx] for idx in pattern_indices[:cols]] for _ in range(rows)]
    return board

# 游戏结束
def game_over():
    reset_game_state("normal")
    screen.blit(background, (0, 0))
    draw_text("游戏结束", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 - 20)
    draw_text("点击返回主菜单", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 40)
    draw_text("点击退出游戏", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 80)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 2 - 100 <= mouse_pos[0] <= WIDTH // 2 + 100 and HEIGHT // 2 + 40 - 20 <= mouse_pos[1] <= HEIGHT // 2 + 40 + 20:
                    main_menu()
                    return
                elif WIDTH // 2 - 100 <= mouse_pos[0] <= WIDTH // 2 + 100 and HEIGHT // 2 + 80 - 20 <= mouse_pos[1] <= HEIGHT // 2 + 80 + 20:
                    pygame.quit()
                    return
        # 更新游戏结束显示，如果需要的话
        screen.blit(background, (0, 0))
        draw_text("游戏结束", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 - 20)
        draw_text("点击返回主菜单", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 40)
        draw_text("点击退出游戏", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 80)
        pygame.display.flip()

# 游戏胜利
def game_win():
    reset_game_state("normal")
    screen.blit(background, (0, 0))
    draw_text("恭喜通关！", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 - 20)
    draw_text("点击返回主菜单", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 40)
    draw_text("点击退出游戏", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 80)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 2 - 100 <= mouse_pos[0] <= WIDTH // 2 + 100 and HEIGHT // 2 + 40 - 20 <= mouse_pos[1] <= HEIGHT // 2 + 40 + 20:
                    main_menu()
                    return
                elif WIDTH // 2 - 100 <= mouse_pos[0] <= WIDTH // 2 + 100 and HEIGHT // 2 + 80 - 20 <= mouse_pos[1] <= HEIGHT // 2 + 80 + 20:
                    pygame.quit()
                    return
        # 更新游戏胜利显示，如果需要的话
        screen.blit(background, (0, 0))
        draw_text("恭喜通关！", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 - 20)
        draw_text("点击返回主菜单", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 40)
        draw_text("点击退出游戏", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 80)
        pygame.display.flip()

# 主菜单
def main_menu():
    screen.blit(background, (0, 0))
    draw_text("主菜单", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 - 20)
    draw_text("点击开始游戏 - 普通模式", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 40)
    draw_text("点击开始游戏 - 困难模式", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 80)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 2 - 150 <= mouse_pos[0] <= WIDTH // 2 + 150 and HEIGHT // 2 + 20 <= mouse_pos[1] <= HEIGHT // 2 + 60:
                    reset_game_state("normal")
                    main_game(mode="normal")
                    waiting = False
                elif WIDTH // 2 - 150 <= mouse_pos[0] <= WIDTH // 2 + 150 and HEIGHT // 2 + 60 <= mouse_pos[1] <= HEIGHT // 2 + 100:
                    reset_game_state("hard")
                    main_game(mode="hard")
                    waiting = False
        # 更新主菜单显示，如果需要的话
        screen.blit(background, (0, 0))
        draw_text("主菜单", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 - 20)
        draw_text("点击开始游戏 - 普通模式", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 40)
        draw_text("点击开始游戏 - 困难模式", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 80)
        pygame.display.flip()

# 主游戏循环
def main_game(mode="normal"):
    global board, selected, clicked_positions, clock, all_cleared, start_time
    
    if mode == "hard":
        COUNTDOWN_TIME = COUNTDOWN_TIME_HARD
        tile_size = TILE_SIZE_HARD
        rows, cols = ROWS_HARD, COLS_HARD
    else:
        COUNTDOWN_TIME = COUNTDOWN_TIME_NORMAL
        tile_size = TILE_SIZE_NORMAL
        rows, cols = ROWS_NORMAL, COLS_NORMAL

    remaining_time = COUNTDOWN_TIME
    board = prepare_board(rows, cols, tile_size)

    selected = []
    clicked_positions = set()
    clock = pygame.time.Clock()
    all_cleared = False
    start_time = time.time()

    while not all_cleared and remaining_time > 0:
        elapsed_time = time.time() - start_time
        remaining_time = COUNTDOWN_TIME - int(elapsed_time)

        if remaining_time <= 0:
            game_over()
            return

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // tile_size, y // tile_size
                if 0 <= row < rows and 0 <= col < cols and (row, col) not in clicked_positions and board[row][col] is not None:
                    clicked_positions.add((row, col))
                    selected.append((row, col))
                    if len(selected) == 2:
                        if check_match(selected, board):
                            if all(tile is None for row in board for tile in row):
                                game_win()
                                return
                        selected.clear()
                        clicked_positions.clear()

        screen.blit(background, (0, 0))
        draw_board(board, tile_size)
        draw_text(f"剩余时间: {remaining_time}", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT - 20)
        pygame.display.flip()

if __name__ == "__main__":
    try:
        while True:
            main_menu()
            main_game()
    except Exception as e:
        print(f"发生错误：{e}")
        pygame.quit()