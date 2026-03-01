# Euclidean GCD

Find the **Greatest Common Divisor** of two integers.

---

## Algorithm

$$\gcd(a, b) = \gcd(b, \; a \bmod b)$$

Base case: $\gcd(a, 0) = a$

**Time:** $O(\log(\min(a, b)))$

---

## Code

```cpp
// Iterative
int gcd(int a, int b) {
    while (b) {
        a %= b;
        swap(a, b);
    }
    return a;
}

// Recursive
int gcd(int a, int b) {
    return b == 0 ? a : gcd(b, a % b);
}

// LCM using GCD
long long lcm(long long a, long long b) {
    return a / gcd(a, b) * b;  // divide first to avoid overflow
}
```

---

## Extended Euclidean Algorithm

Finds $x, y$ such that $ax + by = \gcd(a, b)$.

Used to find **modular inverse** when $\gcd(a, m) = 1$: $a \cdot x \equiv 1 \pmod{m}$.

```cpp
int extgcd(int a, int b, int &x, int &y) {
    if (b == 0) {
        x = 1; y = 0;
        return a;
    }
    int x1, y1;
    int g = extgcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - (a / b) * y1;
    return g;
}

// Modular inverse using extended GCD (works for any m, not just prime)
int modinv(int a, int m) {
    int x, y;
    int g = extgcd(a, m, x, y);
    // inverse exists only if gcd(a, m) == 1
    return (x % m + m) % m;
}
```
