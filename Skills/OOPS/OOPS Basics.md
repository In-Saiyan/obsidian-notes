---
tags:
  - oops
  - fundamentals
---

# OOPS Basics

Object-Oriented Programming (OOP) is a programming paradigm that organises software design around **objects** — entities that bundle state (fields) and behaviour (methods) together.

- [Core Concepts](#core-concepts)
- [Classes and Objects](#classes-and-objects)
- [Encapsulation](#encapsulation)
- [Inheritance](#inheritance)
- [Polymorphism](#polymorphism)
- [Abstraction](#abstraction)
- [Relationships Between Classes](#relationships-between-classes)

---

## Core Concepts

| Pillar | One-liner |
|---|---|
| **Encapsulation** | Hide internal state; expose only a controlled interface |
| **Inheritance** | Derive new types from existing ones to reuse behaviour |
| **Polymorphism** | One interface, many implementations |
| **Abstraction** | Model real-world entities, hide irrelevant details |

---

## Classes and Objects

A **class** is a blueprint; an **object** is a concrete instance of that blueprint.

```java
class Animal {
    String name;

    void speak() {
        System.out.println(name + " makes a sound.");
    }
}

Animal dog = new Animal();   // object instantiation
dog.name = "Rex";
dog.speak();                 // Rex makes a sound.
```

**Key terms:**
- **Field / Attribute** — data stored on an object (`name`)
- **Method** — behaviour defined on a class (`speak()`)
- **Constructor** — special method called when the object is created

---

## Encapsulation

Encapsulation bundles data and methods together and **restricts direct access** to an object's internals using access modifiers.

```java
class BankAccount {
    private double balance;   // hidden from outside

    public void deposit(double amount) {
        if (amount > 0) balance += amount;
    }

    public double getBalance() {
        return balance;
    }
}
```

**Benefits:**
- Prevents invalid state from being set externally
- Internal implementation can change without breaking callers
- Enforces invariants (e.g. balance can never go negative)

---

## Inheritance

Inheritance lets a **child class** acquire the fields and methods of a **parent class**, enabling code reuse and type hierarchies.

```java
class Animal {
    void eat() { System.out.println("Eating..."); }
}

class Dog extends Animal {
    void bark() { System.out.println("Woof!"); }
}

Dog d = new Dog();
d.eat();   // inherited
d.bark();  // own method
```

**Types of inheritance in Java:**

| Type | Support |
|---|---|
| Single | Yes |
| Multilevel | Yes |
| Hierarchical | Yes |
| Multiple (via classes) | No — use interfaces instead |

---

## Polymorphism

Polymorphism means *"many forms"*. A single method call can behave differently depending on the actual object type.

### Compile-time (Method Overloading)

```java
class Calculator {
    int add(int a, int b)       { return a + b; }
    double add(double a, double b) { return a + b; }
}
```

### Runtime (Method Overriding)

```java
class Shape {
    void draw() { System.out.println("Drawing a shape"); }
}

class Circle extends Shape {
    @Override
    void draw() { System.out.println("Drawing a circle"); }
}

Shape s = new Circle();
s.draw();   // Drawing a circle  (resolved at runtime)
```

---

## Abstraction

Abstraction exposes **what** an object does, not **how** it does it. Achieved via **abstract classes** or **interfaces**.

### Abstract Class

```java
abstract class Vehicle {
    abstract void startEngine();   // subclass must implement

    void refuel() { System.out.println("Refuelling..."); }
}
```

### Interface

```java
interface Flyable {
    void fly();   // implicitly public abstract
}

class Bird implements Flyable {
    public void fly() { System.out.println("Bird is flying"); }
}
```

**Abstract class vs Interface:**

| | Abstract Class | Interface |
|---|---|---|
| State (fields) | Yes | No (constants only) |
| Constructor | Yes | No |
| Multiple inheritance | No | Yes |
| Default methods | Yes | Yes (Java 8+) |

---

## Relationships Between Classes

| Relationship | Description | Example |
|---|---|---|
| **Association** | One class uses another | `Order` uses `Product` |
| **Aggregation** | "Has-a", weak ownership | `Team` has `Player`s |
| **Composition** | "Has-a", strong ownership | `House` has `Room`s |
| **Inheritance** | "Is-a" | `Dog` is an `Animal` |
| **Dependency** | Uses temporarily | Method takes param of another type |
