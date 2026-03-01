# Advanced Design Patterns

Advanced topics cover architectural principles and deeper system-design concepts. They help you build enterprise-level, scalable, and robust software systems.

---

## 1 SOLID Principles

The five principles for writing **maintainable, flexible, and scalable** OOP code:

### S — Single Responsibility Principle (SRP)

> A class should have **one, and only one, reason to change.**

```java
// ❌ Violates SRP — class does two unrelated things
class Employee {
    public double calculatePay() { /* payroll logic */ }
    public void saveToDatabase() { /* persistence logic */ }
}

// ✅ Follows SRP — separate responsibilities
class Employee {
    private String name;
    private double salary;
    // only domain data and behaviour
}

class PayrollCalculator {
    public double calculatePay(Employee e) { /* payroll logic */ }
}

class EmployeeRepository {
    public void save(Employee e) { /* persistence logic */ }
}
```

### O — Open/Closed Principle (OCP)

> Software entities should be **open for extension**, but **closed for modification.**

```java
// ❌ Adding a new shape requires modifying the calculator
class AreaCalculator {
    public double calculate(Object shape) {
        if (shape instanceof Circle c) return Math.PI * c.r * c.r;
        if (shape instanceof Rectangle r) return r.w * r.h;
        // add more shapes → modify this class every time
    }
}

// ✅ Extend by adding new classes, not modifying existing ones
interface Shape {
    double area();
}
class Circle implements Shape {
    double r;
    public double area() { return Math.PI * r * r; }
}
class Triangle implements Shape {
    double b, h;
    public double area() { return 0.5 * b * h; }
}
// AreaCalculator just calls shape.area() — never modified
```

### L — Liskov Substitution Principle (LSP)

> Subtypes must be **substitutable** for their base types without breaking the program.

```java
// ❌ Violates LSP — Square overrides setWidth in a way that breaks Rectangle
class Rectangle {
    protected int width, height;
    public void setWidth(int w) { this.width = w; }
    public void setHeight(int h) { this.height = h; }
    public int area() { return width * height; }
}

class Square extends Rectangle {
    @Override
    public void setWidth(int w) { this.width = w; this.height = w; }
    @Override
    public void setHeight(int h) { this.width = h; this.height = h; }
}

// This breaks:
Rectangle r = new Square();
r.setWidth(5);
r.setHeight(10);
r.area();  // Expected 50, got 100! Square silently changed width.

// ✅ Use separate classes or a common interface
interface Shape {
    int area();
}
```

### I — Interface Segregation Principle (ISP)

> Clients should not be forced to depend on interfaces they do **not use.**

```java
// ❌ Fat interface
interface Worker {
    void work();
    void eat();
    void sleep();
}
class Robot implements Worker {
    public void work() { /* ok */ }
    public void eat()  { /* robots don't eat! */ }
    public void sleep() { /* robots don't sleep! */ }
}

// ✅ Segregated interfaces
interface Workable { void work(); }
interface Feedable { void eat(); }
interface Restable { void sleep(); }

class HumanWorker implements Workable, Feedable, Restable {
    public void work()  { /* ok */ }
    public void eat()   { /* ok */ }
    public void sleep() { /* ok */ }
}

class Robot implements Workable {
    public void work() { /* ok — only implements what it needs */ }
}
```

### D — Dependency Inversion Principle (DIP)

> High-level modules should not depend on low-level modules. Both should depend on **abstractions.**

```java
// ❌ High-level depends on low-level concrete class
class OrderService {
    private MySQLDatabase db = new MySQLDatabase();  // tight coupling
    public void save(Order o) { db.insert(o); }
}

// ✅ Both depend on abstraction
interface OrderRepository {
    void save(Order order);
}

class MySQLOrderRepo implements OrderRepository {
    public void save(Order o) { /* MySQL logic */ }
}

class MongoOrderRepo implements OrderRepository {
    public void save(Order o) { /* MongoDB logic */ }
}

class OrderService {
    private final OrderRepository repo;  // depends on abstraction

    public OrderService(OrderRepository repo) {
        this.repo = repo;  // injected
    }

    public void placeOrder(Order o) {
        // business logic
        repo.save(o);
    }
}
```

---

## 2 DRY Principle

> **Don't Repeat Yourself.** Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.

```java
// ❌ Duplicated validation logic
class UserController {
    public void createUser(String email) {
        if (!email.contains("@")) throw new IllegalArgumentException("Invalid email");
        // ...
    }
    public void updateEmail(String email) {
        if (!email.contains("@")) throw new IllegalArgumentException("Invalid email");
        // same logic duplicated!
    }
}

// ✅ Single source of truth
class EmailValidator {
    public static void validate(String email) {
        if (email == null || !email.matches("^[\\w.+-]+@[\\w-]+\\.[\\w.]+$"))
            throw new IllegalArgumentException("Invalid email: " + email);
    }
}

class UserController {
    public void createUser(String email) {
        EmailValidator.validate(email);
        // ...
    }
    public void updateEmail(String email) {
        EmailValidator.validate(email);
        // ...
    }
}
```

---

## 3 KISS Principle

> **Keep It Simple, Stupid.** Most systems work best if they are kept simple. Avoid unnecessary complexity.

```java
// ❌ Over-engineered
class StringReverser {
    public String reverse(String s) {
        return IntStream.range(0, s.length())
            .mapToObj(i -> s.charAt(s.length() - 1 - i))
            .collect(StringBuilder::new, StringBuilder::append, StringBuilder::append)
            .toString();
    }
}

// ✅ Simple and clear
class StringReverser {
    public String reverse(String s) {
        return new StringBuilder(s).reverse().toString();
    }
}
```

---

## 4 YAGNI Principle

> **You Aren't Gonna Need It.** Don't implement something until it is actually needed. Avoid speculative generality.

```java
// ❌ Building for hypothetical future requirements
class UserService {
    public void createUser(User u) { /* ... */ }
    public void createBulkUsers(List<User> users) { /* never called */ }
    public void createUserAsync(User u) { /* never called */ }
    public void createUserWithRetry(User u, int retries) { /* never called */ }
}

// ✅ Build what you need NOW
class UserService {
    public void createUser(User u) { /* ... */ }
    // Add others when actually needed
}
```

---

## 5 Dependency Injection Pattern

> **Intent:** Supply an object's dependencies **from the outside** rather than having the object create them itself. This is the practical application of DIP.

### Three Types

| Type | Mechanism |
|---|---|
| **Constructor Injection** | Dependencies passed via constructor (most common, recommended) |
| **Setter Injection** | Dependencies set via setter methods (optional deps) |
| **Interface Injection** | The dependency provides an injector method |

### Implementation — Java (Manual + Spring)

```java
// --- Manual Dependency Injection ---

interface NotificationService {
    void send(String to, String message);
}

class EmailService implements NotificationService {
    public void send(String to, String msg) {
        System.out.println("Email to " + to + ": " + msg);
    }
}

class SMSService implements NotificationService {
    public void send(String to, String msg) {
        System.out.println("SMS to " + to + ": " + msg);
    }
}

// Constructor injection
class OrderService {
    private final NotificationService notifier;

    public OrderService(NotificationService notifier) {
        this.notifier = notifier;   // injected, not created here
    }

    public void placeOrder(String userId) {
        // business logic...
        notifier.send(userId, "Order confirmed!");
    }
}

// Wiring (composition root)
NotificationService svc = new EmailService();
OrderService orders = new OrderService(svc);
orders.placeOrder("alice");


// --- Spring Boot Dependency Injection ---

@Service
class EmailService implements NotificationService {
    public void send(String to, String msg) { /* ... */ }
}

@Service
class OrderService {
    private final NotificationService notifier;

    @Autowired  // Spring injects automatically
    public OrderService(NotificationService notifier) {
        this.notifier = notifier;
    }
}
```

---

## 6 Composition vs Inheritance

> **Favor composition over inheritance.** — *Gang of Four*

### Inheritance (IS-A)

```java
class Bird {
    public void fly() { System.out.println("Flying"); }
}
class Penguin extends Bird {
    @Override
    public void fly() {
        throw new UnsupportedOperationException("Penguins can't fly!");
        // ❌ Violates LSP
    }
}
```

### Composition (HAS-A)

```java
interface FlyBehaviour {
    void fly();
}

class CanFly implements FlyBehaviour {
    public void fly() { System.out.println("Flying high!"); }
}

class CannotFly implements FlyBehaviour {
    public void fly() { System.out.println("I can't fly."); }
}

class Bird {
    private final String name;
    private final FlyBehaviour flyBehaviour;

    public Bird(String name, FlyBehaviour fb) {
        this.name = name;
        this.flyBehaviour = fb;
    }

    public void performFly() { flyBehaviour.fly(); }
}

Bird eagle   = new Bird("Eagle",   new CanFly());
Bird penguin = new Bird("Penguin", new CannotFly());
eagle.performFly();    // Flying high!
penguin.performFly();  // I can't fly.
```

### When to Use Each

| Use Inheritance | Use Composition |
|---|---|
| True IS-A relationship | HAS-A or CAN-DO relationship |
| Code reuse where LSP holds | Flexible, runtime-swappable behaviour |
| Shallow hierarchies (1-2 levels) | Deep or wide hierarchies |
| Framework extension points | Most other cases |

---

## 7 Event-Driven Architecture

> **Intent:** Components communicate by producing and consuming **events** (asynchronous messages). Producers don't know or care who consumes the event.

### Key Concepts

```
┌──────────┐     Event      ┌──────────────┐     Event     ┌──────────┐
│ Producer  │ ──────────────▶│ Event Broker  │──────────────▶│ Consumer │
│ (Service) │    publishes   │ (Kafka/RMQ)   │  delivers    │ (Service)│
└──────────┘                └──────────────┘               └──────────┘
```

| Component | Description |
|---|---|
| **Event** | Immutable record of something that happened (`OrderPlaced`, `UserCreated`) |
| **Producer** | Emits events when state changes |
| **Consumer** | Subscribes to events and reacts |
| **Broker** | Stores and routes events (Kafka, RabbitMQ, AWS SNS/SQS) |

### Benefits

- **Loose coupling** — services don't need to know about each other.
- **Scalability** — consumers can scale independently.
- **Resilience** — events are stored in the broker; consumers can replay.
- **Eventual consistency** — systems converge to consistent state over time.

### Implementation Sketch — Spring + Kafka

```java
// Event
public record OrderPlacedEvent(
    String orderId, String userId, double total, Instant timestamp
) {}

// Producer
@Service
class OrderService {
    @Autowired
    private KafkaTemplate<String, OrderPlacedEvent> kafka;

    public void placeOrder(Order order) {
        // save order...
        kafka.send("orders", new OrderPlacedEvent(
            order.getId(), order.getUserId(), order.getTotal(), Instant.now()));
    }
}

// Consumer
@Service
class EmailNotificationConsumer {
    @KafkaListener(topics = "orders")
    public void onOrderPlaced(OrderPlacedEvent event) {
        System.out.println("Sending confirmation for order " + event.orderId());
        // send email...
    }
}

@Service
class InventoryConsumer {
    @KafkaListener(topics = "orders")
    public void onOrderPlaced(OrderPlacedEvent event) {
        System.out.println("Reserving inventory for " + event.orderId());
        // update stock...
    }
}
```

---

## 8 CQRS Design Pattern

> **Command Query Responsibility Segregation** — Separate the **read** model from the **write** model.

### The Idea

```
          ┌─── Commands (write) ──▶ Write Model ──▶ Write DB
Client ───┤
          └─── Queries (read)  ──▶ Read Model  ──▶ Read DB (optimised)
```

| Side | Purpose | Optimised For |
|---|---|---|
| **Command** | Create, Update, Delete | Data integrity, business rules |
| **Query** | Read | Performance, denormalised views |

### Why Use CQRS

- Read-heavy systems can scale the read side independently.
- Complex domains where the write model doesn't match the read model.
- Combined with Event Sourcing for full audit trail.

### Implementation — Java

```java
// Command side
class CreateOrderCommand {
    String userId;
    List<OrderItem> items;
}

@Service
class OrderCommandHandler {
    @Autowired private OrderWriteRepository writeRepo;

    public void handle(CreateOrderCommand cmd) {
        Order order = new Order(cmd.userId, cmd.items);
        order.validate();
        writeRepo.save(order);
        // publish event for read side to update
    }
}

// Query side — separate, denormalised read model
class OrderSummary {
    String orderId;
    String customerName;
    double total;
    String status;
}

@Service
class OrderQueryHandler {
    @Autowired private OrderReadRepository readRepo;  // different DB / table

    public OrderSummary getOrderSummary(String orderId) {
        return readRepo.findSummary(orderId);
    }

    public List<OrderSummary> getRecentOrders(String userId) {
        return readRepo.findByUserIdOrderByDateDesc(userId);
    }
}
```

---

## 9 Event Sourcing Patterns

> **Intent:** Instead of storing the *current state*, store the **sequence of events** that led to the current state. The state is derived by replaying events.

### Traditional vs Event Sourcing

```
Traditional:   [Current State: balance=500]

Event Sourced: [AccountCreated(0)]
               [MoneyDeposited(1000)]
               [MoneyWithdrawn(300)]
               [MoneyWithdrawn(200)]
               → Replay: 0 + 1000 - 300 - 200 = 500
```

### Benefits

- **Full audit trail** — every change is recorded.
- **Time travel** — reconstruct state at any point in history.
- **Debugging** — replay events to reproduce bugs.
- **CQRS synergy** — events update the read model asynchronously.

### Implementation — Java

```java
// Events (immutable)
sealed interface AccountEvent {
    String accountId();
    Instant timestamp();
}

record AccountCreated(String accountId, String owner, Instant timestamp)
    implements AccountEvent {}

record MoneyDeposited(String accountId, double amount, Instant timestamp)
    implements AccountEvent {}

record MoneyWithdrawn(String accountId, double amount, Instant timestamp)
    implements AccountEvent {}

// Event Store
class EventStore {
    private Map<String, List<AccountEvent>> store = new HashMap<>();

    public void append(AccountEvent event) {
        store.computeIfAbsent(event.accountId(), k -> new ArrayList<>())
             .add(event);
    }

    public List<AccountEvent> getEvents(String accountId) {
        return store.getOrDefault(accountId, List.of());
    }
}

// Aggregate — rebuild state from events
class BankAccount {
    private String id;
    private double balance;
    private String owner;

    // Rebuild from event history
    public static BankAccount fromEvents(List<AccountEvent> events) {
        BankAccount acc = new BankAccount();
        for (AccountEvent e : events) {
            acc.apply(e);
        }
        return acc;
    }

    private void apply(AccountEvent event) {
        switch (event) {
            case AccountCreated e -> {
                this.id = e.accountId();
                this.owner = e.owner();
                this.balance = 0;
            }
            case MoneyDeposited e -> this.balance += e.amount();
            case MoneyWithdrawn e -> this.balance -= e.amount();
        }
    }

    public double getBalance() { return balance; }
}

// Usage
EventStore store = new EventStore();
String accId = "ACC-001";

store.append(new AccountCreated(accId, "Alice", Instant.now()));
store.append(new MoneyDeposited(accId, 1000, Instant.now()));
store.append(new MoneyWithdrawn(accId, 250, Instant.now()));

BankAccount account = BankAccount.fromEvents(store.getEvents(accId));
System.out.println("Balance: " + account.getBalance());  // 750.0
```

---

## 10 CQRS vs Event Sourcing

| Aspect | CQRS | Event Sourcing |
|---|---|---|
| **Core idea** | Separate read and write models | Store events, not state |
| **State storage** | Current state in both models | Event log (append-only) |
| **Can be used alone** | Yes | Yes |
| **Often combined** | Events update the read model | CQRS provides the read side |
| **Complexity** | Moderate | High |
| **Best for** | Read-heavy / different read-write schemas | Audit trail, temporal queries, event-driven systems |

### When They Work Together

```
Command → Write events → Event Store → Event Bus → Update Read Model → Query
```

1. A **command** triggers business logic.
2. Events are **appended** to the event store (Event Sourcing).
3. Events are published to an **event bus**.
4. Consumers (projections) **update the read model** (CQRS).
5. **Queries** hit the read model (fast, denormalised).

---

## 11 Repository Pattern

> **Intent:** Mediate between the domain and data-mapping layers using a **collection-like interface** for accessing domain objects.

### Why Use It
- Abstracts the persistence mechanism (DB, file, API, cache).
- Domain logic stays clean — no SQL or ORM leaking into services.
- Enables easier testing (swap with an in-memory repo).

### Implementation — Java (Spring Data JPA)

```java
// Domain entity
@Entity
class Product {
    @Id @GeneratedValue
    private Long id;
    private String name;
    private double price;
    private String category;
    // getters, setters
}

// Repository interface
interface ProductRepository extends JpaRepository<Product, Long> {
    // Spring auto-implements these from method name
    List<Product> findByCategory(String category);
    List<Product> findByPriceLessThan(double maxPrice);
    Optional<Product> findByName(String name);

    // Custom query
    @Query("SELECT p FROM Product p WHERE p.price BETWEEN :min AND :max")
    List<Product> findInPriceRange(@Param("min") double min, @Param("max") double max);
}

// Service — uses repository abstraction
@Service
class ProductService {
    private final ProductRepository repo;

    public ProductService(ProductRepository repo) {
        this.repo = repo;
    }

    public Product create(String name, double price, String category) {
        Product p = new Product();
        p.setName(name);
        p.setPrice(price);
        p.setCategory(category);
        return repo.save(p);
    }

    public List<Product> getAffordable(double budget) {
        return repo.findByPriceLessThan(budget);
    }
}

// Testing — swap with a fake
class FakeProductRepo implements ProductRepository {
    private List<Product> store = new ArrayList<>();
    // implement methods using the in-memory list
}
```

### Manual Repository (without Spring)

```java
interface OrderRepository {
    void save(Order order);
    Optional<Order> findById(String id);
    List<Order> findByUserId(String userId);
    void delete(String id);
}

class JdbcOrderRepository implements OrderRepository {
    private DataSource ds;

    @Override
    public Optional<Order> findById(String id) {
        String sql = "SELECT * FROM orders WHERE id = ?";
        try (var conn = ds.getConnection();
             var stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, id);
            var rs = stmt.executeQuery();
            if (rs.next()) return Optional.of(mapRow(rs));
            return Optional.empty();
        }
    }
    // ... other methods
}
```

---

## 12 MVC Design Pattern

> **Model-View-Controller** — Separate an application into three interconnected components.

### Structure

```
          User Action
              │
              ▼
        ┌──────────┐
        │Controller │ ← handles input, updates model
        └────┬──┬───┘
    updates  │  │  selects
      model  │  │  view
        ┌────▼──┘───┐
        │   Model    │ ← data + business logic
        └────┬───────┘
     notifies│
        ┌────▼───────┐
        │    View     │ ← renders the model to the user
        └────────────┘
```

| Component | Responsibility |
|---|---|
| **Model** | Application data, business rules, state. Notifies the view when data changes. |
| **View** | Presentation / UI. Displays data from the model. |
| **Controller** | Handles user input, calls model methods, selects the view. |

### Implementation — Spring Boot MVC

```java
// Model
@Entity
class Task {
    @Id @GeneratedValue
    private Long id;
    private String title;
    private boolean completed;
    // getters, setters
}

// Repository (persistence)
interface TaskRepository extends JpaRepository<Task, Long> {
    List<Task> findByCompleted(boolean completed);
}

// Controller
@Controller
@RequestMapping("/tasks")
class TaskController {
    @Autowired private TaskRepository repo;

    // GET /tasks → renders view
    @GetMapping
    public String listTasks(Model model) {
        model.addAttribute("tasks", repo.findAll());
        model.addAttribute("pending", repo.findByCompleted(false).size());
        return "tasks/index";  // view template name
    }

    // POST /tasks → create new task
    @PostMapping
    public String createTask(@RequestParam String title) {
        Task task = new Task();
        task.setTitle(title);
        task.setCompleted(false);
        repo.save(task);
        return "redirect:/tasks";
    }

    // POST /tasks/{id}/toggle → toggle completion
    @PostMapping("/{id}/toggle")
    public String toggleTask(@PathVariable Long id) {
        Task task = repo.findById(id).orElseThrow();
        task.setCompleted(!task.isCompleted());
        repo.save(task);
        return "redirect:/tasks";
    }
}
```

### REST API variant (headless — View is the JSON response)

```java
@RestController
@RequestMapping("/api/tasks")
class TaskRestController {
    @Autowired private TaskRepository repo;

    @GetMapping
    public List<Task> getAll() { return repo.findAll(); }

    @PostMapping
    public Task create(@RequestBody Task task) { return repo.save(task); }

    @PutMapping("/{id}")
    public Task update(@PathVariable Long id, @RequestBody Task updated) {
        Task task = repo.findById(id).orElseThrow();
        task.setTitle(updated.getTitle());
        task.setCompleted(updated.isCompleted());
        return repo.save(task);
    }

    @DeleteMapping("/{id}")
    public void delete(@PathVariable Long id) { repo.deleteById(id); }
}
```

### MVC Variants

| Pattern | Description |
|---|---|
| **MVC** | Controller handles input, model notifies view |
| **MVP** (Model-View-Presenter) | Presenter mediates between view and model; view is passive |
| **MVVM** (Model-View-ViewModel) | ViewModel exposes bindable properties; used in Android, WPF |

---

## Summary

| Topic | Core Principle |
|---|---|
| **SOLID** | 5 principles for maintainable OOP (SRP, OCP, LSP, ISP, DIP) |
| **DRY** | Single source of truth — no duplicated knowledge |
| **KISS** | Simplicity over cleverness |
| **YAGNI** | Build only what's needed now |
| **Dependency Injection** | Supply dependencies from outside (DIP in practice) |
| **Composition > Inheritance** | Prefer HAS-A over IS-A for flexibility |
| **Event-Driven Architecture** | Async communication via events and brokers |
| **CQRS** | Separate read model from write model |
| **Event Sourcing** | Store events, derive state by replay |
| **Repository** | Collection-like interface over persistence |
| **MVC** | Separate Model, View, Controller |
