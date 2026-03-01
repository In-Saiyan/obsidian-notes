---
tags:
  - oops
  - design-patterns
  - behavioral
---

# Behavioral Design Patterns

Behavioral patterns define how objects **communicate**, **distribute responsibilities**, and **manage control flow**. They focus on interaction and the assignment of responsibilities between objects.

---

## 1 Observer Pattern

> **Intent:** Define a **one-to-many** dependency so that when one object (subject) changes state, all its dependents (observers) are notified and updated automatically.

Also known as **Publish-Subscribe**.

### When to Use
- Event handling systems (GUI buttons, DOM events).
- Notification services (email, push).
- Reactive streams, data binding in MVC/MVVM.

### Implementation — Java

```java
// Observer interface
interface EventListener {
    void update(String event, Object data);
}

// Subject (Observable)
class EventBus {
    private Map<String, List<EventListener>> listeners = new HashMap<>();

    public void subscribe(String event, EventListener listener) {
        listeners.computeIfAbsent(event, k -> new ArrayList<>()).add(listener);
    }

    public void unsubscribe(String event, EventListener listener) {
        List<EventListener> list = listeners.get(event);
        if (list != null) list.remove(listener);
    }

    public void publish(String event, Object data) {
        List<EventListener> list = listeners.getOrDefault(event, List.of());
        for (EventListener l : list) {
            l.update(event, data);
        }
    }
}

// Concrete observers
class EmailAlert implements EventListener {
    @Override
    public void update(String event, Object data) {
        System.out.println("[Email] Event: " + event + " → " + data);
    }
}

class SlackAlert implements EventListener {
    @Override
    public void update(String event, Object data) {
        System.out.println("[Slack] Event: " + event + " → " + data);
    }
}

class LogWriter implements EventListener {
    @Override
    public void update(String event, Object data) {
        System.out.println("[Log] " + event + ": " + data);
    }
}

// Usage
EventBus bus = new EventBus();
bus.subscribe("user.signup", new EmailAlert());
bus.subscribe("user.signup", new SlackAlert());
bus.subscribe("order.placed", new LogWriter());
bus.subscribe("order.placed", new EmailAlert());

bus.publish("user.signup", "alice@example.com");
// [Email] Event: user.signup → alice@example.com
// [Slack] Event: user.signup → alice@example.com

bus.publish("order.placed", "Order #1234");
// [Log] order.placed: Order #1234
// [Email] Event: order.placed → Order #1234
```

---

## 2 Strategy Pattern

> **Intent:** Define a family of algorithms, encapsulate each one, and make them **interchangeable**. Strategy lets the algorithm vary independently from the clients that use it.

### When to Use
- Multiple algorithms for the same task (sorting, compression, routing).
- Avoiding long `if-else` / `switch` chains.
- Selecting behaviour at runtime.

### Implementation — Java

```java
// Strategy interface
interface PaymentStrategy {
    void pay(double amount);
}

// Concrete strategies
class CreditCardPayment implements PaymentStrategy {
    private String cardNumber;

    public CreditCardPayment(String card) { this.cardNumber = card; }

    @Override
    public void pay(double amount) {
        System.out.printf("Paid $%.2f with credit card %s%n", amount, cardNumber);
    }
}

class PayPalPayment implements PaymentStrategy {
    private String email;

    public PayPalPayment(String email) { this.email = email; }

    @Override
    public void pay(double amount) {
        System.out.printf("Paid $%.2f via PayPal (%s)%n", amount, email);
    }
}

class CryptoPayment implements PaymentStrategy {
    private String wallet;

    public CryptoPayment(String wallet) { this.wallet = wallet; }

    @Override
    public void pay(double amount) {
        System.out.printf("Paid $%.2f in crypto to wallet %s%n", amount, wallet);
    }
}

// Context
class ShoppingCart {
    private List<Double> items = new ArrayList<>();
    private PaymentStrategy paymentStrategy;

    public void addItem(double price) { items.add(price); }

    public void setPaymentStrategy(PaymentStrategy strategy) {
        this.paymentStrategy = strategy;
    }

    public void checkout() {
        double total = items.stream().mapToDouble(Double::doubleValue).sum();
        paymentStrategy.pay(total);
    }
}

// Usage — strategy selected at runtime
ShoppingCart cart = new ShoppingCart();
cart.addItem(49.99);
cart.addItem(12.50);

cart.setPaymentStrategy(new CreditCardPayment("4111-1111-1111-1111"));
cart.checkout();  // Paid $62.49 with credit card ...

cart.setPaymentStrategy(new PayPalPayment("user@email.com"));
cart.checkout();  // Paid $62.49 via PayPal ...
```

### Strategy with Lambdas (Java 8+)

```java
// Strategy is a functional interface — use lambdas
cart.setPaymentStrategy(amount ->
    System.out.printf("Paid $%.2f with Apple Pay%n", amount));
cart.checkout();
```

---

## 3 Command Pattern

> **Intent:** Encapsulate a **request as an object**, thereby letting you parameterise clients with different requests, queue or log requests, and support **undo/redo**.

### When to Use
- Undo/redo functionality (text editors, drawing apps).
- Task queues and job scheduling.
- Macro recording (sequence of commands).
- Transactional systems.

### Implementation — Java

```java
// Command interface
interface Command {
    void execute();
    void undo();
}

// Receiver
class TextEditor {
    private StringBuilder text = new StringBuilder();

    public void insert(String s) { text.append(s); }
    public void delete(int count) {
        text.delete(text.length() - count, text.length());
    }
    public String getText() { return text.toString(); }
}

// Concrete commands
class InsertCommand implements Command {
    private TextEditor editor;
    private String textToInsert;

    public InsertCommand(TextEditor editor, String text) {
        this.editor = editor;
        this.textToInsert = text;
    }

    @Override
    public void execute() {
        editor.insert(textToInsert);
    }

    @Override
    public void undo() {
        editor.delete(textToInsert.length());
    }
}

// Invoker — manages command history
class CommandHistory {
    private Deque<Command> undoStack = new ArrayDeque<>();
    private Deque<Command> redoStack = new ArrayDeque<>();

    public void execute(Command cmd) {
        cmd.execute();
        undoStack.push(cmd);
        redoStack.clear();   // new action clears redo history
    }

    public void undo() {
        if (!undoStack.isEmpty()) {
            Command cmd = undoStack.pop();
            cmd.undo();
            redoStack.push(cmd);
        }
    }

    public void redo() {
        if (!redoStack.isEmpty()) {
            Command cmd = redoStack.pop();
            cmd.execute();
            undoStack.push(cmd);
        }
    }
}

// Usage
TextEditor editor = new TextEditor();
CommandHistory history = new CommandHistory();

history.execute(new InsertCommand(editor, "Hello"));
history.execute(new InsertCommand(editor, " World"));
System.out.println(editor.getText());  // "Hello World"

history.undo();
System.out.println(editor.getText());  // "Hello"

history.redo();
System.out.println(editor.getText());  // "Hello World"
```

---

## 4 Chain of Responsibility Pattern

> **Intent:** Avoid coupling the sender of a request to its receiver by giving **multiple objects a chance** to handle the request. Chain the receiving objects and pass the request along the chain until an object handles it.

### When to Use
- Middleware pipelines (logging → auth → validation → handler).
- Event bubbling in GUI.
- Exception handling chains.
- Approval workflows (employee → manager → director → CEO).

### Implementation — Java

```java
// Handler
abstract class SupportHandler {
    private SupportHandler next;

    public SupportHandler setNext(SupportHandler next) {
        this.next = next;
        return next;   // allows chaining
    }

    public void handle(Ticket ticket) {
        if (canHandle(ticket)) {
            process(ticket);
        } else if (next != null) {
            next.handle(ticket);
        } else {
            System.out.println("No handler for: " + ticket);
        }
    }

    protected abstract boolean canHandle(Ticket ticket);
    protected abstract void process(Ticket ticket);
}

class Ticket {
    String severity;  // "low", "medium", "critical"
    String issue;

    public Ticket(String severity, String issue) {
        this.severity = severity;
        this.issue = issue;
    }

    public String toString() { return "[" + severity + "] " + issue; }
}

// Concrete handlers
class BotHandler extends SupportHandler {
    protected boolean canHandle(Ticket t) { return "low".equals(t.severity); }
    protected void process(Ticket t) {
        System.out.println("🤖 Bot resolved: " + t);
    }
}

class TechSupport extends SupportHandler {
    protected boolean canHandle(Ticket t) { return "medium".equals(t.severity); }
    protected void process(Ticket t) {
        System.out.println("👨‍💻 Tech support resolved: " + t);
    }
}

class Engineering extends SupportHandler {
    protected boolean canHandle(Ticket t) { return "critical".equals(t.severity); }
    protected void process(Ticket t) {
        System.out.println("🔧 Engineering team resolved: " + t);
    }
}

// Build chain
SupportHandler chain = new BotHandler();
chain.setNext(new TechSupport())
     .setNext(new Engineering());

chain.handle(new Ticket("low", "Password reset"));
// 🤖 Bot resolved: [low] Password reset

chain.handle(new Ticket("critical", "Database down"));
// 🔧 Engineering team resolved: [critical] Database down
```

---

## 5 Template Method Pattern

> **Intent:** Define the **skeleton of an algorithm** in a base class, letting subclasses override specific steps without changing the algorithm's structure.

### When to Use
- Frameworks with hooks (e.g. Spring's `AbstractController`).
- Common workflow with customisable steps.
- Avoiding code duplication in similar algorithms.

### Implementation — Java

```java
// Abstract class with template method
abstract class DataMiner {

    // Template method — defines the algorithm skeleton
    public final void mine(String source) {
        openSource(source);
        String raw = extractData();
        String parsed = parseData(raw);
        analyzeData(parsed);
        generateReport(parsed);
        closeSource();
    }

    // Steps that subclasses MUST implement
    protected abstract void openSource(String source);
    protected abstract String extractData();
    protected abstract void closeSource();

    // Steps with default implementations (hooks)
    protected String parseData(String raw) {
        System.out.println("Default parsing: trimming whitespace");
        return raw.trim();
    }

    protected void analyzeData(String data) {
        System.out.println("Analyzing " + data.length() + " characters");
    }

    private void generateReport(String data) {
        System.out.println("Report generated. Records: " + data.split(",").length);
    }
}

// Concrete implementations
class CSVDataMiner extends DataMiner {
    protected void openSource(String s) { System.out.println("Opening CSV: " + s); }
    protected String extractData() { return "Alice,Bob,Charlie"; }
    protected void closeSource() { System.out.println("Closing CSV"); }
}

class DatabaseDataMiner extends DataMiner {
    protected void openSource(String s) { System.out.println("Connecting to DB: " + s); }
    protected String extractData() { return "Row1,Row2,Row3,Row4"; }
    protected void closeSource() { System.out.println("Disconnecting from DB"); }

    @Override
    protected String parseData(String raw) {
        System.out.println("Custom DB parsing: converting ResultSet");
        return raw.toUpperCase();
    }
}

// Usage
new CSVDataMiner().mine("data.csv");
new DatabaseDataMiner().mine("jdbc:mysql://localhost/db");
```

---

## 6 Iterator Pattern

> **Intent:** Provide a way to access the elements of a collection **sequentially** without exposing its underlying representation.

### When to Use
- Traversing custom data structures (trees, graphs, linked lists).
- Supporting multiple traversal algorithms.
- Providing a uniform iteration interface.

### Implementation — Java

```java
// Custom collection with iterator
class NumberRange implements Iterable<Integer> {
    private final int start;
    private final int end;
    private final int step;

    public NumberRange(int start, int end, int step) {
        this.start = start;
        this.end = end;
        this.step = step;
    }

    @Override
    public Iterator<Integer> iterator() {
        return new Iterator<>() {
            private int current = start;

            @Override
            public boolean hasNext() {
                return current < end;
            }

            @Override
            public Integer next() {
                int val = current;
                current += step;
                return val;
            }
        };
    }
}

// Usage — works with for-each loop
NumberRange evens = new NumberRange(0, 20, 2);
for (int n : evens) {
    System.out.print(n + " ");  // 0 2 4 6 8 10 12 14 16 18
}

// Tree iterator example
class TreeNode<T> {
    T value;
    TreeNode<T> left, right;

    TreeNode(T val) { this.value = val; }
}

// In-order iterator for BST
class BSTIterator<T> implements Iterator<T> {
    private Deque<TreeNode<T>> stack = new ArrayDeque<>();

    public BSTIterator(TreeNode<T> root) {
        pushLeft(root);
    }

    private void pushLeft(TreeNode<T> node) {
        while (node != null) {
            stack.push(node);
            node = node.left;
        }
    }

    @Override
    public boolean hasNext() { return !stack.isEmpty(); }

    @Override
    public T next() {
        TreeNode<T> node = stack.pop();
        pushLeft(node.right);
        return node.value;
    }
}
```

---

## 7 State Pattern

> **Intent:** Allow an object to **alter its behaviour** when its internal state changes. The object will appear to change its class.

### When to Use
- Objects with state-dependent behaviour (TCP connection, vending machine, order status).
- Replacing complex state-based `if-else` chains.
- Finite state machines.

### Implementation — Java

```java
// State interface
interface OrderState {
    void next(Order order);
    void prev(Order order);
    void printStatus();
}

// Concrete states
class NewState implements OrderState {
    public void next(Order o) { o.setState(new PaidState()); }
    public void prev(Order o) { System.out.println("Already at initial state"); }
    public void printStatus() { System.out.println("Status: NEW"); }
}

class PaidState implements OrderState {
    public void next(Order o) { o.setState(new ShippedState()); }
    public void prev(Order o) { o.setState(new NewState()); }
    public void printStatus() { System.out.println("Status: PAID"); }
}

class ShippedState implements OrderState {
    public void next(Order o) { o.setState(new DeliveredState()); }
    public void prev(Order o) { o.setState(new PaidState()); }
    public void printStatus() { System.out.println("Status: SHIPPED"); }
}

class DeliveredState implements OrderState {
    public void next(Order o) { System.out.println("Order already delivered"); }
    public void prev(Order o) { System.out.println("Cannot go back from delivered"); }
    public void printStatus() { System.out.println("Status: DELIVERED ✓"); }
}

// Context
class Order {
    private OrderState state = new NewState();

    public void setState(OrderState state) { this.state = state; }
    public void nextState() { state.next(this); }
    public void prevState() { state.prev(this); }
    public void printStatus() { state.printStatus(); }
}

// Usage
Order order = new Order();
order.printStatus();   // Status: NEW
order.nextState();
order.printStatus();   // Status: PAID
order.nextState();
order.printStatus();   // Status: SHIPPED
order.nextState();
order.printStatus();   // Status: DELIVERED ✓
```

---

## 8 Mediator Pattern

> **Intent:** Define an object that encapsulates how a set of objects interact. Mediator promotes **loose coupling** by keeping objects from referring to each other explicitly.

### When to Use
- Chat rooms (users don't talk directly — the room mediates).
- Air traffic control (planes don't coordinate directly).
- Form validation (fields interact through a mediator).

### Implementation — Java

```java
// Mediator interface
interface ChatMediator {
    void sendMessage(String message, User sender);
    void addUser(User user);
}

// Concrete mediator
class ChatRoom implements ChatMediator {
    private List<User> users = new ArrayList<>();

    @Override
    public void addUser(User user) {
        users.add(user);
    }

    @Override
    public void sendMessage(String message, User sender) {
        for (User u : users) {
            if (u != sender) {  // don't send to self
                u.receive(message, sender.getName());
            }
        }
    }
}

// Colleague
abstract class User {
    protected ChatMediator mediator;
    protected String name;

    public User(ChatMediator mediator, String name) {
        this.mediator = mediator;
        this.name = name;
    }

    public String getName() { return name; }
    public abstract void send(String message);
    public abstract void receive(String message, String from);
}

class ChatUser extends User {
    public ChatUser(ChatMediator mediator, String name) {
        super(mediator, name);
    }

    @Override
    public void send(String message) {
        System.out.println(name + " sends: " + message);
        mediator.sendMessage(message, this);
    }

    @Override
    public void receive(String message, String from) {
        System.out.println(name + " received from " + from + ": " + message);
    }
}

// Usage
ChatRoom room = new ChatRoom();
User alice = new ChatUser(room, "Alice");
User bob   = new ChatUser(room, "Bob");
User carol = new ChatUser(room, "Carol");
room.addUser(alice);
room.addUser(bob);
room.addUser(carol);

alice.send("Hello everyone!");
// Alice sends: Hello everyone!
// Bob received from Alice: Hello everyone!
// Carol received from Alice: Hello everyone!
```

---

## 9 Memento Pattern

> **Intent:** Capture and externalise an object's internal state without violating encapsulation, so the object can be **restored to this state later**.

### When to Use
- Undo/redo (complements Command pattern).
- Saving game state / checkpoints.
- Transaction rollback.
- Browser back button (page state snapshots).

### Implementation — Java

```java
// Memento — snapshot of state
class EditorMemento {
    private final String content;
    private final int cursorPos;
    private final LocalDateTime timestamp;

    public EditorMemento(String content, int cursorPos) {
        this.content   = content;
        this.cursorPos = cursorPos;
        this.timestamp = LocalDateTime.now();
    }

    // Package-private — only the originator should access these
    String getContent()   { return content; }
    int getCursorPos()    { return cursorPos; }
    LocalDateTime getTimestamp() { return timestamp; }
}

// Originator — the object whose state we want to save
class TextEditor {
    private String content = "";
    private int cursorPos = 0;

    public void type(String text) {
        content = content.substring(0, cursorPos) + text +
                  content.substring(cursorPos);
        cursorPos += text.length();
    }

    public EditorMemento save() {
        return new EditorMemento(content, cursorPos);
    }

    public void restore(EditorMemento m) {
        this.content   = m.getContent();
        this.cursorPos = m.getCursorPos();
    }

    public String getContent() { return content; }
}

// Caretaker — manages memento history
class History {
    private Deque<EditorMemento> snapshots = new ArrayDeque<>();

    public void push(EditorMemento m) { snapshots.push(m); }

    public EditorMemento pop() {
        return snapshots.isEmpty() ? null : snapshots.pop();
    }
}

// Usage
TextEditor editor = new TextEditor();
History history = new History();

editor.type("Hello");
history.push(editor.save());    // save state

editor.type(" World");
history.push(editor.save());    // save state

editor.type("!!!");
System.out.println(editor.getContent());  // "Hello World!!!"

editor.restore(history.pop());
System.out.println(editor.getContent());  // "Hello World"

editor.restore(history.pop());
System.out.println(editor.getContent());  // "Hello"
```

---

## 10 Visitor Pattern

> **Intent:** Represent an **operation to be performed** on the elements of an object structure. Visitor lets you define a new operation without changing the classes of the elements on which it operates.

### When to Use
- Adding new operations to existing class hierarchies without modifying them.
- Compilers: AST traversal (type checker, code generator — each is a visitor).
- File system operations (size calculator, virus scanner, indexer).
- Exporting data in different formats (JSON, XML, CSV).

### Implementation — Java

```java
// Element interface
interface Shape {
    void accept(ShapeVisitor visitor);
}

class CircleShape implements Shape {
    double radius;
    public CircleShape(double r) { this.radius = r; }
    public void accept(ShapeVisitor v) { v.visit(this); }
}

class RectangleShape implements Shape {
    double width, height;
    public RectangleShape(double w, double h) { this.width = w; this.height = h; }
    public void accept(ShapeVisitor v) { v.visit(this); }
}

class TriangleShape implements Shape {
    double base, height;
    public TriangleShape(double b, double h) { this.base = b; this.height = h; }
    public void accept(ShapeVisitor v) { v.visit(this); }
}

// Visitor interface
interface ShapeVisitor {
    void visit(CircleShape c);
    void visit(RectangleShape r);
    void visit(TriangleShape t);
}

// Concrete visitors — new operations without modifying Shape classes
class AreaCalculator implements ShapeVisitor {
    private double totalArea = 0;

    public void visit(CircleShape c) {
        totalArea += Math.PI * c.radius * c.radius;
    }
    public void visit(RectangleShape r) {
        totalArea += r.width * r.height;
    }
    public void visit(TriangleShape t) {
        totalArea += 0.5 * t.base * t.height;
    }

    public double getTotalArea() { return totalArea; }
}

class SVGExporter implements ShapeVisitor {
    StringBuilder svg = new StringBuilder("<svg>\n");

    public void visit(CircleShape c) {
        svg.append(String.format("  <circle r='%.1f'/>\n", c.radius));
    }
    public void visit(RectangleShape r) {
        svg.append(String.format("  <rect w='%.1f' h='%.1f'/>\n", r.width, r.height));
    }
    public void visit(TriangleShape t) {
        svg.append(String.format("  <polygon base='%.1f' h='%.1f'/>\n", t.base, t.height));
    }

    public String export() { return svg.append("</svg>").toString(); }
}

// Usage
List<Shape> shapes = List.of(
    new CircleShape(5),
    new RectangleShape(4, 6),
    new TriangleShape(3, 8)
);

AreaCalculator calc = new AreaCalculator();
shapes.forEach(s -> s.accept(calc));
System.out.printf("Total area: %.2f%n", calc.getTotalArea());

SVGExporter exporter = new SVGExporter();
shapes.forEach(s -> s.accept(exporter));
System.out.println(exporter.export());
```

---

## Summary

| Pattern | Key Idea | Use When |
|---|---|---|
| **Observer** | One-to-many notification | Events, pub-sub, data binding |
| **Strategy** | Swappable algorithms | Payment, sorting, routing |
| **Command** | Request as object | Undo/redo, queues, macros |
| **Chain of Responsibility** | Pass request along a chain | Middleware, approval flows |
| **Template Method** | Algorithm skeleton with customisable steps | Frameworks, workflows |
| **Iterator** | Sequential access without exposing internals | Custom collections, trees |
| **State** | Behaviour changes with internal state | Order status, FSMs |
| **Mediator** | Central hub for object interaction | Chat rooms, UI controllers |
| **Memento** | Snapshot & restore state | Undo, checkpoints, rollback |
| **Visitor** | Add operations without modifying classes | Compilers, exporters |
