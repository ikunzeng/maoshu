import pygame
from pygame import mixer
import random
import time
# 初始化 Pygame
pygame.init()
mixer.init()
# 定义常量
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 100
ROWS, COLS = 6, 6
FPS = 30
FONT_SIZE = 40
COUNTDOWN_TIME = 30
MUSIC_VOLUME = 0.5
# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("猫了个鼠小游戏")
# 加载背景图片
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
# 加载背景音乐
mixer.music.load("backgroundm.mp3")
mixer.music.set_volume(MUSIC_VOLUME)
mixer.music.play(-1)  # -1 表示无限循环播放
# 加载图案图片
def load_patterns():
    patterns = [pygame.image.load(f"pattern_{i}.png") for i in range(1, 7)]
    return [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]

patterns = load_patterns()
# 字体
font = pygame.font.SysFont('Microsoft YaHei UI', FONT_SIZE, bold=True)
# 绘制文本
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
# 绘制棋盘
def draw_board(board):
    for row in range(ROWS):
        for col in range(COLS):
            tile = board[row][col]
            if tile is not None:
                screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))
# 检查匹配
def check_match(selected, board):
    if len(selected) == 2:
        r1, c1 = selected[0]
        r2, c2 = selected[1]
        if board[r1][c1] == board[r2][c2]:
            board[r1][c1] = None
            board[r2][c2] = None
            if all(tile is None for row in board for tile in row):
                return True
            return True
    return False
# 重置游戏状态
def reset_game_state():
    global board, selected, clicked_positions, clock, all_cleared, start_time
    board = None
    selected = None
    clicked_positions = None
    clock = pygame.time.Clock()
    all_cleared = None
    start_time = None
# 读取排行榜数据
def load_leaderboard():
    try:
        with open('leaderboard.txt', 'r') as file:
            leaderboard = [line.strip().split(',') for line in file.readlines()]
            return sorted(leaderboard, key=lambda x: int(x[1]))[:3]  # 只取前三名
    except FileNotFoundError:
        return []
# 显示排行榜
def show_leaderboard():
    leaderboard = load_leaderboard()
    screen.blit(background, (0, 0))
    draw_text("排行榜", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 - 100)
    y = HEIGHT // 2 - 50
    for rank, (name, time) in enumerate(leaderboard, start=1):
        draw_text(f"{rank}. {name} - {time}s", font, (0, 0, 0), screen, WIDTH // 2, y)
        y += 50
    draw_text("点击返回主菜单", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT - 50)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 2 - 100 <= mouse_pos[0] <= WIDTH // 2 + 100 and HEIGHT - 50 - 20 <= mouse_pos[1] <= HEIGHT - 50 + 20:
                    main_menu()
                    return
        # 更新排行榜显示，如果需要的话
        screen.blit(background, (0, 0))
        draw_text("排行榜", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 - 100)
        y = HEIGHT // 2 - 50
        for rank, (name, time) in enumerate(leaderboard, start=1):
            draw_text(f"{rank}. {name} - {time}s", font, (0, 0, 0), screen, WIDTH // 2, y)
            y += 50
        draw_text("点击返回主菜单", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT - 50)
        pygame.display.flip()
# 主菜单
def main_menu():
    global music_playing  # 声明 music_playing 是全局变量
    music_playing = True  # 默认播放音乐
    
    def toggle_music():
        global music_playing
        if music_playing:
            mixer.music.pause()
            music_playing = False
        else:
            mixer.music.unpause()
            music_playing = True
    
    screen.blit(background, (0, 0))
    draw_text("主菜单", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 - 20)
    draw_text("点击开始游戏", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 40)
    draw_text("查看排行榜", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 80)
    draw_text(" BGM", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 120)
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
                    reset_game_state()  # 在进入新游戏前重置状态
                    main_game()
                    waiting = False
                elif WIDTH // 2 - 150 <= mouse_pos[0] <= WIDTH // 2 + 150 and HEIGHT // 2 + 60 <= mouse_pos[1] <= HEIGHT // 2 + 100:
                    show_leaderboard()
                    waiting = False
                elif WIDTH // 2 - 150 <= mouse_pos[0] <= WIDTH // 2 + 150 and HEIGHT // 2 + 100 <= mouse_pos[1] <= HEIGHT // 2 + 140:
                    toggle_music()
                    draw_text("主菜单", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 - 20)
                    draw_text("点击开始游戏", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 40)
                    draw_text("查看排行榜", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 80)
                    draw_text(" BGM", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 120)
                    pygame.display.flip()
        # 更新主菜单显示，如果需要的话
        screen.blit(background, (0, 0))
        draw_text("主菜单", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 - 20)
        draw_text("点击开始游戏", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 40)
        draw_text("查看排行榜", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 80)
        draw_text(" BGM", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 120)
        pygame.display.flip()
# 游戏结束
def game_over():
    reset_game_state()  # 添加状态重置
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
    reset_game_state()  # 添加状态重置
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
# 主游戏循环
def main_game():
    global board, selected, clicked_positions, clock, all_cleared, start_time
    start_time = time.time()
    remaining_time = COUNTDOWN_TIME

    pattern_indices = [i for i in range(len(patterns)) for _ in range(6)]
    random.shuffle(pattern_indices)
    board = [[patterns[pattern_indices.pop()] if pattern_indices else None for _ in range(COLS)] for _ in range(ROWS)]

    selected = []
    clicked_positions = set()
    clock = pygame.time.Clock()
    all_cleared = False

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
                col, row = x // TILE_SIZE, y // TILE_SIZE
                if 0 <= row < ROWS and 0 <= col < COLS and (row, col) not in clicked_positions and board[row][col] is not None:
                    clicked_positions.add((row, col))
                    selected.append((row, col))
                    if len(selected) == 2:
                        if check_match(selected, board):
                            if all(tile is None for row in board for tile in row):
                                update_leaderboard(int(elapsed_time))
                                game_win()
                                return
                        selected.clear()
                        clicked_positions.clear()

        screen.blit(background, (0, 0))
        draw_board(board)
        draw_text(f"剩余时间: {remaining_time}", font, (0, 0, 0), screen, WIDTH // 2, HEIGHT - 20)
        pygame.display.flip()
# 更新排行榜
def update_leaderboard(time):
    leaderboard = load_leaderboard()
    leaderboard.append(("匿名", str(time)))
    with open('leaderboard.txt', 'w') as file:
        for entry in leaderboard:
            file.write(','.join(entry) + '\n')

if __name__ == "__main__":
    while True:
        main_menu()
        main_game()