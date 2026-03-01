# Access Modifiers and Member Variable Scope
| Modifier      | Same Class | Same Package | Subclass (Different Package) | Different Package (Non-subclass) | Keyword Required |
| ------------- | ---------- | ------------ | ---------------------------- | -------------------------------- | ---------------- |
| public    | ✓          | ✓            | ✓                            | ✓                                | `public`         |
| protected | ✓          | ✓            | ✓                            | ✗                                | `protected`      |
| default   | ✓          | ✓            | ✗                            | ✗                                | No keyword       |
| private   | ✓          | ✗            | ✗                            | ✗                                | `private`        |

Access modifiers control the visibility and accessibility of code elements

## For Classes
Classes can use either **public** or **default** access

- **public**: The class is accessible by any other class
- **default**: The class is only accessible by classes in the same package (used when no modifier is specified)

## For Attributes, Methods, and Constructors
Four access levels are available

- **public**: Code is accessible for all classes
- **private**: Code is only accessible within the declared class
- **default**: Code is only accessible in the same package (no modifier specified)
- **protected**: Code is accessible in the same package and subclasses

## Non-Access Modifiers
Non-access modifiers provide functionality beyond access control

## For Classes
- **final**: The class cannot be inherited by other classes
- **abstract**: The class cannot be used to create objects and must be inherited

## For Attributes and Methods

- **final**: Attributes and methods cannot be overridden or modified
- **static**: Attributes and methods belong to the class rather than an object
- **abstract**: Can only be used in abstract classes for methods without a body
- **transient**: Attributes and methods are skipped during serialization
- **synchronized**: Methods can only be accessed by one thread at a time
- **volatile**: Attribute values are not cached thread-locally and always read from main memory


## Key Examples

**Final modifier** prevents modification of values - attempting to change a final variable generates an error

**Static methods** can be called without creating objects, unlike public methods which require object instantiation

**Abstract methods** belong to abstract classes and have no body - the implementation is provided by subclasses

These modifiers enable proper encapsulation, inheritance control, and thread safety in Java applications.

## Access Level Hierarchy

From most restrictive to least restrictive
> private < default < protected < public

## Key Characteristics

**Public**: Most accessible modifier - visible everywhere in the application
**Protected**: Accessible within same package and by subclasses in other packages
**Default (Package-private)**: No keyword required - accessible only within the same package
**Private**: Most restrictive - accessible only within the declaring class