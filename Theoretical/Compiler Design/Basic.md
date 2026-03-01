# 1 Language Processing

A **language processor** is a program that takes source code written in one language and translates / prepares it for execution. The complete pipeline from source to executable involves several components.

## 1.1 Parts of a Language Processor

| # | Component | Role |
|---|---|---|
| 1 | **Preprocessor** | Handles macros, file inclusion (`#include`), conditional compilation (`#ifdef`). Produces expanded source code. |
| 2 | **Compiler** | Translates high-level source code into **assembly language** (or intermediate code). This is the core focus of these notes. |
| 3 | **Assembler** | Converts assembly language into **relocatable machine code** (object file, `.o`). |
| 4 | **Linker** | Combines multiple object files and libraries into a single **executable**. Resolves external symbol references. |
| 5 | **Loader** | Loads the executable into **main memory** and prepares it for execution (relocation, address binding). |

### Flow

$$
\text{Source} \xrightarrow{\text{Preprocessor}} \text{Expanded Source} \xrightarrow{\text{Compiler}} \text{Assembly} \xrightarrow{\text{Assembler}} \text{Object Code} \xrightarrow{\text{Linker}} \text{Executable} \xrightarrow{\text{Loader}} \text{Memory}
$$

### 1.1.1 Compiler vs Interpreter

| Aspect | Compiler | Interpreter |
|---|---|---|
| **Translation** | Entire program at once | Statement by statement |
| **Output** | Machine / intermediate code | Immediate execution result |
| **Speed** | Faster at runtime | Slower at runtime |
| **Error reporting** | After full compilation | At the offending statement |
| **Examples** | GCC, Clang, javac | Python, Ruby, Node.js (JIT hybrid) |

Some systems are **hybrid**: Java compiles to bytecode (compiler), which is then interpreted/JIT-compiled by the JVM.

---

# 2 Stages of Compilation

A compiler is internally organised into **phases**, each transforming the program from one representation to the next.

$$
\boxed{
\text{Source}
\xrightarrow{1.\;\text{Lexical}}
\xrightarrow{2.\;\text{Syntax}}
\xrightarrow{3.\;\text{Semantic}}
\xrightarrow{4.\;\text{Intermediate CG}}
\xrightarrow{5.\;\text{Optimisation}}
\xrightarrow{6.\;\text{Code Gen}}
\text{Target}
}
$$

## 2.1 Overview of Each Phase

| Phase | Input → Output | Key Task |
|---|---|---|
| **1. Lexical Analysis** | Character stream → Token stream | Tokenisation, remove whitespace/comments |
| **2. Syntax Analysis** | Token stream → Parse tree / AST | Check grammatical structure (CFG) |
| **3. Semantic Analysis** | AST → Annotated AST | Type checking, scope resolution |
| **4. Intermediate Code Generation** | Annotated AST → IR (e.g. three-address code) | Machine-independent representation |
| **5. Code Optimisation** | IR → Optimised IR | Improve speed / reduce code size |
| **6. Code Generation** | Optimised IR → Target machine code | Register allocation, instruction selection |

Two components run **across all phases**:
- **Symbol Table Manager** — stores identifiers, types, scopes, memory locations.
- **Error Handler** — detects and reports errors at every phase.

## 2.2 Detailed Phase-by-Phase Example

Source statement:
```c
position = initial + rate * 60;
```

### Phase 1 — Lexical Analysis ([Lexical Analyser](<Lexical Analyser.md>))

$$\langle\text{id},1\rangle\;\langle=\rangle\;\langle\text{id},2\rangle\;\langle+\rangle\;\langle\text{id},3\rangle\;\langle*\rangle\;\langle 60 \rangle$$

### Phase 2 — Syntax Analysis ([Syntax Analyser](<Syntax Analyser.md>))

Produces a parse tree / AST:
```
        =
       / \
    id1    +
          / \
        id2   *
             / \
           id3  60
```

### Phase 3 — Semantic Analysis

- **Type checking**: `60` is an integer, `rate` is a float → insert an `intToFloat` conversion node.
- **Scope checking**: ensure `position`, `initial`, `rate` are declared.

```
        =
       / \
    id1    +
          / \
        id2   *
             / \
           id3  intToFloat
                   |
                  60
```

### Phase 4 — Intermediate Code Generation

Three-address code:
```
t1 = intToFloat(60)
t2 = id3 * t1
t3 = id2 + t2
id1 = t3
```

### Phase 5 — Code Optimisation

```
t1 = id3 * 60.0      ← constant folded intToFloat at compile time
id1 = id2 + t1        ← eliminated temporary t3
```

### Phase 6 — Code Generation

```asm
LDF  R2, id3        ; load rate into R2
MULF R2, R2, #60.0  ; R2 = rate * 60.0
LDF  R1, id2        ; load initial into R1
ADDF R1, R1, R2     ; R1 = initial + rate * 60.0
STF  id1, R1        ; position = R1
```

---

# 3 Passes of a Compiler

| Type | Description |
|---|---|
| **Single-pass** | All phases interleaved in a single traversal of the source. Fast but limited optimisation (e.g. early Pascal compilers). |
| **Multi-pass** | Each phase (or group of phases) is a separate pass over the program representation. Enables more optimisation. |
| **Two-pass** | Common practical choice — **front end** (lexical + syntax + semantic + IR gen) and **back end** (optimisation + code gen). |

### 3.1 Front End vs Back End

```
┌──────────── Front End ────────────┐  ┌────────── Back End ──────────┐
│ Lexical → Syntax → Semantic → IR  │  │ Optimisation → Code Gen      │
│                                   │  │                               │
│ Language-dependent                │  │ Machine-dependent             │
│ Machine-independent               │  │ Language-independent          │
└───────────────────────────────────┘  └───────────────────────────────┘
```

This separation allows **retargeting**: the same front end can emit different back ends for x86, ARM, RISC-V, etc. It also allows **multiple front ends** (C, Fortran, Rust) to share a common back end (e.g. LLVM).

---

# 4 Compiler Construction Tools

| Tool | Purpose | Phase |
|---|---|---|
| **Lex / Flex** | Lexer generator (regex → DFA → C code) | Lexical Analysis |
| **YACC / Bison** | Parser generator (CFG → LALR(1) tables → C code) | Syntax Analysis |
| **LLVM** | Compiler infrastructure — IR, optimisation passes, code gen | All back-end phases |
| **ANTLR** | LL(*) parser generator (Java/Python/C++) | Lexical + Syntax |
| **GCC** | Full production compiler suite | All phases |

---

# 5 The Symbol Table

The **symbol table** is a data structure maintained throughout compilation. Every identifier gets an entry.

| Field | Content |
|---|---|
| **Name** | Lexeme string (e.g. `rate`) |
| **Type** | `int`, `float`, `char*`, function signature, etc. |
| **Scope** | Global, local, block level |
| **Memory location** | Offset in the activation record / data segment |
| **Size** | Number of bytes |
| **Line declared** | For error messages |

### 5.1 Common Implementations

| Structure | Lookup | Insert | Notes |
|---|---|---|---|
| **Linear list** | $O(n)$ | $O(1)$ | Simple; only for tiny programs |
| **Hash table** | $O(1)$ avg | $O(1)$ avg | Most common in practice |
| **BST** | $O(\log n)$ | $O(\log n)$ | Ordered traversal, rarely used |

### 5.2 Scope Management

For block-structured languages, use a **stack of hash tables** — one per scope level:
1. Enter a new scope → push a new table.
2. Declare a variable → insert into the top table.
3. Lookup → search from top to bottom (innermost scope first).
4. Exit a scope → pop the table.

---

# 6 Error Handling

Errors can occur at every phase:

| Phase | Example Error |
|---|---|
| **Lexical** | Invalid character, unterminated string |
| **Syntax** | Missing semicolon, unbalanced parentheses |
| **Semantic** | Type mismatch, undeclared variable, wrong number of arguments |
| **Intermediate CG** | Rare — usually caught earlier |
| **Optimisation** | Rare — internal compiler errors |
| **Code Gen** | Rare — e.g. too many variables for available registers (spill required) |

A good compiler should:
- Report errors **accurately** (correct line number, clear message).
- **Recover** and continue to find more errors in a single compilation.
- Never produce **incorrect** output code silently.

---

# 7 Cousins of the Compiler

| Tool | Description |
|---|---|
| **Preprocessor** | Macro expansion, file inclusion |
| **Assembler** | Assembly → machine code |
| **Linker** | Combines object files, resolves symbols |
| **Loader** | Places executable in memory |
| **Debugger** | Maps machine state back to source (using debug info) |
| **Profiler** | Measures execution time / memory per function |
| **Decompiler** | Machine code → high-level source (reverse engineering) |
| **Cross-compiler** | Runs on platform A, produces code for platform B |
| **Just-In-Time (JIT) compiler** | Compiles at runtime (Java HotSpot, V8) |

---

# 8 Summary

$$
\boxed{
\text{Source Program}
\xrightarrow[\text{Front End}]{\text{Analysis}}
\text{IR}
\xrightarrow[\text{Back End}]{\text{Synthesis}}
\text{Target Program}
}
$$

- The **analysis** (front end) breaks the source into pieces and creates an intermediate representation.
- The **synthesis** (back end) constructs the target program from the IR.
- The **symbol table** and **error handler** support all phases.




