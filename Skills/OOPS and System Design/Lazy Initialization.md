
There are several ways to use lazy initialization.

## General Ways to Lazily Initialize in Java (with Examples)

**1. Conditional Initialization in Getter (Classic Lazy Initialization)**

```java
public class ExpensiveObjectHolder {
    private ExpensiveObject obj;

    public ExpensiveObject getObj() {
        if (obj == null) {
            obj = new ExpensiveObject();
        }
        return obj;
    }
}

```

**2. Thread-Safe Lazy Initialization (Synchronized Method)**

java

```java
public class ExpensiveObjectHolder {
    private ExpensiveObject obj;

    public synchronized ExpensiveObject getObj() {
        if (obj == null) {
            obj = new ExpensiveObject();
        }
        return obj;
    }
}

```

**3. Double-Checked Locking**

java

```java
public class ExpensiveObjectHolder {
    private volatile ExpensiveObject obj;

    public ExpensiveObject getObj() {
        if (obj == null) {
            synchronized (this) {
                if (obj == null) {
                    obj = new ExpensiveObject();
                }
            }
        }
        return obj;
    }
}

```


**4. Initialization-on-Demand Holder Idiom**

java

```java
public class ExpensiveObjectHolder {
    private static class Holder {
        static final ExpensiveObject INSTANCE = new ExpensiveObject();
    }

    public static ExpensiveObject getObj() {
        return Holder.INSTANCE;
    }
}

```


**5. Java 8+ Supplier with Memoization**

java

```java
import java.util.function.Supplier;

public class Lazy<T> implements Supplier<T> {
    private final Supplier<T> supplier;
    private T value;

    public Lazy(Supplier<T> supplier) {
        this.supplier = supplier;
    }

    @Override
    public synchronized T get() {
        if (value == null) {
            value = supplier.get();
        }
        return value;
    }
}

// Usage
Lazy<ExpensiveObject> lazyObj = new Lazy<>(ExpensiveObject::new);
ExpensiveObject obj = lazyObj.get();

```
