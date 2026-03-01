# Code Optimisation

**Code optimisation** transforms the intermediate code (or target code) to improve **execution speed**, **memory usage**, or **power consumption** — without changing the program's observable behaviour.

$$
\text{IR} \xrightarrow{\text{Optimisation}} \text{Optimised IR}
$$

> [!NOTE]
> Optimisation does not mean finding the "optimal" code — it means **improving** the code. Finding the truly optimal program is, in general, undecidable.

---

## 1 Classification of Optimisations

### 1.1 By Scope

| Level | Scope | Examples |
|---|---|---|
| **Local** | Within a single basic block | Constant folding, algebraic simplification, dead code elimination |
| **Global (Intraprocedural)** | Across basic blocks within one function | Common subexpression elimination, loop optimisations, live variable analysis |
| **Interprocedural** | Across function boundaries | Inline expansion, interprocedural constant propagation |

### 1.2 By Dependence on Target

| Kind | Description |
|---|---|
| **Machine-independent** | Applied on IR; doesn't depend on the target architecture. |
| **Machine-dependent** | Applied during/after code generation; exploits specific CPU features (instruction scheduling, register allocation). |

---

## 2 Basic Blocks and Flow Graphs

### 2.1 Basic Block

A **basic block** is a maximal sequence of consecutive instructions such that:
1. Control flow enters only at the **first** instruction.
2. Control flow leaves only at the **last** instruction (no jumps in the middle).

**Algorithm to partition TAC into basic blocks:**
1. Identify **leaders**:
   - The first instruction is a leader.
   - Any target of a conditional/unconditional jump is a leader.
   - Any instruction immediately after a jump is a leader.
2. A basic block goes from a leader to (but not including) the next leader.

### 2.2 Flow Graph (Control Flow Graph — CFG)

- Each **node** is a basic block.
- An **edge** $B_1 \rightarrow B_2$ exists if:
  - $B_1$ ends with a jump to the first instruction of $B_2$, or
  - $B_2$ immediately follows $B_1$ and $B_1$ doesn't end with an unconditional jump.

Example:
```
        ┌──── B1 ────┐
        │ i = 0       │
        │ goto L1     │
        └─────┬───────┘
              ↓
        ┌──── B2 (L1) ─┐
        │ if i<n goto L2│──── false ──→ B4 (exit)
        └─────┬─────────┘
              ↓ true
        ┌──── B3 (L2) ─┐
        │ sum = sum+a[i]│
        │ i = i + 1     │
        │ goto L1       │──→ back to B2
        └───────────────┘
```

---

## 3 Local Optimisations (Within a Basic Block)

### 3.1 Constant Folding

Evaluate constant expressions at **compile time**:
```
t1 = 2 * 3.14           →   t1 = 6.28
t2 = 60                  →   (unchanged)
```

### 3.2 Constant Propagation

If a variable has a known constant value, substitute it:
```
x = 5                        x = 5
y = x + 3          →        y = 5 + 3      →   y = 8    (then fold)
```

### 3.3 Algebraic Simplification / Strength Reduction

| Before | After | Rule |
|---|---|---|
| `x = y + 0` | `x = y` | Additive identity |
| `x = y * 1` | `x = y` | Multiplicative identity |
| `x = y * 0` | `x = 0` | Zero multiplication |
| `x = y * 2` | `x = y + y` (or `x = y << 1`) | Strength reduction |
| `x = y * 8` | `x = y << 3` | Strength reduction |
| `x = y ** 2` | `x = y * y` | Strength reduction |

### 3.4 Dead Code Elimination

Remove instructions whose results are **never used**:
```
t1 = a + b
t2 = t1 * c        ← t2 never used later
t3 = a + d
x  = t3
```
After elimination: instruction for `t2` is removed, and consequently `t1` as well if only used by `t2`.

### 3.5 Common Subexpression Elimination (Local)

If the same expression is computed multiple times with unchanged operands, reuse the first result:
```
t1 = a + b              t1 = a + b
t2 = a + b       →     t2 = t1
t3 = t1 * t2            t3 = t1 * t1
```

### 3.6 Copy Propagation

After `x = y`, replace subsequent uses of `x` with `y` (until `x` or `y` is redefined):
```
x = y                    (delete if x not used later)
z = x + 1        →      z = y + 1
```

---

## 4 Global Optimisations (Across Basic Blocks)

These require **data-flow analysis** — computing information about the flow of data through the program's CFG.

### 4.1 Data-Flow Analysis Framework

A data-flow problem is defined by:
- A **domain** of data-flow values (e.g. sets of expressions).
- A **transfer function** for each basic block.
- A **meet operator** (∪ or ∩) to combine values at join points.
- A **direction** (forward or backward).

The solution is found by iterating until a **fixed point** is reached.

### 4.2 Reaching Definitions

**Direction:** Forward. **Meet:** Union (∪).

A definition $d: x = \ldots$ **reaches** a point $p$ if there is a path from $d$ to $p$ along which $x$ is not redefined.

$$\text{OUT}[B] = \text{GEN}[B] \cup (\text{IN}[B] - \text{KILL}[B])$$
$$\text{IN}[B] = \bigcup_{P \in \text{pred}(B)} \text{OUT}[P]$$

Used for: constant propagation, use-def chains.

### 4.3 Live Variable Analysis

**Direction:** Backward. **Meet:** Union (∪).

A variable $v$ is **live** at point $p$ if there exists a path from $p$ to a use of $v$ that does not pass through a redefinition of $v$.

$$\text{IN}[B] = \text{USE}[B] \cup (\text{OUT}[B] - \text{DEF}[B])$$
$$\text{OUT}[B] = \bigcup_{S \in \text{succ}(B)} \text{IN}[S]$$

Used for: dead code elimination, register allocation.

### 4.4 Available Expressions

**Direction:** Forward. **Meet:** Intersection (∩).

An expression $e$ is **available** at point $p$ if on **every** path from the entry to $p$, $e$ has been computed and none of its operands has been redefined since.

$$\text{OUT}[B] = \text{GEN}[B] \cup (\text{IN}[B] - \text{KILL}[B])$$
$$\text{IN}[B] = \bigcap_{P \in \text{pred}(B)} \text{OUT}[P]$$

Used for: global common subexpression elimination.

---

## 5 Loop Optimisations

Loops execute many times, so optimising them gives the biggest payoff.

### 5.1 Identifying Loops

A **natural loop** has:
- A **back edge** $n \rightarrow d$ where $d$ **dominates** $n$.
- The loop body = $d$ + all nodes that can reach $n$ without going through $d$.

**Dominance:** Node $d$ **dominates** node $n$ if every path from the entry to $n$ passes through $d$.

### 5.2 Loop-Invariant Code Motion (LICM)

Move computations that produce the same result on every iteration **out of the loop**:

```c
// Before                           // After
for (i = 0; i < n; i++) {          t = x * y;      // hoisted
    a[i] = x * y + i;              for (i = 0; i < n; i++) {
}                                       a[i] = t + i;
                                    }
```

Conditions to hoist `s: x = y op z`:
1. The statement is in a block that dominates all loop exits (or `x` is dead after the loop).
2. `y` and `z` are not redefined inside the loop (or their definitions also dominate `s`).
3. There is no other definition of `x` in the loop.

### 5.3 Induction Variable Elimination

An **induction variable** is a variable that increases/decreases by a constant amount in each iteration (e.g. loop counter `i`).

**Strength reduction** on induction variables:

```c
// Before                           // After
for (i = 0; i < n; i++) {          t = &a[0];      // base address
    ... = a[i];  // base + i*4     for (i = 0; i < n; i++) {
}                                       ... = *t;
                                        t = t + 4;  // addition replaces multiplication
                                    }
```

### 5.4 Loop Unrolling

Reduce loop overhead by duplicating the body:

```c
// Before                           // After
for (i = 0; i < 100; i++)          for (i = 0; i < 100; i += 4) {
    a[i] = 0;                          a[i]   = 0;
                                        a[i+1] = 0;
                                        a[i+2] = 0;
                                        a[i+3] = 0;
                                    }
```

Benefits: fewer branch instructions, more instruction-level parallelism.

### 5.5 Loop Fusion & Fission

**Fusion** — merge two adjacent loops with the same bounds:
```c
for (i=0;i<n;i++) a[i]=0;           for (i=0;i<n;i++) {
for (i=0;i<n;i++) b[i]=0;    →         a[i]=0; b[i]=0;
                                     }
```

**Fission** — split a loop to improve cache behaviour or enable vectorisation.

---

## 6 Peephole Optimisation

A **peephole** optimiser scans a small sliding window (2–5 instructions) over the generated code and applies local improvements:

| Pattern | Replacement |
|---|---|
| Redundant load/store: `STORE R1, x; LOAD R1, x` | Remove the LOAD |
| Unreachable code after unconditional jump | Delete |
| Jump to a jump: `goto L1; ... L1: goto L2` | `goto L2` |
| Algebraic: `ADD R1, R1, #0` | Delete (no-op) |
| Strength reduction: `MUL R1, R1, #2` | `SHL R1, R1, #1` |

---

## 7 Data-Flow Analysis — Iterative Algorithm Example

### Reaching Definitions — Iterative Solver

```c
#include <stdio.h>
#include <string.h>

/*
 * Reaching Definitions — iterative forward data-flow analysis.
 *
 * Simplified CFG with 4 blocks:
 *   B1 → B2, B2 → B3, B2 → B4, B3 → B2
 *
 *   B1: d1: x = 5       B2: d2: y = x+1
 *   B3: d3: x = y*2     B4: (exit)
 */

#define NUM_BLOCKS 4
#define NUM_DEFS   3   /* d1, d2, d3 */

typedef unsigned int BitSet;  /* bit i represents definition d_i */

#define SET(s,i)    ((s) |= (1u << (i)))
#define CLEAR(s,i)  ((s) &= ~(1u << (i)))
#define TEST(s,i)   ((s) & (1u << (i)))

/* GEN[B] = definitions generated in B */
/* KILL[B] = definitions killed in B   */
BitSet gen[NUM_BLOCKS]  = {0};
BitSet kill[NUM_BLOCKS] = {0};

/* IN[B], OUT[B] */
BitSet in[NUM_BLOCKS]  = {0};
BitSet out[NUM_BLOCKS] = {0};

/* Predecessors (adjacency list) */
int pred[NUM_BLOCKS][4] = {
    { -1 },         /* B0 (B1): entry, no predecessors */
    { 0, 2, -1 },   /* B1 (B2): predecessors = B1, B3 */
    { 1, -1 },      /* B2 (B3): predecessors = B2 */
    { 1, -1 },      /* B3 (B4): predecessors = B2 */
};

void print_set(const char *label, BitSet s) {
    printf("%s = { ", label);
    for (int i = 0; i < NUM_DEFS; i++)
        if (TEST(s, i)) printf("d%d ", i + 1);
    printf("}\n");
}

int main(void) {
    /* B1: d1: x = 5   → gen={d1}, kill={d3} (d3 also defines x) */
    SET(gen[0], 0);  SET(kill[0], 2);

    /* B2: d2: y = x+1 → gen={d2}, kill={} */
    SET(gen[1], 1);

    /* B3: d3: x = y*2 → gen={d3}, kill={d1} (d1 also defines x) */
    SET(gen[2], 2);  SET(kill[2], 0);

    /* B4: no definitions */

    /* Iterative solver */
    int changed = 1;
    int iter = 0;
    while (changed) {
        changed = 0;
        iter++;
        for (int b = 0; b < NUM_BLOCKS; b++) {
            /* IN[B] = ∪ OUT[P] for all predecessors P */
            BitSet new_in = 0;
            for (int i = 0; pred[b][i] != -1; i++)
                new_in |= out[pred[b][i]];
            in[b] = new_in;

            /* OUT[B] = GEN[B] ∪ (IN[B] - KILL[B]) */
            BitSet new_out = gen[b] | (in[b] & ~kill[b]);
            if (new_out != out[b]) {
                out[b] = new_out;
                changed = 1;
            }
        }
    }

    printf("Reaching Definitions — converged in %d iterations\n\n", iter);
    for (int b = 0; b < NUM_BLOCKS; b++) {
        printf("Block B%d:\n", b + 1);
        print_set("  IN ", in[b]);
        print_set("  OUT", out[b]);
        printf("\n");
    }
    return 0;
}
```

Output:
```
Reaching Definitions — converged in 3 iterations

Block B1:
  IN  = { }
  OUT = { d1 }

Block B2:
  IN  = { d1 d3 }
  OUT = { d1 d2 d3 }

Block B3:
  IN  = { d1 d2 d3 }
  OUT = { d2 d3 }

Block B4:
  IN  = { d1 d2 d3 }
  OUT = { d1 d2 d3 }
```

This tells us, for example, that at the entry to B2, both definition `d1: x=5` and `d3: x=y*2` reach — so we cannot do constant propagation for `x` at B2.

---

## 8 Summary of Key Optimisations

| Optimisation | Level | Technique |
|---|---|---|
| Constant folding | Local | Evaluate constants at compile time |
| Constant propagation | Local/Global | Substitute known constant values |
| Dead code elimination | Local/Global | Remove unused computations (live variable analysis) |
| Common subexpression elimination | Local/Global | Reuse previously computed expressions (available expressions) |
| Copy propagation | Local/Global | Replace copies with original values |
| Loop-invariant code motion | Loop | Hoist invariant computations out of loops |
| Induction variable elimination | Loop | Replace multiplications with additions |
| Strength reduction | Local/Loop | Replace expensive ops with cheaper ones |
| Loop unrolling | Loop | Duplicate body to reduce branch overhead |
| Peephole optimisation | Target code | Small-window pattern replacement |
| Inline expansion | Interprocedural | Replace call with function body |

$$
\boxed{
\text{IR}
\xrightarrow{\text{Data-flow analysis}}
\xrightarrow{\text{Local + Global + Loop opts}}
\text{Optimised IR}
\xrightarrow{\text{next}}
\text{Code Generation}
}
$$
