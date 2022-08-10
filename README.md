# counterfactual-visualization
Visualize counterfactuals of small sized graphs.

<img src="https://github.com/Armagaan/counterfactual-visualization/blob/main/graph_602.png?raw=true" alt="Graph" width="270"/> <img src="https://github.com/Armagaan/counterfactual-visualization/blob/main/colored_graph_602.png?raw=true" alt="Graph" width="270"/> <img src="https://github.com/Armagaan/counterfactual-visualization/blob/main/perturbed_graph_602.png?raw=true" alt="Graph" width="270"/>

## Create conda environment
- Create conda env : `conda env create -f gnn.yaml`
- Run : `conda activate gnn` prior to using this repo.

## Inputs
- A pickled nested dictionary of the form : `{'node_id': {'target': ..., 'adj': ..., 'cfs': ...}}`
    - `node_id` : The target node's ID in the graph.
    - `adj` : Adjacency matrix.
    - `target` : Target node.
        - Same as `node_id` if the entire graph is provided.
        - Mapped `node_id` in case a subadjacency is provided for `adj` and a mapping of nodes of was done while getting the subadjacency.  
    - `cfs` : List of counterfactual edges (CFs).

## Input formats
- Adjacency matrix : `numpy.ndarray` of shape : `n * n`.
- Target node : `int`.
- List of CFs : `[(source: int, destination: int, action: str), (source: int, destination: int, action: str), ...]`.
    - `action` : either `add` or `del`.
- Edges should not be repeated i.e. in an undirected graph each edge is listed twice e.g., `(1,2)` and `(2,1)`. Only one of the entries should be provided.

## Output
- A PNG image with dimensions : `800 x 600`.

## Note
In case the `adj` is a subgraph and not the full graph, and the process involved mapping of node IDs:
- Please provide `target` as the mapped node ID of `node_id`.
- Please provide the mapped `source` and `destionation` node IDs in the list of CFs.
