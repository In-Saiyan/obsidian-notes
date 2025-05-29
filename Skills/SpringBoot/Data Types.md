## Primitive Vs Non Primitive Data Types
Primitive data types are usually stored on the memory stack and are faster.

# Primitive and Non Primitive data types in Java
![[Pasted image 20250525163932.png]]

## Primitive
|Type|Description|Default|Size|Example Literals|Range of values|
|---|---|---|---|---|---|
|boolean|true or false|false|JVM-dependent (typically 1 byte)|true, false|true, false|
|byte|8-bit signed integer|0|1 byte|(none)|-128 to 127|
|char|Unicode character(16 bit)|\u0000|2 bytes|'a', '\u0041', '\101', '\\', '\', '\n', 'β'|0 to 65,535 (unsigned)|
|short|16-bit signed integer|0|2 bytes|(none)|-32,768 to 32,767|
|int|32-bit signed integer|0|4 bytes|-2,0,1|-2,147,483,648<br><br>to<br><br>2,147,483,647|
|long|64-bit signed integer|0L|8 bytes|-2L,0L,1L|-9,223,372,036,854,775,808<br><br>to<br><br>9,223,372,036,854,775,807|
|float|32-bit IEEE 754 floating-point|0.0f|4 bytes|3.14f, -1.23e-10f|~6-7 significant decimal digits|
|double|64-bit IEEE 754 floating-point|0.0d|8 bytes|3.1415d, 1.23e100d|~15-16 significant decimal digits|
## Non-primitive data types java
Non primitive data types in java hold the references to the actual object that needs to be accessed, such data is stored in the heap memory as opposed to the storage in the stack memory that happens with primitive data types. They basically work like pointers to the actual data but with another layer of abstraction.

### Main Types of non-primitive data types in java:

#### Arrays
Collections of elements of same types stored in contiguous memory locations.

#### Classes
User-defined blueprints for creating objects that contain fields and methods representing object behavior. They can be either user-defined or already predefined.

#### Interfaces
Abstract types that define contracts for classes to implement, specifying method signatures that implementing classes must provide

#### Strings
Sequences of characters stored as objects. Unlike primitive types, strings can utilize methods for manipulation and are enclosed in double quotes.

#### Enums 
Fixed sets of named constants that improve code readability and type safety.

### Difference between int and Integer.
## Storage and Memory
**int** stores the actual binary value directly in memory and occupies 32 bits (4 bytes). **Integer** is an object that wraps an int value and requires 128 bits (16 bytes) due to object overhead[](https://www.tutorialspoint.com/difference-between-an-integer-and-int-in-java)

## Functionality Differences

**int** cannot have methods called on it since it's not a class. You cannot use `int.parseInt("1")` because int has no methods

 **Integer** provides numerous static and instance methods for conversion, manipulation, and utility operations like `Integer.parseInt("1")`, `toBinaryString()`, `toHexString()`, and comparison methods


## Object-Oriented Features

**int** cannot be used in generic collections, cannot be compared using `.equals()`, and doesn't support inheritance since it's not an object

 **Integer** can be used in collections, supports `.equals()` comparison, can be assigned null, and inherits from Object class

## Autoboxing and Unboxing

Java provides automatic conversion between int and Integer through autoboxing (primitive to wrapper) and unboxing (wrapper to primitive). This allows `Integer n = 9;` to work automatically since Java 5

## Performance Considerations

**int** operations are faster due to direct memory access and no object creation overhead. **Integer** involves object creation and method calls, making it slightly slower but more flexible for complex operations

The choice between int and Integer depends on whether you need basic numeric storage (use int) or require object features like methods, null values, or collection compatibility (use Integer).

## Java type casting
There is two types of type-casting allowed in Java:
### Widening
`byte` -> `short` -> `char` -> `int` -> `long` -> `float` -> `double`

### Narrowing
`double` -> `float` -> `long` -> `int` -> `char` -> `short` -> `byte`

Other common escape sequences that are valid in Java are:


## Escape Sequences

| Escape Sequence | Name            |
| --------------- | --------------- |
| \n              | New Line        |
| \r              | Carriage Return |
| \t              | Tab             |
| \b              | Backspace       |
| \f              | Form Feed       |
