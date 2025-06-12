# Only Talk to Your Friends: The benefits of Interaction Constraints in Consensus Formation

A simple Python-based simulation of swarm agents in a 2D grid world, supporting agent mobility, binary state consensus, and multiple network topologies.

## ✅ Features

- Grid-based environment with mobile agents
- Agent states: `0` (blue) or `1` (red)
- Real-time visualization using `pygame`
- Four communication network types:
  - `fixed`: predefined agent links (e.g. 0-1-2)
  - `proximity`: neighbors within Manhattan distance ≤ 1
  - `random`: dynamic random links per round
  - `fully_connected`: all-to-all communication

## 🔧 Requirements

```bash
pip install -r requirements.txt
```

## 🚀 Run the Simulation
```bash
python main.py
```
Change the network structure in main.py:
```python
network_type = "fixed"  # options: fixed, proximity, random, fully_connected
```

## 📌 TODO (for future development)
- Add consensus correctness evaluation
- Add CSV result logging
- Add replay/save function
- Extend to larger agent groups
- Add support for dynamic topologies

## 📄 License
MIT
