from stable_baselines3 import PPO
import numpy as np
from overcooked_ai.src.overcooked_ai_py.mdp.overcooked_env import OvercookedEnv, OvercookedGridworld
from overcooked_ai.src.overcooked_ai_py.planning.planners import MediumLevelActionManager, NO_COUNTERS_PARAMS

# Load your trained agents
crafter_agent = PPO.load("ppo_crafter.zip")
minigrid_agent = PPO.load("ppo_minigrid.zip")


## 1. Proper Environment Setup ##

def mdp_generator_fn(mdp_params=None):
    """
    Correct MDP generator function that accepts optional parameters
    and returns a fully configured Overcooked MDP instance
    """
    # Create MDP instance
    mdp = OvercookedGridworld.from_layout_name("cramped_room")

    # Configure Medium Level Action Manager
    mlam_params = {
        'start_orientations': False,
        'wait_allowed': False,
        'counter_goals': NO_COUNTERS_PARAMS,
        'counter_drop': NO_COUNTERS_PARAMS,
        'counter_pickup': NO_COUNTERS_PARAMS,
        'same_motion_goals': True
    }

    mdp.mlam = MediumLevelActionManager(
        mdp=mdp,
        mlam_params=mlam_params,
    )
    return mdp


# Initialize environment
overcooked_env = OvercookedEnv(mdp_generator_fn)


## 2. Agent Action Adapters ##

def crafter_action_to_overcooked(action):
    """Map Crafter action space to Overcooked actions"""
    action_map = [
        'stay',  # 0
        'up',  # 1
        'down',  # 2
        'left',  # 3
        'right',  # 4
        'interact'  # 5
    ]
    return action_map[action] if action < len(action_map) else 'stay'


def minigrid_action_to_overcooked(action):
    """Map MiniGrid action space to Overcooked actions"""
    action_map = [
        'right',  # 0
        'down',  # 1
        'left',  # 2
        'up',  # 3
        'interact',  # 4
        'stay'  # 5
    ]
    return action_map[action] if action < len(action_map) else 'stay'


## 3. Observation Adapters (Placeholders) ##

def adapt_obs_for_crafter(state):
    """Convert Overcooked state to Crafter-compatible observation"""
    # Implement your actual observation transformation here
    return np.zeros(64)  # Dummy observation


def adapt_obs_for_minigrid(state):
    """Convert Overcooked state to MiniGrid-compatible observation"""
    # Implement your actual observation transformation here
    return np.zeros(64)  # Dummy observation


## 4. Main Execution Loop ##

# Load your trained agents (uncomment when ready)
# crafter_agent = PPO.load("ppo_crafter.zip")
# minigrid_agent = PPO.load("ppo_minigrid.zip")

# For testing, use dummy agents
class DummyAgent:
    def predict(self, obs):
        return np.random.randint(0, 6), None


crafter_agent = DummyAgent()
minigrid_agent = DummyAgent()

# Run simulation
state = overcooked_env.reset()
done = False

while not done:
    # Get adapted observations
    crafter_obs = adapt_obs_for_crafter(state)
    minigrid_obs = adapt_obs_for_minigrid(state)

    # Get actions from agents
    crafter_action, _ = crafter_agent.predict(crafter_obs)
    minigrid_action, _ = minigrid_agent.predict(minigrid_obs)

    # Convert to Overcooked actions
    action_p0 = crafter_action_to_overcooked(crafter_action)
    action_p1 = minigrid_action_to_overcooked(minigrid_action)

    # Environment step
    state, reward, done, info = overcooked_env.step([action_p0, action_p1])

    # Render (optional)
    overcooked_env.render()