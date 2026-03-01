---
tags:
  - dsa
  - data-structures
  - dsu
  - union-find
---

# DSU (Disjoint Set Union / Union-Find)

Tracks a set of elements partitioned into **disjoint subsets**. Supports near-constant time union and find.

---

## Operations

| Operation | Description | Time |
|---|---|---|
| `find(x)` | Find the root/representative of x's set | $O(\alpha(n)) \approx O(1)$ |
| `unite(a, b)` | Merge the sets containing a and b | $O(\alpha(n)) \approx O(1)$ |
| `connected(a, b)` | Check if a and b are in the same set | $O(\alpha(n))$ |

$\alpha(n)$ is the inverse Ackermann function — effectively constant for all practical inputs.

---

## Code

```cpp
struct DSU {
    vector<int> par, rank_, size_;

    DSU(int n) : par(n), rank_(n, 0), size_(n, 1) {
        iota(par.begin(), par.end(), 0);
    }

    int find(int x) {
        return par[x] == x ? x : par[x] = find(par[x]);  // path compression
    }

    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;
        if (rank_[a] < rank_[b]) swap(a, b);  // union by rank
        par[b] = a;
        size_[a] += size_[b];
        if (rank_[a] == rank_[b]) rank_[a]++;
        return true;
    }

    bool connected(int a, int b) { return find(a) == find(b); }
    int getSize(int x) { return size_[find(x)]; }
};
```

---

## Use Cases

- **Connected components** — count components, check connectivity
- **Kruskal's MST** — edge-based MST construction
- **Cycle detection** in undirected graphs
- **Dynamic connectivity** — online edge additions
- **Account merging**, friend groups, equivalence classes
