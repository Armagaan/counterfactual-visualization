"""Visualize counterfactual graphs."""

# -----> Imports
import os
import pickle
import shutil
import sys

import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

np.random.seed(7)
plt.style.use('seaborn')
matplotlib.rcParams['figure.figsize'] = (8, 6)

# -----> Checks
if len(sys.argv) != 3:
    print("\nUSAGE: python code/visualize.py [INPUT] [OUTPUT]")
    print("[INPUT]: Path to input dataset.")
    print("[OUTPUT]: Path to folder where the generated plots will be saved.\n")
    exit(1)
INPUT = sys.argv[1]
OUTPUT = sys.argv[2]
os.makedirs(OUTPUT, exist_ok=True)

# -----> Data
with open(INPUT, "rb") as file:
    data = pickle.load(file)
first_key = list(data.keys())[0]
# Reorder the cfs such that the source node label
# is always smaller than the destination.
# It makes plotting easier later on.
for node_id in data:
    for i, cf in enumerate(data[node_id]['cfs']):
        src, dest, action = cf[0], cf[1], cf[2]
        if src > dest:
            src, dest = dest, src
            data[node_id]['cfs'][i] = [src, dest, action]

# -----> Visualize
THRESHOLD = 15
LINE_WIDTH = 2

## -----> Graph
# Folder to store plots.
OUT_PATH = OUTPUT + "/graph/"
if os.path.exists(OUT_PATH):
    shutil.rmtree(OUT_PATH)
os.makedirs(OUT_PATH)

# Iterate over the graphs.
for node_id in data:
    # Discard large graphs.
    if data[node_id]['adj'].sum() // 2 > THRESHOLD:
        continue
    graph = nx.from_numpy_array(data[node_id]['adj'])
    pos = nx.spring_layout(graph, seed=7)
    
    # Assign colors to the nodes.
    color_map = list()
    for node in graph:
        if node == data[node_id]['target']:
            color_map.append("#F28C28")
        else:
            color_map.append("#00308F")

    # Draw and save the plot.
    nx.draw(
        G=graph,
        pos=pos,
        node_color=color_map,
        width=LINE_WIDTH,
    )
    plt.savefig(OUT_PATH + f"{node_id}" + ".png", format="png")
    
    # Clear the plot for next iteration.
    # Otherwise it will draw the new graph on top of it.
    plt.clf()

## -----> Colored Map
# Folder to store plots.
OUT_PATH = OUTPUT + "/colored_graphs/"
if os.path.exists(OUT_PATH):
    shutil.rmtree(OUT_PATH)
os.makedirs(OUT_PATH)

# Iterate over the graphs.
for node_id in data:
    # Discard large graphs.
    if data[node_id]['adj'].sum() // 2 > THRESHOLD:
        continue

    # Create the graph
    graph = nx.from_numpy_array(data[node_id]['adj'])
    pos = nx.spring_layout(graph, seed=7)

    # Assign colors to the nodes.
    color_map = list()
    for node in graph:
        if node == data[node_id]['target']:
            color_map.append("#F28C28")
        else:
            color_map.append("#00308F")

    # Introduce cf edges where the action == add.
    cfs = data[node_id]['cfs']
    for cf in cfs:
        src, dest, action = cf
        if action == 'add':
            graph.add_edge(src, dest)

    # Assign colors to the edges
    cf_edges = [(cf[0], cf[1]) for cf in cfs]
    cf_actions = [cf[2] for cf in cfs]
    edge_color_map = list()
    for edge in graph.edges:
        if edge not in cf_edges:
            edge_color_map.append("black")
            continue
        index = cf_edges.index(edge)
        action = cf_actions[index]
        if action == 'del':
            edge_color_map.append("red")
        else:
            edge_color_map.append("green")

    # Draw
    nx.draw(
        G=graph,
        pos=pos,
        node_color=color_map,
        width=LINE_WIDTH,
        edge_color=edge_color_map,
    )

    # Save the plot.
    plt.savefig(OUT_PATH + f"{node_id}" + ".png", format="png")

    # Clear the plot for next iteration.
    # Otherwise it will draw the new graph on top of it.
    plt.clf()

## -----> Perturbed Graph
# Folder to store plots.
OUT_PATH = OUTPUT + "/perturbed_graphs/"
if os.path.exists(OUT_PATH):
    shutil.rmtree(OUT_PATH)
os.makedirs(OUT_PATH)

# Iterate over the graphs.
for node_id in data:
    # Discard large graphs.
    if data[node_id]['adj'].sum() // 2 > THRESHOLD:
        continue

    # Create the graph
    graph = nx.from_numpy_array(data[node_id]['adj'])
    pos = nx.spring_layout(graph, seed=7)

    # Assign colors to the nodes.
    color_map = list()
    for node in graph:
        if node == data[node_id]['target']:
            color_map.append("#F28C28")
        else:
            color_map.append("#00308F")

    # Perturb the graph
    cfs = data[node_id]['cfs']
    for cf in cfs:
        src, dest, action = cf[0], cf[1], cf[2]
        if action == 'del':
            graph.remove_edge(src, dest)
        else:
            graph.add_edge(src, dest)

    # Draw
    nx.draw(
        G=graph,
        pos=pos,
        node_color=color_map,
        width=LINE_WIDTH,
    )

    # Save the plot.
    plt.savefig(OUT_PATH + f"{node_id}" + ".png", format="png")

    # Clear the plot for next iteration.
    # Otherwise it will draw the new graph on top of it.
    plt.clf()
