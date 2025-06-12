# grid_env.py
# 创建网格、初始化机器人、定义移动规则
import numpy as np
import random

# 网格类 + 机器人移动函数
class GridWorld:
    def __init__(self, width=5, height=5, num_agents=3):
        self.width = width
        self.height = height
        self.num_agents = num_agents
        self.grid = np.full((height, width), -1)  # -1 表示空格
        self.agents = {}
        self._init_agents()

    def _init_agents(self):
        placed = 0
        while placed < self.num_agents:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.grid[y, x] == -1:
                state = random.choice([0, 1])
                self.grid[y, x] = placed
                self.agents[placed] = {
                    "id": placed,
                    "pos": (y, x),
                    "state": state
                }
                placed += 1

    def move_agents(self):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上下左右
        new_grid = np.full((self.height, self.width), -1)
        new_positions = {}

        for agent_id, agent in self.agents.items():
            y, x = agent["pos"]
            dx, dy = random.choice(directions)
            ny, nx = y + dy, x + dx

            # 保持在边界内且新位置未被占用
            if 0 <= ny < self.height and 0 <= nx < self.width and new_grid[ny, nx] == -1:
                new_grid[ny, nx] = agent_id
                new_positions[agent_id] = (ny, nx)
            else:
                new_grid[y, x] = agent_id
                new_positions[agent_id] = (y, x)

        for aid in self.agents:
            self.agents[aid]["pos"] = new_positions[aid]
        self.grid = new_grid

    def get_agent_states(self):
        return {aid: a["state"] for aid, a in self.agents.items()}

    def set_agent_state(self, agent_id, new_state):
        self.agents[agent_id]["state"] = new_state

    def get_agent_positions(self):
        return {aid: a["pos"] for aid, a in self.agents.items()}
