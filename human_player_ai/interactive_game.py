import time
import os
from two_agent_grid import TwoAgentGrid
from state_transition_example.q_agent import QLearningAgent

key_mapping = {
    "w": "up",
    "s": "down",
    "a": "left",
    "d": "right",
    "e": "interact",
    "": "noop"
}


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def state_repr(obs):
    return (
        obs["human_pos"],
        obs["agent_pos"],
        obs["holding"]["agent"]
    )


# Setup
env = TwoAgentGrid()
actions = ["up", "down", "left", "right", "interact"]
agent = QLearningAgent(actions)
transitions = []

obs = env.reset()
prev_state = state_repr(obs)

while True:
    clear()
    env.render()

    move = input("Your move (WASD to move, E to interact, Enter to skip, Q to quit): ").lower()
    if move == "q":
        break

    action = key_mapping.get(move, "noop")
    if action != "noop":
        if action == "interact":
            reward = env.interact("human")
            if reward:
                print("You delivered the onion! 🍲")
        else:
            env.move("human", action)

    # Agent chooses and performs action
    state = state_repr(env.get_obs())
    agent_action = agent.choose_action(state)

    if agent_action == "interact":
        reward = env.interact("agent")
        if reward:
            print("Agent delivered the onion! 🤖")
    else:
        env.move("agent", agent_action)

    next_obs = env.get_obs()
    next_state = state_repr(next_obs)
    reward = 1 if not env.holding["agent"] and tuple(env.agent_pos) == tuple(env.pot_pos) else 0

    agent.update(state, agent_action, reward, next_state)
    transitions.append((state, next_state))
    prev_state = next_state

    time.sleep(0.5)

# Save transitions for visualization
with open("agent_transitions.txt", "w") as f:
    for s1, s2 in transitions:
        f.write(f"{s1} -> {s2}\n")

print("\nSession ended. Transitions saved to agent_transitions.txt")
