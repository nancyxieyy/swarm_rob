# grid_env.py
# 创建网格、初始化机器人、定义移动规则
import numpy as np
import random

# 网格类 + 机器人移动函数
class GridWorld:
    def __init__(self, width, height, num_agents):
        self.width = width  # 网格宽度
        self.height = height    # 网格高度
        self.num_agents = num_agents    # 机器人数量
        self.grid = np.full((height, width), -1)  # 创建空网格
        self.agents = {}    # 存储机器人信息
        self._init_agents() # 初始化代理

    # 初始化代理
    def _init_agents(self):
        placed = 0
        while placed < self.num_agents:
            x = random.randint(0, self.width - 1)   # 随机x坐标
            y = random.randint(0, self.height - 1)  # 随机y坐标
            if self.grid[y, x] == -1:   # 检查位置是否空
                state = random.choice([0, 1])   # 随机初始状态,0/1
                self.grid[y, x] = placed    # 在网格中标记机器人ID
                self.agents[placed] = { # 存储机器人信息
                    "id": placed,
                    "pos": (y, x),
                    "state": state
                }
                placed += 1
    # 代理移动
    def move_agents(self):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上下左右
        new_grid = np.full((self.height, self.width), -1)   # 创建新的网格
        new_positions = {}

        for agent_id, agent in self.agents.items():
            y, x = agent["pos"]
            dx, dy = random.choice(directions)  # 随机选择移动方向
            ny, nx = y + dy, x + dx # 计算新位置

            # 边缘检测,碰撞检测
            if 0 <= ny < self.height and 0 <= nx < self.width and new_grid[ny, nx] == -1:
                new_grid[ny, nx] = agent_id # 移动成功
                new_positions[agent_id] = (ny, nx)
            else:
                new_grid[y, x] = agent_id   # 保持原位
                new_positions[agent_id] = (y, x)

        for aid in self.agents:
            self.agents[aid]["pos"] = new_positions[aid]
        self.grid = new_grid

    # 获取代理状态:0/1
    def get_agent_states(self):
        return {aid: a["state"] for aid, a in self.agents.items()}

    # 获取代理
    def set_agent_state(self, agent_id, new_state):
        self.agents[agent_id]["state"] = new_state

    # 获取代理位置
    def get_agent_positions(self):
        return {aid: a["pos"] for aid, a in self.agents.items()}
