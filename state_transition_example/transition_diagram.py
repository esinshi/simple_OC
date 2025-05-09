# import networkx as nx
# import matplotlib.pyplot as plt
# from state_agent import DummyGridWorld
# from q_agent import QLearningAgent
# from collections import defaultdict
# import matplotlib.cm as cm
#
# # Setup
# env = DummyGridWorld()
# actions = ["do_nothing"]
# aq_agent = QLearningAgent(actions)
#
# transition_counts = {}
# visit_counts = defaultdict(int)
# loop_edges = set()
# path_history = []
#
# # Learning loop
# for _ in range(5):
#     obs = env.get_obs()
#     visit_counts[obs] += 1
#     abstract = obs
#     action = aq_agent.choose_action(abstract)
#     next_obs = env.step(action)
#     reward = 1 if next_obs == "pot_full" else 0
#     next_abstract = next_obs
#     aq_agent.update(abstract, action, reward, next_abstract)
#     path_history.append((abstract, next_abstract))
#
#     if (abstract, next_abstract) not in transition_counts:
#         transition_counts[(abstract, next_abstract)] = 0
#     transition_counts[(abstract, next_abstract)] += 1
#
# # Detect loops
# for (s1, s2), _ in transition_counts.items():
#     if (s2, s1) in transition_counts:
#         loop_edges.add((s1, s2))
#         loop_edges.add((s2, s1))
#
# # Build graph
# G = nx.DiGraph()
# for (s1, s2), count in transition_counts.items():
#     G.add_edge(s1, s2, weight=count)
#
# # Normalize visit frequency for node colors
# max_visits = max(visit_counts.values())
# node_colors = [visit_counts.get(n, 0) / max_visits for n in G.nodes()]
#
# # Graph layout
# pos = nx.spring_layout(G, seed=42)
#
# # Plot
# fig, ax = plt.subplots(figsize=(10, 7))
# nx.draw(
#     G, pos,
#     with_labels=True,
#     node_size=1500,
#     node_color=node_colors,
#     cmap=cm.OrRd,
#     edge_color=["red" if (u, v) in loop_edges else "gray" for u, v in G.edges()],
#     font_size=12,
#     ax=ax
# )
# edge_labels = nx.get_edge_attributes(G, 'weight')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
# ax.set_title("State Transition Graph")
# plt.colorbar(plt.cm.ScalarMappable(cmap=cm.OrRd), ax=ax, label="Visit Frequency")
# plt.show()
#
# # Print Q-table
# print("\nLearned Q-values:")
# for state, values in aq_agent.get_q_values().items():
#     print(f"{state}: {values}")

import networkx as nx
import matplotlib.pyplot as plt

# Load transitions
def load_transitions(filename):
    edges = []
    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().split(" -> ")
            if len(parts) == 2:
                edges.append((parts[0], parts[1]))
    return edges

edges1 = load_transitions("agent1_transitions.txt")
edges2 = load_transitions("agent2_transitions.txt")

G = nx.DiGraph()
G.add_edges_from(edges1)
G.add_edges_from(edges2)

# Frequency-based sizing/color
node_freq = {}
for s1, s2 in edges1 + edges2:
    node_freq[s1] = node_freq.get(s1, 0) + 1
    node_freq[s2] = node_freq.get(s2, 0) + 1

edge_colors = []
for edge in G.edges():
    if edge in edges1 and edge in edges2:
        edge_colors.append("purple")  # shared transition
    elif edge in edges1:
        edge_colors.append("blue")
    else:
        edge_colors.append("green")

# Draw graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)

nx.draw_networkx_nodes(G, pos, node_size=[300 + node_freq[n]*50 for n in G.nodes()], node_color="lightgray")
nx.draw_networkx_labels(G, pos, font_size=7)
nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrows=True)

plt.title("State Transition Graph - Agent1 (Blue), Agent2 (Green), Shared (Purple)")
plt.tight_layout()
plt.show()
