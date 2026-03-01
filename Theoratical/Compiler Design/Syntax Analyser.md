# Syntax Analyser (Parser)

The **Syntax Analyser** (parser) is the second phase of a compiler. It takes the token stream produced by the [[Lexical Analyser]] and checks whether it conforms to the **context-free grammar** (CFG) of the language, producing a **parse tree** (or abstract syntax tree).

$$
\text{Token stream} \xrightarrow{\text{Parser}} \text{Parse Tree / AST}
$$

---

## 1 Context-Free Grammars (CFG)

A CFG is defined as a 4-tuple: $G = (V, T, P, S)$

| Symbol | Meaning |
|---|---|
| $V$ | Set of **non-terminals** (syntactic variables) |
| $T$ | Set of **terminals** (tokens from lexer) |
| $P$ | Set of **productions** (rules) |
| $S$ | **Start symbol** ($S \in V$) |

### 1.1 Example Grammar for Arithmetic Expressions

$$
\begin{aligned}
E &\rightarrow E + T \mid T \\
T &\rightarrow T * F \mid F \\
F &\rightarrow ( E ) \mid \textbf{id} \mid \textbf{num}
\end{aligned}
$$

This grammar encodes **operator precedence** ($*$ binds tighter than $+$) and **left-associativity** structurally.

### 1.2 Derivations

- **Leftmost derivation** — always expand the leftmost non-terminal first.
- **Rightmost derivation** — always expand the rightmost non-terminal first.

Example: derive `id + id * id`

Leftmost:
$$E \Rightarrow E + T \Rightarrow T + T \Rightarrow F + T \Rightarrow \textbf{id} + T \Rightarrow \textbf{id} + T * F \Rightarrow \textbf{id} + F * F \Rightarrow \textbf{id} + \textbf{id} * F \Rightarrow \textbf{id} + \textbf{id} * \textbf{id}$$

### 1.3 Parse Tree vs AST

- A **parse tree** includes every grammar symbol (verbose).
- An **AST** (Abstract Syntax Tree) omits redundant nodes (parentheses, chain productions) — this is what compilers actually use downstream.

### 1.4 Ambiguity

A grammar is **ambiguous** if a string has more than one parse tree. Classic example — the **dangling else**:

```
S → if E then S
  | if E then S else S
  | other
```

The string `if E then if E then S else S` has two parse trees. Fix: rewrite the grammar to associate `else` with the **nearest** unmatched `if`.

---

## 2 Top-Down Parsing

Top-down parsers build the parse tree from the **root** (start symbol) **down** to the leaves (tokens). They try to find a **leftmost derivation** for the input.

### 2.1 Recursive Descent Parsing

A **recursive descent parser** is a set of **mutually recursive functions**, one for each non-terminal in the grammar. Each function "descends" into the grammar rules.

#### How It Works

1. Start by calling the function for the start symbol.
2. Each function looks at the **current token** (lookahead).
3. Based on the token, choose which production to apply.
4. For each symbol in the production:
   - **Terminal** → match it with the current token and advance.
   - **Non-terminal** → call that non-terminal's function.
5. If no production matches → **syntax error**.

#### Problem: Left Recursion

A grammar like $A \rightarrow A \alpha \mid \beta$ causes **infinite recursion** in recursive descent. The function for $A$ calls itself before consuming any input.

**Elimination:** Convert left recursion to right recursion.

$$
A \rightarrow A \alpha \mid \beta \quad \Longrightarrow \quad
\begin{cases}
A  \rightarrow \beta \; A' \\
A' \rightarrow \alpha \; A' \mid \varepsilon
\end{cases}
$$

Our expression grammar becomes:

$$
\begin{aligned}
E  &\rightarrow T \; E' \\
E' &\rightarrow + \; T \; E' \mid \varepsilon \\
T  &\rightarrow F \; T' \\
T' &\rightarrow * \; F \; T' \mid \varepsilon \\
F  &\rightarrow ( \; E \; ) \mid \textbf{id} \mid \textbf{num}
\end{aligned}
$$

#### Complete Recursive Descent Parser in C

```c
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

/*
 * Grammar (left-recursion eliminated):
 *   E  -> T E'
 *   E' -> + T E' | - T E' | ε
 *   T  -> F T'
 *   T' -> * F T' | / F T' | ε
 *   F  -> ( E ) | number | identifier
 */

/* ============ Lexer (simplified) ============ */

typedef enum {
    TOK_NUM, TOK_ID, TOK_PLUS, TOK_MINUS,
    TOK_STAR, TOK_SLASH, TOK_LPAREN, TOK_RPAREN,
    TOK_EOF, TOK_UNKNOWN
} TokenType;

typedef struct {
    TokenType type;
    char      text[64];
} Token;

const char *src;
int         pos;
Token       lookahead;

void next_token(void) {
    /* skip whitespace */
    while (src[pos] == ' ' || src[pos] == '\t')
        pos++;

    char c = src[pos];

    if (c == '\0') {
        lookahead = (Token){ TOK_EOF, "EOF" };
        return;
    }
    if (isdigit(c)) {
        int i = 0;
        while (isdigit(src[pos]))
            lookahead.text[i++] = src[pos++];
        lookahead.text[i] = '\0';
        lookahead.type = TOK_NUM;
        return;
    }
    if (isalpha(c) || c == '_') {
        int i = 0;
        while (isalnum(src[pos]) || src[pos] == '_')
            lookahead.text[i++] = src[pos++];
        lookahead.text[i] = '\0';
        lookahead.type = TOK_ID;
        return;
    }
    lookahead.text[0] = c;
    lookahead.text[1] = '\0';
    pos++;
    switch (c) {
        case '+': lookahead.type = TOK_PLUS;   break;
        case '-': lookahead.type = TOK_MINUS;  break;
        case '*': lookahead.type = TOK_STAR;   break;
        case '/': lookahead.type = TOK_SLASH;  break;
        case '(': lookahead.type = TOK_LPAREN; break;
        case ')': lookahead.type = TOK_RPAREN; break;
        default:  lookahead.type = TOK_UNKNOWN; break;
    }
}

void match(TokenType expected) {
    if (lookahead.type == expected) {
        printf("  matched: %s\n", lookahead.text);
        next_token();
    } else {
        printf("Syntax error: expected token type %d, got '%s'\n",
               expected, lookahead.text);
        exit(1);
    }
}

/* ============ Parser ============ */

void E(void);    /* E  -> T E'         */
void E_p(void);  /* E' -> +T E' | ε    */
void T(void);    /* T  -> F T'         */
void T_p(void);  /* T' -> *F T' | ε    */
void F(void);    /* F  -> (E) | num | id */

void E(void) {
    printf("E -> T E'\n");
    T();
    E_p();
}

void E_p(void) {
    if (lookahead.type == TOK_PLUS) {
        printf("E' -> + T E'\n");
        match(TOK_PLUS);
        T();
        E_p();
    } else if (lookahead.type == TOK_MINUS) {
        printf("E' -> - T E'\n");
        match(TOK_MINUS);
        T();
        E_p();
    } else {
        printf("E' -> ε\n");   /* follow set check in production */
    }
}

void T(void) {
    printf("T -> F T'\n");
    F();
    T_p();
}

void T_p(void) {
    if (lookahead.type == TOK_STAR) {
        printf("T' -> * F T'\n");
        match(TOK_STAR);
        F();
        T_p();
    } else if (lookahead.type == TOK_SLASH) {
        printf("T' -> / F T'\n");
        match(TOK_SLASH);
        F();
        T_p();
    } else {
        printf("T' -> ε\n");
    }
}

void F(void) {
    if (lookahead.type == TOK_LPAREN) {
        printf("F -> ( E )\n");
        match(TOK_LPAREN);
        E();
        match(TOK_RPAREN);
    } else if (lookahead.type == TOK_NUM) {
        printf("F -> num\n");
        match(TOK_NUM);
    } else if (lookahead.type == TOK_ID) {
        printf("F -> id\n");
        match(TOK_ID);
    } else {
        printf("Syntax error in F: unexpected '%s'\n", lookahead.text);
        exit(1);
    }
}

/* ============ Main ============ */

int main(void) {
    const char *input = "x + 2 * ( y - 3 )";
    printf("Input: %s\n\n", input);

    src = input;
    pos = 0;
    next_token();

    E();

    if (lookahead.type == TOK_EOF)
        printf("\nParsing succeeded!\n");
    else
        printf("\nSyntax error: unexpected trailing '%s'\n", lookahead.text);

    return 0;
}
```

Running this on `x + 2 * ( y - 3 )` produces a trace of every grammar rule applied — showing exactly how the recursive descent works.

---

### 2.2 Predictive Parsing & LL(1) Grammars

A **predictive parser** is a recursive descent parser that **never backtracks**. It uses exactly one token of lookahead to decide which production to use. This works when the grammar is **LL(1)**.

**LL(1)** = **L**eft-to-right scan, **L**eftmost derivation, **1** token of lookahead.

#### FIRST and FOLLOW Sets

| Set | Definition |
|---|---|
| $\text{FIRST}(\alpha)$ | The set of terminals that can appear as the first symbol of any string derived from $\alpha$. If $\alpha \Rightarrow^* \varepsilon$, then $\varepsilon \in \text{FIRST}(\alpha)$. |
| $\text{FOLLOW}(A)$ | The set of terminals that can appear immediately after $A$ in some sentential form. $\$ \in \text{FOLLOW}(S)$ always. |

**Rules for FIRST:**
1. If $X$ is a terminal: $\text{FIRST}(X) = \{X\}$.
2. If $X \rightarrow \varepsilon$: add $\varepsilon$ to $\text{FIRST}(X)$.
3. If $X \rightarrow Y_1 Y_2 \ldots Y_k$: add $\text{FIRST}(Y_1)$ (minus $\varepsilon$). If $\varepsilon \in \text{FIRST}(Y_1)$, also add $\text{FIRST}(Y_2)$, and so on.

**Rules for FOLLOW:**
1. $\$ \in \text{FOLLOW}(S)$ (start symbol).
2. If $A \rightarrow \alpha B \beta$: add $\text{FIRST}(\beta) - \{\varepsilon\}$ to $\text{FOLLOW}(B)$.
3. If $A \rightarrow \alpha B$ or $\varepsilon \in \text{FIRST}(\beta)$: add $\text{FOLLOW}(A)$ to $\text{FOLLOW}(B)$.

#### Example: Compute FIRST & FOLLOW

Grammar:
$$
\begin{aligned}
E  &\rightarrow T \; E'  &\quad  E' &\rightarrow + \; T \; E' \mid \varepsilon \\
T  &\rightarrow F \; T'  &\quad  T' &\rightarrow * \; F \; T' \mid \varepsilon \\
F  &\rightarrow ( \; E \; ) \mid \textbf{id}
\end{aligned}
$$

| Non-terminal | FIRST | FOLLOW |
|---|---|---|
| $E$ | $\{(, \textbf{id}\}$ | $\{\$, )\}$ |
| $E'$ | $\{+, \varepsilon\}$ | $\{\$, )\}$ |
| $T$ | $\{(, \textbf{id}\}$ | $\{+, \$, )\}$ |
| $T'$ | $\{*, \varepsilon\}$ | $\{+, \$, )\}$ |
| $F$ | $\{(, \textbf{id}\}$ | $\{*, +, \$, )\}$ |

#### LL(1) Parsing Table

Build the table $M[A, a]$:
- For each production $A \rightarrow \alpha$:
  - For each terminal $a \in \text{FIRST}(\alpha)$, set $M[A, a] = A \rightarrow \alpha$.
  - If $\varepsilon \in \text{FIRST}(\alpha)$, for each $b \in \text{FOLLOW}(A)$, set $M[A, b] = A \rightarrow \alpha$.

| | **id** | **+** | **\*** | **(** | **)** | **$** |
|---|---|---|---|---|---|---|
| $E$ | $E \rightarrow TE'$ | | | $E \rightarrow TE'$ | | |
| $E'$ | | $E' \rightarrow +TE'$ | | | $E' \rightarrow \varepsilon$ | $E' \rightarrow \varepsilon$ |
| $T$ | $T \rightarrow FT'$ | | | $T \rightarrow FT'$ | | |
| $T'$ | | $T' \rightarrow \varepsilon$ | $T' \rightarrow *FT'$ | | $T' \rightarrow \varepsilon$ | $T' \rightarrow \varepsilon$ |
| $F$ | $F \rightarrow \textbf{id}$ | | | $F \rightarrow (E)$ | | |

If any cell has **more than one** entry, the grammar is **not LL(1)**.

#### Table-Driven LL(1) Parser in C

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

/*
 * Table-driven LL(1) parser for:
 *   E  -> T E'
 *   E' -> + T E' | ε
 *   T  -> F T'
 *   T' -> * F T' | ε
 *   F  -> ( E ) | id
 */

/* ---- Symbol definitions ---- */
enum Symbol {
    /* terminals */
    S_ID, S_PLUS, S_STAR, S_LPAREN, S_RPAREN, S_DOLLAR,
    /* non-terminals */
    S_E, S_EP, S_T, S_TP, S_F,
    /* special */
    S_EPSILON
};
const char *sym_name[] = {
    "id","+","*","(",")","$",
    "E","E'","T","T'","F","ε"
};

#define NUM_NT   5  /* E, E', T, T', F */
#define NUM_T    6  /* id, +, *, (, ), $ */

/* ---- Productions stored as arrays of symbols ---- */
/*  0: E  -> T E'            */
/*  1: E' -> + T E'          */
/*  2: E' -> ε               */
/*  3: T  -> F T'            */
/*  4: T' -> * F T'          */
/*  5: T' -> ε               */
/*  6: F  -> ( E )           */
/*  7: F  -> id              */

int prods[8][4] = {
    { S_T, S_EP, -1 },           /* 0 */
    { S_PLUS, S_T, S_EP, -1 },   /* 1 */
    { S_EPSILON, -1 },            /* 2 */
    { S_F, S_TP, -1 },            /* 3 */
    { S_STAR, S_F, S_TP, -1 },    /* 4 */
    { S_EPSILON, -1 },            /* 5 */
    { S_LPAREN, S_E, S_RPAREN, -1 }, /* 6 */
    { S_ID, -1 },                 /* 7 */
};

/* ---- Parsing table  M[non-terminal_index][terminal_index] = prod# ---- */
/* NT index: E=0, E'=1, T=2, T'=3, F=4                                    */
/* T  index: id=0, +=1, *=2, (=3, )=4, $=5                                */

int table[NUM_NT][NUM_T] = {
    /*        id   +   *   (   )   $ */
    /* E  */ { 0, -1, -1,  0, -1, -1 },
    /* E' */ {-1,  1, -1, -1,  2,  2 },
    /* T  */ { 3, -1, -1,  3, -1, -1 },
    /* T' */ {-1,  5,  4, -1,  5,  5 },
    /* F  */ { 7, -1, -1,  6, -1, -1 },
};

/* ---- Stack ---- */
int stack[256];
int sp = -1;
void push(int s)   { stack[++sp] = s; }
int  pop(void)     { return stack[sp--]; }
int  top(void)     { return stack[sp]; }

/* ---- Lexer (tokeniser) ---- */
const char *input;
int         ipos;
int         cur_token;

int next_t(void) {
    while (input[ipos] == ' ') ipos++;
    char c = input[ipos];
    if (c == '\0') return S_DOLLAR;
    if (isalpha(c) || c == '_') {
        while (isalnum(input[ipos]) || input[ipos] == '_') ipos++;
        return S_ID;
    }
    ipos++;
    switch (c) {
        case '+': return S_PLUS;
        case '*': return S_STAR;
        case '(': return S_LPAREN;
        case ')': return S_RPAREN;
    }
    return -1; /* error */
}

/* ---- Parser ---- */
int main(void) {
    input = "a + b * ( c + d )";
    ipos  = 0;
    printf("Input: %s\n\n", input);

    push(S_DOLLAR);
    push(S_E);
    cur_token = next_t();

    while (top() != S_DOLLAR) {
        int X = top();

        if (X == cur_token) {
            /* terminal matches */
            printf("Match  : %s\n", sym_name[X]);
            pop();
            cur_token = next_t();
        }
        else if (X < S_E) {
            /* X is a terminal but doesn't match */
            printf("Error: expected %s\n", sym_name[X]);
            return 1;
        }
        else {
            /* X is a non-terminal */
            int nt_idx = X - S_E;   /* 0..4 */
            int t_idx  = cur_token; /* 0..5 */
            int p = table[nt_idx][t_idx];
            if (p == -1) {
                printf("Error: no table entry for M[%s, %s]\n",
                       sym_name[X], sym_name[cur_token]);
                return 1;
            }
            pop();
            printf("Apply  : %s -> ", sym_name[X]);
            /* push production RHS in reverse order */
            int len = 0;
            while (prods[p][len] != -1) len++;
            if (prods[p][0] == S_EPSILON) {
                printf("ε\n");
            } else {
                for (int i = 0; i < len; i++)
                    printf("%s ", sym_name[prods[p][i]]);
                printf("\n");
                for (int i = len - 1; i >= 0; i--)
                    push(prods[p][i]);
            }
        }
    }

    if (cur_token == S_DOLLAR)
        printf("\nParsing succeeded!\n");
    else
        printf("\nError: input not fully consumed\n");

    return 0;
}
```

---

### 2.3 LL(1) Parsing — Conditions & Limitations

A grammar is LL(1) **if and only if** for every pair of productions $A \rightarrow \alpha \mid \beta$:
1. $\text{FIRST}(\alpha) \cap \text{FIRST}(\beta) = \emptyset$
2. If $\varepsilon \in \text{FIRST}(\alpha)$, then $\text{FIRST}(\beta) \cap \text{FOLLOW}(A) = \emptyset$

**Grammars that are NOT LL(1):**
- Left-recursive grammars
- Ambiguous grammars
- Grammars needing more than 1 token of lookahead

**Fixes:**
- **Left factoring** — extract common prefixes.
- **Left recursion elimination** — convert to right-recursive form.

Left factoring example:
$$
S \rightarrow \textbf{if}\; E\; \textbf{then}\; S \mid \textbf{if}\; E\; \textbf{then}\; S\; \textbf{else}\; S
$$
becomes:
$$
\begin{aligned}
S  &\rightarrow \textbf{if}\; E\; \textbf{then}\; S\; S' \\
S' &\rightarrow \textbf{else}\; S \mid \varepsilon
\end{aligned}
$$

---

## 3 Bottom-Up Parsing

Bottom-up parsers build the parse tree from the **leaves** (tokens) **up** to the root (start symbol). They try to find a **rightmost derivation in reverse**.

The key operation is **reduction**: replace a substring matching the right side of a production with the non-terminal on the left side.

### 3.1 Shift-Reduce Parsing

The parser uses a **stack** and scans input left-to-right. Four actions:

| Action | Description |
|---|---|
| **Shift** | Push the next input token onto the stack. |
| **Reduce** | Pop symbols matching a production's RHS, push the LHS non-terminal. |
| **Accept** | Input is fully parsed, start symbol is on the stack. |
| **Error** | No valid action possible. |

#### Handle

A **handle** is a substring of the sentential form that matches the right side of a production and whose reduction represents one step in the reverse of a rightmost derivation.

#### Example: Shift-Reduce Trace

Grammar:
$$
\begin{aligned}
E &\rightarrow E + T \mid T \\
T &\rightarrow T * F \mid F \\
F &\rightarrow ( E ) \mid \textbf{id}
\end{aligned}
$$

Input: `id + id * id`

| Stack | Input | Action |
|---|---|---|
| `$` | `id + id * id $` | Shift |
| `$ id` | `+ id * id $` | Reduce $F \rightarrow \textbf{id}$ |
| `$ F` | `+ id * id $` | Reduce $T \rightarrow F$ |
| `$ T` | `+ id * id $` | Reduce $E \rightarrow T$ |
| `$ E` | `+ id * id $` | Shift |
| `$ E +` | `id * id $` | Shift |
| `$ E + id` | `* id $` | Reduce $F \rightarrow \textbf{id}$ |
| `$ E + F` | `* id $` | Reduce $T \rightarrow F$ |
| `$ E + T` | `* id $` | Shift |
| `$ E + T *` | `id $` | Shift |
| `$ E + T * id` | `$` | Reduce $F \rightarrow \textbf{id}$ |
| `$ E + T * F` | `$` | Reduce $T \rightarrow T * F$ |
| `$ E + T` | `$` | Reduce $E \rightarrow E + T$ |
| `$ E` | `$` | **Accept** |

---

### 3.2 LR Parsing

**LR** = **L**eft-to-right scan, **R**ightmost derivation (in reverse).

LR parsers are the most powerful class of shift-reduce parsers. Variants:

| Parser | Description |
|---|---|
| **LR(0)** | No lookahead. Very limited. |
| **SLR(1)** | Uses FOLLOW sets to resolve conflicts. Simple to implement. |
| **LALR(1)** | Merges LR(1) states with same core. Used by YACC/Bison. |
| **CLR(1)** | Full canonical LR. Most powerful, largest tables. |

### 3.3 LR(0) Items and the Canonical Collection

An **LR(0) item** is a production with a **dot** indicating how much of the RHS has been seen:

$$A \rightarrow \alpha \cdot \beta$$

- Dot at the beginning: nothing matched yet.
- Dot at the end: ready to reduce.

For $E \rightarrow E + T$:
- $E \rightarrow \cdot E + T$ (nothing seen)
- $E \rightarrow E \cdot + T$ (seen $E$)
- $E \rightarrow E + \cdot T$ (seen $E +$)
- $E \rightarrow E + T \cdot$ (ready to reduce)

#### Closure Operation

Given a set of items $I$:
1. Start with $I$.
2. If $A \rightarrow \alpha \cdot B \beta$ is in the set, add all productions $B \rightarrow \cdot \gamma$ for every production of $B$.
3. Repeat until no new items are added.

#### GOTO Operation

$\text{GOTO}(I, X)$ = closure of all items $A \rightarrow \alpha X \cdot \beta$ where $A \rightarrow \alpha \cdot X \beta \in I$.

This moves the dot past symbol $X$.

### 3.4 SLR(1) Parsing Table Construction

1. Augment the grammar: add $S' \rightarrow S$.
2. Build the **canonical collection** of LR(0) item sets using closure and GOTO.
3. For each state $I_i$:
   - If $A \rightarrow \alpha \cdot a \beta \in I_i$ (dot before terminal $a$) and $\text{GOTO}(I_i, a) = I_j$
     → $\text{ACTION}[i, a] = \text{shift } j$
   - If $A \rightarrow \alpha \cdot \in I_i$ ($A \neq S'$)
     → for each $a \in \text{FOLLOW}(A)$: $\text{ACTION}[i, a] = \text{reduce } A \rightarrow \alpha$
   - If $S' \rightarrow S \cdot \in I_i$
     → $\text{ACTION}[i, \$] = \text{accept}$
4. For non-terminal $A$: if $\text{GOTO}(I_i, A) = I_j$ → $\text{GOTO}[i, A] = j$

**Conflicts:**
- **Shift-reduce conflict** — a cell has both shift and reduce.
- **Reduce-reduce conflict** — a cell has two different reductions.
If any conflict exists → grammar is **not SLR(1)**.

### 3.5 SLR(1) Worked Example

Augmented grammar:
$$
\begin{aligned}
S' &\rightarrow E \\
E  &\rightarrow E + T \mid T \\
T  &\rightarrow T * F \mid F \\
F  &\rightarrow ( E ) \mid \textbf{id}
\end{aligned}
$$

**Item sets (abbreviated):**

| State | Items (key items shown) |
|---|---|
| $I_0$ | $S' \rightarrow \cdot E$, $E \rightarrow \cdot E+T$, $E \rightarrow \cdot T$, $T \rightarrow \cdot T*F$, $T \rightarrow \cdot F$, $F \rightarrow \cdot (E)$, $F \rightarrow \cdot \textbf{id}$ |
| $I_1$ | $S' \rightarrow E \cdot$, $E \rightarrow E \cdot + T$ |
| $I_2$ | $E \rightarrow T \cdot$, $T \rightarrow T \cdot * F$ |
| $I_3$ | $T \rightarrow F \cdot$ |
| $I_4$ | $F \rightarrow ( \cdot E )$, ... |
| $I_5$ | $F \rightarrow \textbf{id} \cdot$ |
| $I_6$ | $E \rightarrow E + \cdot T$, ... |
| $I_7$ | $T \rightarrow T * \cdot F$, ... |
| $I_8$ | $F \rightarrow ( E \cdot )$, $E \rightarrow E \cdot + T$ |
| $I_9$ | $E \rightarrow E + T \cdot$, $T \rightarrow T \cdot * F$ |
| $I_{10}$ | $T \rightarrow T * F \cdot$ |
| $I_{11}$ | $F \rightarrow ( E ) \cdot$ |

**ACTION / GOTO Table:**

| State | id | + | * | ( | ) | $ | E | T | F |
|---|---|---|---|---|---|---|---|---|---|
| 0 | s5 | | | s4 | | | 1 | 2 | 3 |
| 1 | | s6 | | | | acc | | | |
| 2 | | r2 | s7 | | r2 | r2 | | | |
| 3 | | r4 | r4 | | r4 | r4 | | | |
| 4 | s5 | | | s4 | | | 8 | 2 | 3 |
| 5 | | r6 | r6 | | r6 | r6 | | | |
| 6 | s5 | | | s4 | | | | 9 | 3 |
| 7 | s5 | | | s4 | | | | | 10 |
| 8 | | s6 | | | s11 | | | | |
| 9 | | r1 | s7 | | r1 | r1 | | | |
| 10 | | r3 | r3 | | r3 | r3 | | | |
| 11 | | r5 | r5 | | r5 | r5 | | | |

Where: r1 = $E \rightarrow E+T$, r2 = $E \rightarrow T$, r3 = $T \rightarrow T*F$, r4 = $T \rightarrow F$, r5 = $F \rightarrow (E)$, r6 = $F \rightarrow \textbf{id}$.

---

### 3.6 Shift-Reduce Parser Implementation in C

```c
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

/*
 * SLR(1) Shift-Reduce Parser for:
 *   (0) S' -> E
 *   (1) E  -> E + T
 *   (2) E  -> T
 *   (3) T  -> T * F
 *   (4) T  -> F
 *   (5) F  -> ( E )
 *   (6) F  -> id
 */

/* ---- Terminals / Non-terminals ---- */
/* Terminals: 0=id, 1=+, 2=*, 3=(, 4=), 5=$  */
/* Non-terms: 0=E, 1=T, 2=F                   */

#define SHIFT  1
#define REDUCE 2
#define ACCEPT 3
#define ERROR  0

typedef struct { int action; int value; } Entry;

/* ACTION table [12 states][6 terminals] */
Entry action_table[12][6] = {
 /* state 0  */ {{ SHIFT,5},{ERROR,0},{ERROR,0},{SHIFT,4},{ERROR,0},{ERROR,0}},
 /* state 1  */ {{ERROR,0},{SHIFT,6},{ERROR,0},{ERROR,0},{ERROR,0},{ACCEPT,0}},
 /* state 2  */ {{ERROR,0},{REDUCE,2},{SHIFT,7},{ERROR,0},{REDUCE,2},{REDUCE,2}},
 /* state 3  */ {{ERROR,0},{REDUCE,4},{REDUCE,4},{ERROR,0},{REDUCE,4},{REDUCE,4}},
 /* state 4  */ {{SHIFT,5},{ERROR,0},{ERROR,0},{SHIFT,4},{ERROR,0},{ERROR,0}},
 /* state 5  */ {{ERROR,0},{REDUCE,6},{REDUCE,6},{ERROR,0},{REDUCE,6},{REDUCE,6}},
 /* state 6  */ {{SHIFT,5},{ERROR,0},{ERROR,0},{SHIFT,4},{ERROR,0},{ERROR,0}},
 /* state 7  */ {{SHIFT,5},{ERROR,0},{ERROR,0},{SHIFT,4},{ERROR,0},{ERROR,0}},
 /* state 8  */ {{ERROR,0},{SHIFT,6},{ERROR,0},{ERROR,0},{SHIFT,11},{ERROR,0}},
 /* state 9  */ {{ERROR,0},{REDUCE,1},{SHIFT,7},{ERROR,0},{REDUCE,1},{REDUCE,1}},
 /* state 10 */ {{ERROR,0},{REDUCE,3},{REDUCE,3},{ERROR,0},{REDUCE,3},{REDUCE,3}},
 /* state 11 */ {{ERROR,0},{REDUCE,5},{REDUCE,5},{ERROR,0},{REDUCE,5},{REDUCE,5}},
};

/* GOTO table [12 states][3 non-terminals] (E=0, T=1, F=2) */
int goto_table[12][3] = {
    { 1,  2,  3}, /* state 0  */
    {-1, -1, -1}, /* state 1  */
    {-1, -1, -1}, /* state 2  */
    {-1, -1, -1}, /* state 3  */
    { 8,  2,  3}, /* state 4  */
    {-1, -1, -1}, /* state 5  */
    {-1,  9,  3}, /* state 6  */
    {-1, -1, 10}, /* state 7  */
    {-1, -1, -1}, /* state 8  */
    {-1, -1, -1}, /* state 9  */
    {-1, -1, -1}, /* state 10 */
    {-1, -1, -1}, /* state 11 */
};

/* Production info: { lhs_nonterminal_index, rhs_length } */
int prod_lhs[]  = { -1, 0, 0, 1, 1, 2, 2 };   /* E=0, T=1, F=2 */
int prod_len[]  = { -1, 3, 1, 3, 1, 3, 1 };
const char *prod_str[] = {
    "", "E -> E + T", "E -> T", "T -> T * F",
    "T -> F", "F -> ( E )", "F -> id"
};

/* ---- State stack ---- */
int stk[256];
int sp = 0;

/* ---- Tokeniser ---- */
const char *src;
int spos;

int next_terminal(void) {
    while (src[spos] == ' ') spos++;
    char c = src[spos];
    if (c == '\0') return 5; /* $ */
    if (isalpha(c)) { while (isalnum(src[spos])) spos++; return 0; } /* id */
    spos++;
    switch (c) {
        case '+': return 1;
        case '*': return 2;
        case '(': return 3;
        case ')': return 4;
    }
    return -1;
}

const char *tname[] = {"id","+","*","(",")","$"};

int main(void) {
    src  = "a + b * ( c + d )";
    spos = 0;
    printf("Input: %s\n\n", src);

    stk[sp] = 0; /* push initial state */
    int a = next_terminal();

    while (1) {
        int s = stk[sp];
        Entry e = action_table[s][a];

        if (e.action == SHIFT) {
            printf("Shift   %s,  goto state %d\n", tname[a], e.value);
            stk[++sp] = e.value;
            a = next_terminal();
        }
        else if (e.action == REDUCE) {
            int p = e.value;
            printf("Reduce  %s\n", prod_str[p]);
            sp -= prod_len[p];           /* pop RHS symbols */
            int t = stk[sp];             /* state after pop */
            int nt = prod_lhs[p];        /* LHS non-terminal */
            stk[++sp] = goto_table[t][nt];
        }
        else if (e.action == ACCEPT) {
            printf("\n** Accepted! **\n");
            break;
        }
        else {
            printf("Syntax error at state %d, token %s\n", s, tname[a]);
            break;
        }
    }
    return 0;
}
```

---

### 3.7 LALR(1) and CLR(1) — Brief Comparison

| Feature | SLR(1) | LALR(1) | CLR(1) |
|---|---|---|---|
| **Item type** | LR(0) items | LR(1) items (merged cores) | LR(1) items |
| **Lookahead for reduce** | FOLLOW set | Precise lookahead per item | Precise lookahead per item |
| **Number of states** | Same as LR(0) | Same as LR(0) | Potentially much larger |
| **Power** | Weakest | Middle (practical sweet spot) | Strongest |
| **Tool** | — | YACC / Bison | Rarely used directly |

**CLR(1)** uses LR(1) items: $A \rightarrow \alpha \cdot \beta, \; a$ where $a$ is the lookahead symbol. This gives precise reduce actions but can lead to a huge number of states.

**LALR(1)** merges CLR(1) states that have the same **core** (same LR(0) items, ignoring lookaheads). This greatly reduces the table size while keeping most of CLR(1)'s power. Almost all practical programming languages have LALR(1) grammars.

---

## 4 Parser Generators — YACC / Bison

Instead of hand-coding parsers, use a **parser generator**. **Bison** (GNU version of YACC) generates an LALR(1) parser from a grammar specification.

### 4.1 Bison Grammar File (`.y`)

```yacc
/* calc.y — simple calculator */
%{
#include <stdio.h>
#include <stdlib.h>
int yylex(void);
void yyerror(const char *s);
%}

%token NUM ID
%left '+' '-'
%left '*' '/'

%%

expr : expr '+' expr   { printf("reduce: E -> E + E\n"); }
     | expr '-' expr   { printf("reduce: E -> E - E\n"); }
     | expr '*' expr   { printf("reduce: E -> E * E\n"); }
     | expr '/' expr   { printf("reduce: E -> E / E\n"); }
     | '(' expr ')'    { printf("reduce: E -> ( E )\n"); }
     | NUM             { printf("reduce: E -> num\n");    }
     | ID              { printf("reduce: E -> id\n");     }
     ;

%%

void yyerror(const char *s) { fprintf(stderr, "Error: %s\n", s); }
int main(void) { return yyparse(); }
```

Pair this with the Flex scanner from the [[Lexical Analyser]] notes and build:
```bash
bison -d calc.y        # generates calc.tab.c and calc.tab.h
flex scanner.l         # generates lex.yy.c
gcc calc.tab.c lex.yy.c -o calc -lfl
echo "a + b * (c + d)" | ./calc
```

---

## 5 Error Recovery in Syntax Analysis

| Strategy | Description |
|---|---|
| **Panic mode** | Discard tokens until a **synchronising token** (e.g. `;`, `}`) is found. Simple and widely used. |
| **Phrase-level** | Perform local corrections (insert a missing `;`, delete an extra token). |
| **Error productions** | Add grammar rules that anticipate common mistakes. |
| **Global correction** | Find the minimum-edit-distance correction (theoretical; too expensive in practice). |

In LR parsing, **panic mode** pops states from the stack until it finds one with a GOTO entry for a designated non-terminal (like `statement`), then discards input tokens until a token in FOLLOW of that non-terminal is found.

---

## 6 Top-Down vs Bottom-Up — Comparison

| Aspect | Top-Down (LL) | Bottom-Up (LR) |
|---|---|---|
| **Direction** | Root → Leaves | Leaves → Root |
| **Derivation** | Leftmost | Rightmost (in reverse) |
| **Grammar power** | LL(1) — restricted | LR(1) — very broad |
| **Left recursion** | Must be eliminated | Handled naturally |
| **Implementation** | Easier (recursive descent) | More complex (table-driven) |
| **Error messages** | Naturally better | Harder to produce good messages |
| **Tools** | ANTLR, hand-written | YACC, Bison |
| **Use case** | Hand-written parsers, IDEs | Production compilers |

---

## 7 Summary

$$
\boxed{
\underbrace{\text{Token stream}}_{\text{from lexer}}
\xrightarrow[\text{Top-down (LL) or Bottom-up (LR)}]{\text{Syntax Analyser}}
\underbrace{\text{Parse tree / AST}}_{\text{to semantic analysis}}
}
$$

**Top-down** methods (recursive descent, LL(1) table-driven) are intuitive and great for hand-written parsers. **Bottom-up** methods (SLR, LALR, CLR) are more powerful and form the basis of professional parser generators like YACC/Bison.
