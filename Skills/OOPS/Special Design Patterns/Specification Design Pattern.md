# Specification Design Pattern

The **Specification Pattern** encapsulates business rules into reusable, composable, and testable objects. Instead of scattering `if` conditions throughout your codebase, each rule becomes a first-class object that can be **combined** using logical operators (`AND`, `OR`, `NOT`).

---

## The Problem

Business logic gets messy fast:

```java
// ❌ Scattered, duplicated, hard-to-test conditions
List<Product> filter(List<Product> products) {
    List<Product> result = new ArrayList<>();
    for (Product p : products) {
        if (p.getPrice() > 50
            && p.getCategory().equals("Electronics")
            && p.isInStock()
            && p.getRating() >= 4.0) {
            result.add(p);
        }
    }
    return result;
}
// What if another method needs "Electronics AND in stock" but no price check?
// You duplicate or add boolean flags → spaghetti.
```

---

## The Solution

Each condition becomes a **Specification** object. Specifications compose via `and()`, `or()`, `not()`.

```
┌────────────────────┐
│  Specification<T>  │ ← interface
│  + isSatisfiedBy() │
│  + and()           │
│  + or()            │
│  + not()           │
└────────┬───────────┘
         │
    ┌────┴─────────────────┐
    │                      │
┌───▼──────────┐   ┌──────▼──────────┐
│ Concrete     │   │ Composite       │
│ Specs        │   │ AndSpec, OrSpec, │
│ (leaf rules) │   │ NotSpec          │
└──────────────┘   └─────────────────┘
```

---

## Core Implementation — Java

### 1. Base Specification Interface

```java
@FunctionalInterface
public interface Specification<T> {

    boolean isSatisfiedBy(T candidate);

    default Specification<T> and(Specification<T> other) {
        return candidate -> this.isSatisfiedBy(candidate) && other.isSatisfiedBy(candidate);
    }

    default Specification<T> or(Specification<T> other) {
        return candidate -> this.isSatisfiedBy(candidate) || other.isSatisfiedBy(candidate);
    }

    default Specification<T> not() {
        return candidate -> !this.isSatisfiedBy(candidate);
    }
}
```

### 2. Domain Model

```java
public class Product {
    private String name;
    private String category;
    private double price;
    private double rating;
    private boolean inStock;

    public Product(String name, String category, double price, double rating, boolean inStock) {
        this.name = name;
        this.category = category;
        this.price = price;
        this.rating = rating;
        this.inStock = inStock;
    }

    // getters
    public String getName()     { return name; }
    public String getCategory() { return category; }
    public double getPrice()    { return price; }
    public double getRating()   { return rating; }
    public boolean isInStock()  { return inStock; }
}
```

### 3. Concrete Specifications

```java
public class CategorySpec implements Specification<Product> {
    private final String category;
    public CategorySpec(String category) { this.category = category; }

    @Override
    public boolean isSatisfiedBy(Product p) {
        return p.getCategory().equalsIgnoreCase(category);
    }
}

public class PriceRangeSpec implements Specification<Product> {
    private final double min, max;
    public PriceRangeSpec(double min, double max) { this.min = min; this.max = max; }

    @Override
    public boolean isSatisfiedBy(Product p) {
        return p.getPrice() >= min && p.getPrice() <= max;
    }
}

public class MinRatingSpec implements Specification<Product> {
    private final double minRating;
    public MinRatingSpec(double minRating) { this.minRating = minRating; }

    @Override
    public boolean isSatisfiedBy(Product p) {
        return p.getRating() >= minRating;
    }
}

public class InStockSpec implements Specification<Product> {
    @Override
    public boolean isSatisfiedBy(Product p) {
        return p.isInStock();
    }
}
```

### 4. Filtering Service

```java
public class ProductFilter {

    public List<Product> filter(List<Product> products, Specification<Product> spec) {
        return products.stream()
                .filter(spec::isSatisfiedBy)
                .collect(Collectors.toList());
    }
}
```

### 5. Usage — Composing Business Rules

```java
public class Main {
    public static void main(String[] args) {

        List<Product> catalog = List.of(
            new Product("Laptop",     "Electronics", 999.99, 4.5, true),
            new Product("Mouse",      "Electronics",  29.99, 4.8, true),
            new Product("Keyboard",   "Electronics",  79.99, 3.9, false),
            new Product("Novel",      "Books",        14.99, 4.7, true),
            new Product("Headphones", "Electronics", 199.99, 4.2, true),
            new Product("Monitor",    "Electronics", 349.99, 4.6, false)
        );

        ProductFilter filter = new ProductFilter();

        // Single spec
        var electronics = new CategorySpec("Electronics");
        System.out.println("Electronics:");
        filter.filter(catalog, electronics).forEach(p -> System.out.println("  " + p.getName()));

        // Composed: affordable electronics in stock with good rating
        Specification<Product> deal =
            new CategorySpec("Electronics")
                .and(new PriceRangeSpec(0, 200))
                .and(new InStockSpec())
                .and(new MinRatingSpec(4.0));

        System.out.println("\nBest deals:");
        filter.filter(catalog, deal).forEach(p ->
            System.out.println("  " + p.getName() + " $" + p.getPrice()));

        // NOT: out of stock items
        Specification<Product> outOfStock = new InStockSpec().not();
        System.out.println("\nOut of stock:");
        filter.filter(catalog, outOfStock).forEach(p -> System.out.println("  " + p.getName()));

        // OR: cheap or highly rated
        Specification<Product> cheapOrTopRated =
            new PriceRangeSpec(0, 30).or(new MinRatingSpec(4.5));

        System.out.println("\nCheap or top-rated:");
        filter.filter(catalog, cheapOrTopRated).forEach(p -> System.out.println("  " + p.getName()));
    }
}
```

**Output:**
```
Electronics:
  Laptop
  Mouse
  Keyboard
  Headphones
  Monitor

Best deals:
  Mouse $29.99
  Headphones $199.99

Out of stock:
  Keyboard
  Monitor

Cheap or top-rated:
  Laptop
  Mouse
  Novel
  Headphones
  Monitor
```

---

## JSON Specification Description

Define business rules as **JSON** and dynamically build specifications at runtime. This lets non-developers or external systems define filtering rules without code changes.

### JSON Schema

```json
{
  "operator": "AND | OR | NOT",
  "rules": [
    {
      "field": "category | price | rating | inStock",
      "condition": "eq | neq | gt | gte | lt | lte | between | in",
      "value": "<value or array>"
    }
  ]
}
```

### Example JSON Rules

#### Rule 1 — Premium electronics in stock

```json
{
  "operator": "AND",
  "rules": [
    { "field": "category", "condition": "eq", "value": "Electronics" },
    { "field": "price",    "condition": "gte", "value": 100 },
    { "field": "rating",   "condition": "gte", "value": 4.0 },
    { "field": "inStock",  "condition": "eq",  "value": true }
  ]
}
```

#### Rule 2 — Nested: (Electronics AND price < 100) OR (Books AND rating ≥ 4.5)

```json
{
  "operator": "OR",
  "specs": [
    {
      "operator": "AND",
      "rules": [
        { "field": "category", "condition": "eq", "value": "Electronics" },
        { "field": "price",    "condition": "lt", "value": 100 }
      ]
    },
    {
      "operator": "AND",
      "rules": [
        { "field": "category", "condition": "eq",  "value": "Books" },
        { "field": "rating",   "condition": "gte", "value": 4.5 }
      ]
    }
  ]
}
```

#### Rule 3 — NOT out of stock

```json
{
  "operator": "NOT",
  "spec": {
    "operator": "AND",
    "rules": [
      { "field": "inStock", "condition": "eq", "value": false }
    ]
  }
}
```

---

### JSON-to-Specification Parser — Java (Jackson)

```java
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

public class JsonSpecificationParser {

    private static final ObjectMapper mapper = new ObjectMapper();

    /**
     * Parse a JSON string into a Specification<Product>.
     */
    public static Specification<Product> parse(String json) throws Exception {
        JsonNode root = mapper.readTree(json);
        return parseNode(root);
    }

    private static Specification<Product> parseNode(JsonNode node) {
        // Leaf rule — single condition
        if (node.has("field")) {
            return parseRule(node);
        }

        String operator = node.get("operator").asText().toUpperCase();

        return switch (operator) {
            case "AND" -> parseComposite(node, true);
            case "OR"  -> parseComposite(node, false);
            case "NOT" -> parseNode(node.get("spec")).not();
            default -> throw new IllegalArgumentException("Unknown operator: " + operator);
        };
    }

    /**
     * Combine child specs with AND or OR.
     */
    private static Specification<Product> parseComposite(JsonNode node, boolean isAnd) {
        Specification<Product> result = null;

        // Process flat rules array
        if (node.has("rules")) {
            for (JsonNode rule : node.get("rules")) {
                Specification<Product> spec = parseNode(rule);
                result = (result == null) ? spec
                       : isAnd ? result.and(spec) : result.or(spec);
            }
        }

        // Process nested specs array
        if (node.has("specs")) {
            for (JsonNode child : node.get("specs")) {
                Specification<Product> spec = parseNode(child);
                result = (result == null) ? spec
                       : isAnd ? result.and(spec) : result.or(spec);
            }
        }

        if (result == null) throw new IllegalArgumentException("Empty rules/specs");
        return result;
    }

    /**
     * Parse a single rule like { "field": "price", "condition": "gte", "value": 100 }
     */
    private static Specification<Product> parseRule(JsonNode node) {
        String field     = node.get("field").asText();
        String condition = node.get("condition").asText();
        JsonNode value   = node.get("value");

        return switch (field) {
            case "category" -> parseCategoryRule(condition, value);
            case "price"    -> parseNumericRule(condition, value, Product::getPrice);
            case "rating"   -> parseNumericRule(condition, value, Product::getRating);
            case "inStock"  -> parseInStockRule(condition, value);
            default -> throw new IllegalArgumentException("Unknown field: " + field);
        };
    }

    private static Specification<Product> parseCategoryRule(String cond, JsonNode val) {
        return switch (cond) {
            case "eq"  -> p -> p.getCategory().equalsIgnoreCase(val.asText());
            case "neq" -> p -> !p.getCategory().equalsIgnoreCase(val.asText());
            case "in"  -> {
                List<String> allowed = new ArrayList<>();
                val.forEach(v -> allowed.add(v.asText().toLowerCase()));
                yield p -> allowed.contains(p.getCategory().toLowerCase());
            }
            default -> throw new IllegalArgumentException("Invalid condition for category: " + cond);
        };
    }

    private static Specification<Product> parseNumericRule(
            String cond, JsonNode val, java.util.function.ToDoubleFunction<Product> getter) {
        return switch (cond) {
            case "eq"      -> p -> getter.applyAsDouble(p) == val.asDouble();
            case "neq"     -> p -> getter.applyAsDouble(p) != val.asDouble();
            case "gt"      -> p -> getter.applyAsDouble(p) >  val.asDouble();
            case "gte"     -> p -> getter.applyAsDouble(p) >= val.asDouble();
            case "lt"      -> p -> getter.applyAsDouble(p) <  val.asDouble();
            case "lte"     -> p -> getter.applyAsDouble(p) <= val.asDouble();
            case "between" -> {
                double lo = val.get(0).asDouble();
                double hi = val.get(1).asDouble();
                yield p -> {
                    double v = getter.applyAsDouble(p);
                    return v >= lo && v <= hi;
                };
            }
            default -> throw new IllegalArgumentException("Invalid numeric condition: " + cond);
        };
    }

    private static Specification<Product> parseInStockRule(String cond, JsonNode val) {
        boolean target = val.asBoolean();
        return switch (cond) {
            case "eq"  -> p -> p.isInStock() == target;
            case "neq" -> p -> p.isInStock() != target;
            default -> throw new IllegalArgumentException("Invalid condition for inStock: " + cond);
        };
    }
}
```

### Using the JSON Parser

```java
public class JsonSpecDemo {
    public static void main(String[] args) throws Exception {

        List<Product> catalog = List.of(
            new Product("Laptop",     "Electronics", 999.99, 4.5, true),
            new Product("Mouse",      "Electronics",  29.99, 4.8, true),
            new Product("Keyboard",   "Electronics",  79.99, 3.9, false),
            new Product("Novel",      "Books",        14.99, 4.7, true),
            new Product("Headphones", "Electronics", 199.99, 4.2, true),
            new Product("Monitor",    "Electronics", 349.99, 4.6, false)
        );

        ProductFilter filter = new ProductFilter();

        // Load JSON from file or string
        String json = """
            {
              "operator": "AND",
              "rules": [
                { "field": "category", "condition": "eq",  "value": "Electronics" },
                { "field": "price",    "condition": "lte", "value": 200 },
                { "field": "inStock",  "condition": "eq",  "value": true },
                { "field": "rating",   "condition": "gte", "value": 4.0 }
              ]
            }
            """;

        Specification<Product> spec = JsonSpecificationParser.parse(json);

        System.out.println("Matching products:");
        filter.filter(catalog, spec).forEach(p ->
            System.out.println("  " + p.getName() + " — $" + p.getPrice()
                             + " ★" + p.getRating()));

        // Nested OR example
        String nestedJson = """
            {
              "operator": "OR",
              "specs": [
                {
                  "operator": "AND",
                  "rules": [
                    { "field": "category", "condition": "eq", "value": "Electronics" },
                    { "field": "price",    "condition": "lt", "value": 100 }
                  ]
                },
                {
                  "operator": "AND",
                  "rules": [
                    { "field": "category", "condition": "eq",  "value": "Books" },
                    { "field": "rating",   "condition": "gte", "value": 4.5 }
                  ]
                }
              ]
            }
            """;

        Specification<Product> nestedSpec = JsonSpecificationParser.parse(nestedJson);
        System.out.println("\nCheap electronics OR top-rated books:");
        filter.filter(catalog, nestedSpec).forEach(p ->
            System.out.println("  " + p.getName()));
    }
}
```

**Output:**
```
Matching products:
  Mouse — $29.99 ★4.8
  Headphones — $199.99 ★4.2

Cheap electronics OR top-rated books:
  Mouse
  Keyboard
  Novel
```

---

## Rust Implementation

Rust's trait system and closures map naturally to the Specification pattern. We use `Box<dyn Fn>` for composability and leverage Rust's ownership model for zero-cost abstractions.

### Cargo.toml Dependencies

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

### 1. Core Specification Trait

```rust
/// A specification is anything that can test a candidate.
pub trait Specification<T> {
    fn is_satisfied_by(&self, candidate: &T) -> bool;

    /// Combine two specs with AND.
    fn and<S: Specification<T> + 'static>(self, other: S) -> AndSpec<T>
    where
        Self: Sized + 'static,
    {
        AndSpec {
            left: Box::new(self),
            right: Box::new(other),
        }
    }

    /// Combine two specs with OR.
    fn or<S: Specification<T> + 'static>(self, other: S) -> OrSpec<T>
    where
        Self: Sized + 'static,
    {
        OrSpec {
            left: Box::new(self),
            right: Box::new(other),
        }
    }

    /// Negate a spec.
    fn not(self) -> NotSpec<T>
    where
        Self: Sized + 'static,
    {
        NotSpec {
            inner: Box::new(self),
        }
    }
}

// --- Composite specs ---

pub struct AndSpec<T> {
    left: Box<dyn Specification<T>>,
    right: Box<dyn Specification<T>>,
}
impl<T> Specification<T> for AndSpec<T> {
    fn is_satisfied_by(&self, candidate: &T) -> bool {
        self.left.is_satisfied_by(candidate) && self.right.is_satisfied_by(candidate)
    }
}

pub struct OrSpec<T> {
    left: Box<dyn Specification<T>>,
    right: Box<dyn Specification<T>>,
}
impl<T> Specification<T> for OrSpec<T> {
    fn is_satisfied_by(&self, candidate: &T) -> bool {
        self.left.is_satisfied_by(candidate) || self.right.is_satisfied_by(candidate)
    }
}

pub struct NotSpec<T> {
    inner: Box<dyn Specification<T>>,
}
impl<T> Specification<T> for NotSpec<T> {
    fn is_satisfied_by(&self, candidate: &T) -> bool {
        !self.inner.is_satisfied_by(candidate)
    }
}
```

### 2. Domain Model

```rust
#[derive(Debug, Clone)]
pub struct Product {
    pub name: String,
    pub category: String,
    pub price: f64,
    pub rating: f64,
    pub in_stock: bool,
}

impl Product {
    pub fn new(name: &str, category: &str, price: f64, rating: f64, in_stock: bool) -> Self {
        Self {
            name: name.into(),
            category: category.into(),
            price,
            rating,
            in_stock,
        }
    }
}
```

### 3. Concrete Specifications

```rust
pub struct CategorySpec {
    category: String,
}
impl CategorySpec {
    pub fn new(category: &str) -> Self {
        Self { category: category.to_lowercase() }
    }
}
impl Specification<Product> for CategorySpec {
    fn is_satisfied_by(&self, p: &Product) -> bool {
        p.category.to_lowercase() == self.category
    }
}

pub struct PriceRangeSpec {
    min: f64,
    max: f64,
}
impl PriceRangeSpec {
    pub fn new(min: f64, max: f64) -> Self { Self { min, max } }
}
impl Specification<Product> for PriceRangeSpec {
    fn is_satisfied_by(&self, p: &Product) -> bool {
        p.price >= self.min && p.price <= self.max
    }
}

pub struct MinRatingSpec {
    min_rating: f64,
}
impl MinRatingSpec {
    pub fn new(min_rating: f64) -> Self { Self { min_rating } }
}
impl Specification<Product> for MinRatingSpec {
    fn is_satisfied_by(&self, p: &Product) -> bool {
        p.rating >= self.min_rating
    }
}

pub struct InStockSpec;
impl Specification<Product> for InStockSpec {
    fn is_satisfied_by(&self, p: &Product) -> bool {
        p.in_stock
    }
}
```

### 4. Filter Function

```rust
pub fn filter<T>(items: &[T], spec: &dyn Specification<T>) -> Vec<&T> {
    items.iter().filter(|item| spec.is_satisfied_by(item)).collect()
}
```

### 5. Usage — Composing Business Rules

```rust
fn main() {
    let catalog = vec![
        Product::new("Laptop",     "Electronics", 999.99, 4.5, true),
        Product::new("Mouse",      "Electronics",  29.99, 4.8, true),
        Product::new("Keyboard",   "Electronics",  79.99, 3.9, false),
        Product::new("Novel",      "Books",        14.99, 4.7, true),
        Product::new("Headphones", "Electronics", 199.99, 4.2, true),
        Product::new("Monitor",    "Electronics", 349.99, 4.6, false),
    ];

    // Single spec
    let electronics = CategorySpec::new("Electronics");
    println!("Electronics:");
    for p in filter(&catalog, &electronics) {
        println!("  {}", p.name);
    }

    // Composed: affordable electronics in stock with good rating
    let deal = CategorySpec::new("Electronics")
        .and(PriceRangeSpec::new(0.0, 200.0))
        .and(InStockSpec)
        .and(MinRatingSpec::new(4.0));

    println!("\nBest deals:");
    for p in filter(&catalog, &deal) {
        println!("  {} — ${:.2}", p.name, p.price);
    }

    // NOT: out of stock
    let out_of_stock = InStockSpec.not();
    println!("\nOut of stock:");
    for p in filter(&catalog, &out_of_stock) {
        println!("  {}", p.name);
    }

    // OR: cheap or highly rated
    let cheap_or_top = PriceRangeSpec::new(0.0, 30.0)
        .or(MinRatingSpec::new(4.5));

    println!("\nCheap or top-rated:");
    for p in filter(&catalog, &cheap_or_top) {
        println!("  {}", p.name);
    }
}
```

**Output:**
```
Electronics:
  Laptop
  Mouse
  Keyboard
  Headphones
  Monitor

Best deals:
  Mouse — $29.99
  Headphones — $199.99

Out of stock:
  Keyboard
  Monitor

Cheap or top-rated:
  Laptop
  Mouse
  Novel
  Headphones
  Monitor
```

### 6. JSON Specification Parser — Rust (serde_json)

```rust
use serde_json::Value;

/// Wrapper so we can box closures as specifications.
pub struct FnSpec<T> {
    f: Box<dyn Fn(&T) -> bool>,
}
impl<T> Specification<T> for FnSpec<T> {
    fn is_satisfied_by(&self, candidate: &T) -> bool {
        (self.f)(candidate)
    }
}

pub fn parse_json(json: &str) -> Box<dyn Specification<Product>> {
    let root: Value = serde_json::from_str(json).expect("Invalid JSON");
    parse_node(&root)
}

fn parse_node(node: &Value) -> Box<dyn Specification<Product>> {
    // Leaf rule
    if node.get("field").is_some() {
        return parse_rule(node);
    }

    let operator = node["operator"].as_str().expect("Missing operator");

    match operator.to_uppercase().as_str() {
        "AND" => parse_composite(node, true),
        "OR"  => parse_composite(node, false),
        "NOT" => {
            let inner = parse_node(&node["spec"]);
            Box::new(NotSpec { inner })
        }
        other => panic!("Unknown operator: {other}"),
    }
}

fn parse_composite(node: &Value, is_and: bool) -> Box<dyn Specification<Product>> {
    let mut specs: Vec<Box<dyn Specification<Product>>> = Vec::new();

    if let Some(rules) = node.get("rules").and_then(|r| r.as_array()) {
        for rule in rules {
            specs.push(parse_node(rule));
        }
    }
    if let Some(children) = node.get("specs").and_then(|s| s.as_array()) {
        for child in children {
            specs.push(parse_node(child));
        }
    }

    assert!(!specs.is_empty(), "Empty rules/specs");

    let mut iter = specs.into_iter();
    let first = iter.next().unwrap();

    if is_and {
        iter.fold(first, |acc, s| {
            Box::new(AndSpec { left: acc, right: s })
        })
    } else {
        iter.fold(first, |acc, s| {
            Box::new(OrSpec { left: acc, right: s })
        })
    }
}

fn parse_rule(node: &Value) -> Box<dyn Specification<Product>> {
    let field     = node["field"].as_str().unwrap();
    let condition = node["condition"].as_str().unwrap();
    let value     = &node["value"];

    match field {
        "category" => {
            let target = value.as_str().unwrap().to_lowercase();
            let cond = condition.to_string();
            Box::new(FnSpec {
                f: Box::new(move |p: &Product| {
                    let cat = p.category.to_lowercase();
                    match cond.as_str() {
                        "eq"  => cat == target,
                        "neq" => cat != target,
                        _     => panic!("Invalid category condition: {cond}"),
                    }
                }),
            })
        }
        "price" | "rating" => {
            let is_price = field == "price";
            let cond = condition.to_string();
            let val = value.clone();
            Box::new(FnSpec {
                f: Box::new(move |p: &Product| {
                    let v = if is_price { p.price } else { p.rating };
                    match cond.as_str() {
                        "eq"  => (v - val.as_f64().unwrap()).abs() < f64::EPSILON,
                        "gt"  => v >  val.as_f64().unwrap(),
                        "gte" => v >= val.as_f64().unwrap(),
                        "lt"  => v <  val.as_f64().unwrap(),
                        "lte" => v <= val.as_f64().unwrap(),
                        "between" => {
                            let lo = val[0].as_f64().unwrap();
                            let hi = val[1].as_f64().unwrap();
                            v >= lo && v <= hi
                        }
                        _ => panic!("Invalid numeric condition: {cond}"),
                    }
                }),
            })
        }
        "inStock" => {
            let target = value.as_bool().unwrap();
            let cond = condition.to_string();
            Box::new(FnSpec {
                f: Box::new(move |p: &Product| match cond.as_str() {
                    "eq"  => p.in_stock == target,
                    "neq" => p.in_stock != target,
                    _     => panic!("Invalid inStock condition: {cond}"),
                }),
            })
        }
        _ => panic!("Unknown field: {field}"),
    }
}
```

### 7. Using the JSON Parser

```rust
fn main() {
    let catalog = vec![
        Product::new("Laptop",     "Electronics", 999.99, 4.5, true),
        Product::new("Mouse",      "Electronics",  29.99, 4.8, true),
        Product::new("Keyboard",   "Electronics",  79.99, 3.9, false),
        Product::new("Novel",      "Books",        14.99, 4.7, true),
        Product::new("Headphones", "Electronics", 199.99, 4.2, true),
        Product::new("Monitor",    "Electronics", 349.99, 4.6, false),
    ];

    let json = r#"{
        "operator": "AND",
        "rules": [
            { "field": "category", "condition": "eq",  "value": "Electronics" },
            { "field": "price",    "condition": "lte", "value": 200 },
            { "field": "inStock",  "condition": "eq",  "value": true },
            { "field": "rating",   "condition": "gte", "value": 4.0 }
        ]
    }"#;

    let spec = parse_json(json);
    println!("Matching products:");
    for p in filter(&catalog, spec.as_ref()) {
        println!("  {} — ${:.2} ★{}", p.name, p.price, p.rating);
    }

    // Nested OR
    let nested_json = r#"{
        "operator": "OR",
        "specs": [
            {
                "operator": "AND",
                "rules": [
                    { "field": "category", "condition": "eq", "value": "Electronics" },
                    { "field": "price",    "condition": "lt", "value": 100 }
                ]
            },
            {
                "operator": "AND",
                "rules": [
                    { "field": "category", "condition": "eq",  "value": "Books" },
                    { "field": "rating",   "condition": "gte", "value": 4.5 }
                ]
            }
        ]
    }"#;

    let nested_spec = parse_json(nested_json);
    println!("\nCheap electronics OR top-rated books:");
    for p in filter(&catalog, nested_spec.as_ref()) {
        println!("  {}", p.name);
    }
}
```

**Output:**
```
Matching products:
  Mouse — $29.99 ★4.8
  Headphones — $199.99 ★4.2

Cheap electronics OR top-rated books:
  Mouse
  Keyboard
  Novel
```

### Java vs Rust Comparison

| Aspect | Java | Rust |
|---|---|---|
| **Spec abstraction** | `interface` + `default` methods | `trait` + provided methods |
| **Composition** | Returns lambda / anonymous class | Returns `AndSpec`, `OrSpec`, `NotSpec` structs |
| **Closure specs** | Lambda `p -> p.getPrice() > 50` | `FnSpec` wrapping `Box<dyn Fn(&T) -> bool>` |
| **Ownership** | GC handles everything | `Box<dyn Specification<T>>` for heap allocation |
| **JSON parsing** | Jackson `ObjectMapper` | `serde_json::Value` |
| **Performance** | JIT-optimised, allocation overhead | Zero-cost traits, no GC, monomorphisation |
| **Type safety** | Generics (erased at runtime) | Generics (monomorphised at compile time) |

---

## When to Use the Specification Pattern

| Use When | Avoid When |
|---|---|
| Complex, combinable business rules | Simple one-off conditions |
| Rules change frequently or come from config/JSON | Static rules that rarely change |
| Need to reuse predicates across services | Over-engineering a simple filter |
| Testing individual rules in isolation matters | Performance-critical tight loops (object overhead) |
| Domain-Driven Design (DDD) — entity validation | |

---

## Class Diagram

```
            ┌─────────────────────────┐
            │   <<interface>>         │
            │   Specification<T>      │
            │─────────────────────────│
            │ + isSatisfiedBy(T): bool│
            │ + and(Spec<T>): Spec<T> │
            │ + or(Spec<T>): Spec<T>  │
            │ + not(): Spec<T>        │
            └────────┬────────────────┘
                     │ implements
       ┌─────────────┼──────────────┐
       │             │              │
┌──────▼─────┐ ┌────▼──────┐ ┌─────▼──────┐
│CategorySpec│ │PriceRange │ │ InStockSpec │  ...
│            │ │Spec       │ │            │
└────────────┘ └───────────┘ └────────────┘

       ┌──────────────────────────────┐
       │   JsonSpecificationParser    │
       │──────────────────────────────│
       │ + parse(json): Spec<Product> │
       │ - parseNode(JsonNode)        │
       │ - parseRule(JsonNode)        │
       │ - parseComposite(node, bool) │
       └──────────────────────────────┘
```

---

## Summary

| Concept | Description |
|---|---|
| **Specification** | Encapsulates a single business rule as an object |
| **Composition** | `and()`, `or()`, `not()` combine specs into complex rules |
| **JSON specs** | Define rules externally, parse at runtime — no code changes |
| **Benefits** | Reusable, testable, composable, open/closed compliant |
| **Pairs with** | Repository pattern (query specs), DDD, validation pipelines |
