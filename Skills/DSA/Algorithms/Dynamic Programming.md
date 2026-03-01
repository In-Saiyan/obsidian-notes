# Dynamic Programming

Solve problems by breaking them into **overlapping subproblems** and storing results.

**Key ingredients:**
1. **Optimal substructure** — optimal solution uses optimal solutions to subproblems
2. **Overlapping subproblems** — same subproblems are solved repeatedly

---

## 1D DP

### Fibonacci

```cpp
// O(n) time, O(1) space
int fib(int n) {
    if (n <= 1) return n;
    int a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        int c = a + b;
        a = b; b = c;
    }
    return b;
}
```

### Climbing Stairs

Ways to reach step $n$ (can take 1 or 2 steps at a time).

```cpp
int climbStairs(int n) {
    vector<int> dp(n + 1);
    dp[0] = dp[1] = 1;
    for (int i = 2; i <= n; i++)
        dp[i] = dp[i-1] + dp[i-2];
    return dp[n];
}
```

### Longest Increasing Subsequence (LIS)

```cpp
// O(n log n) using patience sorting
int lis(vector<int>& a) {
    vector<int> tails;
    for (int x : a) {
        auto it = lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) tails.push_back(x);
        else *it = x;
    }
    return tails.size();
}
```

---

## 2D DP

### 0/1 Knapsack

Given $n$ items with weight $w_i$ and value $v_i$, maximise value within capacity $W$.

$dp[i][j]$ = max value using first $i$ items with capacity $j$.

```cpp
int knapsack(vector<int>& wt, vector<int>& val, int W) {
    int n = wt.size();
    vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0));
    for (int i = 1; i <= n; i++) {
        for (int j = 0; j <= W; j++) {
            dp[i][j] = dp[i-1][j];  // skip item
            if (j >= wt[i-1])
                dp[i][j] = max(dp[i][j], dp[i-1][j - wt[i-1]] + val[i-1]);
        }
    }
    return dp[n][W];
}
```

### Longest Common Subsequence (LCS)

```cpp
int lcs(string& a, string& b) {
    int n = a.size(), m = b.size();
    vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= m; j++)
            dp[i][j] = (a[i-1] == b[j-1])
                ? dp[i-1][j-1] + 1
                : max(dp[i-1][j], dp[i][j-1]);
    return dp[n][m];
}
```

### Grid Unique Paths

Count paths from $(0,0)$ to $(m-1, n-1)$ moving only right or down.

```cpp
int uniquePaths(int m, int n) {
    vector<vector<int>> dp(m, vector<int>(n, 1));
    for (int i = 1; i < m; i++)
        for (int j = 1; j < n; j++)
            dp[i][j] = dp[i-1][j] + dp[i][j-1];
    return dp[m-1][n-1];
}
```

---

## 3D DP

### K Transactions Stock Problem

Maximise profit with at most $k$ transactions on $n$ days.

$dp[t][d][holding]$ = max profit on day $d$ with $t$ transactions used.

```cpp
int maxProfit(int k, vector<int>& prices) {
    int n = prices.size();
    if (n == 0) return 0;
    // dp[t][0] = not holding, dp[t][1] = holding
    vector<vector<int>> dp(k + 1, vector<int>(2, 0));
    for (int t = 0; t <= k; t++) dp[t][1] = -1e9;

    for (int d = 0; d < n; d++) {
        // iterate in reverse to avoid using updated values
        for (int t = k; t >= 1; t--) {
            dp[t][0] = max(dp[t][0], dp[t][1] + prices[d]);     // sell
            dp[t][1] = max(dp[t][1], dp[t-1][0] - prices[d]);   // buy
        }
    }
    return dp[k][0];
}
```

### 3D Grid DP — Two Players

Two players traverse an $n \times n$ grid simultaneously from $(0,0)$ to $(n-1, n-1)$, collecting maximum cherries. Same cells are not double-counted.

State: $dp[r1][c1][r2]$ (derive $c2 = r1 + c1 - r2$).

```cpp
int cherryPickup(vector<vector<int>>& grid) {
    int n = grid.size();
    // dp[r1][c1][r2], c2 = r1 + c1 - r2
    vector<vector<vector<int>>> dp(n, vector<vector<int>>(n, vector<int>(n, -1e9)));
    dp[0][0][0] = grid[0][0];

    for (int r1 = 0; r1 < n; r1++)
      for (int c1 = 0; c1 < n; c1++)
        for (int r2 = 0; r2 < n; r2++) {
            int c2 = r1 + c1 - r2;
            if (c2 < 0 || c2 >= n) continue;
            if (grid[r1][c1] == -1 || grid[r2][c2] == -1) continue;
            int val = grid[r1][c1];
            if (r1 != r2) val += grid[r2][c2];
            // transitions from 4 previous states
            for (auto [pr1, pc1] : vector<pair<int,int>>{{r1-1,c1},{r1,c1-1}})
              for (auto [pr2, pc2] : vector<pair<int,int>>{{r2-1,c2},{r2,c2-1}}) {
                  if (pr1 >= 0 && pc1 >= 0 && pr2 >= 0 && pc2 >= 0)
                      dp[r1][c1][r2] = max(dp[r1][c1][r2], dp[pr1][pc1][pr2] + val);
              }
        }
    return max(0, dp[n-1][n-1][n-1]);
}
```

---

## DP Patterns Cheat Sheet

| Pattern | Dimension | Examples |
|---|---|---|
| Linear | 1D | Fibonacci, Climbing Stairs, House Robber, LIS |
| Two-sequence | 2D | LCS, Edit Distance, Interleaving String |
| Knapsack | 2D | 0/1 Knapsack, Subset Sum, Coin Change |
| Grid | 2D | Unique Paths, Min Path Sum |
| Interval | 2D | Matrix Chain Multiplication, Burst Balloons |
| Multi-state | 3D | Stock with k transactions, Cherry Pickup |
| Bitmask | $2^n$ | TSP, Assign tasks to workers |
