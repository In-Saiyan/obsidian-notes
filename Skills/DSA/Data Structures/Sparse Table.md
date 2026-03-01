# Sparse Table

Static range query structure. Answers **idempotent** queries (min, max, gcd) in $O(1)$ after $O(n \log n)$ preprocessing.

---

## When to Use

- Array is **static** (no updates)
- Need fast **range min/max/gcd** queries
- Not suitable for range sum (use prefix sums or segment tree instead)

---

## How It Works

$st[i][j]$ = answer for the range starting at index $i$ with length $2^j$.

$$st[i][j] = \min(st[i][j-1], \; st[i + 2^{j-1}][j-1])$$

For a query $[l, r]$: find $k = \lfloor\log_2(r - l + 1)\rfloor$, then:

$$\text{answer} = \min(st[l][k], \; st[r - 2^k + 1][k])$$

The two ranges may overlap, but for idempotent operations that's fine.

---

## Code

```cpp
struct SparseTable {
    vector<vector<int>> st;
    vector<int> lg;

    SparseTable(vector<int>& a) {
        int n = a.size();
        int K = __lg(n) + 1;
        st.assign(n, vector<int>(K));
        lg.assign(n + 1, 0);
        for (int i = 2; i <= n; i++) lg[i] = lg[i / 2] + 1;

        for (int i = 0; i < n; i++) st[i][0] = a[i];
        for (int j = 1; j < K; j++)
            for (int i = 0; i + (1 << j) <= n; i++)
                st[i][j] = min(st[i][j-1], st[i + (1 << (j-1))][j-1]);
    }

    // Range minimum query [l, r] — O(1)
    int query(int l, int r) {
        int k = lg[r - l + 1];
        return min(st[l][k], st[r - (1 << k) + 1][k]);
    }
};
```

---

## Complexity

| Operation | Time |
|---|---|
| Build | $O(n \log n)$ |
| Query | $O(1)$ |
| Update | **Not supported** (rebuild needed) |
| Space | $O(n \log n)$ |
