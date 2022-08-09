# counterfactual-visualization
Visualize counterfactuals of small sized graphs.

## Create conda environment
- Create conda env : `conda env create -f gnn.yaml`
- Run : `conda activate gnn` prior to using this repo.

## Inputs
- A pickled nested dictionary of the form : `{'node_id': {'target': ..., 'adj': ..., 'cfs': ...}}`
    - `node_id` : The target node's ID in the graph. This will be different from `target` in case a subadjacency is provided for `adj` and a remapping of nodes of was done while getting the subadjacency.
    - `adj` : Adjacency matrix
    - `target` : Target node
    - `cfs` : List of counterfactual edges (CFs)

## Input formats
- Adjacency matrix : `numpy.ndarray` of shape : `n*n`.
- Target node : `int`
- List of CFs : `[(source, destination, action), (source, destination, action), ...]`
- Edges should not be repeated i.e. in an undirected graph each edge is listed twice e.g., `(1,2)` and `(2,1)`. Only one of the entries should be provided.

## Output
- A PNG image with dimensions : `800 x 600`
