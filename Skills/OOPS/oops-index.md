---
tags:
  - index
  - oops
  - design-patterns
---

# OOPS & Design Patterns

- [OOPS Basics](<OOPS Basics.md>)

---

# Design Pattern Basics

Design patterns provide reusable solutions to common software design problems. They help developers write cleaner, maintainable, and scalable applications.

- [Introduction](#introduction)
- [Types of Design Patterns](#types-of-design-patterns)
- [Gang of Four (GoF) Overview](#gang-of-four-gof-overview)

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

These [Creational Design Patterns](<Creational Design Patterns.md>) deal with object creation in a flexible and efficient manner. They help you control how and when objects are instantiated.

- [Singleton Pattern](<Creational Design Patterns.md#1-singleton-pattern>)
- [Factory Method Pattern](<Creational Design Patterns.md#2-factory-method-pattern>)
- [Abstract Factory Pattern](<Creational Design Patterns.md#3-abstract-factory-pattern>)
- [Builder Pattern](<Creational Design Patterns.md#4-builder-pattern>)
- [Prototype Pattern](<Creational Design Patterns.md#5-prototype-pattern>)
- [Object Pool Pattern](<Creational Design Patterns.md#6-object-pool-pattern>)
- [Lazy Initialization](<Creational Design Patterns.md#7-lazy-initialization>)

---

# Structural Design Patterns

[Structural Design Patterns](<Structural Design Patterns.md>) explain how classes and objects are combined to form larger structures. They improve code flexibility by simplifying relationships between components.

- [Adapter Pattern](<Structural Design Patterns.md#1-adapter-pattern>)
- [Decorator Pattern](<Structural Design Patterns.md#2-decorator-pattern>)
- [Facade Pattern](<Structural Design Patterns.md#3-facade-pattern>)
- [Composite Pattern](<Structural Design Patterns.md#4-composite-pattern>)
- [Proxy Pattern](<Structural Design Patterns.md#5-proxy-pattern>)
- [Bridge Pattern](<Structural Design Patterns.md#6-bridge-pattern>)
- [Flyweight Pattern](<Structural Design Patterns.md#7-flyweight-pattern>)

---

# Behavioral Design Patterns

[Behavioral Design Patterns](<Behavioral Design Patterns.md>) define how objects communicate and distribute responsibilities. They help manage workflows, interactions, and decision-making within a system.

- [Observer Pattern](<Behavioral Design Patterns.md#1-observer-pattern>)
- [Strategy Pattern](<Behavioral Design Patterns.md#2-strategy-pattern>)
- [Command Pattern](<Behavioral Design Patterns.md#3-command-pattern>)
- [Chain of Responsibility Pattern](<Behavioral Design Patterns.md#4-chain-of-responsibility-pattern>)
- [Template Method Pattern](<Behavioral Design Patterns.md#5-template-method-pattern>)
- [Iterator Pattern](<Behavioral Design Patterns.md#6-iterator-pattern>)
- [State Pattern](<Behavioral Design Patterns.md#7-state-pattern>)
- [Mediator Pattern](<Behavioral Design Patterns.md#8-mediator-pattern>)
- [Memento Pattern](<Behavioral Design Patterns.md#9-memento-pattern>)
- [Visitor Pattern](<Behavioral Design Patterns.md#10-visitor-pattern>)

---

# Advanced Design Patterns

[Advanced Design Patterns](<Advanced Design Patterns.md>) cover architectural principles and deeper system-design concepts. They help you build enterprise-level, scalable, and robust software systems.

- [SOLID Principles](<Advanced Design Patterns.md#1-solid-principles>)
- [DRY Principle](<Advanced Design Patterns.md#2-dry-principle>)
- [KISS Principle](<Advanced Design Patterns.md#3-kiss-principle>)
- [YAGNI Principle](<Advanced Design Patterns.md#4-yagni-principle>)
- [Dependency Injection Pattern](<Advanced Design Patterns.md#5-dependency-injection-pattern>)
- [Composition Vs Inheritance](<Advanced Design Patterns.md#6-composition-vs-inheritance>)
- [Event-Driven Architecture](<Advanced Design Patterns.md#7-event-driven-architecture>)
- [CQRS Design Pattern](<Advanced Design Patterns.md#8-cqrs-design-pattern>)
- [Event Sourcing Patterns](<Advanced Design Patterns.md#9-event-sourcing-patterns>)
- [CQRS Vs Event Sourcing Patterns](<Advanced Design Patterns.md#10-cqrs-vs-event-sourcing>)
- [Repository Pattern](<Advanced Design Patterns.md#11-repository-pattern>)
- [MVC Design Pattern](<Advanced Design Patterns.md#12-mvc-design-pattern>)

---

# Special Design Patterns

Specialised patterns for specific problem domains — business rule engines, query builders, and domain-driven design.

- [Specification Design Pattern](<Special Design Patterns/Specification Design Pattern.md>)
