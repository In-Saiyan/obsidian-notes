---
tags:
  - cryptography
  - randomness
  - prng
  - trng
  - rng
---

# Classification of Randomness

Since computers are inherently "Deterministic" the true randomness is very difficult to achieve using computers.

A good test of randomness can be done by mapping the values obtained from a random algorithm and plotting it on a image/grid with each pixel/element ranging in brightness between [0, 1] (set the range of RNG to 1), By changing the grid size if you are able to notice some pattern, then that means the algorithm used is easier to infer than the algorithms which don't leak their working so easily. 

Also see:
- [How Hacker's reverse Math.random()](https://www.youtube.com/watch?v=XDsYPXRCXAs)

Hence we classify randomness into 2 different categories:
1. TRNG(True Random Number Generator)
2. PRNG(Pseudo Random Number Generator)

## 1. TRNG
This derives randomness from physical phenomenon, since true randomness is almost impossible to achieve using computers.
There are many examples of this, one of the famous one's is the ones which Cloudflare uses, for example the [lava lamps](https://www.cloudflare.com/learning/ssl/lava-lamp-encryption/), [double pendulums](https://blog.cloudflare.com/harnessing-office-chaos/#londons-unpredictable-pendulums) or [mobile spin entropy](https://blog.cloudflare.com/harnessing-office-chaos/#austins-mesmerizing-mobiles) which are amazing concepts which actually work great for randomness used in encryption.

## 2. PRNG
These use some kind of deterministic mathematical models to stimulate randomness to some degree. This requires an initial starting value called: "seed". So if you know the seed and the algorithm, you can easily recreate the same RNG(random number generator) as the other guy with the same seed and algorithm. When dealing with pseudorandom number generators, the **period** is the number of values the sequence yields before it begins to repeat itself.

There are several types of PRNG algorithms developed till date.

### 1. Linear Congruential Generator (LCG) or LCPRNG
The LCG is one of the oldest, simplest, and most widely used PRNG algorithms. Under the hood, many legacy `rand()` functions in C/C++ libraries are just LCGs.
**The Mathematics:** An LCG produces a sequence of pseudorandom numbers using a piecewise linear equation. 

#### Math:
The next number in the sequence is calculated based on the current number using this formula:

$$X_{n+1}​\equiv(aX_n​+c) ( mod \ m)$$ 
Where:
- $X$ is the sequence of pseudorandom values.
- $X_0$​ is the **seed** (the initial state).
- $m$ is the **modulus** (determines the maximum possible period/range of the numbers).
- $a$ is the **multiplier**
- $m$ is the **increment**.

#### Implementation:
```cpp
#include <iostream>

class LCG {
private:
    unsigned long long state; // The current X_n
    // POSIX rand() parameters as an example
    const unsigned long long a = 25214903917;
    const unsigned long long c = 11;
    const unsigned long long m = 281474976710656; // 2^48

public:
    LCG(unsigned long long seed) : state(seed) {}

    unsigned int next() {
        state = (a * state + c) % m;
        return state >> 16; // Often, lower bits are discarded for better perceived randomness
    }
};

int main() {
    LCG prng(1337); // Seed is 1337
    std::cout << "Rand 1: " << prng.next() << "\n";
    std::cout << "Rand 2: " << prng.next() << "\n";
    return 0;
}
```

> [!NOTE]
> You can also divide the `prng.next()` by `m` to set the value between [0, 1]

#### Shortcomings
For an LCG defined by $X_{n+1}​=(aX_n​+c)(mod\ m)$, the maximum possible period is $m$. This means the generator will output every single integer from $0$ to $m−1$ exactly once before the sequence restarts. If an LCG achieves this, it is said to have a **full period**.

If the parameters ($a$, $c$, and $m$) are chosen poorly, the generator might fall into a short cycle. For example, it might just bounce between three numbers endlessly, which destroys any illusion of randomness.

This can be fixed to a limit (allegedly) using:
#### The Hull-Dobell Theorem
The Hull-Dobell Theorem (1962) provides the exact mathematical proof and conditions required for an LCG to have a full period for all seed values.
An LCG will have a full period (a period equal to m) **if and only if** the following three conditions are met simultaneously:
1. **m and c are relatively prime (coprime):** This means the greatest common divisor (GCD) of the modulus m and the increment c must be 1. Mathematically: $gcd(c,\ m)=1$.
2. **a−1 is divisible by all prime factors of m:** If p is any prime number that divides m, then p must also divide $(a−1)$.
3. **a−1 is divisible by 4 if m is divisible by 4:** This is a special boundary condition specifically for the number 4. If m is a multiple of 4, then $(a−1)$ must also be a multiple of 4.

> [!WARNING]
> It is important to note that while the Hull-Dobell theorem guarantees the _maximum distribution_ of numbers (preventing short cycles), it does **not** provide cryptographic security. Even an LCG with a massive, mathematically perfect full period is entirely predictable once an attacker captures a few sequential outputs.

