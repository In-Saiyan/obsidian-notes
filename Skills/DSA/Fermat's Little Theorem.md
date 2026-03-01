---
tags:
  - dsa
  - algorithms
  - number-theory
  - math
---

# Fermat's Little Theorem

- [Concept](#concept)
- [Conditions](#conditions)
- [Uses](#uses)
- [Binary Exponentiation](#binary-exponentiation)
- [Code](#code)

---

## Concept

[Video Explanation](https://www.youtube.com/watch?v=XPMzosLWGHo)

For a **prime** number $p$ and an integer $a$ **not divisible** by $p$:

$$a^{p-1} \equiv 1 \pmod{p}$$

Equivalently: $a^p \equiv a \pmod{p}$ for **any** integer $a$ (even when $p \mid a$).

**Intuition:** If you arrange $a$ types of objects into $p$ slots (necklace argument), the count $a^p - a$ is always divisible by $p$.

---

## Conditions

| # | Condition | Why it matters |
|---|---|---|
| 1 | $p$ **must be prime** | Fails for composite numbers (use Euler's theorem instead) |
| 2 | $a$ **not divisible by** $p$ (i.e. $\gcd(a, p) = 1$) | Required for $a^{p-1} \equiv 1$; if $p \mid a$ then $a^{p-1} \equiv 0$ |
| 3 | All arithmetic is done **modulo** $p$ | Without mod, numbers overflow; the theorem is about modular equivalence |

> **Warning:** The converse is **not** true — $a^{n-1} \equiv 1 \pmod{n}$ does **not** guarantee $n$ is prime. Numbers that pass this test but are composite are called **Carmichael numbers** (e.g. 561).

---

## Uses

### Modular Multiplicative Inverse (MMI)

From $a^{p-1} \equiv 1 \pmod{p}$, multiply both sides by $a^{-1}$:

$$a^{p-2} \equiv a^{-1} \pmod{p}$$

So $a^{p-2} \bmod p$ gives the **modular inverse** of $a$ modulo a prime $p$.

### Modular Division

To compute $\frac{a}{b} \bmod p$: calculate $a \cdot b^{p-2} \bmod p$.

### Primality Testing (Miller-Rabin basis)

Fermat's test is the foundation of probabilistic primality tests.

---

## Binary Exponentiation

Use **binary exponentiation** instead of naive $O(n)$ power — it runs in $O(\log n)$ and avoids overflow by taking mod at every step.

---

## Code

```cpp
const long long MOD = 1e9 + 7;

long long binexp(long long a, long long b, long long m = MOD) {
    long long ans = 1;
    a %= m;
    while (b > 0) {
        if (b & 1)
            ans = ans % m * a % m;
        a = a % m * a % m;
        b >>= 1;
    }
    return ans;
}

// Modular inverse of a (mod prime p)
long long modinv(long long a, long long p = MOD) {
    return binexp(a, p - 2, p);
}

// Usage:
// binexp(2, 10)         → 1024 % MOD
// modinv(5)             → 5^(MOD-2) % MOD
// (a * modinv(b)) % MOD → (a / b) % MOD
```

> **MOD values:** use $10^9 + 7$ for values under $10^9$, and $10^{18} + 3$ for larger ranges — both are prime.
