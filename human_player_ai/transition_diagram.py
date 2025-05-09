
import networkx as nx
import matplotlib.pyplot as plt
import time

# Load transitions from file
with open("agent_transitions.txt", "r") as f:
    lines = f.readlines()

edges = []
for line in lines:
    parts = line.strip().split(" -> ")
    if len(parts) == 2:
        edges.append((parts[0], parts[1]))

# Create graph
G = nx.DiGraph()
G.add_edges_from(edges)

# Count visit frequencies
node_freq = {}
for s1, s2 in edges:
    node_freq[s1] = node_freq.get(s1, 0) + 1
    node_freq[s2] = node_freq.get(s2, 0) + 1

# Layout
pos = nx.spring_layout(G)

# Draw static parts
plt.ion()
fig, ax = plt.subplots(figsize=(10, 7))

nx.draw_networkx_nodes(G, pos, node_size=[300 + node_freq[n]*50 for n in G.nodes()], node_color="lightblue", ax=ax)
nx.draw_networkx_labels(G, pos, ax=ax, font_size=8)
nx.draw_networkx_edges(G, pos, edge_color="gray", arrows=True, ax=ax)
plt.title("Agent State Transition Replay")
plt.pause(1)

# Animate the actual run
for s1, s2 in edges:
    nx.draw_networkx_edges(G, pos, edgelist=[(s1, s2)], edge_color="red", width=2, arrows=True, ax=ax)
    plt.pause(0.3)

plt.ioff()
plt.show()
