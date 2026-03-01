# Linked List

A linear data structure where elements are connected via pointers.

---

## Types

| Type | Description |
|---|---|
| Singly Linked List | Each node points to the next |
| Doubly Linked List | Each node points to next and previous |
| Circular | Last node points back to head |

---

## Node Definition

```cpp
// Singly
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int v) : val(v), next(nullptr) {}
};

// Doubly
struct DListNode {
    int val;
    DListNode *prev, *next;
    DListNode(int v) : val(v), prev(nullptr), next(nullptr) {}
};
```

---

## Common Operations

```cpp
// Insert at head — O(1)
void insertHead(ListNode*& head, int val) {
    ListNode* node = new ListNode(val);
    node->next = head;
    head = node;
}

// Insert at tail — O(n)
void insertTail(ListNode*& head, int val) {
    ListNode* node = new ListNode(val);
    if (!head) { head = node; return; }
    ListNode* cur = head;
    while (cur->next) cur = cur->next;
    cur->next = node;
}

// Delete node with value — O(n)
void deleteNode(ListNode*& head, int val) {
    if (!head) return;
    if (head->val == val) { head = head->next; return; }
    ListNode* cur = head;
    while (cur->next && cur->next->val != val)
        cur = cur->next;
    if (cur->next) cur->next = cur->next->next;
}

// Reverse — O(n)
ListNode* reverse(ListNode* head) {
    ListNode *prev = nullptr, *cur = head;
    while (cur) {
        ListNode* nxt = cur->next;
        cur->next = prev;
        prev = cur;
        cur = nxt;
    }
    return prev;
}

// Detect cycle (Floyd's) — O(n)
bool hasCycle(ListNode* head) {
    ListNode *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true;
    }
    return false;
}
```

---

## Complexity

| Operation | Singly | Doubly |
|---|---|---|
| Insert head | $O(1)$ | $O(1)$ |
| Insert tail | $O(n)$ or $O(1)$ with tail ptr | $O(1)$ with tail ptr |
| Delete by value | $O(n)$ | $O(n)$ |
| Search | $O(n)$ | $O(n)$ |
| Reverse | $O(n)$ | $O(n)$ |
