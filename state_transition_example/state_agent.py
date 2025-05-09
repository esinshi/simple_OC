import random


class DummyGridWorld:
    def __init__(self):
        self.states = ["idle", "holding_onion", "near_pot", "blocked", "pot_full"]
        self.current_state = "idle"
        self.transitions = {
            "idle": ["holding_onion", "blocked"],
            "holding_onion": ["near_pot", "blocked"],
            "near_pot": ["pot_full", "blocked"],
            "blocked": ["idle", "holding_onion"],
            "pot_full": ["idle"]
        }

    def get_obs(self):
        return self.current_state

    def step(self, action):
        # Random transition ignoring the action
        self.current_state = random.choice(self.transitions[self.current_state])
        return self.get_obs()
