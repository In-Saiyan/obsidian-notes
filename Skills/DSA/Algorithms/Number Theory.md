# Number Theory

- [Fermat's Little Theorem](#fermats-little-theorem)
- [Binary Exponentiation & Modular Inverse](#binary-exponentiation--modular-inverse)
- [Sieve of Eratosthenes](#sieve-of-eratosthenes)
- [Linear Sieve](#linear-sieve)
- [Smallest Prime Factor (SPF) Sieve](#smallest-prime-factor-spf-sieve)
- [Prime Factorisation using SPF](#prime-factorisation-using-spf)
- [Trial Division Factorisation](#trial-division-factorisation)
- [Miller-Rabin Primality Test](#miller-rabin-primality-test)
- [Pollard's Rho Factorisation](#pollards-rho-factorisation)
- [Full Factorisation (large numbers)](#full-factorisation-large-numbers)

---

## Fermat's Little Theorem

[Video Explanation](https://www.youtube.com/watch?v=XPMzosLWGHo)

For a **prime** number $p$ and an integer $a$ **not divisible** by $p$:

$$a^{p-1} \equiv 1 \pmod{p}$$

Equivalently: $a^p \equiv a \pmod{p}$ for **any** integer $a$ (even when $p \mid a$).

**Intuition:** If you arrange $a$ types of objects into $p$ slots (necklace argument), the count $a^p - a$ is always divisible by $p$.

### Conditions

| # | Condition | Why it matters |
|---|---|---|
| 1 | $p$ **must be prime** | Fails for composite numbers (use Euler's theorem instead) |
| 2 | $a$ **not divisible by** $p$ (i.e. $\gcd(a, p) = 1$) | Required for $a^{p-1} \equiv 1$; if $p \mid a$ then $a^{p-1} \equiv 0$ |
| 3 | All arithmetic is done **modulo** $p$ | Without mod, numbers overflow; the theorem is about modular equivalence |

> **Warning:** The converse is **not** true — $a^{n-1} \equiv 1 \pmod{n}$ does **not** guarantee $n$ is prime. Numbers that pass this test but are composite are called **Carmichael numbers** (e.g. 561).

### Uses

- **Modular Multiplicative Inverse:** $a^{p-2} \equiv a^{-1} \pmod{p}$
- **Modular Division:** $\frac{a}{b} \bmod p = a \cdot b^{p-2} \bmod p$
- **Primality Testing:** Foundation of Miller-Rabin

---

## Binary Exponentiation & Modular Inverse

$O(\log n)$ exponentiation with overflow-safe modular arithmetic.

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

// Modular inverse of a (mod prime p) — uses Fermat's Little Theorem
long long modinv(long long a, long long p = MOD) {
    return binexp(a, p - 2, p);
}

// Usage:
// binexp(2, 10)         → 1024 % MOD
// modinv(5)             → 5^(MOD-2) % MOD
// (a * modinv(b)) % MOD → (a / b) % MOD
```

> **MOD values:** use $10^9 + 7$ for values under $10^9$, and $10^{18} + 3$ for larger ranges — both are prime.

---

## Sieve of Eratosthenes

Find all primes up to $n$.

**Time:** $O(n \log \log n)$ | **Space:** $O(n)$

```cpp
vector<bool> sieve(int n) {
    vector<bool> is_prime(n + 1, true);
    is_prime[0] = is_prime[1] = false;
    for (int i = 2; i * i <= n; i++)
        if (is_prime[i])
            for (int j = i * i; j <= n; j += i)
                is_prime[j] = false;
    return is_prime;
}

// Collect primes into a vector
vector<int> getPrimes(int n) {
    auto is_prime = sieve(n);
    vector<int> primes;
    for (int i = 2; i <= n; i++)
        if (is_prime[i]) primes.push_back(i);
    return primes;
}
```

---

## Linear Sieve

Marks each composite **exactly once**. Also builds a list of primes.

**Time:** $O(n)$

```cpp
vector<int> linearSieve(int n) {
    vector<int> primes;
    vector<bool> is_composite(n + 1, false);
    for (int i = 2; i <= n; i++) {
        if (!is_composite[i]) primes.push_back(i);
        for (int j = 0; j < (int)primes.size() && i * primes[j] <= n; j++) {
            is_composite[i * primes[j]] = true;
            if (i % primes[j] == 0) break;  // key optimisation
        }
    }
    return primes;
}
```

---

## Smallest Prime Factor (SPF) Sieve

Store the **smallest prime factor** for every number up to $n$. Enables $O(\log n)$ factorisation per query.

```cpp
vector<int> spf;

void buildSPF(int n) {
    spf.assign(n + 1, 0);
    iota(spf.begin(), spf.end(), 0);  // spf[i] = i
    for (int i = 2; i * i <= n; i++)
        if (spf[i] == i)  // i is prime
            for (int j = i * i; j <= n; j += i)
                if (spf[j] == j)
                    spf[j] = i;
}
```

---

## Prime Factorisation using SPF

After building the SPF sieve, factorise any $x \leq n$ in $O(\log x)$.

```cpp
// Requires buildSPF(n) called beforehand
vector<pair<int,int>> factorise(int x) {
    vector<pair<int,int>> factors;
    while (x > 1) {
        int p = spf[x], cnt = 0;
        while (x % p == 0) {
            x /= p;
            cnt++;
        }
        factors.push_back({p, cnt});
    }
    return factors;  // {prime, exponent} pairs
}
```

| Approach | Factorise one number | Factorise many numbers ≤ n |
|---|---|---|
| Trial division | $O(\sqrt{x})$ | $O(q \cdot \sqrt{x})$ |
| SPF sieve + lookup | $O(\log x)$ | $O(n \log \log n + q \cdot \log x)$ |

---

## Trial Division Factorisation

No precomputation. Works for any number up to ~$10^{14}$.

**Time:** $O(\sqrt{n})$

```cpp
vector<pair<long long, int>> trialDivision(long long n) {
    vector<pair<long long, int>> factors;
    for (long long d = 2; d * d <= n; d++) {
        if (n % d == 0) {
            int cnt = 0;
            while (n % d == 0) { n /= d; cnt++; }
            factors.push_back({d, cnt});
        }
    }
    if (n > 1) factors.push_back({n, 1});
    return factors;
}
```

---

## Miller-Rabin Primality Test

Probabilistic primality test. **Deterministic** for numbers up to $3.3 \times 10^{24}$ with the right witness set.

**Time:** $O(k \cdot \log^2 n)$ where $k$ = number of witnesses.

```cpp
using u64 = unsigned long long;
using u128 = __uint128_t;

u64 mulmod(u64 a, u64 b, u64 m) {
    return (u128)a * b % m;
}

u64 powmod(u64 a, u64 b, u64 m) {
    u64 res = 1;
    a %= m;
    while (b > 0) {
        if (b & 1) res = mulmod(res, a, m);
        a = mulmod(a, a, m);
        b >>= 1;
    }
    return res;
}

bool millerTest(u64 d, u64 n, u64 a) {
    u64 x = powmod(a, d, n);
    if (x == 1 || x == n - 1) return true;
    while (d != n - 1) {
        x = mulmod(x, x, n);
        d <<= 1;
        if (x == 1) return false;
        if (x == n - 1) return true;
    }
    return false;
}

bool isPrime(u64 n) {
    if (n < 2) return false;
    if (n < 4) return true;
    if (n % 2 == 0) return false;

    u64 d = n - 1;
    while (d % 2 == 0) d >>= 1;

    // Deterministic for n < 3.3e24
    for (u64 a : {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37})
        if (n != a && !millerTest(d, n, a))
            return false;
    return true;
}
```

---

## Pollard's Rho Factorisation

Finds a **non-trivial factor** of a composite number. Expected time $O(n^{1/4})$.

Used for factorising numbers too large for trial division ($10^{15}$ to $10^{18}$).

```cpp
u64 pollardRho(u64 n) {
    if (n % 2 == 0) return 2;
    u64 x = rand() % (n - 2) + 2;
    u64 y = x;
    u64 c = rand() % (n - 1) + 1;
    u64 d = 1;

    while (d == 1) {
        x = (mulmod(x, x, n) + c) % n;  // tortoise
        y = (mulmod(y, y, n) + c) % n;   // hare (2 steps)
        y = (mulmod(y, y, n) + c) % n;
        d = __gcd(x > y ? x - y : y - x, n);
    }
    return d;
}
```

### Brent's Optimisation

Faster cycle detection variant — groups GCD computations.

```cpp
u64 brentRho(u64 n) {
    if (n % 2 == 0) return 2;
    u64 y = rand() % (n - 1) + 1;
    u64 c = rand() % (n - 1) + 1;
    u64 m = rand() % (n - 1) + 1;
    u64 g = 1, q = 1, r = 1;
    u64 ys, x;

    while (g == 1) {
        x = y;
        for (u64 i = 0; i < r; i++)
            y = (mulmod(y, y, n) + c) % n;

        u64 k = 0;
        while (k < r && g == 1) {
            ys = y;
            for (u64 i = 0; i < min(m, r - k); i++) {
                y = (mulmod(y, y, n) + c) % n;
                q = mulmod(q, x > y ? x - y : y - x, n);
            }
            g = __gcd(q, n);
            k += m;
        }
        r <<= 1;
    }

    if (g == n) {
        while (true) {
            ys = (mulmod(ys, ys, n) + c) % n;
            g = __gcd(x > ys ? x - ys : ys - x, n);
            if (g > 1) break;
        }
    }
    return g == n ? 0 : g;  // 0 = failed, retry with different c
}
```

---

## Full Factorisation (large numbers)

Combine **Miller-Rabin** + **Pollard's Rho** for complete factorisation of numbers up to $10^{18}$.

```cpp
map<u64, int> fullFactorise(u64 n) {
    map<u64, int> factors;
    if (n <= 1) return factors;

    // Pull out small primes first
    for (u64 p : {2, 3, 5, 7, 11, 13}) {
        while (n % p == 0) {
            factors[p]++;
            n /= p;
        }
    }
    if (n == 1) return factors;

    // Recursive factorisation
    queue<u64> work;
    work.push(n);
    while (!work.empty()) {
        u64 x = work.front(); work.pop();
        if (x == 1) continue;
        if (isPrime(x)) {
            factors[x]++;
            continue;
        }
        // Find a non-trivial factor
        u64 d = x;
        while (d == x) d = brentRho(x);
        work.push(d);
        work.push(x / d);
    }
    return factors;  // {prime → exponent}
}
```

---

## When to Use What

| Method | Range | Time | Precomputation |
|---|---|---|---|
| **Sieve of Eratosthenes** | Primes up to $n$ | $O(n \log \log n)$ | Yes |
| **SPF Sieve** | Factorise many numbers ≤ $n$ | $O(\log x)$ per query | $O(n)$ |
| **Trial Division** | Single number ≤ $10^{14}$ | $O(\sqrt{n})$ | None |
| **Miller-Rabin** | Primality check ≤ $10^{18}$ | $O(\log^2 n)$ | None |
| **Pollard's Rho** | Factor large composites ≤ $10^{18}$ | $O(n^{1/4})$ expected | None |
| **Fermat's Little Theorem** | Modular inverse (mod prime) | $O(\log p)$ | None |
