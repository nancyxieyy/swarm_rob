# simulation.py
# 状态传播规则（投票 + 噪声）
# 局部物理邻近网络
# 状态更新（如0/1共识），加噪声逻辑

import numpy as np
import random

def get_neighbors(agent_id, positions, network_type="proximity", max_dist=1, total_agents=3, fixed_links=None):
    """根据所选连接方式返回邻居列表"""
    # 邻近网络
    if network_type == "proximity":
        ax, ay = positions[agent_id]
        neighbors = []
        for other_id, (ox, oy) in positions.items():
            if other_id != agent_id:
                dist = abs(ax - ox) + abs(ay - oy)  # 曼哈顿距离
                if dist <= max_dist:
                    neighbors.append(other_id)
        return neighbors

    # 固定网络
    elif network_type == "fixed":
        if fixed_links is None:
            raise ValueError("固定拓扑要求传入 fixed_links 参数")
        return fixed_links.get(agent_id, [])

    # 随机网络
    elif network_type == "random":
        # 每轮随机连接（30% 概率连接其他每个 agent）
        return [i for i in range(total_agents) if i != agent_id and random.random() < 0.3]

    # 全链接网络 
    elif network_type == "fully_connected":
        return [i for i in range(total_agents) if i != agent_id]

    else:
        raise ValueError(f"未知网络结构类型：{network_type}")

# 状态更新算法
def update_states(env, noise=0.1, max_dist=1, network_type="proximity", fixed_links=None):
    positions = env.get_agent_positions()
    current_states = env.get_agent_states()
    new_states = {}

    total_agents = len(current_states)

    for aid in current_states:
        #  获取邻居
        neighbors = get_neighbors(
            aid,
            positions,
            network_type=network_type,
            max_dist=max_dist,
            total_agents=total_agents,
            fixed_links=fixed_links
        )

        if not neighbors:   # 没有邻居就保持原状态
            new_states[aid] = current_states[aid]
            continue

        neighbor_states = [current_states[nid] for nid in neighbors]
        majority = round(np.mean(neighbor_states))  # 计算邻居状态的多数

        # 加入噪声
        if random.random() < noise:
            new_states[aid] = 1 - majority # 翻转决策
        else:
            new_states[aid] = majority  # 采用多数决策

    for aid, new_state in new_states.items():
        env.set_agent_state(aid, new_state)
