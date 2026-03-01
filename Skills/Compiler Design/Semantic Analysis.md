# Semantic Analysis

**Semantic analysis** is the third phase of a compiler. It uses the AST from the [[Syntax Analyser]] along with the **symbol table** to check whether the program is meaningful — i.e. that it follows the language's **type rules**, **scope rules**, and other context-sensitive constraints that cannot be captured by a context-free grammar.

$$
\text{AST} \xrightarrow{\text{Semantic Analyser}} \text{Annotated AST (with types, coercions, resolved references)}
$$

---

## 1 Tasks of Semantic Analysis

| Task | Description |
|---|---|
| **Type checking** | Ensure operators and functions receive operands of compatible types. |
| **Type coercion** | Insert implicit conversions (e.g. `int` → `float`) where the language allows. |
| **Scope resolution** | Verify that every identifier is declared, resolve which declaration a name refers to. |
| **Flow-of-control checks** | `break` only inside loops, `return` in every path of a non-void function, etc. |
| **Uniqueness checks** | No duplicate declarations in the same scope, no duplicate case labels, etc. |
| **Array bounds (static)** | If array size is a constant, check that constant indices are in range. |

---

## 2 Type Systems

### 2.1 Basic Types

Most languages provide:
- **Primitive types:** `int`, `float`, `char`, `bool`, `void`
- **Constructed types:** arrays `T[n]`, pointers `T*`, records/structs, functions $T_1 \times T_2 \rightarrow T_r$

### 2.2 Type Equivalence

| Kind | Rule |
|---|---|
| **Structural equivalence** | Two types are equal if they have the same structure (e.g. C arrays). |
| **Name equivalence** | Two types are equal only if they have the same name (e.g. Ada, Pascal). |

Example — in C:
```c
typedef struct { int x; int y; } Point;
typedef struct { int x; int y; } Coord;
```
Under **structural equivalence**, `Point ≡ Coord`. Under **name equivalence**, `Point ≢ Coord`.

### 2.3 Type Compatibility & Coercion (Widening)

Languages often allow **implicit widening**:
$$\text{char} \rightarrow \text{int} \rightarrow \text{long} \rightarrow \text{float} \rightarrow \text{double}$$

When an operator has mixed types, the "narrower" operand is coerced:
```c
float x = 3 + 2.5;   // 3 is coerced to 3.0, result is 5.5
```

The semantic analyser inserts an explicit conversion node in the AST:
```
    +
   / \
 intToFloat  2.5
   |
   3
```

### 2.4 Type Checking Rules (Examples)

For an expression $E_1 \;\text{op}\; E_2$:

$$
\text{type}(E_1 + E_2) =
\begin{cases}
\text{int}   & \text{if } \text{type}(E_1) = \text{int} \wedge \text{type}(E_2) = \text{int} \\
\text{float} & \text{if either operand is float (coerce the other)} \\
\text{error} & \text{otherwise}
\end{cases}
$$

For assignment $\text{id} = E$:
- $\text{type}(E)$ must be **assignment-compatible** with $\text{type}(\text{id})$.
- Widening is usually allowed; narrowing may produce a warning.

For function calls $f(a_1, a_2, \ldots, a_n)$:
- Number of arguments must match.
- $\text{type}(a_i)$ must be compatible with the $i$-th parameter type.

---

## 3 Syntax-Directed Definitions (SDDs)

An SDD attaches **semantic rules** (attribute computations) to grammar productions. This is the formal framework used to implement semantic analysis.

### 3.1 Attributes

| Kind | Direction | Example |
|---|---|---|
| **Synthesised** | Bottom-up (child → parent) | `E.type`, `E.val` |
| **Inherited** | Top-down (parent/sibling → child) | `T.inh_type` in declarations |

### 3.2 S-Attributed vs L-Attributed Definitions

| Type | Allowed Attributes | Evaluation Order |
|---|---|---|
| **S-attributed** | Only synthesised | Any bottom-up traversal (post-order) |
| **L-attributed** | Synthesised + inherited (from left siblings / parent only) | Single left-to-right depth-first traversal |

Every S-attributed SDD is also L-attributed.

### 3.3 Example: Type-Checking SDD for Expressions

Grammar with semantic rules:

| Production | Semantic Rule |
|---|---|
| $E \rightarrow E_1 + T$ | `E.type = if (E1.type == int && T.type == int) then int else if (E1.type == float || T.type == float) then float else error` |
| $E \rightarrow T$ | `E.type = T.type` |
| $T \rightarrow T_1 * F$ | `T.type = if (T1.type == int && F.type == int) then int else if (T1.type == float || F.type == float) then float else error` |
| $T \rightarrow F$ | `T.type = F.type` |
| $F \rightarrow ( E )$ | `F.type = E.type` |
| $F \rightarrow \textbf{num}_{int}$ | `F.type = int` |
| $F \rightarrow \textbf{num}_{float}$ | `F.type = float` |
| $F \rightarrow \textbf{id}$ | `F.type = lookup(id.lexeme).type` |

---

## 4 Syntax-Directed Translation Schemes (SDTs)

An **SDT** embeds semantic **actions** (code fragments) within the grammar rules, indicating *when* during parsing the action should execute.

```
E → E1 + T    { E.type = check_add(E1.type, T.type); }
```

In a **bottom-up parser**, actions at the end of a production execute on reduction.
In a **top-down parser**, actions can be placed anywhere (for L-attributed SDDs).

---

## 5 Attribute Grammars — Evaluated Example

### 5.1 Declaration Processing

Grammar:
$$
\begin{aligned}
D &\rightarrow T \; L \; ; \\
T &\rightarrow \textbf{int} \mid \textbf{float} \\
L &\rightarrow L , \textbf{id} \mid \textbf{id}
\end{aligned}
$$

SDD (using inherited attribute `L.inh`):

| Production | Rules |
|---|---|
| $D \rightarrow T \; L \; ;$ | `L.inh = T.type` |
| $T \rightarrow \textbf{int}$ | `T.type = int` |
| $T \rightarrow \textbf{float}$ | `T.type = float` |
| $L \rightarrow L_1 , \textbf{id}$ | `L1.inh = L.inh; addType(id.lexeme, L.inh)` |
| $L \rightarrow \textbf{id}$ | `addType(id.lexeme, L.inh)` |

For `int a, b, c;`:
1. $T \rightarrow \textbf{int}$ → `T.type = int`.
2. $D$ passes `L.inh = int`.
3. Each `id` in the list gets `addType(name, int)` → stored in the symbol table.

---

## 6 Scope Checking Implementation

```c
/* --- Scope stack using chained hash tables --- */

#define TABLE_SIZE 211

typedef struct Symbol {
    char            name[64];
    char            type[32];
    int             scope_level;
    struct Symbol  *next;       /* chain in hash bucket */
} Symbol;

typedef struct Scope {
    Symbol        *table[TABLE_SIZE];
    struct Scope  *parent;
    int            level;
} Scope;

Scope *current_scope = NULL;

unsigned hash(const char *s) {
    unsigned h = 0;
    while (*s) h = h * 31 + *s++;
    return h % TABLE_SIZE;
}

/* Enter a new scope */
void push_scope(void) {
    Scope *s = calloc(1, sizeof(Scope));
    s->parent = current_scope;
    s->level  = current_scope ? current_scope->level + 1 : 0;
    current_scope = s;
}

/* Exit the current scope */
void pop_scope(void) {
    Scope *s = current_scope;
    current_scope = s->parent;
    /* free symbols in s ... */
    free(s);
}

/* Declare a symbol in the current scope */
int declare(const char *name, const char *type) {
    unsigned h = hash(name);
    /* check for duplicate in current scope */
    for (Symbol *p = current_scope->table[h]; p; p = p->next)
        if (strcmp(p->name, name) == 0)
            return 0;  /* error: already declared */
    Symbol *sym = malloc(sizeof(Symbol));
    strcpy(sym->name, name);
    strcpy(sym->type, type);
    sym->scope_level = current_scope->level;
    sym->next = current_scope->table[h];
    current_scope->table[h] = sym;
    return 1;
}

/* Look up a symbol (innermost scope first) */
Symbol *lookup(const char *name) {
    for (Scope *s = current_scope; s; s = s->parent) {
        unsigned h = hash(name);
        for (Symbol *p = s->table[h]; p; p = p->next)
            if (strcmp(p->name, name) == 0)
                return p;
    }
    return NULL;  /* undeclared */
}
```

Usage during semantic analysis:
```c
push_scope();                       /* enter function body */
declare("x", "int");
declare("rate", "float");

Symbol *s = lookup("rate");         /* found in current scope */
Symbol *g = lookup("globalVar");    /* found in outer scope  */
Symbol *u = lookup("undefined");    /* NULL → semantic error */

pop_scope();                        /* exit function body */
```

---

## 7 Full Semantic Analyser Example (AST Type-Checking)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ---- AST Node ---- */
typedef enum { NODE_NUM, NODE_ID, NODE_BINOP, NODE_ASSIGN } NodeKind;
typedef enum { TYPE_INT, TYPE_FLOAT, TYPE_ERROR } Type;

typedef struct ASTNode {
    NodeKind kind;
    Type     type;          /* filled by semantic analysis */

    /* NODE_NUM */
    double   num_val;
    int      is_float_lit;

    /* NODE_ID */
    char     name[64];

    /* NODE_BINOP */
    char     op;            /* '+', '-', '*', '/' */
    struct ASTNode *left;
    struct ASTNode *right;
} ASTNode;

/* ---- Symbol table (simplified flat) ---- */
typedef struct { char name[64]; Type type; } SymEntry;
SymEntry symtab[100];
int sym_count = 0;

void sym_add(const char *name, Type t) {
    strcpy(symtab[sym_count].name, name);
    symtab[sym_count].type = t;
    sym_count++;
}

Type sym_lookup(const char *name) {
    for (int i = 0; i < sym_count; i++)
        if (strcmp(symtab[i].name, name) == 0)
            return symtab[i].type;
    printf("Semantic error: '%s' undeclared\n", name);
    return TYPE_ERROR;
}

/* ---- Coercion helper ---- */
Type check_arithmetic(Type a, Type b) {
    if (a == TYPE_ERROR || b == TYPE_ERROR) return TYPE_ERROR;
    if (a == TYPE_FLOAT || b == TYPE_FLOAT) return TYPE_FLOAT;
    return TYPE_INT;
}

/* ---- Semantic Analysis (recursive AST walk) ---- */
Type analyse(ASTNode *n) {
    if (!n) return TYPE_ERROR;

    switch (n->kind) {
        case NODE_NUM:
            n->type = n->is_float_lit ? TYPE_FLOAT : TYPE_INT;
            break;

        case NODE_ID:
            n->type = sym_lookup(n->name);
            break;

        case NODE_BINOP: {
            Type lt = analyse(n->left);
            Type rt = analyse(n->right);
            n->type = check_arithmetic(lt, rt);
            if (n->type == TYPE_FLOAT) {
                /* mark coercions needed */
                if (lt == TYPE_INT)
                    printf("  [coerce] left of '%c' : int -> float\n", n->op);
                if (rt == TYPE_INT)
                    printf("  [coerce] right of '%c' : int -> float\n", n->op);
            }
            break;
        }

        case NODE_ASSIGN: {
            Type lt = analyse(n->left);   /* must be an id */
            Type rt = analyse(n->right);
            if (lt == TYPE_ERROR || rt == TYPE_ERROR) {
                n->type = TYPE_ERROR;
            } else if (lt == TYPE_INT && rt == TYPE_FLOAT) {
                printf("  [warning] narrowing: float assigned to int '%s'\n",
                       n->left->name);
                n->type = lt;
            } else {
                n->type = lt;
            }
            break;
        }
    }
    return n->type;
}

const char *type_name(Type t) {
    return (const char *[]){"int","float","error"}[t];
}

/* ---- Demo ---- */
int main(void) {
    /* Simulate: int position; float rate; float initial;
     *           position = initial + rate * 60;           */

    sym_add("position", TYPE_INT);
    sym_add("initial",  TYPE_FLOAT);
    sym_add("rate",     TYPE_FLOAT);

    /* Build AST for: position = initial + rate * 60 */
    ASTNode n60      = { .kind=NODE_NUM, .num_val=60, .is_float_lit=0 };
    ASTNode nRate    = { .kind=NODE_ID,  .name="rate" };
    ASTNode nMul     = { .kind=NODE_BINOP, .op='*', .left=&nRate, .right=&n60 };
    ASTNode nInitial = { .kind=NODE_ID,  .name="initial" };
    ASTNode nAdd     = { .kind=NODE_BINOP, .op='+', .left=&nInitial, .right=&nMul };
    ASTNode nPos     = { .kind=NODE_ID,  .name="position" };
    ASTNode nAssign  = { .kind=NODE_ASSIGN, .left=&nPos, .right=&nAdd };

    printf("Semantic analysis of: position = initial + rate * 60\n\n");
    Type result = analyse(&nAssign);
    printf("\nResult type of assignment: %s\n", type_name(result));

    return 0;
}
```

Output:
```
Semantic analysis of: position = initial + rate * 60

  [coerce] right of '*' : int -> float
  [warning] narrowing: float assigned to int 'position'

Result type of assignment: int
```

---

## 8 Summary

| What | How |
|---|---|
| **Type checking** | Walk the AST bottom-up; compute types using synthesis rules |
| **Scope resolution** | Stack of hash tables; look up from innermost to outermost |
| **Coercions** | Insert conversion nodes where the language allows widening |
| **Framework** | Syntax-Directed Definitions (SDD) / Translation Schemes (SDT) |
| **Attribute kinds** | Synthesised (bottom-up) and Inherited (top-down / left-to-right) |

$$
\boxed{
\text{AST}
\xrightarrow{\text{Type checking + Scope resolution}}
\text{Annotated AST}
\xrightarrow{\text{next phase}}
\text{Intermediate Code}
}
$$
