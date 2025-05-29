Java Collection framework is a set of comprehensive data structures to store, group and manipulate objects efficiently.

![[Pasted image 20250525174049.png]]

## List Interface:
### ArrayList
Internally Implemented re-sizable array.

**Performance Characteristics:**

- **Access**: O(1) - Fast random access by index
- **Insertion**: O(1) amortized at end, O(n) at middle
- **Deletion**: O(n) for arbitrary positions
- **Search**: O(n) for unsorted data

**Spring Boot Usage:**
- Storing query results from databases
- Holding collections of DTOs in REST responses
- Managing request body arrays
- Configuration lists in application properties

```java
import java.util.*;

class SampleArrayList {
	public static void main(String []args) {
		List<String> people = new ArrayList<>();
		people.add("Aryan");
		people.add("Suijt");
		System.out.println(people); //[Aryan, Suijt]
		System.out.println(people.get(1)); // Sujit
	}
}
```

### LinkedList
Simple doubly linked list implementation.

**Performance Characteristics:**
- **Access**: O(n) - Must traverse from head or tail
- **Insertion**: O(1) at ends, O(n) at arbitrary positions
- **Deletion**: O(1) if node reference available
- **Memory**: Higher overhead due to node pointers

**Spring Boot Usage:**
- Queue implementations for message processing
- Scenarios with heavy insert/delete operations
- Implementing custom data processing pipelines

```java
import java.util.*;

public class SampleLinkedList {
  public static void main(String []args) {
    LinkedList<String> people = new LinkedList<>();
    people.addFirst("First");
    people.addFirst("NewFirst");
    people.addLast("Last");
    people.add(2, "Middle");
    people.add(2, "Before Middle");
    System.out.println("The size of the linkedlist = " + people.size());
    System.out.println("State of the linked list: " + people);
  }
}
```

## Set Interface
### HashSet
#### Key Characteristics
- **No duplicates**: Automatically prevents duplicate entries
- **Unordered**: Most implementations don't guarantee order
- **Null handling**: Most allow single null value

```java
import java.util.*;

class SampleHashSet {
  public static void main (String []args) {
    Set<String> friends = new HashSet<>();
    friends.add("Aryan");
    friends.add("Shivansh");
    System.out.println(friends);
    friends.add("Aryan");
    System.out.println("After adding duplicate element: " + friends);
  }
}
```

Performance Characteristics:
 - Add/Remove/Contains: O(1) average case
 -  Iteration: O(capacity + size)
 -  No ordering: Elements stored in hash order
Spring Boot Usage:
 -  Storing unique user roles and permissions
 -  Managing unique tags or categories
 -  Enforcing unique constraints in business logic
 -  Caching unique identifiers

### TreeSet
Implented using red-black trees.

```java
import java.util.*;

public class SampleTreeSet {
  public static void main(String []args) {
    Set<Integer> numbers = new TreeSet<>();
    numbers.add(4);
    numbers.add(5);
    numbers.add(1);
    numbers.add(-10);
    System.out.println(numbers);

    numbers.add(1);
    System.out.println(numbers);
  }
}

```

**Performance Characteristics:**
- **Add/Remove/Contains**: O(log n)
- **Sorted iteration**: Natural ordering maintained
- **Range operations**: Efficient subset operations

**Spring Boot Usage:**
- Maintaining sorted collections of data
- Priority-based processing
- Range queries on sorted data

## Map Interface
Stores data as Key-value pairs. It has relatively fast lookup.

### HashMap
#### Key Characteristics
- **Key-value pairs**: Associates keys with values
- **Unique keys**: No duplicate keys allowed
- **Fast lookup**: Efficient value retrieval by key

```java
import java.util.*;

public class SampleHashMap {
  public static void main(String []args) {
    Map<String, Integer> marks = new HashMap<>();
    marks.put("Aryan", 36);
    marks.put("Satyam", 38);
    marks.put("Shivansh", 21);
    System.out.println(marks);
  }
}
```

**Performance Characteristics:**
- **Get/Put/Remove**: O(1) average case
- **Iteration**: O(capacity + size)
- **Null values**: Allows one null key and multiple null values

**Spring Boot Usage:**
- Configuration property mapping
- JSON payload processing
- Caching mechanisms
- Request parameter mapping
- Database query result mapping

### TreeSet
#### Key Characteristics
**Performance Characteristics:**
- **Get/Put/Remove**: O(log n)
- **Sorted iteration**: Keys maintained in natural order
- **Range operations**: Efficient submap operations

```java
import java.util.*;

public class SampleTreeMap {
  public static void main(String []args) {
    Map<Integer, String> mapped = new TreeMap<>();

    mapped.put(1, "Aryan");
    mapped.put(2, "Shivansh");

    System.out.println(mapped);

    for(Map.Entry<Integer, String> pair: mapped.entrySet()) {
      System.out.println(pair);
    }
  }
}
```

**Spring Boot Usage:**
- Sorted configuration management
- Time-series data storage
- Priority-based processing queues
- Range-based queries



## Performance Comparison Table

| Operation    | ArrayList | LinkedList | HashSet | TreeSet  | HashMap | TreeMap  |
| ------------ | --------- | ---------- | ------- | -------- | ------- | -------- |
| **Access**   | O(1)      | O(n)       | N/A     | N/A      | O(1)    | O(log n) |
| **Insert**   | O(1)*     | O(1)       | O(1)    | O(log n) | O(1)    | O(log n) |
| **Delete**   | O(n)      | O(1)**     | O(1)    | O(log n) | O(1)    | O(log n) |
| **Search**   | O(n)      | O(n)       | O(1)    | O(log n) | O(1)    | O(log n) |
| **Ordering** | Insertion | Insertion  | None    | Sorted   | None    | Sorted   |

## Summary
# Java Collections Framework - Complete Summary Table

|Collection|Type|Interface|Ordering|Duplicates|Null Values|Key Characteristics|Performance (Access/Insert/Delete)|Spring Boot Use Cases|
|---|---|---|---|---|---|---|---|---|
|**ArrayList**|List|List|Insertion order|✓ Allowed|✓ Multiple|Resizable array, indexed access|O(1) / O(1)* / O(n)|Query results, DTOs, request bodies, pagination|
|**LinkedList**|List|List, Deque, Queue|Insertion order|✓ Allowed|✓ Multiple|Doubly-linked list, efficient insert/delete|O(n) / O(1) / O(1)**|Message queues, processing pipelines, undo operations|
|**HashSet**|Set|Set|No order|✗ Not allowed|✓ One null|Hash table, fast lookup|O(1) / O(1) / O(1)|User roles, permissions, unique tags, cache keys|
|**TreeSet**|Set|NavigableSet|Sorted order|✗ Not allowed|✗ No nulls|Red-Black tree, sorted|O(log n) / O(log n) / O(log n)|Sorted collections, priority processing, rankings|
|**HashMap**|Map|Map|No order|Keys: ✗, Values: ✓|✓ One null key|Hash table, key-value pairs|O(1) / O(1) / O(1)|Config properties, JSON payloads, caching|
|**TreeMap**|Map|NavigableMap|Sorted by keys|Keys: ✗, Values: ✓|✗ No null keys|Red-Black tree, sorted keys|O(log n) / O(log n) / O(log n)|Time-series data, sorted configs, range queries|

## Key Method Categories

|Collection|Unique Methods|Iterator Types|Capacity Methods|Navigation Methods|
|---|---|---|---|---|
|**ArrayList**|`ensureCapacity()`, `trimToSize()`|Iterator, ListIterator|✓|✗|
|**LinkedList**|`addFirst/Last()`, `poll()`, `peek()`, `push()`, `pop()`|Iterator, ListIterator, DescendingIterator|✗|✗|
|**HashSet**|Standard Set methods only|Iterator|✗|✗|
|**TreeSet**|`first()`, `last()`, `higher()`, `lower()`, `subSet()`|Iterator, DescendingIterator|✗|✓|
|**HashMap**|`compute()`, `merge()`, `putIfAbsent()`|KeySet, Values, EntrySet iterators|✗|✗|
|**TreeMap**|`firstKey()`, `lastKey()`, `subMap()`, `headMap()`, `tailMap()`|KeySet, Values, EntrySet, DescendingMap|✗|✓|

## Spring Boot Integration Patterns

|Layer|ArrayList|LinkedList|HashSet|TreeMap|HashMap|TreeMap|
|---|---|---|---|---|---|---|
|**Controller**|Response lists|Queue processing|Role filtering|Sorted responses|Request mapping|Time-based data|
|**Service**|Business logic|Workflow chains|Deduplication|Priority handling|Config management|Ordered processing|
|**Repository**|Query results|Batch operations|Unique constraints|Sorted queries|Parameter mapping|Range queries|
|**Configuration**|Property lists|Processing order|Feature flags|Sorted properties|Key-value configs|Hierarchical configs|
