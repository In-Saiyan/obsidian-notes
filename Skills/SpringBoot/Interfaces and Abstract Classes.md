Java provides two powerful mechanisms for achieving abstraction: abstract classes and interfaces. Both serve as blueprints for other classes but have distinct characteristics and use cases.

## Abstract Classes

An abstract class is a class declared with the `abstract` keyword that cannot be instantiated directly. It serves as a template for subclasses and can contain both abstract methods (without implementation) and concrete methods (with implementation)

## Key Characteristics of Abstract Classes

Abstract classes can have constructors, instance variables, static methods, and methods with any access modifier (private, protected, public)

They must be extended using the `extends` keyword, and subclasses must implement all abstract methods unless the subclass is also declared abstract

## Example of Abstract Class
```java
interface Flyable {
    // Implicitly public, static, final
    int MAX_ALTITUDE = 50000;
    
    // Abstract method
    void fly();
    
    // Default method (Java 8+)
    default void land() {
        System.out.println("Landing safely");
    }
}

interface Swimmable {
    void swim();
}

class Duck implements Flyable, Swimmable {
    @Override
    public void fly() {
        System.out.println("Duck is flying");
    }
    
    @Override
    public void swim() {
        System.out.println("Duck is swimming");
    }
}

```

## Interfaces
An interface is a reference type that defines a contract of methods that implementing classes must provide. All methods in an interface are implicitly public and abstract (except default and static methods introduced in Java 8)

## Key Characteristics of Interfaces

Interfaces cannot have constructors or instance variables. All fields are implicitly public, static, and final. Classes implement interfaces using the `implements` keyword and can implement multiple interfaces simultaneously

## Example of Interface

```java
interface Flyable {
    // Implicitly public, static, final
    int MAX_ALTITUDE = 50000;
    
    // Abstract method
    void fly();
    
    // Default method (Java 8+)
    default void land() {
        System.out.println("Landing safely");
    }
}

interface Swimmable {
    void swim();
}

class Duck implements Flyable, Swimmable {
    @Override
    public void fly() {
        System.out.println("Duck is flying");
    }
    
    @Override
    public void swim() {
        System.out.println("Duck is swimming");
    }
}

```

## Key Differences Between Abstract Classes and Interfaces

|Aspect|Abstract Class|Interface|
|---|---|---|
|**Declaration**|`abstract class ClassName`|`interface InterfaceName`|
|**Methods**|Can have abstract and concrete methods|All methods abstract by default (except default/static)|
|**Variables**|Can have instance variables with any access modifier|Only public, static, final fields|
|**Constructors**|Can have constructors|Cannot have constructors|
|**Inheritance**|Single inheritance (extends one class)|Multiple inheritance (implements multiple interfaces)|
|**Access Modifiers**|Methods can be private, protected, public|Methods implicitly public|
|**Implementation**|Subclass uses `extends` keyword|Class uses `implements` keyword|
|**Instantiation**|Cannot be instantiated|Cannot be instantiated|

## When to Use Abstract Classes vs Interfaces

**Use Abstract Classes when:**

- You want to share common functionality among related classes
- You need to provide default implementations for some methods
- You want to define non-public methods or instance variables
- Classes are closely related and share a common base

**Use Interfaces when:**
- You want to specify a contract that unrelated classes can implement
- You need multiple inheritance capabilities
- You want to achieve loose coupling between classes
- You're defining capabilities that can be mixed and matched

## Practical Example Combining Both
```java
// Interface defining a contract
interface Drawable {
    void draw();
}

// Abstract class providing common functionality
abstract class Shape implements Drawable {
    protected String color;
    
    public Shape(String color) {
        this.color = color;
    }
    
    // Concrete method
    public String getColor() {
        return color;
    }
    
    // Abstract method
    public abstract double getArea();
}

// Concrete implementation
class Circle extends Shape {
    private double radius;
    
    public Circle(String color, double radius) {
        super(color);
        this.radius = radius;
    }
    
    @Override
    public double getArea() {
        return Math.PI * radius * radius;
    }
    
    @Override
    public void draw() {
        System.out.println("Drawing a " + color + " circle");
    }
}

```

This design combines the benefits of both: the interface defines what can be drawn, while the abstract class provides shared functionality for all shapes. The concrete class implements the specific behavior for a circle.
