### <span style="color:rgb(0, 112, 192)">1. Basics of Regex</span>

A regex is made up of _literals_ and _special characters_.

- **Literal characters**: Match the exact characters (e.g., `cat` matches "cat").
- **Special characters**: Used for defining patterns.

#### <span style="color:rgb(0, 176, 80)">Common Special Characters:</span>

| Character | Description                                                  | Example                                              |
| --------- | ------------------------------------------------------------ | ---------------------------------------------------- |
| `.`       | Matches **any character** except a newline                   | `c.t` matches "cat", "cut", "c4t"                    |
| `^`       | Matches the **start** of a string                            | `^Hello` matches "Hello world" but not "World Hello" |
| `$`       | Matches the **end** of a string                              | `world$` matches "Hello world" but not "world Hello" |
| `*`       | Matches **0 or more** repetitions of the preceding character | `ca*t` matches "ct", "cat", "caat"                   |
| `+`       | Matches **1 or more** repetitions                            | `ca+t` matches "cat", "caat" but not "ct"            |
| `?`       | Matches **0 or 1** of the preceding character                | `ca?t` matches "ct" or "cat"                         |
| `         | `                                                            | Logical OR                                           |

---

### <span style="color:rgb(0, 112, 192)"> 2. Character Classes</span>

Character classes define a set of characters you want to match.

|Character Class|Description|Example|
|---|---|---|
|`[abc]`|Matches **a**, **b**, or **c**|`b[aeiou]t` matches "bat", "bit", "but"|
|`[^abc]`|Matches **anything but** a, b, or c|`[^aeiou]` matches consonants|
|`[a-z]`|Matches **any lowercase letter**|`[a-z]` matches "a" to "z"|
|`[A-Z]`|Matches **any uppercase letter**|`[A-Z]` matches "A" to "Z"|
|`[0-9]`|Matches **any digit**|`[0-9]` matches "0" to "9"|
|`\d`|Matches **any digit** (same as `[0-9]`)|`\d\d` matches "12", "34"|
|`\w`|Matches **alphanumeric characters** (same as `[a-zA-Z0-9_]`)|`\w+` matches "word123"|
|`\s`|Matches **whitespace**|`\s+` matches spaces, tabs, etc.|

---

### <span style="color:rgb(0, 112, 192)">3. Quantifiers</span>

Quantifiers define how many times the preceding character or group must appear.

|Quantifier|Description|Example|
|---|---|---|
|`{n}`|Exactly **n** times|`\d{4}` matches "2024"|
|`{n,}`|**At least n** times|`\d{3,}` matches "123", "4567"|
|`{n,m}`|Between **n and m** times|`\d{2,4}` matches "12", "123", "1234"|

---

### <span style="color:rgb(0, 112, 192)">4. Grouping and Capturing</span>

You can group parts of a regex using parentheses `( )`.

- Grouping allows you to capture and reuse parts of the match.

|Feature|Description|Example|
|---|---|---|
|`( )`|Groups expressions|`(ab)+` matches "ababab"|
|`\1`|Refers to the **first captured group**|`(a)b\1` matches "aba"|

---

### <span style="color:rgb(0, 112, 192)">5. Anchors</span>

Anchors match positions in the string, rather than characters.

|Anchor|Description|Example|
|---|---|---|
|`^`|Start of a string|`^Hello` matches "Hello world"|
|`$`|End of a string|`world$` matches "Hello world"|
|`\b`|Word boundary|`\bcat\b` matches "cat" but not "cats"|

---

### <span style="color:rgb(0, 112, 192)">6. Escaping Special Characters</span>

To match special characters (like `.` or `*`), you need to escape them using a backslash (`\`).

|Character|Example Match|
|---|---|
|`\.`|Matches a literal period `.`|
|`\*`|Matches a literal asterisk `*`|

-----

### <span style="color:rgb(0, 112, 192)">7. Examples</span>

1. **Match an email**:
```less
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
```

2. **Match a phone number (e.g., (123) 456-7890 or 123-456-7890)**:
```less
(\(\d{3}\)\s|\d{3}-)\d{3}-\d{4}
```

3. **Match a date (e.g.,11-11-2011)**:
```less
\d{2}-\d{2}-\d{4}
```
