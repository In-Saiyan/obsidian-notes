# Lexical Analyser (Scanner)

The **Lexical Analyser** is the first phase of a compiler. It reads the raw source code as a stream of characters and converts it into a stream of **tokens** — the smallest meaningful units of the language.

---

## 1 Role of the Lexical Analyser

1. Read the input characters of the source program.
2. Group them into **lexemes** (meaningful character sequences).
3. Produce a **token** for each lexeme:
$$\langle \text{token-name},\; \text{attribute-value} \rangle$$
4. Strip out **whitespace** and **comments**.
5. Keep track of **line numbers** for error reporting.
6. Interact with the **symbol table** to store identifier information.

### 1.1 Why Separate Lexical Analysis from Syntax Analysis?

| Reason | Explanation |
|---|---|
| **Simplicity** | Separating concerns keeps both phases simpler. Syntax rules are context-free; lexical rules are regular. |
| **Efficiency** | Specialised buffering and look-ahead techniques can be applied at the character level. |
| **Portability** | Platform-specific character-set issues are isolated in the lexer. |

---

## 2 Key Terminology

| Term | Meaning |
|---|---|
| **Token** | A pair $\langle \text{name}, \text{value} \rangle$ — the category + optional attribute. |
| **Lexeme** | The actual character sequence in the source that matches a token pattern (e.g. `count`, `42`, `+`). |
| **Pattern** | A rule (usually a regex) describing the set of lexemes for a token (e.g. `[a-zA-Z_][a-zA-Z0-9_]*` for identifiers). |

Example with the statement `total = price + tax * 5`:

| Lexeme | Token |
|---|---|
| `total` | $\langle \text{id}, 1 \rangle$ |
| `=` | $\langle \text{assign\_op} \rangle$ |
| `price` | $\langle \text{id}, 2 \rangle$ |
| `+` | $\langle \text{add\_op} \rangle$ |
| `tax` | $\langle \text{id}, 3 \rangle$ |
| `*` | $\langle \text{mul\_op} \rangle$ |
| `5` | $\langle \text{num}, 5 \rangle$ |

---

## 3 Input Buffering

Reading one character at a time from disk is expensive. Lexers use a **buffer pair** scheme:

```
┌───────────────────────┬───────────────────────┐
│      Buffer 1 (N)     │      Buffer 2 (N)     │
└───────────────────────┴───────────────────────┘
         ↑ lexemeBegin         ↑ forward
```

- Two buffers of size $N$ (typically 4096 bytes).
- **`lexemeBegin`** — marks the start of the current lexeme.
- **`forward`** — scans ahead to find the end.
- When `forward` reaches the end of one buffer, refill the other.

### 3.1 Sentinel Technique

Place a special **sentinel** character (e.g. `EOF`) at the end of each buffer so that the inner loop only needs **one** test per character instead of two (end-of-buffer + actual character).

---

## 4 Specification of Tokens — Regular Expressions

Tokens are specified using **regular expressions** (regex).

### 4.1 Operations on Languages

| Operation | Notation | Meaning |
|---|---|---|
| Union | $L \cup M$ | $\{s \mid s \in L \text{ or } s \in M\}$ |
| Concatenation | $LM$ | $\{st \mid s \in L, t \in M\}$ |
| Kleene Closure | $L^*$ | $\bigcup_{i=0}^{\infty} L^i$ |
| Positive Closure | $L^+$ | $\bigcup_{i=1}^{\infty} L^i$ |

### 4.2 Common Token Patterns

| Token | Pattern (Regex) |
|---|---|
| **Identifier** | `[a-zA-Z_][a-zA-Z0-9_]*` |
| **Integer literal** | `[0-9]+` |
| **Float literal** | `[0-9]+\.[0-9]+([eE][+-]?[0-9]+)?` |
| **String literal** | `"[^"]*"` |
| **Relational op** | `<  \|  >  \|  <=  \|  >=  \|  ==  \|  !=` |

### 4.3 Regular Definitions

A **regular definition** gives names to regular expressions for readability:

$$
\begin{aligned}
\text{letter} &\rightarrow [A\text{-}Za\text{-}z] \\
\text{digit}  &\rightarrow [0\text{-}9] \\
\text{id}     &\rightarrow \text{letter}(\text{letter} \mid \text{digit})^*
\end{aligned}
$$

---

## 5 Finite Automata — The Engine Behind the Lexer

Regular expressions are converted into **Finite Automata** for efficient pattern matching.

### 5.1 NFA (Non-deterministic Finite Automaton)

- Can have **multiple transitions** on the same input symbol.
- Can have **ε (epsilon) transitions** (moves without consuming input).
- Formally: $NFA = (Q, \Sigma, \delta, q_0, F)$

### 5.2 DFA (Deterministic Finite Automaton)

- Exactly **one** transition per symbol from every state.
- **No** epsilon transitions.
- Faster execution but potentially more states.
- Formally: $DFA = (Q, \Sigma, \delta, q_0, F)$

### 5.3 Conversion Pipeline

$$
\text{Regex} \xrightarrow{\text{Thompson's}} \text{NFA} \xrightarrow{\text{Subset Construction}} \text{DFA} \xrightarrow{\text{Minimisation}} \text{Minimal DFA}
$$

### 5.4 Thompson's Construction (Regex → NFA)

Build small NFAs for base cases and combine them:

**Base:** Single character $a$
```
 (start) --a--> (accept)
```

**Union:** $r_1 | r_2$
```
          ε --> [NFA for r1] --ε--\
(start) -<                         >--> (accept)
          ε --> [NFA for r2] --ε--/
```

**Concatenation:** $r_1 r_2$
```
(start) --> [NFA for r1] --> [NFA for r2] --> (accept)
```

**Kleene Star:** $r^*$
```
          ε --> [NFA for r] --ε--\
(start) -<         ↑___ε____|     >--> (accept)
          ε ─────────────────────/
```

### 5.5 Subset Construction (NFA → DFA)

1. Compute **ε-closure** of the start state → this is the DFA start state.
2. For each DFA state $S$ and input symbol $a$:
   - Compute $\text{move}(S, a)$ — the set of NFA states reachable on $a$.
   - Compute $\varepsilon\text{-closure}(\text{move}(S, a))$ → new DFA state.
3. Repeat until no new DFA states are generated.
4. A DFA state is **accepting** if it contains any NFA accepting state.

### 5.6 DFA Minimisation (Hopcroft's Algorithm)

1. Partition states into **accepting** and **non-accepting** groups.
2. Repeatedly split groups: if two states in the same group transition to *different* groups on some input, they must be separated.
3. Continue until no more splits are possible.
4. Each final group becomes one state in the **minimal DFA**.

---

## 6 Implementation of a Lexer

### 6.1 Hand-Coded Lexer in C

```c
#include <stdio.h>
#include <ctype.h>
#include <string.h>

typedef enum {
    TOK_INT, TOK_FLOAT, TOK_ID, TOK_KEYWORD,
    TOK_ASSIGN, TOK_PLUS, TOK_MINUS, TOK_STAR, TOK_SLASH,
    TOK_LPAREN, TOK_RPAREN, TOK_SEMI,
    TOK_EQ, TOK_NEQ, TOK_LT, TOK_GT, TOK_LE, TOK_GE,
    TOK_NUM, TOK_EOF, TOK_UNKNOWN
} TokenType;

typedef struct {
    TokenType type;
    char      lexeme[256];
} Token;

/* --- keyword table --- */
const char *keywords[] = {
    "if", "else", "while", "return", "int", "float", "void", NULL
};

int is_keyword(const char *s) {
    for (int i = 0; keywords[i]; i++)
        if (strcmp(s, keywords[i]) == 0) return 1;
    return 0;
}

/* --- The Lexer --- */
typedef struct {
    const char *src;   /* source string  */
    int         pos;   /* current index  */
    int         line;  /* line number    */
} Lexer;

void lexer_init(Lexer *l, const char *source) {
    l->src  = source;
    l->pos  = 0;
    l->line = 1;
}

static char peek(Lexer *l)    { return l->src[l->pos]; }
static char advance(Lexer *l) { return l->src[l->pos++]; }

static void skip_whitespace_and_comments(Lexer *l) {
    while (1) {
        char c = peek(l);
        if (c == ' ' || c == '\t' || c == '\r') {
            advance(l);
        } else if (c == '\n') {
            advance(l);
            l->line++;
        } else if (c == '/' && l->src[l->pos + 1] == '/') {
            /* single-line comment */
            while (peek(l) != '\n' && peek(l) != '\0')
                advance(l);
        } else if (c == '/' && l->src[l->pos + 1] == '*') {
            /* multi-line comment */
            advance(l); advance(l);
            while (!(peek(l) == '*' && l->src[l->pos + 1] == '/')) {
                if (peek(l) == '\n') l->line++;
                if (peek(l) == '\0') break;
                advance(l);
            }
            advance(l); advance(l); /* skip closing * / */
        } else {
            break;
        }
    }
}

Token next_token(Lexer *l) {
    Token tok;
    tok.lexeme[0] = '\0';

    skip_whitespace_and_comments(l);

    char c = peek(l);

    /* --- end of file --- */
    if (c == '\0') {
        tok.type = TOK_EOF;
        strcpy(tok.lexeme, "EOF");
        return tok;
    }

    /* --- numbers (integer or float) --- */
    if (isdigit(c)) {
        int i = 0;
        while (isdigit(peek(l)))
            tok.lexeme[i++] = advance(l);

        if (peek(l) == '.') {               /* fractional part */
            tok.lexeme[i++] = advance(l);
            while (isdigit(peek(l)))
                tok.lexeme[i++] = advance(l);
            tok.type = TOK_FLOAT;
        } else {
            tok.type = TOK_NUM;
        }
        tok.lexeme[i] = '\0';
        return tok;
    }

    /* --- identifiers and keywords --- */
    if (isalpha(c) || c == '_') {
        int i = 0;
        while (isalnum(peek(l)) || peek(l) == '_')
            tok.lexeme[i++] = advance(l);
        tok.lexeme[i] = '\0';
        tok.type = is_keyword(tok.lexeme) ? TOK_KEYWORD : TOK_ID;
        return tok;
    }

    /* --- two-character operators --- */
    char next = l->src[l->pos + 1];

    if (c == '=' && next == '=') {
        tok.type = TOK_EQ;
        strcpy(tok.lexeme, "==");
        advance(l); advance(l);
        return tok;
    }
    if (c == '!' && next == '=') {
        tok.type = TOK_NEQ;
        strcpy(tok.lexeme, "!=");
        advance(l); advance(l);
        return tok;
    }
    if (c == '<' && next == '=') {
        tok.type = TOK_LE;
        strcpy(tok.lexeme, "<=");
        advance(l); advance(l);
        return tok;
    }
    if (c == '>' && next == '=') {
        tok.type = TOK_GE;
        strcpy(tok.lexeme, ">=");
        advance(l); advance(l);
        return tok;
    }

    /* --- single-character tokens --- */
    advance(l);
    tok.lexeme[0] = c;
    tok.lexeme[1] = '\0';

    switch (c) {
        case '=': tok.type = TOK_ASSIGN; break;
        case '+': tok.type = TOK_PLUS;   break;
        case '-': tok.type = TOK_MINUS;  break;
        case '*': tok.type = TOK_STAR;   break;
        case '/': tok.type = TOK_SLASH;  break;
        case '(': tok.type = TOK_LPAREN; break;
        case ')': tok.type = TOK_RPAREN; break;
        case ';': tok.type = TOK_SEMI;   break;
        case '<': tok.type = TOK_LT;     break;
        case '>': tok.type = TOK_GT;     break;
        default:  tok.type = TOK_UNKNOWN; break;
    }
    return tok;
}

/* --- Driver --- */
int main(void) {
    const char *code =
        "int main() {\n"
        "    float rate = 3.14;\n"
        "    int x = rate * 60; // compute\n"
        "    if (x >= 100) return x;\n"
        "}\n";

    printf("Source:\n%s\n--- Tokens ---\n", code);

    Lexer lex;
    lexer_init(&lex, code);

    Token t;
    do {
        t = next_token(&lex);
        printf("%-12s  ->  %s\n", t.lexeme,
            (const char *[]){
                "INT","FLOAT","ID","KEYWORD",
                "ASSIGN","PLUS","MINUS","STAR","SLASH",
                "LPAREN","RPAREN","SEMI",
                "EQ","NEQ","LT","GT","LE","GE",
                "NUM","EOF","UNKNOWN"
            }[t.type]);
    } while (t.type != TOK_EOF);

    return 0;
}
```

### 6.2 Using a Lexer Generator — Lex / Flex

Instead of hand-coding, you can describe token patterns in a `.l` file and let **Flex** generate the C code.

```lex
/* scanner.l */
%{
#include <stdio.h>
%}

DIGIT    [0-9]
LETTER   [a-zA-Z_]
ID       {LETTER}({LETTER}|{DIGIT})*
NUMBER   {DIGIT}+(\.{DIGIT}+)?

%%

"if"        { printf("KEYWORD: %s\n", yytext);  }
"else"      { printf("KEYWORD: %s\n", yytext);  }
"while"     { printf("KEYWORD: %s\n", yytext);  }
"return"    { printf("KEYWORD: %s\n", yytext);  }
"int"       { printf("KEYWORD: %s\n", yytext);  }
"float"     { printf("KEYWORD: %s\n", yytext);  }
{ID}        { printf("ID: %s\n",      yytext);  }
{NUMBER}    { printf("NUMBER: %s\n",   yytext);  }
"=="        { printf("OP: EQ\n");                }
"!="        { printf("OP: NEQ\n");               }
"<="        { printf("OP: LE\n");                }
">="        { printf("OP: GE\n");                }
[+\-*/=<>(){}; ] { printf("SYM: %s\n", yytext); }
\n          { /* skip newlines */ }
.           { printf("UNKNOWN: %s\n", yytext);   }

%%

int yywrap() { return 1; }
int main() { yylex(); return 0; }
```

Build and run:
```bash
flex scanner.l
gcc lex.yy.c -o scanner -lfl
echo "int x = 42 + y;" | ./scanner
```

---

## 7 Error Recovery in Lexical Analysis

| Strategy | Description |
|---|---|
| **Panic mode** | Delete characters from the remaining input until a well-formed token is found. |
| **Delete one character** | Remove the offending character, try again. |
| **Insert a missing character** | e.g. insert a closing `"` for an unterminated string. |
| **Replace a character** | Swap the illegal character with a legal one. |
| **Transpose** | Swap two adjacent characters (`fi` → `if`). |

The lexer should aim to report the error, recover, and continue scanning so that subsequent errors can also be found in a single pass.

---

## 8 Symbol Table Interaction

The lexer does **not** fully build the symbol table, but it **initiates entries**:

1. When an identifier lexeme is seen for the first time → insert it into the symbol table, get an index $i$.
2. Produce $\langle \text{id}, i \rangle$.
3. Later phases (semantic analysis) fill in type, scope, memory location, etc.

The symbol table is typically implemented as a **hash table** for $O(1)$ average look-up.

---

## 9 Summary

$$
\boxed{
\text{Source chars} \xrightarrow{\text{Lexer}} \text{Token stream} \xrightarrow{\text{Parser}} \text{Parse tree}
}
$$

The lexical analyser converts a character stream into a token stream by:
1. **Specifying** token patterns with regular expressions.
2. **Recognising** patterns using finite automata (NFA/DFA).
3. **Implementing** via hand-coded scanners or generator tools (Lex/Flex).
4. **Handling** whitespace, comments, errors, and symbol table interaction.
