# Structural Design Patterns

Structural patterns explain how classes and objects are **combined to form larger structures**. They use **inheritance** and **composition** to simplify relationships between components and improve code flexibility.

---

## 1 Adapter Pattern

> **Intent:** Convert the interface of a class into another interface that clients expect. Adapter lets classes work together that couldn't otherwise because of incompatible interfaces.

Also known as **Wrapper**.

### When to Use
- Integrating a third-party library with an incompatible interface.
- Working with legacy code that can't be modified.
- Unifying disparate interfaces behind a common one.

### Structure

```
┌──────────┐       ┌───────────┐       ┌──────────┐
│  Client   │──────▶│  Target    │       │ Adaptee  │
│           │       │(interface) │       │(existing)│
└──────────┘       └─────┬─────┘       └─────┬────┘
                         │                    │
                   ┌─────┴─────┐              │
                   │  Adapter   │─────────────┘
                   │ (wraps)    │   delegates calls
                   └────────────┘
```

### Implementation — Java

```java
// Existing (incompatible) service — the Adaptee
class LegacyPrinter {
    public void printDocument(String text, int copies) {
        for (int i = 0; i < copies; i++)
            System.out.println("[Legacy] " + text);
    }
}

// Target interface (what our code expects)
interface ModernPrinter {
    void print(String text);
}

// Adapter
class PrinterAdapter implements ModernPrinter {
    private final LegacyPrinter legacyPrinter;

    public PrinterAdapter(LegacyPrinter legacyPrinter) {
        this.legacyPrinter = legacyPrinter;
    }

    @Override
    public void print(String text) {
        legacyPrinter.printDocument(text, 1);  // adapt the call
    }
}

// Real-world: adapting a JSON library to your internal API
interface DataParser {
    Map<String, Object> parse(String input);
}

// Adapter for Jackson
class JacksonAdapter implements DataParser {
    private final ObjectMapper mapper = new ObjectMapper();

    @Override
    public Map<String, Object> parse(String input) {
        try {
            return mapper.readValue(input, Map.class);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}

// Adapter for Gson
class GsonAdapter implements DataParser {
    private final Gson gson = new Gson();

    @Override
    public Map<String, Object> parse(String input) {
        return gson.fromJson(input, Map.class);
    }
}

// Client code — works with any parser
DataParser parser = new JacksonAdapter();
Map<String, Object> data = parser.parse("{\"name\": \"Alice\"}");
```

---

## 2 Decorator Pattern

> **Intent:** Attach **additional responsibilities** to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality.

### When to Use
- Adding behaviour at runtime without modifying existing classes.
- Java I/O streams (`BufferedReader(new FileReader(...))`) use this pattern.
- Logging, encryption, compression layers.

### Structure

```
┌────────────┐      ┌────────────────┐
│ Component   │◄─────│ Decorator      │
│ (interface) │      │ (abstract)     │
└──────┬─────┘      │ -component     │
       │             └───────┬────────┘
┌──────┴──────┐         ┌───┴───────────┐
│ Concrete    │         │ConcreteDecorA  │
│ Component   │         │ConcreteDecorB  │
└─────────────┘         └────────────────┘
```

### Implementation — Java

```java
// Component interface
interface Coffee {
    String getDescription();
    double getCost();
}

// Concrete component
class SimpleCoffee implements Coffee {
    public String getDescription() { return "Simple coffee"; }
    public double getCost() { return 2.00; }
}

// Base decorator
abstract class CoffeeDecorator implements Coffee {
    protected final Coffee wrapped;

    public CoffeeDecorator(Coffee coffee) {
        this.wrapped = coffee;
    }

    public String getDescription() { return wrapped.getDescription(); }
    public double getCost() { return wrapped.getCost(); }
}

// Concrete decorators
class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee coffee) { super(coffee); }

    @Override
    public String getDescription() {
        return wrapped.getDescription() + ", milk";
    }
    @Override
    public double getCost() {
        return wrapped.getCost() + 0.50;
    }
}

class SugarDecorator extends CoffeeDecorator {
    public SugarDecorator(Coffee coffee) { super(coffee); }

    @Override
    public String getDescription() {
        return wrapped.getDescription() + ", sugar";
    }
    @Override
    public double getCost() {
        return wrapped.getCost() + 0.25;
    }
}

class WhipCreamDecorator extends CoffeeDecorator {
    public WhipCreamDecorator(Coffee coffee) { super(coffee); }

    @Override
    public String getDescription() {
        return wrapped.getDescription() + ", whip cream";
    }
    @Override
    public double getCost() {
        return wrapped.getCost() + 0.75;
    }
}

// Usage — decorators compose at runtime
Coffee order = new WhipCreamDecorator(
                   new MilkDecorator(
                       new SimpleCoffee()));

System.out.println(order.getDescription());  // Simple coffee, milk, whip cream
System.out.println("$" + order.getCost());   // $3.25
```

---

## 3 Facade Pattern

> **Intent:** Provide a **simplified interface** to a complex subsystem. The facade doesn't add new functionality — it just makes the subsystem easier to use.

### When to Use
- Simplifying interaction with complex libraries / APIs.
- Providing a single entry point for a layer (e.g. service layer in a web app).
- Decoupling client code from subsystem internals.

### Implementation — Java

```java
// Complex subsystem classes
class VideoDecoder {
    public void decode(String file) {
        System.out.println("Decoding video: " + file);
    }
}

class AudioDecoder {
    public void decode(String file) {
        System.out.println("Decoding audio: " + file);
    }
}

class SubtitleLoader {
    public void load(String file) {
        System.out.println("Loading subtitles: " + file);
    }
}

class VideoRenderer {
    public void render() { System.out.println("Rendering video on screen"); }
}

// Facade — simple interface
class MediaPlayer {
    private VideoDecoder videoDecoder = new VideoDecoder();
    private AudioDecoder audioDecoder = new AudioDecoder();
    private SubtitleLoader subtitleLoader = new SubtitleLoader();
    private VideoRenderer renderer = new VideoRenderer();

    public void play(String file) {
        System.out.println("--- Playing: " + file + " ---");
        videoDecoder.decode(file);
        audioDecoder.decode(file);
        subtitleLoader.load(file.replace(".mp4", ".srt"));
        renderer.render();
    }
}

// Client — simple!
MediaPlayer player = new MediaPlayer();
player.play("movie.mp4");
```

---

## 4 Composite Pattern

> **Intent:** Compose objects into **tree structures** to represent part-whole hierarchies. Composite lets clients treat individual objects and compositions **uniformly**.

### When to Use
- File system (files and folders).
- GUI (a panel contains buttons, which are also components).
- Organisation hierarchies (employee → team → department).

### Implementation — Java

```java
// Component
interface FileSystemItem {
    String getName();
    long getSize();
    void display(String indent);
}

// Leaf
class File implements FileSystemItem {
    private String name;
    private long size;

    public File(String name, long size) {
        this.name = name;
        this.size = size;
    }

    public String getName() { return name; }
    public long getSize() { return size; }
    public void display(String indent) {
        System.out.println(indent + "📄 " + name + " (" + size + " bytes)");
    }
}

// Composite
class Folder implements FileSystemItem {
    private String name;
    private List<FileSystemItem> children = new ArrayList<>();

    public Folder(String name) { this.name = name; }

    public void add(FileSystemItem item) { children.add(item); }
    public void remove(FileSystemItem item) { children.remove(item); }

    public String getName() { return name; }

    public long getSize() {
        return children.stream()
                .mapToLong(FileSystemItem::getSize)
                .sum();
    }

    public void display(String indent) {
        System.out.println(indent + "📁 " + name + " (" + getSize() + " bytes)");
        for (FileSystemItem child : children)
            child.display(indent + "  ");
    }
}

// Usage
Folder root = new Folder("project");
Folder src = new Folder("src");
src.add(new File("Main.java", 2048));
src.add(new File("Utils.java", 1024));
root.add(src);
root.add(new File("README.md", 512));
root.add(new File("pom.xml", 768));

root.display("");
// 📁 project (4352 bytes)
//   📁 src (3072 bytes)
//     📄 Main.java (2048 bytes)
//     📄 Utils.java (1024 bytes)
//   📄 README.md (512 bytes)
//   📄 pom.xml (768 bytes)
```

---

## 5 Proxy Pattern

> **Intent:** Provide a **surrogate or placeholder** for another object to control access to it.

### Types of Proxy

| Type | Purpose |
|---|---|
| **Virtual Proxy** | Delays expensive object creation (lazy loading) |
| **Protection Proxy** | Controls access based on permissions |
| **Remote Proxy** | Represents an object in a different address space (RPC) |
| **Caching Proxy** | Caches results of expensive operations |
| **Logging Proxy** | Adds logging around method calls |

### Implementation — Java

```java
// Subject interface
interface Image {
    void display();
}

// Real (expensive) subject
class HighResImage implements Image {
    private String filename;

    public HighResImage(String filename) {
        this.filename = filename;
        loadFromDisk();   // expensive!
    }

    private void loadFromDisk() {
        System.out.println("Loading high-res image: " + filename + " (3 seconds)...");
    }

    @Override
    public void display() {
        System.out.println("Displaying: " + filename);
    }
}

// Virtual Proxy — delays loading until display() is called
class ImageProxy implements Image {
    private String filename;
    private HighResImage realImage;  // lazy

    public ImageProxy(String filename) {
        this.filename = filename;
        // No loading here!
    }

    @Override
    public void display() {
        if (realImage == null) {
            realImage = new HighResImage(filename);  // load on first use
        }
        realImage.display();
    }
}

// Protection Proxy — access control
class SecureImageProxy implements Image {
    private Image realImage;
    private String userRole;

    public SecureImageProxy(Image image, String role) {
        this.realImage = image;
        this.userRole  = role;
    }

    @Override
    public void display() {
        if ("ADMIN".equals(userRole)) {
            realImage.display();
        } else {
            System.out.println("Access denied for role: " + userRole);
        }
    }
}

// Usage
Image img1 = new ImageProxy("photo1.jpg");  // no loading yet
Image img2 = new ImageProxy("photo2.jpg");  // no loading yet

img1.display();  // NOW loads and displays photo1
img1.display();  // already loaded, just displays
```

---

## 6 Bridge Pattern

> **Intent:** Decouple an **abstraction** from its **implementation** so that the two can vary independently.

### When to Use
- When you want to avoid a cartesian product of classes (e.g. 3 shapes × 3 renderers = 9 classes without Bridge).
- Switching implementations at runtime.
- Cross-platform rendering, device drivers.

### Structure

```
┌─────────────┐        ┌───────────────┐
│ Abstraction │ has-a  │ Implementor   │
│             │───────▶│ (interface)   │
└──────┬──────┘        └───────┬───────┘
       │                       │
┌──────┴──────┐    ┌───────────┴──────────┐
│ Refined     │    │ ConcreteImplementorA  │
│ Abstraction │    │ ConcreteImplementorB  │
└─────────────┘    └──────────────────────┘
```

### Implementation — Java

```java
// Implementor — rendering engine
interface Renderer {
    void renderCircle(float x, float y, float radius);
    void renderRect(float x, float y, float w, float h);
}

class SVGRenderer implements Renderer {
    public void renderCircle(float x, float y, float r) {
        System.out.printf("<circle cx='%.0f' cy='%.0f' r='%.0f'/>\n", x, y, r);
    }
    public void renderRect(float x, float y, float w, float h) {
        System.out.printf("<rect x='%.0f' y='%.0f' w='%.0f' h='%.0f'/>\n", x, y, w, h);
    }
}

class CanvasRenderer implements Renderer {
    public void renderCircle(float x, float y, float r) {
        System.out.printf("canvas.drawCircle(%.0f, %.0f, %.0f)\n", x, y, r);
    }
    public void renderRect(float x, float y, float w, float h) {
        System.out.printf("canvas.drawRect(%.0f, %.0f, %.0f, %.0f)\n", x, y, w, h);
    }
}

// Abstraction — Shape
abstract class Shape {
    protected Renderer renderer;  // bridge

    public Shape(Renderer renderer) {
        this.renderer = renderer;
    }

    abstract void draw();
}

// Refined abstractions
class Circle extends Shape {
    private float x, y, radius;

    public Circle(Renderer r, float x, float y, float radius) {
        super(r);
        this.x = x; this.y = y; this.radius = radius;
    }

    void draw() { renderer.renderCircle(x, y, radius); }
}

class Rectangle extends Shape {
    private float x, y, w, h;

    public Rectangle(Renderer r, float x, float y, float w, float h) {
        super(r);
        this.x = x; this.y = y; this.w = w; this.h = h;
    }

    void draw() { renderer.renderRect(x, y, w, h); }
}

// Usage — mix and match independently
Renderer svg = new SVGRenderer();
Renderer canvas = new CanvasRenderer();

Shape c1 = new Circle(svg, 10, 20, 5);
Shape c2 = new Circle(canvas, 10, 20, 5);  // same shape, different renderer

c1.draw();  // <circle cx='10' cy='20' r='5'/>
c2.draw();  // canvas.drawCircle(10, 20, 5)
```

---

## 7 Flyweight Pattern

> **Intent:** Use **sharing** to support large numbers of fine-grained objects efficiently. Store shared state (**intrinsic**) separately from unique state (**extrinsic**).

### When to Use
- Rendering millions of characters in a text editor (share font/style objects).
- Game particles, tiles, map cells.
- Caching immutable objects (e.g. `Integer.valueOf()` in Java).

### Implementation — Java

```java
// Flyweight (intrinsic state = shared)
class TreeType {
    private final String name;
    private final String color;
    private final String texture;   // heavy resource

    public TreeType(String name, String color, String texture) {
        this.name    = name;
        this.color   = color;
        this.texture = texture;
        System.out.println("  Creating TreeType: " + name);
    }

    public void draw(int x, int y) {
        System.out.printf("  Drawing %s tree at (%d,%d)%n", name, x, y);
    }
}

// Flyweight factory — ensures sharing
class TreeTypeFactory {
    private static Map<String, TreeType> cache = new HashMap<>();

    public static TreeType get(String name, String color, String texture) {
        String key = name + ":" + color + ":" + texture;
        return cache.computeIfAbsent(key,
            k -> new TreeType(name, color, texture));
    }
}

// Context (extrinsic state = unique per instance)
class Tree {
    private int x, y;              // unique per tree
    private TreeType type;          // shared

    public Tree(int x, int y, TreeType type) {
        this.x = x; this.y = y; this.type = type;
    }

    public void draw() { type.draw(x, y); }
}

// Usage — a forest with 1 million trees but only a few TreeType objects
class Forest {
    private List<Tree> trees = new ArrayList<>();

    public void plantTree(int x, int y, String name, String color, String texture) {
        TreeType type = TreeTypeFactory.get(name, color, texture);
        trees.add(new Tree(x, y, type));
    }

    public void draw() {
        trees.forEach(Tree::draw);
    }
}

Forest forest = new Forest();
// Plants 10,000 trees but only creates ~3 TreeType objects
for (int i = 0; i < 10_000; i++) {
    String[] types = {"Oak", "Pine", "Birch"};
    String t = types[i % 3];
    forest.plantTree(i * 10, i * 5, t, "green", t + ".png");
}
// Creating TreeType: Oak      ← only 3 flyweight objects
// Creating TreeType: Pine
// Creating TreeType: Birch
```

---

## Summary

| Pattern | Key Idea | Use When |
|---|---|---|
| **Adapter** | Convert interface A → interface B | Integrating incompatible APIs |
| **Decorator** | Add behaviour dynamically, wrap layers | I/O streams, middleware |
| **Facade** | Simplify complex subsystem | Service layer, library wrappers |
| **Composite** | Tree structure, uniform leaf/branch API | File systems, UI hierarchies |
| **Proxy** | Surrogate controlling access | Lazy loading, security, caching |
| **Bridge** | Separate abstraction from implementation | Cross-platform, renderers |
| **Flyweight** | Share intrinsic state across instances | Massive object counts |
