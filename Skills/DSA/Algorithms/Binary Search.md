# Binary Search

Find target in a **sorted** array, or find the boundary where a condition changes.

**Time:** $O(\log n)$ | **Space:** $O(1)$

---

## Standard Binary Search

```cpp
int binarySearch(vector<int>& a, int target) {
    int lo = 0, hi = a.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return mid;
        else if (a[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;  // not found
}
```

---

## Lower Bound / Upper Bound

```cpp
// First index where a[i] >= target
int lowerBound(vector<int>& a, int target) {
    int lo = 0, hi = a.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < target) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

// First index where a[i] > target
int upperBound(vector<int>& a, int target) {
    int lo = 0, hi = a.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] <= target) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}
```

---

## Binary Search on Answer

When the answer space is monotonic (all `false` then all `true`), binary search for the boundary.

```cpp
// Find minimum x in [lo, hi] such that check(x) is true
int bsAnswer(int lo, int hi) {
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (check(mid)) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}
```

**Common applications:** minimum time, maximum capacity, smallest cost that satisfies a constraint.
