---
tags:
  - dsa
  - data-structures
  - hash-map
  - hash-set
  - hashing
---

# Hash Map & Hash Set

Unordered containers with **average $O(1)$** lookup, insert, and delete.

---

## C++ STL

```cpp
// Hash map — key → value
unordered_map<string, int> mp;
mp["alice"] = 1;
mp["bob"] = 2;
cout << mp["alice"];      // 1
cout << mp.count("bob");  // 1
mp.erase("bob");

for (auto& [key, val] : mp)
    cout << key << ": " << val << "\n";

// Hash set — unique keys only
unordered_set<int> st;
st.insert(5);
st.insert(3);
st.insert(5);  // ignored (duplicate)
cout << st.size();       // 2
cout << st.count(3);     // 1
st.erase(3);
```

---

## Ordered vs Unordered

| | `map` / `set` | `unordered_map` / `unordered_set` |
|---|---|---|
| Underlying structure | Red-black tree | Hash table |
| Lookup | $O(\log n)$ | $O(1)$ average, $O(n)$ worst |
| Ordered iteration | Yes | No |
| Custom comparator | Easy | Need custom hash |

---

## Custom Hash (for `pair`, etc.)

```cpp
struct PairHash {
    size_t operator()(const pair<int,int>& p) const {
        auto h1 = hash<int>{}(p.first);
        auto h2 = hash<int>{}(p.second);
        return h1 ^ (h2 << 32);
    }
};

unordered_map<pair<int,int>, int, PairHash> mp;
```

---

## Common Patterns

### Two Sum

```cpp
vector<int> twoSum(vector<int>& a, int target) {
    unordered_map<int, int> mp;
    for (int i = 0; i < (int)a.size(); i++) {
        int complement = target - a[i];
        if (mp.count(complement))
            return {mp[complement], i};
        mp[a[i]] = i;
    }
    return {};
}
```

### Frequency Count

```cpp
unordered_map<int, int> freq;
for (int x : a) freq[x]++;
```

---

## Complexity

| Operation | Average | Worst |
|---|---|---|
| Insert | $O(1)$ | $O(n)$ |
| Lookup | $O(1)$ | $O(n)$ |
| Delete | $O(1)$ | $O(n)$ |
| Space | $O(n)$ | $O(n)$ |

> **Tip:** Worst case ($O(n)$) happens with hash collisions. In competitive programming, use a custom hash or `map` to avoid anti-hash attacks.
