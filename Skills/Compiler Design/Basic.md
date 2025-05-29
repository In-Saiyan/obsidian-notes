# 1	Compilation
## 1.1	Parts of a Compiler:
1. Preprocessor
2. Compiler
3. Assembler
4. Linker
5. Loader

![[Pasted image 20250529141750.png]]

## 1.2	Stages of Compilation


![[Pasted image 20250529144127.png]]

## 1.3	Lexical Analysis
This is the first phase of a compilation process, this is also called _scanning_. The *lexical analyzer* or *lexer* reads the stream of the source program. It groups the characters into meaningful sequences known as *lexems*. For each *lexeme* lexer produces an output called *token* of the form: 
$$<token-name,attribute-value>$$
this is passed onto for the subsequent phases, like *syntax analysis*.

Here the $token-name$ is an abstract symbol used during syntax analysis, and the $attribute-value$ points to a value in the symbol table for the particular entry.

for ex:
```
position = initial + rate * 60
```
here the tokens generated would be like:
$$<id,1>,<=>,<id,2>,<+>,<id,3>,<*>,<60>$$
here $id$ stands for identifier. and the operators don't need any value since they are pretty self explanatory. And the literal 60 is also a pretty self explanatory thing.

Here +, * , = are abstract symbols.



