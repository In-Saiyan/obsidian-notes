# Ordered Set (Policy-Based)

A **balanced BST** from GCC's policy-based data structures that supports all `std::set` operations **plus** order-statistics queries in $O(\log n)$.

---

## Setup

```cpp
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/tree_policy.hpp>

template <typename T>
using oset = __gnu_pbds::tree<
    T,
    __gnu_pbds::null_type,
    std::less<T>,
    __gnu_pbds::rb_tree_tag,
    __gnu_pbds::tree_order_statistics_node_update
>;
```

> For an **ordered multiset** (allow duplicates), use `std::less_equal<T>` — but `erase()` and `find()` break. Prefer storing `pair<T, int>` instead (value + unique id).

---

## Extra Operations

| Method | Description | Time |
|---|---|---|
| `find_by_order(k)` | Iterator to the **k-th** element (0-indexed) | $O(\log n)$ |
| `order_of_key(x)` | Count of elements **strictly less than** x | $O(\log n)$ |

All standard `set` operations (`insert`, `erase`, `find`, `lower_bound`, `upper_bound`) also work.

---

## Usage

```cpp
oset<int> s;
s.insert(1);
s.insert(3);
s.insert(5);
s.insert(7);
s.insert(9);
// s = {1, 3, 5, 7, 9}

// find_by_order(k) — 0-indexed k-th smallest
auto it = s.find_by_order(0);  // → 1
it = s.find_by_order(2);       // → 5
it = s.find_by_order(4);       // → 9

// order_of_key(x) — number of elements < x
s.order_of_key(5);   // 2  (elements 1, 3 are < 5)
s.order_of_key(6);   // 3  (elements 1, 3, 5 are < 6)
s.order_of_key(1);   // 0  (no elements < 1)
s.order_of_key(10);  // 5  (all elements < 10)

// standard set operations
s.erase(3);
s.find(5);             // iterator to 5
s.lower_bound(4);      // iterator to 5
```

---

## Ordered Multiset (with duplicates)

```cpp
// Store pair<value, unique_id> to handle duplicates
using omset = oset<pair<int, int>>;

omset ms;
int uid = 0;
auto insert = [&](int x) { ms.insert({x, uid++}); };
auto erase  = [&](int x) { auto it = ms.lower_bound({x, 0}); if (it != ms.end() && it->first == x) ms.erase(it); };
auto kth    = [&](int k) { return ms.find_by_order(k)->first; };
auto rank   = [&](int x) { return (int)ms.order_of_key({x, 0}); };

insert(5); insert(3); insert(5); insert(1);
// ms = {1, 3, 5, 5}
kth(0);    // 1
kth(2);    // 5
rank(5);   // 2  (elements 1, 3 are < 5)
```

---

## Common CP Patterns

### K-th Smallest Element (dynamic)

```cpp
oset<int> s;
// insert elements as they come
s.insert(x);
// query k-th smallest at any point
int kth = *s.find_by_order(k);
```

### Count of Elements in Range [lo, hi]

```cpp
int count = s.order_of_key(hi + 1) - s.order_of_key(lo);
```

### Rank of an Element

```cpp
int rank = s.order_of_key(x);  // 0-indexed rank (# elements < x)
```

---

## vs `std::set`

| | `std::set` | `oset` (pb_ds) |
|---|---|---|
| Insert / Erase / Find | $O(\log n)$ | $O(\log n)$ |
| k-th element | $O(n)$ — `advance(it, k)` | $O(\log n)$ — `find_by_order(k)` |
| Rank of element | $O(n)$ — `distance(begin, it)` | $O(\log n)$ — `order_of_key(x)` |
| Portability | Standard C++ | GCC only |

> **Note:** This is GCC-specific (`<ext/pb_ds/...>`). It works on Codeforces, AtCoder, and most CP judges but **not** on MSVC.
