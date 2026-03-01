# Trie (Prefix Tree)

Tree structure for efficient **prefix-based** string operations.

---

## Structure

Each node represents a character. Paths from root to marked nodes form stored strings.

```
        root
       / | \
      a   b  c
     /     \
    p       a
   / \       \
  p   i      t   ← "bat"
  |
  l
  |
  e   ← "apple", "api" (marked at i)
```

---

## Code

```cpp
struct Trie {
    struct Node {
        Node* children[26] = {};
        bool isEnd = false;
    };

    Node* root = new Node();

    void insert(const string& word) {
        Node* cur = root;
        for (char c : word) {
            int i = c - 'a';
            if (!cur->children[i])
                cur->children[i] = new Node();
            cur = cur->children[i];
        }
        cur->isEnd = true;
    }

    bool search(const string& word) {
        Node* cur = root;
        for (char c : word) {
            int i = c - 'a';
            if (!cur->children[i]) return false;
            cur = cur->children[i];
        }
        return cur->isEnd;
    }

    bool startsWith(const string& prefix) {
        Node* cur = root;
        for (char c : prefix) {
            int i = c - 'a';
            if (!cur->children[i]) return false;
            cur = cur->children[i];
        }
        return true;
    }
};
```

---

## Complexity

| Operation | Time | Space |
|---|---|---|
| Insert | $O(L)$ | $O(L)$ per word |
| Search | $O(L)$ | — |
| Prefix check | $O(L)$ | — |

$L$ = length of the string.

---

## Use Cases

- Autocomplete / prefix search
- Spell checking
- IP routing (longest prefix match)
- Word games (Boggle, Scrabble)
- XOR maximisation (binary trie)
