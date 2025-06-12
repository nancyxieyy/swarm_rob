# 控制整个仿真流程、调用其他模块
from grid_env import GridWorld
from simulation import update_states
from visualize import init_pygame, draw_grid
import pygame
import time

# 初始化 + 运行一轮仿真 + 动画可视化
def main():
    # 参数设置
    width, height = 5, 5
    num_agents = 3
    steps = 50
    noise = 0.1
    max_dist = 1  # 仅用于 proximity 模式

    # 可选网络结构：'fixed', 'proximity', 'random', 'fully_connected'
    network_type = "fixed"

    # 固定拓扑结构（仅当 network_type == 'fixed' 时生效）
    fixed_links = {
        0: [1],
        1: [0, 2],
        2: [1]
    } if network_type == "fixed" else None

    # 初始化系统
    env = GridWorld(width, height, num_agents)
    screen = init_pygame(width, height)

    running = True
    clock = pygame.time.Clock()
    step = 0

    # 主循环
    while running and step < steps:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 绘制当前状态
        draw_grid(screen, env)

        # 打印状态统计信息
        state_counts = list(env.get_agent_states().values())
        ones = state_counts.count(1)
        zeros = state_counts.count(0)
        print(f"Step {step}: 0s = {zeros}, 1s = {ones}")

        # 状态更新 + 移动
        update_states(
            env,
            noise=noise,
            max_dist=max_dist,
            network_type=network_type,
            fixed_links=fixed_links
        )
        env.move_agents()

        step += 1
        clock.tick(2)  # 控制刷新频率（2帧/秒）

    pygame.quit()

if __name__ == "__main__":
    main()