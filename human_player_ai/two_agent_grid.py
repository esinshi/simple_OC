import random

class TwoAgentGrid:
    def __init__(self, width=4, height=4):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.grid = [[" " for _ in range(self.width)] for _ in range(self.height)]
        self.human_pos = [1, 1]
        self.agent_pos = [1, 2]
        self.onion_pos = [0, 1]
        self.pot_pos = [0, 3]
        self.holding = {"human": False, "agent": False}
        self.steps = 0
        return self.get_obs()

    def get_obs(self):
        return {
            "human_pos": tuple(self.human_pos),
            "agent_pos": tuple(self.agent_pos),
            "onion_pos": tuple(self.onion_pos),
            "pot_pos": tuple(self.pot_pos),
            "holding": dict(self.holding),
        }

    def render(self):
        display = [[" " for _ in range(self.width)] for _ in range(self.height)]
        x, y = self.onion_pos
        display[y][x] = "O"
        x, y = self.pot_pos
        display[y][x] = "P"
        x, y = self.human_pos
        display[y][x] = "H"
        x, y = self.agent_pos
        display[y][x] = "A"

        print("\n" + "-" * (self.width * 4))
        for row in display:
            print(" ".join(f"[{c}]" for c in row))
        print("-" * (self.width * 4))
        print(f"Holding: H={self.holding['human']}, A={self.holding['agent']}")

    def move(self, who, direction):
        pos = self.human_pos if who == "human" else self.agent_pos
        dx, dy = 0, 0
        if direction == "up": dy = -1
        elif direction == "down": dy = 1
        elif direction == "left": dx = -1
        elif direction == "right": dx = 1

        new_x = max(0, min(self.width - 1, pos[0] + dx))
        new_y = max(0, min(self.height - 1, pos[1] + dy))
        pos[0], pos[1] = new_x, new_y

    def interact(self, who):
        pos = self.human_pos if who == "human" else self.agent_pos
        if tuple(pos) == tuple(self.onion_pos) and not self.holding[who]:
            self.holding[who] = True
        elif tuple(pos) == tuple(self.pot_pos) and self.holding[who]:
            self.holding[who] = False
            return 1  # reward for successful delivery
        return 0
