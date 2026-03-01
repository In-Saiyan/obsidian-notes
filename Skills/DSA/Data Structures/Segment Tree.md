# Segment Tree

Supports **range queries** and **point/range updates** in $O(\log n)$.

---

## When to Use

- Need range queries (sum, min, max, gcd, etc.)
- Array is **dynamic** (elements can be updated)
- Sparse Table won't work because of updates

---

## Basic Segment Tree (Point Update, Range Query)

```cpp
struct SegTree {
    int n;
    vector<long long> tree;

    SegTree(vector<int>& a) : n(a.size()), tree(4 * a.size(), 0) {
        build(a, 1, 0, n - 1);
    }

    void build(vector<int>& a, int node, int lo, int hi) {
        if (lo == hi) { tree[node] = a[lo]; return; }
        int mid = (lo + hi) / 2;
        build(a, 2 * node, lo, mid);
        build(a, 2 * node + 1, mid + 1, hi);
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }

    // Point update: a[pos] = val
    void update(int pos, int val, int node, int lo, int hi) {
        if (lo == hi) { tree[node] = val; return; }
        int mid = (lo + hi) / 2;
        if (pos <= mid) update(pos, val, 2 * node, lo, mid);
        else update(pos, val, 2 * node + 1, mid + 1, hi);
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }

    // Range query: sum of [l, r]
    long long query(int l, int r, int node, int lo, int hi) {
        if (r < lo || hi < l) return 0;  // out of range
        if (l <= lo && hi <= r) return tree[node];  // fully inside
        int mid = (lo + hi) / 2;
        return query(l, r, 2 * node, lo, mid)
             + query(l, r, 2 * node + 1, mid + 1, hi);
    }

    // Convenience wrappers
    void update(int pos, int val) { update(pos, val, 1, 0, n - 1); }
    long long query(int l, int r) { return query(l, r, 1, 0, n - 1); }
};
```

---

## Lazy Propagation (Range Update, Range Query)

Defer updates to child nodes until needed.

```cpp
struct LazySegTree {
    int n;
    vector<long long> tree, lazy;

    LazySegTree(int n) : n(n), tree(4 * n, 0), lazy(4 * n, 0) {}

    void push(int node, int lo, int hi) {
        if (lazy[node] == 0) return;
        int mid = (lo + hi) / 2;
        apply(2 * node, lo, mid, lazy[node]);
        apply(2 * node + 1, mid + 1, hi, lazy[node]);
        lazy[node] = 0;
    }

    void apply(int node, int lo, int hi, long long val) {
        tree[node] += val * (hi - lo + 1);
        lazy[node] += val;
    }

    // Range update: add val to all elements in [l, r]
    void update(int l, int r, long long val, int node, int lo, int hi) {
        if (r < lo || hi < l) return;
        if (l <= lo && hi <= r) { apply(node, lo, hi, val); return; }
        push(node, lo, hi);
        int mid = (lo + hi) / 2;
        update(l, r, val, 2 * node, lo, mid);
        update(l, r, val, 2 * node + 1, mid + 1, hi);
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }

    // Range query: sum of [l, r]
    long long query(int l, int r, int node, int lo, int hi) {
        if (r < lo || hi < l) return 0;
        if (l <= lo && hi <= r) return tree[node];
        push(node, lo, hi);
        int mid = (lo + hi) / 2;
        return query(l, r, 2 * node, lo, mid)
             + query(l, r, 2 * node + 1, mid + 1, hi);
    }

    void update(int l, int r, long long val) { update(l, r, val, 1, 0, n - 1); }
    long long query(int l, int r) { return query(l, r, 1, 0, n - 1); }
};
```

---

## Complexity

| Operation | Basic | Lazy Propagation |
|---|---|---|
| Build | $O(n)$ | $O(n)$ |
| Point Update | $O(\log n)$ | $O(\log n)$ |
| Range Update | $O(n \log n)$ | $O(\log n)$ |
| Range Query | $O(\log n)$ | $O(\log n)$ |
| Space | $O(n)$ | $O(n)$ |

---

## Segment Tree vs Sparse Table vs Fenwick (BIT)

| | Segment Tree | Sparse Table | Fenwick Tree |
|---|---|---|---|
| Range query | $O(\log n)$ | $O(1)$ | $O(\log n)$ |
| Point update | $O(\log n)$ | Not supported | $O(\log n)$ |
| Range update | $O(\log n)$ (lazy) | Not supported | $O(\log n)$ |
| Code complexity | High | Low | Medium |
| Best for | General purpose | Static RMQ | Prefix sums with updates |
