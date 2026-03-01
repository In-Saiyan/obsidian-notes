---
tags:
  - dsa
  - algorithms
  - graph
  - shortest-path
  - mst
  - dijkstra
---

# Graph Algorithms — Shortest Path & MST

---

## Dijkstra's Algorithm

**Shortest path** from a single source in a **non-negative weight** graph.

**Time:** $O((V + E) \log V)$ with min-heap

```cpp
vector<long long> dijkstra(int src, vector<vector<pair<int,int>>>& adj, int n) {
    vector<long long> dist(n, 1e18);
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
    dist[src] = 0;
    pq.push({0, src});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```

| Property | Value |
|---|---|
| Negative weights | **Not supported** |
| Graph type | Directed or undirected |
| Best for | Sparse graphs with non-negative weights |

---

## Bellman-Ford Algorithm

**Single-source shortest path** that handles **negative weights**. Detects negative cycles.

**Time:** $O(V \cdot E)$

```cpp
struct Edge { int u, v, w; };

vector<long long> bellmanFord(int src, vector<Edge>& edges, int n) {
    vector<long long> dist(n, 1e18);
    dist[src] = 0;
    for (int i = 0; i < n - 1; i++) {
        for (auto& [u, v, w] : edges) {
            if (dist[u] < 1e18 && dist[u] + w < dist[v])
                dist[v] = dist[u] + w;
        }
    }
    // Check for negative cycles
    for (auto& [u, v, w] : edges) {
        if (dist[u] < 1e18 && dist[u] + w < dist[v])
            return {};  // negative cycle exists
    }
    return dist;
}
```

| Property | Value |
|---|---|
| Negative weights | **Yes** |
| Negative cycle detection | **Yes** |
| Best for | Graphs with negative edges |

---

## Floyd-Warshall Algorithm

**All-pairs shortest path.**

**Time:** $O(V^3)$ | **Space:** $O(V^2)$

```cpp
void floydWarshall(vector<vector<long long>>& dist, int n) {
    // dist[i][j] initialised to edge weight or INF if no edge; dist[i][i] = 0
    for (int k = 0; k < n; k++)
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
}
```

| Property | Value |
|---|---|
| Negative weights | **Yes** (no negative cycles) |
| Negative cycle detection | `dist[i][i] < 0` after running |
| Best for | Dense graphs, all-pairs queries |

---

## Kruskal's Algorithm (MST)

Build a **Minimum Spanning Tree** by greedily picking the smallest edges using **Union-Find**.

**Time:** $O(E \log E)$

```cpp
struct Edge { int u, v, w; };

struct DSU {
    vector<int> par, rank_;
    DSU(int n) : par(n), rank_(n, 0) { iota(par.begin(), par.end(), 0); }
    int find(int x) { return par[x] == x ? x : par[x] = find(par[x]); }
    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;
        if (rank_[a] < rank_[b]) swap(a, b);
        par[b] = a;
        if (rank_[a] == rank_[b]) rank_[a]++;
        return true;
    }
};

long long kruskal(vector<Edge>& edges, int n) {
    sort(edges.begin(), edges.end(), [](auto& a, auto& b) {
        return a.w < b.w;
    });
    DSU dsu(n);
    long long mst = 0;
    int count = 0;
    for (auto& [u, v, w] : edges) {
        if (dsu.unite(u, v)) {
            mst += w;
            if (++count == n - 1) break;
        }
    }
    return mst;
}
```

---

## Prim's Algorithm (MST)

Grow the MST from a starting vertex using a **min-heap**.

**Time:** $O((V + E) \log V)$

```cpp
long long prim(vector<vector<pair<int,int>>>& adj, int n) {
    vector<bool> inMST(n, false);
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
    pq.push({0, 0});
    long long mst = 0;
    int count = 0;
    while (!pq.empty() && count < n) {
        auto [w, u] = pq.top(); pq.pop();
        if (inMST[u]) continue;
        inMST[u] = true;
        mst += w;
        count++;
        for (auto [v, wt] : adj[u])
            if (!inMST[v]) pq.push({wt, v});
    }
    return mst;
}
```

---

## A* Search Algorithm

**Informed** shortest-path search using a **heuristic** $h(n)$ to guide exploration. Optimal when $h$ is **admissible** (never overestimates).

$f(n) = g(n) + h(n)$

- $g(n)$ = actual cost from start
- $h(n)$ = estimated cost to goal

```cpp
struct Node {
    int id;
    long long g, f;
    bool operator>(const Node& o) const { return f > o.f; }
};

long long aStar(int src, int goal, vector<vector<pair<int,int>>>& adj,
                function<long long(int)> heuristic, int n) {
    vector<long long> g(n, 1e18);
    priority_queue<Node, vector<Node>, greater<>> pq;
    g[src] = 0;
    pq.push({src, 0, heuristic(src)});

    while (!pq.empty()) {
        auto [u, gu, fu] = pq.top(); pq.pop();
        if (u == goal) return gu;
        if (gu > g[u]) continue;
        for (auto [v, w] : adj[u]) {
            long long ng = gu + w;
            if (ng < g[v]) {
                g[v] = ng;
                pq.push({v, ng, ng + heuristic(v)});
            }
        }
    }
    return -1;  // unreachable
}

// Common heuristics for grids:
// Manhattan: |x1 - x2| + |y1 - y2|
// Euclidean: sqrt((x1-x2)^2 + (y1-y2)^2)
```

---

## Comparison

| Algorithm | Type | Negative Weights | Time |
|---|---|---|---|
| **Dijkstra** | Single-source | No | $O((V+E)\log V)$ |
| **Bellman-Ford** | Single-source | Yes | $O(VE)$ |
| **Floyd-Warshall** | All-pairs | Yes | $O(V^3)$ |
| **A*** | Single-pair | No | Depends on heuristic |
| **Kruskal** | MST | N/A | $O(E \log E)$ |
| **Prim** | MST | N/A | $O((V+E)\log V)$ |
