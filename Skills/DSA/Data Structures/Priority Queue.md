---
tags:
  - dsa
  - data-structures
  - priority-queue
  - heap
---

# Priority Queue / Heap

A container where the **highest (or lowest) priority** element is always at the front.

---

## Min-Heap vs Max-Heap

| | Top element | C++ default |
|---|---|---|
| **Max-Heap** | Largest | `priority_queue<int>` |
| **Min-Heap** | Smallest | `priority_queue<int, vector<int>, greater<int>>` |

---

## C++ STL Usage

```cpp
// Max-heap (default)
priority_queue<int> maxPQ;
maxPQ.push(5);
maxPQ.push(2);
maxPQ.push(8);
cout << maxPQ.top();  // 8
maxPQ.pop();

// Min-heap
priority_queue<int, vector<int>, greater<int>> minPQ;
minPQ.push(5);
minPQ.push(2);
minPQ.push(8);
cout << minPQ.top();  // 2

// Custom comparator (pair: sort by second element)
auto cmp = [](pair<int,int>& a, pair<int,int>& b) {
    return a.second > b.second;  // min by second
};
priority_queue<pair<int,int>, vector<pair<int,int>>, decltype(cmp)> pq(cmp);
```

---

## Manual Binary Heap

```cpp
struct MinHeap {
    vector<int> h;

    void push(int val) {
        h.push_back(val);
        int i = h.size() - 1;
        while (i > 0 && h[i] < h[(i - 1) / 2]) {
            swap(h[i], h[(i - 1) / 2]);
            i = (i - 1) / 2;
        }
    }

    int top() { return h[0]; }

    void pop() {
        h[0] = h.back();
        h.pop_back();
        int i = 0, n = h.size();
        while (true) {
            int smallest = i;
            int l = 2 * i + 1, r = 2 * i + 2;
            if (l < n && h[l] < h[smallest]) smallest = l;
            if (r < n && h[r] < h[smallest]) smallest = r;
            if (smallest == i) break;
            swap(h[i], h[smallest]);
            i = smallest;
        }
    }

    bool empty() { return h.empty(); }
    int size() { return h.size(); }
};
```

---

## Complexity

| Operation | Time |
|---|---|
| push | $O(\log n)$ |
| pop | $O(\log n)$ |
| top | $O(1)$ |
| heapify (build from array) | $O(n)$ |

---

## Use Cases

- **Dijkstra's algorithm** — min-heap for next closest vertex
- **K-th largest/smallest** — maintain heap of size k
- **Merge k sorted lists** — min-heap of list heads
- **Task scheduling** — process highest priority first
- **Median maintenance** — two heaps (max-heap + min-heap)
