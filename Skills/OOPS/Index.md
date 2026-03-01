# OOPS & Design Patterns

- [[OOPS Basics]]

---

# Design Pattern Basics

Design patterns provide reusable solutions to common software design problems. They help developers write cleaner, maintainable, and scalable applications.

- [[#Introduction]]
- [[#Types of Design Patterns]]
- [[#Gang of Four (GoF) Overview]]

---

## Introduction

A **design pattern** is a general, reusable solution to a commonly occurring problem within a given context in software design. It is not a finished design that can be transformed directly into code — it is a **template** for how to solve a problem that can be used in many different situations.

**Why use design patterns?**
- **Proven solutions** — patterns are battle-tested by thousands of developers.
- **Common vocabulary** — saying "use a Singleton" instantly communicates intent.
- **Avoid reinventing the wheel** — don't solve the same problem from scratch.
- **Better architecture** — patterns promote loose coupling, high cohesion, and SOLID principles.
- **Easier maintenance** — well-structured code is easier to modify and extend.

**When NOT to use design patterns:**
- Don't force a pattern where a simpler solution works.
- Patterns add abstraction — unnecessary patterns add unnecessary complexity.
- Understand the problem first, then pick the pattern (not the other way around).

---

## Types of Design Patterns

| Category | Purpose | Focus |
|---|---|---|
| **Creational** | Control *how* objects are created | Object instantiation |
| **Structural** | Control *how* classes/objects are composed | Relationships and composition |
| **Behavioral** | Control *how* objects communicate | Interaction and responsibility |

---

## Gang of Four (GoF) Overview

The **Gang of Four** refers to the four authors — *Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides* — of the book **"Design Patterns: Elements of Reusable Object-Oriented Software"** (1994).

They catalogued **23 design patterns** in three categories:

| Creational (5) | Structural (7) | Behavioral (11) |
|---|---|---|
| Singleton | Adapter | Observer |
| Factory Method | Decorator | Strategy |
| Abstract Factory | Facade | Command |
| Builder | Composite | Chain of Responsibility |
| Prototype | Proxy | Template Method |
| | Bridge | Iterator |
| | Flyweight | State |
| | | Mediator |
| | | Memento |
| | | Visitor |
| | | Interpreter |

---

# Creational Design Patterns

These [[Creational Design Patterns]] deal with object creation in a flexible and efficient manner. They help you control how and when objects are instantiated.

- [[Creational Design Patterns#1 Singleton Pattern|Singleton Pattern]]
- [[Creational Design Patterns#2 Factory Method Pattern|Factory Method Pattern]]
- [[Creational Design Patterns#3 Abstract Factory Pattern|Abstract Factory Pattern]]
- [[Creational Design Patterns#4 Builder Pattern|Builder Pattern]]
- [[Creational Design Patterns#5 Prototype Pattern|Prototype Pattern]]
- [[Creational Design Patterns#6 Object Pool Pattern|Object Pool Pattern]]
- [[Creational Design Patterns#7 Lazy Initialization|Lazy Initialization]]

---

# Structural Design Patterns

[[Structural Design Patterns]] explain how classes and objects are combined to form larger structures. They improve code flexibility by simplifying relationships between components.

- [[Structural Design Patterns#1 Adapter Pattern|Adapter Pattern]]
- [[Structural Design Patterns#2 Decorator Pattern|Decorator Pattern]]
- [[Structural Design Patterns#3 Facade Pattern|Facade Pattern]]
- [[Structural Design Patterns#4 Composite Pattern|Composite Pattern]]
- [[Structural Design Patterns#5 Proxy Pattern|Proxy Pattern]]
- [[Structural Design Patterns#6 Bridge Pattern|Bridge Pattern]]
- [[Structural Design Patterns#7 Flyweight Pattern|Flyweight Pattern]]

---

# Behavioral Design Patterns

[[Behavioral Design Patterns]] define how objects communicate and distribute responsibilities. They help manage workflows, interactions, and decision-making within a system.

- [[Behavioral Design Patterns#1 Observer Pattern|Observer Pattern]]
- [[Behavioral Design Patterns#2 Strategy Pattern|Strategy Pattern]]
- [[Behavioral Design Patterns#3 Command Pattern|Command Pattern]]
- [[Behavioral Design Patterns#4 Chain of Responsibility Pattern|Chain of Responsibility Pattern]]
- [[Behavioral Design Patterns#5 Template Method Pattern|Template Method Pattern]]
- [[Behavioral Design Patterns#6 Iterator Pattern|Iterator Pattern]]
- [[Behavioral Design Patterns#7 State Pattern|State Pattern]]
- [[Behavioral Design Patterns#8 Mediator Pattern|Mediator Pattern]]
- [[Behavioral Design Patterns#9 Memento Pattern|Memento Pattern]]
- [[Behavioral Design Patterns#10 Visitor Pattern|Visitor Pattern]]

---

# Advanced Design Patterns

[[Advanced Design Patterns]] cover architectural principles and deeper system-design concepts. They help you build enterprise-level, scalable, and robust software systems.

- [[Advanced Design Patterns#1 SOLID Principles|SOLID Principles]]
- [[Advanced Design Patterns#2 DRY Principle|DRY Principle]]
- [[Advanced Design Patterns#3 KISS Principle|KISS Principle]]
- [[Advanced Design Patterns#4 YAGNI Principle|YAGNI Principle]]
- [[Advanced Design Patterns#5 Dependency Injection Pattern|Dependency Injection Pattern]]
- [[Advanced Design Patterns#6 Composition vs Inheritance|Composition Vs Inheritance]]
- [[Advanced Design Patterns#7 Event-Driven Architecture|Event-Driven Architecture]]
- [[Advanced Design Patterns#8 CQRS Design Pattern|CQRS Design Pattern]]
- [[Advanced Design Patterns#9 Event Sourcing Patterns|Event Sourcing Patterns]]
- [[Advanced Design Patterns#10 CQRS vs Event Sourcing|CQRS Vs Event Sourcing Patterns]]
- [[Advanced Design Patterns#11 Repository Pattern|Repository Pattern]]
- [[Advanced Design Patterns#12 MVC Design Pattern|MVC Design Pattern]]

---

# Special Design Patterns

Specialised patterns for specific problem domains — business rule engines, query builders, and domain-driven design.

- [[Special Design Patterns/Specification Design Pattern|Specification Design Pattern]]
