# 绘制每一步网格状态（颜色区分状态）
import pygame

CELL_SIZE = 60
MARGIN = 2
COLORS = {
    0: (0, 102, 204),   # 蓝色
    1: (204, 0, 0),     # 红色
    -1: (240, 240, 240) # 空格背景
}

def init_pygame(width, height):
    pygame.init()
    screen_width = width * (CELL_SIZE + MARGIN) + MARGIN
    screen_height = height * (CELL_SIZE + MARGIN) + MARGIN
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Grid World - Agent Consensus")
    return screen

def draw_grid(screen, env):
    screen.fill((255, 255, 255))
    grid = env.grid
    states = env.get_agent_states()
    positions = env.get_agent_positions()

    for y in range(env.height):
        for x in range(env.width):
            aid = grid[y][x]
            if aid == -1:
                color = COLORS[-1]
            else:
                color = COLORS[states[aid]]
            rect = pygame.Rect(
                x * (CELL_SIZE + MARGIN) + MARGIN,
                y * (CELL_SIZE + MARGIN) + MARGIN,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, color, rect)
    pygame.display.flip()