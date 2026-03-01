---
tags:
  - dsa
  - algorithms
  - graph
  - dfs
  - bfs
  - traversal
---

# DFS & BFS

Graph/tree traversal fundamentals.

---

## DFS — Depth-First Search

Go as **deep** as possible before backtracking.

**Time:** $O(V + E)$ | **Space:** $O(V)$

### Recursive

```cpp
vector<vector<int>> adj;
vector<bool> visited;

void dfs(int u) {
    visited[u] = true;
    // process node u
    for (int v : adj[u]) {
        if (!visited[v])
            dfs(v);
    }
}
```

### Iterative (using stack)

```cpp
void dfs(int start) {
    stack<int> st;
    st.push(start);
    visited[start] = true;
    while (!st.empty()) {
        int u = st.top(); st.pop();
        for (int v : adj[u]) {
            if (!visited[v]) {
                visited[v] = true;
                st.push(v);
            }
        }
    }
}
```

**Use cases:** cycle detection, topological sort, connected components, backtracking.

---

## BFS — Breadth-First Search

Explore **level by level**. Guarantees shortest path in **unweighted** graphs.

**Time:** $O(V + E)$ | **Space:** $O(V)$

```cpp
vector<int> bfs(int start, int n) {
    vector<int> dist(n, -1);
    queue<int> q;
    dist[start] = 0;
    q.push(start);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }
    return dist;  // dist[i] = shortest distance from start to i
}
```

**Use cases:** shortest path (unweighted), level-order traversal, flood fill, multi-source BFS.

---

## BFS on Grid

```cpp
int dx[] = {0, 0, 1, -1};
int dy[] = {1, -1, 0, 0};

void bfsGrid(vector<vector<int>>& grid, int sr, int sc) {
    int n = grid.size(), m = grid[0].size();
    vector<vector<bool>> vis(n, vector<bool>(m, false));
    queue<pair<int,int>> q;
    q.push({sr, sc});
    vis[sr][sc] = true;
    while (!q.empty()) {
        auto [x, y] = q.front(); q.pop();
        for (int d = 0; d < 4; d++) {
            int nx = x + dx[d], ny = y + dy[d];
            if (nx >= 0 && nx < n && ny >= 0 && ny < m
                && !vis[nx][ny] && grid[nx][ny] == 0) {
                vis[nx][ny] = true;
                q.push({nx, ny});
            }
        }
    }
}
```

---

## DFS vs BFS

| | DFS | BFS |
|---|---|---|
| Data structure | Stack / recursion | Queue |
| Shortest path (unweighted) | No | Yes |
| Memory | $O(h)$ where $h$ = depth | $O(w)$ where $w$ = max width |
| Best for | Backtracking, exhaustive search | Shortest path, level-order |
