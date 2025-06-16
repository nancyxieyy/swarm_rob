# main.py
# 控制整个仿真流程、调用其他模块
from grid_env import GridWorld
from simulation import update_states
from visualize import init_pygame, draw_grid
from metrics import SimpleMetrics
import pygame
import time

# 初始化 + 运行一轮仿真 + 动画可视化
def main():
    # 参数设置
    width, height = 5, 5    # 网格大小
    num_agents = 3  # 机器人数量
    steps = 50  # 仿真步数
    noise = 0.1 # 噪声水平
    max_dist = 1  # 仅用于 proximity 模式, 通信距离

    # 可选网络结构：'fixed', 'proximity', 'random', 'fully_connected'
    # network_type = "fixed"
    # network_type = "proximity"
    # network_type = "random"
    network_type = "fully_connected"

    # fixed固定拓扑结构（仅当 network_type == 'fixed' 时生效）
    fixed_links = {
        0: [1], # 代理0只与代理1连接
        1: [0, 2],  # 代理1与代理0和2连接
        2: [1]  # 代理2至于代理1连接
    } if network_type == "fixed" else None

    # 设置目标状态
    target_state = 1
    
    # 输出环境基础信息
    print("启动群体机器人仿真")
    print(f"配置: {num_agents}个机器人, {width}x{height}网格, {steps}步")
    print(f"网络类型: {network_type}")
    print(f"噪声水平: {noise}")
    print(f"目标状态: {target_state}")
    print("-" * 50)

    # 初始化系统
    env = GridWorld(width, height, num_agents)
    metrics = SimpleMetrics(target_state)
    
    # 显示初始状态
    initial_states = env.get_agent_states()
    print(f"初始状态: {initial_states}")
    
    # 确保pygame正确初始化
    try:
        print("初始化pygame...")
        pygame.init()  # 明确调用pygame.init()
        screen = init_pygame(width, height)
        clock = pygame.time.Clock()
        print("pygame初始化成功!")
        use_visualization = True
    except Exception as e:
        print(f"pygame初始化失败: {e}")
        print("切换到无可视化模式...")
        use_visualization = False
        screen = None
        clock = None
        
    # 仿真主循环
    running = True
    step = 0

    # 主循环
    while running and step < steps:
        # 1. 只有在可视化模式下才处理pygame事件
        if use_visualization and screen is not None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("用户关闭窗口")
                    running = False
                    break
        
        if not running:
            break

        # 2. 收集当前步的数据
        current_states = env.get_agent_states()
        metrics.update_metrics(step, current_states)
        
        # 3. 可视化绘制（如果可用）
        if use_visualization and screen is not None:
            try:
                draw_grid(screen, env)
            except Exception as e:
                print(f"绘制警告: {e}")

        # 4. 在控制台显示当前统计信息
        stats = metrics.get_current_stats()
        print(stats)
        
        # 5. 如果已经收敛，可以选择提前结束
        if metrics.is_converged and step > metrics.convergence_step + 5:
            print("已稳定收敛，提前结束仿真")
            break
        
        # 6. 更新状态和位置
        try:
            update_states(
                env,
                noise=noise,
                max_dist=max_dist,
                network_type=network_type,
                fixed_links=fixed_links
            )
            env.move_agents()
        except Exception as e:
            print(f"更新出错: {e}")
            break
        
        step += 1
        
        # 控制帧率
        if use_visualization and clock is not None:
            clock.tick(2)
        else:
            time.sleep(0.5)  # 无可视化模式下用sleep代替
    
    # 7. 显示最终报告 (移到循环外面)
    final_report = metrics.get_final_report()
    print(final_report)

    # 8. 等待用户关闭窗口 (移到循环外面)
    if use_visualization and screen is not None:
        print("\n仿真完成！查看可视化窗口，按关闭按钮退出。")
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
            if clock is not None:
                clock.tick(10)
        pygame.quit()
    else:
        print("\n仿真完成！")

if __name__ == "__main__":
    main()