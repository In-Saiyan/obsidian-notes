---
tags:
  - dsa
  - data-structures
  - tree
  - binary-tree
  - bst
---

# Trees

Hierarchical data structure with a root node and children.

---

## Binary Tree

Each node has at most **2 children**.

```cpp
struct TreeNode {
    int val;
    TreeNode *left, *right;
    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};
```

---

## Traversals

```cpp
// Inorder (Left, Root, Right) — gives sorted order for BST
void inorder(TreeNode* root) {
    if (!root) return;
    inorder(root->left);
    cout << root->val << " ";
    inorder(root->right);
}

// Preorder (Root, Left, Right)
void preorder(TreeNode* root) {
    if (!root) return;
    cout << root->val << " ";
    preorder(root->left);
    preorder(root->right);
}

// Postorder (Left, Right, Root)
void postorder(TreeNode* root) {
    if (!root) return;
    postorder(root->left);
    postorder(root->right);
    cout << root->val << " ";
}

// Level-order (BFS)
void levelOrder(TreeNode* root) {
    if (!root) return;
    queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        TreeNode* node = q.front(); q.pop();
        cout << node->val << " ";
        if (node->left)  q.push(node->left);
        if (node->right) q.push(node->right);
    }
}
```

---

## Binary Search Tree (BST)

Left child < parent < right child.

```cpp
TreeNode* insert(TreeNode* root, int val) {
    if (!root) return new TreeNode(val);
    if (val < root->val) root->left = insert(root->left, val);
    else root->right = insert(root->right, val);
    return root;
}

TreeNode* search(TreeNode* root, int val) {
    if (!root || root->val == val) return root;
    return val < root->val ? search(root->left, val) : search(root->right, val);
}
```

| Operation | Average | Worst (skewed) |
|---|---|---|
| Search | $O(\log n)$ | $O(n)$ |
| Insert | $O(\log n)$ | $O(n)$ |
| Delete | $O(\log n)$ | $O(n)$ |

---

## Tree Properties

| Property | Definition |
|---|---|
| **Height** | Longest path from root to leaf |
| **Depth** | Distance from root to a node |
| **Balanced** | Height difference of subtrees ≤ 1 |
| **Complete** | All levels filled except possibly the last (filled left to right) |
| **Full** | Every node has 0 or 2 children |
| **Perfect** | All internal nodes have 2 children; all leaves at same level |

---

## Common Algorithms

```cpp
// Height of tree — O(n)
int height(TreeNode* root) {
    if (!root) return 0;
    return 1 + max(height(root->left), height(root->right));
}

// Check if balanced — O(n)
int checkBalanced(TreeNode* root) {
    if (!root) return 0;
    int l = checkBalanced(root->left);
    int r = checkBalanced(root->right);
    if (l == -1 || r == -1 || abs(l - r) > 1) return -1;
    return 1 + max(l, r);
}

// Lowest Common Ancestor (BST) — O(h)
TreeNode* lca(TreeNode* root, int p, int q) {
    if (root->val > p && root->val > q) return lca(root->left, p, q);
    if (root->val < p && root->val < q) return lca(root->right, p, q);
    return root;
}
```
