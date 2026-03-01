# Intermediate Code Generation

After [[Semantic Analysis]], the compiler translates the annotated AST into an **intermediate representation (IR)** — a machine-independent form that sits between the source language and the target machine code.

$$
\text{Annotated AST} \xrightarrow{\text{ICG}} \text{Intermediate Code (IR)} \xrightarrow{\text{next}} \text{Optimisation}
$$

---

## 1 Why Use an Intermediate Representation?

| Reason | Explanation |
|---|---|
| **Retargeting** | Same front end, multiple back ends (x86, ARM, RISC-V). |
| **Multiple source languages** | Different front ends (C, Fortran) share the same back end via a common IR. |
| **Optimisation** | Machine-independent optimisations are easier to apply on IR than on source or assembly. |
| **Portability** | IR can be serialised and shipped (e.g. Java bytecode, LLVM bitcode). |

If you have $m$ languages and $n$ machines:
- **Without IR:** $m \times n$ compilers.
- **With IR:** $m$ front ends + $n$ back ends = $m + n$ components.

---

## 2 Types of Intermediate Representations

### 2.1 High-Level IR — Abstract Syntax Tree (AST)

The AST itself is an IR. Some compilers perform optimisations directly on the AST (e.g. constant folding).

### 2.2 Medium-Level IR — Three-Address Code (TAC)

The most common IR for teaching and many real compilers. Each instruction has **at most three addresses** (operands/result):

$$x = y \;\text{op}\; z$$

where `x`, `y`, `z` are names, constants, or compiler-generated temporaries.

### 2.3 Low-Level IR — Close to Machine Code

Register-transfer-level (RTL) used by GCC. Very close to the target instruction set but still abstracting over specific registers.

### 2.4 Stack-Based IR

Java bytecode and .NET CIL use a **stack machine** model:
```
push a
push b
add          // pops a, b; pushes a+b
store c
```

### 2.5 SSA Form (Static Single Assignment)

Every variable is assigned **exactly once**. Multiple definitions use versioned names:
```
x1 = 5
x2 = x1 + 1
x3 = φ(x1, x2)    // φ-function at join points
```

Used by LLVM, GCC (GIMPLE → SSA), and most modern optimising compilers.

---

## 3 Three-Address Code (TAC) — In Depth

### 3.1 Instruction Types

| Form | Meaning |
|---|---|
| `x = y op z` | Binary operation |
| `x = op y` | Unary operation |
| `x = y` | Copy / assignment |
| `goto L` | Unconditional jump |
| `if x relop y goto L` | Conditional jump |
| `param x` | Pass parameter |
| `call p, n` | Call procedure `p` with `n` arguments |
| `return x` | Return value |
| `x = y[i]` | Indexed load |
| `x[i] = y` | Indexed store |
| `x = &y` | Address of |
| `x = *y` | Pointer dereference (load) |
| `*x = y` | Pointer dereference (store) |

### 3.2 Implementation — Quadruples, Triples, Indirect Triples

**Quadruples** — 4 fields: `(op, arg1, arg2, result)`

| # | op | arg1 | arg2 | result |
|---|---|---|---|---|
| 0 | `*` | rate | 60 | t1 |
| 1 | `+` | initial | t1 | t2 |
| 2 | `=` | t2 | — | position |

**Triples** — 3 fields, result is the instruction number itself: `(op, arg1, arg2)`

| # | op | arg1 | arg2 |
|---|---|---|---|
| 0 | `*` | rate | 60 |
| 1 | `+` | initial | (0) |
| 2 | `=` | position | (1) |

**Indirect Triples** — Use a separate list of pointers to triples, allowing easy reordering during optimisation.

---

## 4 Syntax-Directed Translation to TAC

### 4.1 Expressions

For a production $E \rightarrow E_1 + T$:

```
E.place = newTemp()
emit(E.place '=' E1.place '+' T.place)
```

`newTemp()` generates a fresh temporary variable each time.

### 4.2 Full Translation Rules

| Production | Semantic Actions |
|---|---|
| $E \rightarrow E_1 + T$ | `E.place = newTemp(); emit(E.place = E1.place + T.place)` |
| $E \rightarrow T$ | `E.place = T.place` |
| $T \rightarrow T_1 * F$ | `T.place = newTemp(); emit(T.place = T1.place * F.place)` |
| $T \rightarrow F$ | `T.place = F.place` |
| $F \rightarrow ( E )$ | `F.place = E.place` |
| $F \rightarrow \textbf{id}$ | `F.place = id.lexeme` |
| $F \rightarrow \textbf{num}$ | `F.place = num.value` |

### 4.3 Worked Example

Source: `a = b + c * d - e`

```
t1 = c * d
t2 = b + t1
t3 = t2 - e
a  = t3
```

---

## 5 Control Flow Statements

### 5.1 If-Else

Source:
```c
if (a < b)
    x = 1;
else
    x = 2;
```

TAC:
```
    if a < b goto L1
    goto L2
L1: x = 1
    goto L3
L2: x = 2
L3:
```

### 5.2 While Loop

Source:
```c
while (a < b) {
    a = a + 1;
}
```

TAC:
```
L1: if a < b goto L2
    goto L3
L2: t1 = a + 1
    a = t1
    goto L1
L3:
```

### 5.3 For Loop

Source:
```c
for (i = 0; i < n; i++) {
    sum = sum + a[i];
}
```

TAC:
```
    i = 0
L1: if i < n goto L2
    goto L3
L2: t1 = i * 4          // assuming int = 4 bytes
    t2 = a[t1]
    sum = sum + t2
    i = i + 1
    goto L1
L3:
```

---

## 6 Boolean Expressions — Short-Circuit Evaluation

### 6.1 Using Jump Code (Backpatching)

For `a < b && c < d`:
```
    if a < b goto L1
    goto Lfalse
L1: if c < d goto Ltrue
    goto Lfalse
```

For `a < b || c < d`:
```
    if a < b goto Ltrue
    goto L1
L1: if c < d goto Ltrue
    goto Lfalse
```

### 6.2 Backpatching

**Backpatching** avoids multiple passes by maintaining lists of incomplete jumps:
- **truelist** — jumps that should go to the "true" target.
- **falselist** — jumps that should go to the "false" target.

When the target is finally known, patch all entries in the list.

```
makelist(i)     — create a new list containing only index i
merge(p1, p2)   — concatenate two lists
backpatch(p, t) — set the target of every jump in list p to t
```

---

## 7 Function Calls & Activation Records

### 7.1 TAC for Function Calls

Source:
```c
int result = add(x, y);
```

TAC:
```
param x
param y
t1 = call add, 2
result = t1
```

### 7.2 Activation Record (Stack Frame)

Each function call pushes an **activation record** on the runtime stack:

```
┌─────────────────────┐  ← High address
│  Actual parameters   │
│  Return address      │
│  Old frame pointer   │  ← Frame pointer (FP)
│  Local variables     │
│  Temporaries         │
│  Saved registers     │
└─────────────────────┘  ← Stack pointer (SP)
```

---

## 8 Array Access — Address Calculation

For a 1D array `A[i]` with base address `base_A` and element size `w`:
$$\text{addr}(A[i]) = \text{base\_A} + i \times w$$

For a 2D row-major array `A[i][j]` with dimensions $[0..n_1][0..n_2]$:
$$\text{addr}(A[i][j]) = \text{base\_A} + (i \times n_2 + j) \times w$$

TAC for `x = A[i][j]`:
```
t1 = i * n2
t2 = t1 + j
t3 = t2 * w
t4 = base_A[t3]
x  = t4
```

---

## 9 TAC Generator Implementation in C

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ---- Three-Address Code Generator ---- */

typedef struct {
    char op[8];
    char arg1[32];
    char arg2[32];
    char result[32];
} Quad;

Quad code[1000];
int  nextQuad = 0;
int  tempCount = 0;

char *newTemp(void) {
    static char buf[32];
    sprintf(buf, "t%d", tempCount++);
    return buf;
}

int newLabel(void) {
    static int labelCount = 0;
    return labelCount++;
}

void emit(const char *op, const char *a1, const char *a2, const char *res) {
    Quad *q = &code[nextQuad++];
    strcpy(q->op, op);
    strcpy(q->arg1, a1 ? a1 : "");
    strcpy(q->arg2, a2 ? a2 : "");
    strcpy(q->result, res ? res : "");
}

void printCode(void) {
    for (int i = 0; i < nextQuad; i++) {
        Quad *q = &code[i];
        if (strcmp(q->op, "=") == 0)
            printf("%3d:  %s = %s\n", i, q->result, q->arg1);
        else if (strcmp(q->op, "goto") == 0)
            printf("%3d:  goto L%s\n", i, q->result);
        else if (strcmp(q->op, "if<") == 0)
            printf("%3d:  if %s < %s goto L%s\n", i, q->arg1, q->arg2, q->result);
        else if (strcmp(q->op, "label") == 0)
            printf("%3d:  L%s:\n", i, q->result);
        else if (strcmp(q->op, "param") == 0)
            printf("%3d:  param %s\n", i, q->arg1);
        else if (strcmp(q->op, "call") == 0)
            printf("%3d:  %s = call %s, %s\n", i, q->result, q->arg1, q->arg2);
        else
            printf("%3d:  %s = %s %s %s\n", i, q->result, q->arg1, q->op, q->arg2);
    }
}

/* ---- Generate TAC for: ----
 *   a = b + c * d - e;
 *   if (a < 100) goto done;
 *   result = compute(a, e);
 */
int main(void) {
    char *t;

    printf("=== Source ===\n");
    printf("a = b + c * d - e;\n");
    printf("if (a < 100) goto done;\n");
    printf("result = compute(a, e);\n\n");

    /* a = b + c * d - e */
    t = newTemp();  /* t0 */
    emit("*", "c", "d", strdup(t));

    t = newTemp();  /* t1 */
    emit("+", "b", "t0", strdup(t));

    t = newTemp();  /* t2 */
    emit("-", "t1", "e", strdup(t));

    emit("=", "t2", NULL, "a");

    /* if (a < 100) goto L0 */
    char lbl[8]; sprintf(lbl, "%d", newLabel());
    emit("if<", "a", "100", strdup(lbl));

    /* result = compute(a, e) */
    emit("param", "a", NULL, NULL);
    emit("param", "e", NULL, NULL);
    t = newTemp();  /* t3 */
    emit("call", "compute", "2", strdup(t));
    emit("=", "t3", NULL, "result");

    /* L0: (done) */
    emit("label", NULL, NULL, lbl);

    printf("=== Three-Address Code (Quadruples) ===\n");
    printCode();

    return 0;
}
```

---

## 10 Summary

| Concept | Key Point |
|---|---|
| **Purpose of IR** | Decouple front end from back end; enable optimisation |
| **Three-Address Code** | At most 3 addresses per instruction; stored as quadruples/triples |
| **Temporaries** | Compiler-generated variables for intermediate results |
| **Control flow** | Translate `if`, `while`, `for` into conditional/unconditional jumps |
| **Boolean expressions** | Short-circuit via jump code; use **backpatching** |
| **Arrays** | Compute addresses with base + offset arithmetic |
| **Calls** | `param`, `call`, `return` instructions; activation records on the stack |

$$
\boxed{
\text{Annotated AST}
\xrightarrow{\text{SDT rules}}
\text{Three-Address Code}
\xrightarrow{\text{next}}
\text{Code Optimisation}
}
$$
