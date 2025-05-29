# Creation Pattern
## 1. Singleton 

Only one object is instantiated from a particular class.

```java
public class Singleton {
    private static Singleton instance;

    private Singleton() {} // private constructor

    public static Singleton getInstance() {
        if (instance == null) {
            instance = new Singleton();
        }
        return instance;
    }
}

```


There are two ways of creating a singleton class
1. Eager Initialization
2. Lazy Initialization

| Aspect                       | Eager Initialization                                                                | Lazy Initialization                                                         |
| ---------------------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **When Instance is Created** | At application startup or when the class is loaded.                                 | Only when the instance is first requested/accessed.                         |
| **Resource Usage**           | May use resources unnecessarily if the instance is never used.                      | Saves resources by creating the instance only if/when needed.               |
| **Startup Time**             | Can increase startup time, especially if the instance is heavy or has dependencies. | Reduces startup time, as instantiation is deferred until required.          |
| **Thread Safety**            | Simple to implement and inherently thread-safe (since instance is created early).   | Requires careful handling to be thread-safe in multi-threaded environments. |
| **Use Cases**                | When the instance is always needed or must be ready immediately.                    | When the instance is heavy or may not be needed in every execution path.    |
## 2. Abstract Factory
The Abstract Factory pattern is a creational design pattern that provides an interface for creating families of related or dependent objects without specifying their concrete classes. It acts as a "factory of factories," allowing you to produce sets of related objects that are designed to work together, while keeping the client code independent of the actual product classes.

### Key Concepts
- **Abstract Factory:** Declares methods to create abstract products (interfaces or abstract classes).
- **Concrete Factory:** Implements the abstract factory, producing concrete products of a specific family.
- **Abstract Product:** Interface or abstract class for a type of product.
- **Concrete Product:** Specific implementation of an abstract product.
- **Client:** Uses only the interfaces/factories, never directly instantiates products

### When to Use
- When your code needs to work with various families of related products (e.g., UI components for different operating systems).
- When you want to enforce that products from one family are used together.
- When you want to avoid binding your code to specific classes.

### Example Scenario: GUI Toolkit

Suppose you want to build a cross-platform GUI library that supports both Windows and macOS. Each platform has its own style of buttons and checkboxes. The Abstract Factory pattern allows you to create a family of related objects (WindowsButton, WindowsCheckbox, MacButton, MacCheckbox) without specifying their concrete classes in the client code.

```java
// Abstract Products
interface Button {
    void paint();
}

interface Checkbox {
    void paint();
}

// Concrete Products (Windows)
class WindowsButton implements Button {
    public void paint() {
        System.out.println("Rendering Windows Button");
    }
}

class WindowsCheckbox implements Checkbox {
    public void paint() {
        System.out.println("Rendering Windows Checkbox");
    }
}

// Concrete Products (Mac)
class MacButton implements Button {
    public void paint() {
        System.out.println("Rendering Mac Button");
    }
}

class MacCheckbox implements Checkbox {
    public void paint() {
        System.out.println("Rendering Mac Checkbox");
    }
}

// Abstract Factory
interface GUIFactory {
    Button createButton();
    Checkbox createCheckbox();
}

// Concrete Factories
class WindowsFactory implements GUIFactory {
    public Button createButton() {
        return new WindowsButton();
    }
    public Checkbox createCheckbox() {
        return new WindowsCheckbox();
    }
}

class MacFactory implements GUIFactory {
    public Button createButton() {
        return new MacButton();
    }
    public Checkbox createCheckbox() {
        return new MacCheckbox();
    }
}

// Client Code
class Application {
    private Button button;
    private Checkbox checkbox;

    public Application(GUIFactory factory) {
        button = factory.createButton();
        checkbox = factory.createCheckbox();
    }

    public void paint() {
        button.paint();
        checkbox.paint();
    }
}

// Usage
public class Main {
    public static void main(String[] args) {
        GUIFactory factory = new WindowsFactory(); // or new MacFactory()
        Application app = new Application(factory);
        app.paint();
    }
}

```

---
# Structural Patterns
## 1. Adapter
The Adapter pattern is a structural design pattern that allows objects with incompatible interfaces to work together. It acts as a bridge or wrapper between two incompatible interfaces, converting the interface of a class into another interface that a client expects.

### When to Use
- When you want to use an existing class, but its interface does not match the one you need.
- When you want to integrate third-party or legacy code into your system without modifying their source code.
- When you want to enable classes to work together that otherwise couldn’t due to incompatible interfaces.

### How It Works
- The Adapter implements the interface expected by the client (the "Target" interface).
- It internally uses (wraps) an instance of the class with the incompatible interface (the "Adaptee").
- The Adapter translates calls from the client to the appropriate calls on the Adaptee.

### Types of Adapter Pattern in Java
- **Object Adapter:** Uses composition; the adapter contains an instance of the adaptee.
- **Class Adapter:** Uses inheritance; the adapter inherits from both the target interface and the adaptee class (limited by Java’s single inheritance).

#### Real-World Example
A card reader acts as an adapter between a memory card and a laptop. The memory card cannot be directly plugged into the laptop, but the card reader allows the laptop to read the card.

### Java Example (Object Adapter)
Suppose you have a `Socket` that produces 120V and you need to charge a mobile that requires 3V.

```java
// Existing class (Adaptee)
public class Socket {
    public int getVolt() {
        return 120;
    }
}

// Target interface
public interface SocketAdapter {
    int get3Volt();
    int get12Volt();
    int get120Volt();
}

// Adapter implementation using composition
public class SocketObjectAdapterImpl implements SocketAdapter {
    private Socket socket = new Socket();

    @Override
    public int get3Volt() {
        return convertVolt(socket.getVolt(), 40);
    }

    @Override
    public int get12Volt() {
        return convertVolt(socket.getVolt(), 10);
    }

    @Override
    public int get120Volt() {
        return socket.getVolt();
    }

    private int convertVolt(int v, int i) {
        return v / i;
    }
}

// Client code
public class Main {
    public static void main(String[] args) {
        SocketAdapter adapter = new SocketObjectAdapterImpl();
        System.out.println("3V output: " + adapter.get3Volt());
        System.out.println("12V output: " + adapter.get12Volt());
        System.out.println("120V output: " + adapter.get120Volt());
    }
}

```

**Summary Table**

| Role    | Description                                       |
| ------- | ------------------------------------------------- |
| Target  | The interface expected by the client              |
| Adaptee | The existing class with incompatible interface    |
| Adapter | Bridges Target and Adaptee, translating calls     |
| Client  | Uses the Target interface, unaware of the Adaptee |

## 2. Facade
The Facade pattern is a structural design pattern that provides a simplified, unified interface to a complex subsystem of classes, libraries, or APIs. It acts as a front-facing interface that hides the complexities of the underlying system, making it easier for clients to interact with it.

### Purpose and Use Cases
- Simplifies the use of complex systems by exposing only the functionality that clients need.
- Decouples client code from the internal workings of subsystems, improving maintainability and flexibility.
- Useful when working with third-party libraries or legacy code that is difficult to use directly.

### How It Works
- The **Facade** class is created as a single entry point for the client.
- The Facade contains references to the subsystem classes and delegates client requests to the appropriate subsystem methods.
- The client interacts only with the Facade, not with the subsystem classes directly

### Example in Java
Here’s a clear and practical example using an **order placement system**. This demonstrates how the Facade pattern simplifies client interaction with multiple subsystems (Payment, Inventory, Shipping).

```java
class PaymentService {
    public void processPayment(Order order) {
        System.out.println("Processing payment for order: " + order.getId());
    }
}

class InventoryService {
    public boolean checkAvailability(Order order) {
        System.out.println("Checking inventory for order: " + order.getId());
        return true; // Assume always available for simplicity
    }
}

class ShippingService {
    public void shipOrder(Order order) {
        System.out.println("Shipping order: " + order.getId());
    }
}

class Order {
    private final String id;
    public Order(String id) { this.id = id; }
    public String getId() { return id; }
}

public class OrderFacade {
    private final PaymentService paymentService;
    private final InventoryService inventoryService;
    private final ShippingService shippingService;

    public OrderFacade() {
        paymentService = new PaymentService();
        inventoryService = new InventoryService();
        shippingService = new ShippingService();
    }

    public void placeOrder(Order order) {
        if (inventoryService.checkAvailability(order)) {
            paymentService.processPayment(order);
            shippingService.shipOrder(order);
            System.out.println("Order placed successfully!");
        } else {
            System.out.println("Order cannot be placed. Items are out of stock.");
        }
    }
}


```

Main.java
```java
public class Main {
    public static void main(String[] args) {
        Order order = new Order("A123");
        OrderFacade orderFacade = new OrderFacade();
        orderFacade.placeOrder(order);
    }
}
```

## 3. Flyweight Design Pattern
The **Flyweight pattern** is a structural design pattern focused on minimizing memory usage by sharing as much data as possible between similar objects. It is especially useful when you need to create a large number of objects that share common properties, and the cost of storing all of them individually would be prohibitive.

## Key Concepts
- **Intrinsic State:** Shared, immutable data stored inside the Flyweight object (e.g., color, shape type).
- **Extrinsic State:** Context-specific, mutable data passed in by the client (e.g., position, size).
- **Flyweight:** The shared object containing intrinsic state.
- **Flyweight Factory:** Manages and returns shared Flyweight objects, ensuring reuse.
- **Client:** Uses Flyweight objects and supplies extrinsic state as needed.

## How It Works
1. **Divide Object State:** Separate object properties into intrinsic (shared) and extrinsic (unique per use).
2. **Flyweight Factory:** When a client requests an object, the factory checks if a Flyweight with the required intrinsic state exists:
    - If yes, returns the existing object.
    - If no, creates, caches, and returns a new Flyweight.
3. **Client Supplies Extrinsic State:** The client provides extrinsic state when using the Flyweight, so the object can behave correctly in its context.

## Example: Drawing Shapes
Suppose you are drawing thousands of circles and lines, many with the same color or fill property. Instead of creating a new object for each, the Flyweight pattern allows you to reuse objects that share the same intrinsic state.

#### Base Class
```java
// Intrinsic state: color (shared)
abstract class ShapeFlyweight {
    protected final String color;
    public ShapeFlyweight(String color) {
        this.color = color;
    }
    public abstract void draw(int x, int y); // Extrinsic: position
}

```

#### Concrete Flyweights
```java
class CircleFlyweight extends ShapeFlyweight {
    public CircleFlyweight(String color) {
        super(color);
    }
    @Override
    public void draw(int x, int y) {
        System.out.println("Drawing " + color + " circle at (" + x + ", " + y + ")");
    }
}

```

#### Flyweight Factory
```java
import java.util.*;

class ShapeFactory {
    private static final Map<String, ShapeFlyweight> circleMap = new HashMap<>();
    public static ShapeFlyweight getCircle(String color) {
        ShapeFlyweight circle = circleMap.get(color);
        if (circle == null) {
            circle = new CircleFlyweight(color);
            circleMap.put(color, circle);
        }
        return circle;
    }
}

```

#### Client Side
```java
public class Main {
    public static void main(String[] args) {
        ShapeFlyweight redCircle1 = ShapeFactory.getCircle("red");
        ShapeFlyweight redCircle2 = ShapeFactory.getCircle("red");
        ShapeFlyweight blueCircle = ShapeFactory.getCircle("blue");

        redCircle1.draw(10, 20); // extrinsic state: position
        redCircle2.draw(30, 40);
        blueCircle.draw(50, 60);

        System.out.println(redCircle1 == redCircle2); // true, same object reused
    }
}

```

## Key Points
- **Intrinsic state** (e.g., color) is stored in the Flyweight and shared.
- **Extrinsic state** (e.g., position) is supplied by the client at runtime.
- The **factory** ensures that only one object per intrinsic state is created and reused

---
## 3. Behavioral Patterns

