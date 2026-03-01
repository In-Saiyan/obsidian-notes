# Stack

**LIFO** (Last In, First Out) — the last element added is the first one removed.

---

## C++ STL

```cpp
stack<int> st;
st.push(1);
st.push(2);
st.push(3);
cout << st.top();  // 3
st.pop();
cout << st.top();  // 2
cout << st.size(); // 2
cout << st.empty(); // false
```

---

## Common Patterns

### Monotonic Stack

Maintain a stack where elements are in **increasing** (or decreasing) order. Used to find the **next greater/smaller element** in $O(n)$.

```cpp
// Next Greater Element for each index
vector<int> nextGreater(vector<int>& a) {
    int n = a.size();
    vector<int> res(n, -1);
    stack<int> st;  // stores indices
    for (int i = 0; i < n; i++) {
        while (!st.empty() && a[st.top()] < a[i]) {
            res[st.top()] = a[i];
            st.pop();
        }
        st.push(i);
    }
    return res;
}
```

### Valid Parentheses

```cpp
bool isValid(string s) {
    stack<char> st;
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') st.push(c);
        else {
            if (st.empty()) return false;
            char top = st.top(); st.pop();
            if ((c == ')' && top != '(') ||
                (c == ']' && top != '[') ||
                (c == '}' && top != '{')) return false;
        }
    }
    return st.empty();
}
```

### Largest Rectangle in Histogram

```cpp
int largestRectangle(vector<int>& heights) {
    stack<int> st;
    int maxArea = 0, n = heights.size();
    for (int i = 0; i <= n; i++) {
        int h = (i == n) ? 0 : heights[i];
        while (!st.empty() && h < heights[st.top()]) {
            int height = heights[st.top()]; st.pop();
            int width = st.empty() ? i : i - st.top() - 1;
            maxArea = max(maxArea, height * width);
        }
        st.push(i);
    }
    return maxArea;
}
```

---

## Complexity

| Operation | Time |
|---|---|
| push | $O(1)$ |
| pop | $O(1)$ |
| top | $O(1)$ |
| size | $O(1)$ |

---

## Use Cases

- Expression evaluation & parsing
- Undo/redo operations
- DFS (iterative)
- Monotonic stack problems (next greater, stock span, histogram)
- Backtracking
