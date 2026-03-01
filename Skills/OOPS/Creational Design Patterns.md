---
tags:
  - oops
  - design-patterns
  - creational
---

# Creational Design Patterns

Creational patterns deal with **object creation mechanisms** — trying to create objects in a manner suitable to the situation. They abstract the instantiation process, making a system independent of how its objects are created, composed, and represented.

---

## 1 Singleton Pattern

> **Intent:** Ensure a class has only **one instance** and provide a **global point of access** to it.

### When to Use
- Database connection pool
- Logger
- Configuration manager
- Thread pool
- Cache

### Structure

```
┌──────────────┐
│  Singleton   │
├──────────────┤
│ -instance    │
├──────────────┤
│ -Singleton() │ ← private constructor
│ +getInstance │ → returns the single instance
└──────────────┘
```

### Implementation — Java (Thread-Safe)

```java
public class Singleton {
    // volatile ensures visibility across threads
    private static volatile Singleton instance;

    // Private constructor prevents external instantiation
    private Singleton() {
        // Prevent reflection attack
        if (instance != null) {
            throw new RuntimeException("Use getInstance()");
        }
    }

    // Double-checked locking
    public static Singleton getInstance() {
        if (instance == null) {                  // 1st check (no lock)
            synchronized (Singleton.class) {
                if (instance == null) {          // 2nd check (with lock)
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

### Alternate: Enum Singleton (safest in Java)

```java
public enum DatabaseConnection {
    INSTANCE;

    private Connection conn;

    DatabaseConnection() {
        // initialise connection
        conn = DriverManager.getConnection("jdbc:...");
    }

    public Connection getConnection() {
        return conn;
    }
}

// Usage
Connection c = DatabaseConnection.INSTANCE.getConnection();
```

### Pros & Cons

| Pros | Cons |
|---|---|
| Controlled access to sole instance | Violates Single Responsibility Principle |
| Lazy initialisation possible | Hard to unit test (global state) |
| Thread-safe with proper implementation | Can hide dependencies |

---

## 2 Factory Method Pattern

> **Intent:** Define an interface for creating objects, but let **subclasses** decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses.

### When to Use
- When a class can't anticipate the type of objects it must create.
- When you want to delegate responsibility to subclasses.
- Frameworks where the library code calls user-defined factory methods.

### Structure

```
        ┌───────────┐          ┌───────────┐
        │  Creator   │          │  Product   │ (interface)
        ├───────────┤          └─────┬─────┘
        │+createP() │ abstract       │
        └─────┬─────┘          ┌─────┴─────┐
              │                │ConcreteP_A │
     ┌────────┴────────┐      │ConcreteP_B │
     │ConcreteCreator_A│      └────────────┘
     │ConcreteCreator_B│
     └─────────────────┘
```

### Implementation — Java

```java
// Product interface
interface Notification {
    void send(String message);
}

// Concrete products
class EmailNotification implements Notification {
    @Override
    public void send(String message) {
        System.out.println("Email: " + message);
    }
}

class SMSNotification implements Notification {
    @Override
    public void send(String message) {
        System.out.println("SMS: " + message);
    }
}

class PushNotification implements Notification {
    @Override
    public void send(String message) {
        System.out.println("Push: " + message);
    }
}

// Creator (Factory)
abstract class NotificationFactory {
    // Factory Method
    abstract Notification createNotification();

    // Template method using the factory method
    public void notify(String message) {
        Notification n = createNotification();
        n.send(message);
    }
}

// Concrete Creators
class EmailFactory extends NotificationFactory {
    @Override
    Notification createNotification() {
        return new EmailNotification();
    }
}

class SMSFactory extends NotificationFactory {
    @Override
    Notification createNotification() {
        return new SMSNotification();
    }
}

// Usage
NotificationFactory factory = new SMSFactory();
factory.notify("Hello World");  // SMS: Hello World
```

### Simple Factory (not a GoF pattern but widely used)

```java
class NotificationFactory {
    public static Notification create(String type) {
        return switch (type.toLowerCase()) {
            case "email" -> new EmailNotification();
            case "sms"   -> new SMSNotification();
            case "push"  -> new PushNotification();
            default -> throw new IllegalArgumentException("Unknown: " + type);
        };
    }
}

Notification n = NotificationFactory.create("email");
```

---

## 3 Abstract Factory Pattern

> **Intent:** Provide an interface for creating **families of related objects** without specifying their concrete classes.

### When to Use
- UI toolkit that must support multiple look-and-feels (Windows, macOS, Linux).
- Database access layer that supports multiple databases.
- Cross-platform components.

### Implementation — Java

```java
// Abstract products
interface Button {
    void render();
}
interface TextBox {
    void render();
}

// Windows family
class WindowsButton implements Button {
    public void render() { System.out.println("[Windows Button]"); }
}
class WindowsTextBox implements TextBox {
    public void render() { System.out.println("[Windows TextBox]"); }
}

// macOS family
class MacButton implements Button {
    public void render() { System.out.println("[Mac Button]"); }
}
class MacTextBox implements TextBox {
    public void render() { System.out.println("[Mac TextBox]"); }
}

// Abstract Factory
interface UIFactory {
    Button createButton();
    TextBox createTextBox();
}

// Concrete Factories
class WindowsUIFactory implements UIFactory {
    public Button createButton()   { return new WindowsButton(); }
    public TextBox createTextBox() { return new WindowsTextBox(); }
}

class MacUIFactory implements UIFactory {
    public Button createButton()   { return new MacButton(); }
    public TextBox createTextBox() { return new MacTextBox(); }
}

// Client — works with ANY factory
class Application {
    private Button button;
    private TextBox textBox;

    public Application(UIFactory factory) {
        this.button  = factory.createButton();
        this.textBox = factory.createTextBox();
    }

    public void render() {
        button.render();
        textBox.render();
    }
}

// Usage
UIFactory factory = new MacUIFactory();
Application app = new Application(factory);
app.render();
// [Mac Button]
// [Mac TextBox]
```

### Factory Method vs Abstract Factory

| Factory Method | Abstract Factory |
|---|---|
| Creates **one** product | Creates a **family** of related products |
| Uses inheritance (subclass overrides) | Uses composition (factory object passed in) |
| Single method | Multiple creation methods |

---

## 4 Builder Pattern

> **Intent:** Separate the **construction** of a complex object from its **representation**, so the same construction process can create different representations.

### When to Use
- Objects with many optional parameters (avoids telescoping constructors).
- Step-by-step construction of complex objects.
- When the construction process must allow different representations.

### Implementation — Java

```java
public class HttpRequest {
    private final String url;
    private final String method;
    private final Map<String, String> headers;
    private final String body;
    private final int timeout;

    // Private constructor — only Builder can construct
    private HttpRequest(Builder builder) {
        this.url     = builder.url;
        this.method  = builder.method;
        this.headers = builder.headers;
        this.body    = builder.body;
        this.timeout = builder.timeout;
    }

    // Static inner Builder class
    public static class Builder {
        // Required
        private final String url;

        // Optional — with defaults
        private String method = "GET";
        private Map<String, String> headers = new HashMap<>();
        private String body = "";
        private int timeout = 30_000;

        public Builder(String url) {
            this.url = url;
        }

        public Builder method(String method) {
            this.method = method;
            return this;        // fluent API
        }

        public Builder header(String key, String value) {
            this.headers.put(key, value);
            return this;
        }

        public Builder body(String body) {
            this.body = body;
            return this;
        }

        public Builder timeout(int ms) {
            this.timeout = ms;
            return this;
        }

        public HttpRequest build() {
            // Validation
            if (url == null || url.isEmpty())
                throw new IllegalStateException("URL is required");
            return new HttpRequest(this);
        }
    }

    @Override
    public String toString() {
        return method + " " + url + " headers=" + headers
               + " body=" + body + " timeout=" + timeout;
    }
}

// Usage — fluent builder
HttpRequest request = new HttpRequest.Builder("https://api.example.com/users")
        .method("POST")
        .header("Content-Type", "application/json")
        .header("Authorization", "Bearer token123")
        .body("{\"name\": \"Alice\"}")
        .timeout(5000)
        .build();

System.out.println(request);
```

---

## 5 Prototype Pattern

> **Intent:** Create new objects by **cloning** an existing object (the prototype) instead of creating from scratch.

### When to Use
- When object creation is expensive (DB query, network call, heavy computation).
- When you need many objects that differ only slightly.
- Runtime configuration of instances.

### Implementation — Java

```java
// Prototype interface
interface GameUnit extends Cloneable {
    GameUnit clone();
    void setPosition(int x, int y);
    String describe();
}

class Soldier implements GameUnit {
    private String type;
    private int health;
    private int attack;
    private int x, y;
    private List<String> equipment;  // deep clone needed

    public Soldier(String type, int health, int attack, List<String> equipment) {
        this.type = type;
        this.health = health;
        this.attack = attack;
        this.equipment = new ArrayList<>(equipment);
        // Simulate expensive initialisation
        System.out.println("  [Expensive init for " + type + "]");
    }

    // Copy constructor (for cloning)
    private Soldier(Soldier other) {
        this.type      = other.type;
        this.health    = other.health;
        this.attack    = other.attack;
        this.equipment = new ArrayList<>(other.equipment); // deep copy
        // No expensive init!
    }

    @Override
    public GameUnit clone() {
        return new Soldier(this);
    }

    @Override
    public void setPosition(int x, int y) {
        this.x = x; this.y = y;
    }

    @Override
    public String describe() {
        return type + " at (" + x + "," + y + ") HP=" + health;
    }
}

// Prototype Registry
class UnitRegistry {
    private Map<String, GameUnit> prototypes = new HashMap<>();

    public void register(String key, GameUnit prototype) {
        prototypes.put(key, prototype);
    }

    public GameUnit create(String key) {
        return prototypes.get(key).clone();
    }
}

// Usage
UnitRegistry registry = new UnitRegistry();
registry.register("infantry", new Soldier("Infantry", 100, 15,
        List.of("Rifle", "Grenade")));   // expensive init happens once

// Create 100 soldiers by cloning — cheap!
for (int i = 0; i < 100; i++) {
    GameUnit unit = registry.create("infantry");
    unit.setPosition(i * 10, 0);
}
```

---

## 6 Object Pool Pattern

> **Intent:** Manage a pool of **reusable objects** to avoid the overhead of creating and destroying them repeatedly.

### When to Use
- Database connections
- Thread pools
- Socket connections
- Heavy objects that are expensive to create

### Implementation — Java

```java
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

public class ConnectionPool {
    private final BlockingQueue<Connection> pool;
    private final int maxSize;

    public ConnectionPool(int maxSize) {
        this.maxSize = maxSize;
        this.pool = new LinkedBlockingQueue<>(maxSize);

        // Pre-fill the pool
        for (int i = 0; i < maxSize; i++) {
            pool.offer(createNewConnection(i));
        }
    }

    private Connection createNewConnection(int id) {
        System.out.println("Creating connection #" + id);
        return new Connection(id);
    }

    public Connection acquire() throws InterruptedException {
        Connection conn = pool.take();  // blocks if pool is empty
        System.out.println("Acquired connection #" + conn.getId());
        return conn;
    }

    public void release(Connection conn) {
        conn.reset();
        pool.offer(conn);
        System.out.println("Released connection #" + conn.getId());
    }

    public int available() {
        return pool.size();
    }
}

class Connection {
    private final int id;
    private boolean inUse;

    public Connection(int id) { this.id = id; }
    public int getId() { return id; }
    public void reset() { this.inUse = false; }
    public void execute(String query) {
        System.out.println("  Conn#" + id + " executing: " + query);
    }
}

// Usage
ConnectionPool pool = new ConnectionPool(3);

Connection c1 = pool.acquire();
Connection c2 = pool.acquire();
c1.execute("SELECT * FROM users");
pool.release(c1);

Connection c3 = pool.acquire();  // reuses c1's connection
```

---

## 7 Lazy Initialization

> **Intent:** Delay the creation of an object or computation of a value until the **first time it is needed**.

### When to Use
- Expensive objects that may never be used.
- Database connections opened on demand.
- Configuration loaded only when accessed.

### Implementation — Java

```java
// Simple lazy init
public class HeavyResource {
    private ExpensiveObject obj;

    public ExpensiveObject getObject() {
        if (obj == null) {
            obj = new ExpensiveObject();  // created only on first access
        }
        return obj;
    }
}

// Thread-safe with Holder pattern (Bill Pugh Singleton)
public class Config {
    private Config() { }

    // Inner class is loaded only when getInstance() is called
    private static class Holder {
        static final Config INSTANCE = new Config();
    }

    public static Config getInstance() {
        return Holder.INSTANCE;  // lazy + thread-safe + no synchronisation
    }
}

// Java's built-in: Supplier + memoization
import java.util.function.Supplier;

public class Lazy<T> {
    private Supplier<T> supplier;
    private T value;
    private boolean initialised = false;

    public Lazy(Supplier<T> supplier) {
        this.supplier = supplier;
    }

    public synchronized T get() {
        if (!initialised) {
            value = supplier.get();
            initialised = true;
            supplier = null;  // allow GC of the supplier
        }
        return value;
    }
}

// Usage
Lazy<List<String>> data = new Lazy<>(() -> {
    System.out.println("Loading from database...");
    return database.fetchAllRecords();
});

// Nothing loaded yet...
System.out.println("App started");
// Now it loads:
List<String> records = data.get();  // "Loading from database..."
```

---

## Summary

| Pattern | Key Idea | Use When |
|---|---|---|
| **Singleton** | One instance, global access | Shared resource (DB, config, logger) |
| **Factory Method** | Subclass decides what to create | Varying product types |
| **Abstract Factory** | Family of related products | Cross-platform / themed UI |
| **Builder** | Step-by-step construction | Many optional parameters |
| **Prototype** | Clone existing objects | Expensive creation, similar objects |
| **Object Pool** | Reuse expensive objects | Connections, threads |
| **Lazy Init** | Create on first access | Expensive, possibly unused objects |
