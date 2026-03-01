# Code Generation

**Code generation** is the final phase of the compiler. It translates the optimised intermediate representation (IR) into **target machine code** — assembly instructions for a specific processor architecture.

$$
\text{Optimised IR} \xrightarrow{\text{Code Generator}} \text{Target Machine Code}
$$

---

## 1 Requirements of the Code Generator

| Requirement | Description |
|---|---|
| **Correctness** | The generated code must faithfully implement the semantics of the source program. |
| **Efficiency** | Produce fast, compact code. Use registers well, minimise memory accesses. |
| **Register allocation** | Map temporaries to a finite set of physical registers (critical for performance). |
| **Instruction selection** | Choose the best machine instructions to implement each IR operation. |
| **Instruction ordering** | Arrange instructions to exploit pipelining and avoid stalls. |

---

## 2 Target Machine Model

We assume a simple **RISC-like** machine (similar to MIPS / RISC-V):

| Feature | Detail |
|---|---|
| **Registers** | $R_0, R_1, \ldots, R_{n-1}$ (e.g. 32 general-purpose registers) |
| **Memory** | Flat address space; accessed via LOAD/STORE |
| **Instruction format** | `OP Rd, Rs1, Rs2` or `OP Rd, Rs1, #imm` |
| **Addressing modes** | Register, Immediate, Register+Offset (for memory) |

### 2.1 Core Instructions

| Instruction | Meaning |
|---|---|
| `LD Rd, addr` | Load from memory into register |
| `ST addr, Rs` | Store register to memory |
| `ADD Rd, Rs1, Rs2` | $Rd = Rs1 + Rs2$ |
| `SUB Rd, Rs1, Rs2` | $Rd = Rs1 - Rs2$ |
| `MUL Rd, Rs1, Rs2` | $Rd = Rs1 \times Rs2$ |
| `DIV Rd, Rs1, Rs2` | $Rd = Rs1 / Rs2$ |
| `MOV Rd, Rs` | $Rd = Rs$ (copy) |
| `ADDI Rd, Rs, #imm` | $Rd = Rs + \text{imm}$ |
| `CMP Rs1, Rs2` | Set condition flags |
| `BEQ label` | Branch if equal |
| `BNE label` | Branch if not equal |
| `BLT label` | Branch if less than |
| `BGE label` | Branch if greater or equal |
| `J label` | Unconditional jump |
| `CALL label` | Function call |
| `RET` | Return |

---

## 3 Simple Code Generation Algorithm

### 3.1 For Each TAC Instruction

Naïve approach — generate code one instruction at a time, loading operands from memory and storing results back:

| TAC | Generated Code |
|---|---|
| `x = y + z` | `LD R0, y` <br> `LD R1, z` <br> `ADD R0, R0, R1` <br> `ST x, R0` |
| `x = y` | `LD R0, y` <br> `ST x, R0` |
| `if x < y goto L` | `LD R0, x` <br> `LD R1, y` <br> `CMP R0, R1` <br> `BLT L` |
| `goto L` | `J L` |
| `param x` | `LD R0, x` <br> `PUSH R0` |
| `call f, n` | `CALL f` |
| `return x` | `LD R0, x` <br> `RET` |

This is correct but **highly inefficient** — far too many loads and stores. The solution: **register allocation**.

---

## 4 Register Allocation

### 4.1 The Problem

IR code uses an **unlimited** number of temporaries. Real machines have a **finite** number of registers (e.g. 16–32). We need to map temporaries to registers, **spilling** to memory when necessary.

### 4.2 Register Descriptor & Address Descriptor

| Descriptor | Tracks |
|---|---|
| **Register descriptor** | For each register: which variables are currently in it. |
| **Address descriptor** | For each variable: where its current value lives (register, memory, or both). |

### 4.3 `getReg` — Register Selection Function

When generating code for `x = y op z`, `getReg` determines which register to use for `x`, `y`, and `z`.

**Strategies for choosing a register $R$ for result $x$:**
1. If $y$ is in register $R$ and $y$ is not needed after this instruction (last use) → reuse $R$.
2. If there is an empty register → use it.
3. Find a register $R$ whose contents are also in memory (no spill cost) → use $R$.
4. Otherwise, **spill**: pick a register, store its value to memory, then use it.

### 4.4 Live Variable Info → Smarter getReg

If we know **live variables** at each point (from [[Code Optimisation]] data-flow analysis), we can:
- Never spill a dead variable (already not needed).
- Prefer to evict the variable whose **next use** is farthest in the future (Belady's algorithm analogy).

### 4.5 Graph Colouring Register Allocation

The most general approach:

1. **Build interference graph**: nodes = variables; edge $u - v$ if $u$ and $v$ are live at the same point.
2. **Colour the graph** with $k$ colours ($k$ = number of registers). Two adjacent nodes cannot share a colour.
3. If colouring fails → **spill** a variable (move it to memory), simplify, retry.

**Algorithm (simplified Chaitin's):**
1. While the graph has a node with degree $< k$: remove it (push on stack). It can always be coloured.
2. If all nodes removed → pop and assign colours (registers).
3. If stuck (all nodes have degree $\geq k$) → pick a node to **spill**, remove it, retry.

---

## 5 Instruction Selection

### 5.1 Tree-Pattern Matching

The AST or IR can be viewed as a tree. Instruction selection = **tiling** the tree with machine-instruction patterns that cover all nodes.

Example — different ways to compute `a[i]`:
```
Pattern 1: LD Rd, a(Ri)         — indexed load (1 instruction)
Pattern 2: MUL Rt, Ri, #4       — compute offset
            ADD Rt, Ra, Rt       — add to base
            LD  Rd, 0(Rt)       — load (3 instructions)
```

Choose the tiling that minimises total cost (instruction count, cycles, etc.).

### 5.2 CISC Considerations

On CISC machines (x86), one instruction can do complex things:
```x86asm
MOV EAX, [EBX + ECX*4 + 8]   ; base+index*scale+displacement
```
Instruction selection then tries to match rich addressing modes to reduce instruction count.

---

## 6 Instruction Scheduling

Reorder instructions to avoid **pipeline stalls** and exploit **instruction-level parallelism**:

```
; Before scheduling (stall after LD):
LD  R1, a        ; takes 2 cycles
ADD R2, R1, R3   ; must wait for R1 — STALL

; After scheduling (interleave independent work):
LD  R1, a
LD  R4, b        ; independent load fills the gap
ADD R2, R1, R3   ; R1 now ready
ADD R5, R4, R6
```

**List scheduling** — build a dependency DAG of instructions, then greedily schedule ready instructions in each cycle.

---

## 7 Complete Code Generator Implementation

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * Simple code generator:
 *   Input  — Three-Address Code (TAC)
 *   Output — Assembly for a RISC-like machine
 *
 * Includes register descriptors, address descriptors,
 * and a getReg function.
 */

#define NUM_REGS 4   /* R0..R3 — small to demonstrate spilling */

/* ---- Variable / Register descriptors ---- */

typedef struct {
    char var[32];       /* which variable is in this register ("" = empty) */
    int  dirty;         /* 1 if value in reg differs from memory */
} RegDesc;

RegDesc regs[NUM_REGS];

typedef struct {
    char name[32];
    int  in_reg;        /* -1 if not in any register */
    int  in_mem;        /* 1 if current value is in memory */
} VarDesc;

#define MAX_VARS 64
VarDesc vars[MAX_VARS];
int num_vars = 0;

/* ---- TAC instruction ---- */
typedef struct {
    char op[8];      /* +, -, *, /, =, goto, if<, label, param, call, ret */
    char arg1[32];
    char arg2[32];
    char result[32];
} TAC;

/* ---- Helpers ---- */

VarDesc *find_var(const char *name) {
    for (int i = 0; i < num_vars; i++)
        if (strcmp(vars[i].name, name) == 0)
            return &vars[i];
    /* auto-create */
    VarDesc *v = &vars[num_vars++];
    strcpy(v->name, name);
    v->in_reg = -1;
    v->in_mem = 1;   /* assume initially in memory */
    return v;
}

int find_reg_for(const char *var) {
    for (int i = 0; i < NUM_REGS; i++)
        if (strcmp(regs[i].var, var) == 0)
            return i;
    return -1;
}

void emit_asm(const char *fmt, ...) {
    va_list ap;
    va_start(ap, fmt);
    printf("    ");
    vprintf(fmt, ap);
    printf("\n");
    va_end(ap);
}

/* Spill register r to memory if dirty */
void spill(int r) {
    if (regs[r].var[0] && regs[r].dirty) {
        emit_asm("ST   %s, R%d", regs[r].var, r);
        VarDesc *v = find_var(regs[r].var);
        v->in_mem = 1;
    }
    if (regs[r].var[0]) {
        VarDesc *v = find_var(regs[r].var);
        if (v->in_reg == r) v->in_reg = -1;
    }
    regs[r].var[0] = '\0';
    regs[r].dirty = 0;
}

/* Get register: load variable 'var' into a register, return reg index */
int getReg_load(const char *var) {
    /* already in a register? */
    int r = find_reg_for(var);
    if (r >= 0) return r;

    /* find an empty register */
    for (int i = 0; i < NUM_REGS; i++) {
        if (regs[i].var[0] == '\0') {
            r = i;
            goto load;
        }
    }

    /* spill: pick register 0 (simplistic — a real compiler uses heuristics) */
    r = 0;
    spill(r);

load:
    emit_asm("LD   R%d, %s", r, var);
    strcpy(regs[r].var, var);
    regs[r].dirty = 0;
    VarDesc *v = find_var(var);
    v->in_reg = r;
    return r;
}

/* Get register for result (may reuse arg's register if possible) */
int getReg_result(const char *result, int reuse_hint) {
    /* if result already has a register, use it */
    int r = find_reg_for(result);
    if (r >= 0) return r;

    /* try to reuse the hint register */
    if (reuse_hint >= 0) {
        /* the previous occupant is being overwritten */
        VarDesc *old = find_var(regs[reuse_hint].var);
        if (old->in_mem || !regs[reuse_hint].dirty) {
            if (old->in_reg == reuse_hint) old->in_reg = -1;
            strcpy(regs[reuse_hint].var, result);
            regs[reuse_hint].dirty = 1;
            VarDesc *v = find_var(result);
            v->in_reg = reuse_hint;
            v->in_mem = 0;
            return reuse_hint;
        }
    }

    /* find empty */
    for (int i = 0; i < NUM_REGS; i++) {
        if (regs[i].var[0] == '\0') {
            r = i;
            goto done;
        }
    }

    /* spill */
    r = (reuse_hint + 1) % NUM_REGS;
    spill(r);

done:
    strcpy(regs[r].var, result);
    regs[r].dirty = 1;
    VarDesc *v = find_var(result);
    v->in_reg = r;
    v->in_mem = 0;
    return r;
}

/* Flush all dirty registers to memory (e.g. at end of block) */
void flush_all(void) {
    for (int i = 0; i < NUM_REGS; i++)
        spill(i);
}

/* ---- Code generator ---- */

const char *op_to_asm(const char *op) {
    if (strcmp(op, "+") == 0) return "ADD";
    if (strcmp(op, "-") == 0) return "SUB";
    if (strcmp(op, "*") == 0) return "MUL";
    if (strcmp(op, "/") == 0) return "DIV";
    return "???";
}

void generate(TAC *tac, int count) {
    for (int i = 0; i < count; i++) {
        TAC *t = &tac[i];

        if (strcmp(t->op, "=") == 0) {
            /* result = arg1  (copy) */
            int r1 = getReg_load(t->arg1);
            int rd = getReg_result(t->result, r1);
            if (rd != r1)
                emit_asm("MOV  R%d, R%d", rd, r1);
        }
        else if (strcmp(t->op, "label") == 0) {
            flush_all();
            printf("L%s:\n", t->result);
        }
        else if (strcmp(t->op, "goto") == 0) {
            flush_all();
            emit_asm("J    L%s", t->result);
        }
        else if (strcmp(t->op, "if<") == 0) {
            int r1 = getReg_load(t->arg1);
            int r2 = getReg_load(t->arg2);
            emit_asm("CMP  R%d, R%d", r1, r2);
            flush_all();
            emit_asm("BLT  L%s", t->result);
        }
        else if (strcmp(t->op, "ret") == 0) {
            int r1 = getReg_load(t->arg1);
            if (r1 != 0)
                emit_asm("MOV  R0, R%d", r1);
            emit_asm("RET");
        }
        else {
            /* Binary: result = arg1 op arg2 */
            int r1 = getReg_load(t->arg1);
            int r2 = getReg_load(t->arg2);
            int rd = getReg_result(t->result, r1);
            emit_asm("%-4s R%d, R%d, R%d", op_to_asm(t->op), rd, r1, r2);
        }
    }
    flush_all();
}

/* ---- Driver ---- */
int main(void) {
    /*
     * TAC for:  z = (a + b) * (c - d)
     *           if z < e goto L0
     *           return z
     * L0:       return e
     */
    TAC program[] = {
        { "+",    "a",  "b",  "t1"  },
        { "-",    "c",  "d",  "t2"  },
        { "*",    "t1", "t2", "z"   },
        { "if<",  "z",  "e",  "0"   },
        { "ret",  "z",  "",   ""    },
        { "label","",   "",   "0"   },
        { "ret",  "e",  "",   ""    },
    };
    int n = sizeof(program) / sizeof(program[0]);

    printf("=== Source TAC ===\n");
    printf("t1 = a + b\n");
    printf("t2 = c - d\n");
    printf("z  = t1 * t2\n");
    printf("if z < e goto L0\n");
    printf("return z\n");
    printf("L0:\n");
    printf("return e\n");
    printf("\n=== Generated Assembly (4 registers) ===\n\n");

    generate(program, n);

    return 0;
}
```

Sample output:
```
=== Generated Assembly (4 registers) ===

    LD   R0, a
    LD   R1, b
    ADD  R0, R0, R1
    LD   R1, c
    LD   R2, d
    SUB  R1, R1, R2
    MUL  R0, R0, R1
    LD   R1, e
    CMP  R0, R1
    ST   z, R0
    ST   e, R1
    BLT  L0
    LD   R0, z
    MOV  R0, R0
    RET
L0:
    LD   R0, e
    MOV  R0, R0
    RET
```

---

## 8 Calling Conventions & Activation Records (Code Gen Perspective)

The code generator must emit the **function prologue** and **epilogue** that set up and tear down the stack frame.

### Prologue (at function entry):
```asm
PUSH FP              ; save old frame pointer
MOV  FP, SP          ; set new frame pointer
SUBI SP, SP, #locals ; allocate space for local variables
PUSH R_saved...      ; save callee-saved registers
```

### Epilogue (at function exit):
```asm
POP  R_saved...      ; restore callee-saved registers
MOV  SP, FP          ; deallocate locals
POP  FP              ; restore old frame pointer
RET
```

### Caller side:
```asm
PUSH arg_n           ; push arguments right-to-left
...
PUSH arg_1
CALL func
ADDI SP, SP, #n*4    ; clean up arguments
; result in R0
```

---

## 9 Target-Specific Considerations

### 9.1 x86 Example

```x86asm
; z = a + b  (x86-64, AT&T syntax)
movl  a(%rip), %eax       ; load a
addl  b(%rip), %eax       ; add b directly from memory (CISC!)
movl  %eax, z(%rip)       ; store z
```

x86 has memory operands in ALU instructions — the instruction selector can combine load+op into one instruction.

### 9.2 ARM Example

```arm
; z = a + b  (ARM)
LDR  R0, =a
LDR  R0, [R0]
LDR  R1, =b
LDR  R1, [R1]
ADD  R0, R0, R1
LDR  R2, =z
STR  R0, [R2]
```

ARM is load/store — all arithmetic operates on registers only.

---

## 10 Summary

| Component | Key Technique |
|---|---|
| **Instruction selection** | Pattern matching / tiling on IR trees |
| **Register allocation** | Graph colouring (Chaitin's algorithm) or linear scan |
| **Instruction scheduling** | List scheduling on dependency DAG |
| **Calling convention** | Prologue/epilogue, caller/callee saved registers, stack frame |
| **Spilling** | When registers are exhausted, store values to memory |

$$
\boxed{
\text{Optimised IR}
\xrightarrow[\text{Register allocation}]{\text{Instruction selection}}
\text{Target Assembly}
\xrightarrow{\text{Assembler}}
\text{Machine Code}
}
$$

---

## 11 The Complete Compilation Pipeline

Bringing all phases together:

$$
\text{Source}
\xrightarrow{1.\;[\![Lexical\;Analyser]\!]}
\xrightarrow{2.\;[\![Syntax\;Analyser]\!]}
\xrightarrow{3.\;[\![Semantic\;Analysis]\!]}
\xrightarrow{4.\;[\![Intermediate\;Code\;Generation]\!]}
\xrightarrow{5.\;[\![Code\;Optimisation]\!]}
\xrightarrow{6.\;\text{Code Generation}}
\text{Target}
$$

Each phase note is linked above — together they form the complete Compiler Design notes.
