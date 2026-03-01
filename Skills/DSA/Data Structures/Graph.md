---
tags:
  - dsa
  - data-structures
  - graph
---

# Graph

A collection of **vertices** (nodes) connected by **edges**.

---

## Representations

### Adjacency List (preferred for sparse graphs)

```cpp
int n = 5;  // number of vertices
vector<vector<int>> adj(n);

// Add undirected edge
adj[0].push_back(1);
adj[1].push_back(0);

// Weighted graph
vector<vector<pair<int,int>>> wadj(n);  // {neighbour, weight}
wadj[0].push_back({1, 10});
```

### Adjacency Matrix (for dense graphs)

```cpp
vector<vector<int>> mat(n, vector<int>(n, 0));
mat[0][1] = 1;  // edge from 0 to 1
mat[1][0] = 1;  // undirected
```

### Edge List

```cpp
struct Edge { int u, v, w; };
vector<Edge> edges;
edges.push_back({0, 1, 10});
```

---

## Types

| Type | Description |
|---|---|
| **Undirected** | Edges have no direction |
| **Directed (Digraph)** | Edges have direction |
| **Weighted** | Edges have costs |
| **Unweighted** | All edges cost 1 |
| **DAG** | Directed Acyclic Graph |
| **Bipartite** | Vertices split into 2 sets; edges only between sets |

---

## Common Operations

### Topological Sort (DAG only)

```cpp
// Kahn's algorithm (BFS) — O(V + E)
vector<int> topoSort(vector<vector<int>>& adj, int n) {
    vector<int> indeg(n, 0);
    for (int u = 0; u < n; u++)
        for (int v : adj[u]) indeg[v]++;

    queue<int> q;
    for (int i = 0; i < n; i++)
        if (indeg[i] == 0) q.push(i);

    vector<int> order;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        order.push_back(u);
        for (int v : adj[u])
            if (--indeg[v] == 0) q.push(v);
    }
    return order;  // if order.size() < n → cycle exists
}
```

### Cycle Detection (Undirected — Union-Find)

```cpp
struct DSU {
    vector<int> par;
    DSU(int n) : par(n) { iota(par.begin(), par.end(), 0); }
    int find(int x) { return par[x] == x ? x : par[x] = find(par[x]); }
    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;  // cycle!
        par[b] = a;
        return true;
    }
};
```

### Bipartite Check (BFS colouring)

```cpp
bool isBipartite(vector<vector<int>>& adj, int n) {
    vector<int> color(n, -1);
    for (int i = 0; i < n; i++) {
        if (color[i] != -1) continue;
        queue<int> q;
        q.push(i);
        color[i] = 0;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int v : adj[u]) {
                if (color[v] == -1) {
                    color[v] = color[u] ^ 1;
                    q.push(v);
                } else if (color[v] == color[u]) return false;
            }
        }
    }
    return true;
}
```

---

## Complexity

| Representation | Space | Add Edge | Check Edge | Iterate Neighbours |
|---|---|---|---|---|
| Adjacency List | $O(V + E)$ | $O(1)$ | $O(\text{deg})$ | $O(\text{deg})$ |
| Adjacency Matrix | $O(V^2)$ | $O(1)$ | $O(1)$ | $O(V)$ |
| Edge List | $O(E)$ | $O(1)$ | $O(E)$ | $O(E)$ |
