from collections import Counter
from state_agent import DummyGridWorld

def abstract_state(state):
    return state

def collect_transitions(env, steps=200):
    transition_counts = Counter()
    prev_abstract_state = None

    for _ in range(steps):
        obs = env.get_obs()
        abstract = abstract_state(obs)
        if prev_abstract_state is not None:
            transition_counts[(prev_abstract_state, abstract)] += 1
        prev_abstract_state = abstract
        env.step(None)

    return transition_counts
