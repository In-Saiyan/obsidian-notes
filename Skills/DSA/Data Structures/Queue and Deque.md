---
tags:
  - dsa
  - data-structures
  - queue
  - deque
---

# Queue & Deque

---

## Queue — FIFO

**First In, First Out.**

```cpp
queue<int> q;
q.push(1);
q.push(2);
q.push(3);
cout << q.front(); // 1
cout << q.back();  // 3
q.pop();           // removes 1
cout << q.front(); // 2
```

**Use cases:** BFS, task scheduling, buffering.

---

## Deque — Double-Ended Queue

Insert and remove from **both ends** in $O(1)$.

```cpp
deque<int> dq;
dq.push_back(1);
dq.push_front(2);
dq.push_back(3);
// dq = [2, 1, 3]
cout << dq.front(); // 2
cout << dq.back();  // 3
dq.pop_front();
dq.pop_back();
// dq = [1]
```

---

## Sliding Window Maximum (Monotonic Deque)

Find the maximum in every window of size $k$ in $O(n)$.

```cpp
vector<int> maxSlidingWindow(vector<int>& a, int k) {
    deque<int> dq;  // stores indices, front = index of max in window
    vector<int> res;
    for (int i = 0; i < (int)a.size(); i++) {
        // remove elements outside window
        while (!dq.empty() && dq.front() <= i - k)
            dq.pop_front();
        // maintain decreasing order
        while (!dq.empty() && a[dq.back()] <= a[i])
            dq.pop_back();
        dq.push_back(i);
        if (i >= k - 1)
            res.push_back(a[dq.front()]);
    }
    return res;
}
```

---

## Complexity

| Operation | Queue | Deque |
|---|---|---|
| push_back | $O(1)$ | $O(1)$ |
| push_front | — | $O(1)$ |
| pop_front | $O(1)$ | $O(1)$ |
| pop_back | — | $O(1)$ |
| front / back | $O(1)$ | $O(1)$ |
| Random access | — | $O(1)$ |
