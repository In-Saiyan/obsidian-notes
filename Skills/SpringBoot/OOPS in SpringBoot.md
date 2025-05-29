Since the whole SpringBoot framework follows the Object Oriented Paradigm of Programming, it also exploits to principles of OOPS in order to enhance the implementation patters the framework.

## Encapsulation
Encapsulation bundles data (fields) and methods that operate on that data within a single unit, while restricting direct access to internal components through access modifiers.

### Entity/Model Implementation with Encapsulation
```java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String username;
    
    @Column(nullable = false)
    private String email;
    
    @Column(nullable = false)
    private String password;
    
    // Private constructor for JPA
    protected User() {}
    
    // Public constructor
    public User(String username, String email, String password) {
        this.username = username;
        this.email = email;
        this.password = password;
    }
    
    // Getters
    public Long getId() { return id; }
    public String getUsername() { return username; }
    public String getEmail() { return email; }
    
    // Setters with validation
    public void setUsername(String username) {
        if (username == null || username.trim().isEmpty()) {
            throw new IllegalArgumentException("Username cannot be empty");
        }
        this.username = username;
    }
    
    public void setEmail(String email) {
        if (!isValidEmail(email)) {
            throw new IllegalArgumentException("Invalid email format");
        }
        this.email = email;
    }
    
    // Encapsulated business logic
    private boolean isValidEmail(String email) {
        return email != null && email.contains("@");
    }
    
    // Controlled password access
    public void setPassword(String password) {
        if (password == null || password.length() < 8) {
            throw new IllegalArgumentException("Password must be at least 8 characters");
        }
        this.password = hashPassword(password);
    }
    
    private String hashPassword(String password) {
        // Encapsulated password hashing logic
        return BCrypt.hashpw(password, BCrypt.gensalt());
    }
}

```

**Benefits in Spring Boot:**
- **Data Protection**: Private fields prevent direct manipulation
- **Validation Control**: Setters enforce business rules
- **Internal Logic Hiding**: Password hashing is encapsulated
- **JPA Integration**: Works seamlessly with Hibernate

## Abstraction
Abstraction hides implementation details while exposing essential functionality through interfaces or abstract classes.

### Repository using Abstraction with JPA (Jakarta Persistence)
```java
// Abstract interface hiding database complexity
public interface UserRepository extends JpaRepository<User, Long> {
    // Abstract method - implementation hidden
    Optional<User> findByUsername(String username);
    
    // Custom query abstraction
    @Query("SELECT u FROM User u WHERE u.email = ?1")
    Optional<User> findByEmail(String email);
    
    // Method name abstraction
    List<User> findByUsernameContainingIgnoreCase(String username);
}

// Service abstraction layer
public interface UserService {
    User createUser(UserDto userDto);
    User getUserById(Long id);
    User updateUser(Long id, UserDto userDto);
    void deleteUser(Long id);
    List<User> searchUsers(String keyword);
}

// Concrete implementation
@Service
@Transactional
public class UserServiceImpl implements UserService {
    
    @Autowired
    private UserRepository userRepository;
    
    @Override
    public User createUser(UserDto userDto) {
        // Implementation details hidden from client
        validateUserDto(userDto);
        User user = convertToEntity(userDto);
        return userRepository.save(user);
    }
    
    @Override
    public User getUserById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException("User not found with id: " + id));
    }
    
    // Private methods hide implementation complexity
    private void validateUserDto(UserDto userDto) {
        if (userRepository.findByUsername(userDto.getUsername()).isPresent()) {
            throw new DuplicateUserException("Username already exists");
        }
    }
    
    private User convertToEntity(UserDto userDto) {
        return new User(userDto.getUsername(), userDto.getEmail(), userDto.getPassword());
    }
}

```

### Configuration with Abstraction
```java
@Configuration
public abstract class DatabaseConfig {
    
    // Abstract method for different environments
    protected abstract DataSource createDataSource();
    
    // Common configuration
    @Bean
    public JdbcTemplate jdbcTemplate() {
        return new JdbcTemplate(createDataSource());
    }
}

@Configuration
@Profile("dev")
public class DevDatabaseConfig extends DatabaseConfig {
    
    @Override
    protected DataSource createDataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:h2:mem:devdb");
        return new HikariDataSource(config);
    }
}
```

## Inheritance

Inheritance allows classes to inherit properties and methods from parent classes, promoting code reuse and establishing hierarchical relationships.

### Entity inheritance
```java
@Entity
@Inheritance(strategy = InheritanceType.SINGLE_TABLE)
@DiscriminatorColumn(name = "employee_type")
public abstract class Employee {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String name;
    
    @Column(nullable = false)
    private String email;
    
    @Column(nullable = false)
    private BigDecimal baseSalary;
    
    // Constructor
    protected Employee() {}
    
    public Employee(String name, String email, BigDecimal baseSalary) {
        this.name = name;
        this.email = email;
        this.baseSalary = baseSalary;
    }
    
    // Abstract method for salary calculation
    public abstract BigDecimal calculateTotalSalary();
    
    // Common methods inherited by all employees
    public String getEmployeeInfo() {
        return String.format("Employee: %s (%s)", name, email);
    }
    
    // Getters and setters
    public Long getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
    public BigDecimal getBaseSalary() { return baseSalary; }
}

@Entity
@DiscriminatorValue("FULL_TIME")
public class FullTimeEmployee extends Employee {
    
    @Column(name = "annual_bonus")
    private BigDecimal annualBonus;
    
    protected FullTimeEmployee() {}
    
    public FullTimeEmployee(String name, String email, BigDecimal baseSalary, BigDecimal annualBonus) {
        super(name, email, baseSalary);
        this.annualBonus = annualBonus;
    }
    
    @Override
    public BigDecimal calculateTotalSalary() {
        return getBaseSalary().add(annualBonus);
    }
    
    public BigDecimal getAnnualBonus() { return annualBonus; }
}

@Entity
@DiscriminatorValue("CONTRACTOR")
public class Contractor extends Employee {
    
    @Column(name = "hourly_rate")
    private BigDecimal hourlyRate;
    
    @Column(name = "hours_worked")
    private Integer hoursWorked;
    
    protected Contractor() {}
    
    public Contractor(String name, String email, BigDecimal hourlyRate, Integer hoursWorked) {
        super(name, email, BigDecimal.ZERO);
        this.hourlyRate = hourlyRate;
        this.hoursWorked = hoursWorked;
    }
    
    @Override
    public BigDecimal calculateTotalSalary() {
        return hourlyRate.multiply(BigDecimal.valueOf(hoursWorked));
    }
    
    public BigDecimal getHourlyRate() { return hourlyRate; }
    public Integer getHoursWorked() { return hoursWorked; }
}

```

### Repository Inheritance
```java
// Base repository with common methods
public interface BaseRepository<T, ID> extends JpaRepository<T, ID> {
    
    @Query("SELECT e FROM #{#entityName} e WHERE e.createdDate >= :date")
    List<T> findCreatedAfter(@Param("date") LocalDateTime date);
    
    @Modifying
    @Query("UPDATE #{#entityName} e SET e.lastModified = :now WHERE e.id = :id")
    void updateLastModified(@Param("id") ID id, @Param("now") LocalDateTime now);
}

// Specific repository inheriting common functionality
public interface EmployeeRepository extends BaseRepository<Employee, Long> {
    List<Employee> findByNameContainingIgnoreCase(String name);
    
    @Query("SELECT e FROM Employee e WHERE TYPE(e) = :employeeType")
    List<Employee> findByEmployeeType(@Param("employeeType") Class<? extends Employee> employeeType);
}

```

## Polymorphism
Polymorphism allows objects of different types to be treated as instances of the same type through a common interface, enabling different behaviors based on the actual object type.

### Service Polymorphism 
```java
// Common interface for different payment methods
public interface PaymentProcessor {
    PaymentResult processPayment(PaymentRequest request);
    boolean supports(PaymentMethod method);
}

@Component
public class CreditCardProcessor implements PaymentProcessor {
    
    @Override
    public PaymentResult processPayment(PaymentRequest request) {
        // Credit card specific processing
        validateCreditCard(request.getCardNumber());
        return new PaymentResult("SUCCESS", "Credit card payment processed", generateTransactionId());
    }
    
    @Override
    public boolean supports(PaymentMethod method) {
        return method == PaymentMethod.CREDIT_CARD;
    }
    
    private void validateCreditCard(String cardNumber) {
        // Credit card validation logic
        if (cardNumber == null || cardNumber.length() != 16) {
            throw new InvalidPaymentException("Invalid credit card number");
        }
    }
    
    private String generateTransactionId() {
        return "CC_" + System.currentTimeMillis();
    }
}

@Component
public class PayPalProcessor implements PaymentProcessor {
    
    @Override
    public PaymentResult processPayment(PaymentRequest request) {
        // PayPal specific processing
        validatePayPalAccount(request.getEmail());
        return new PaymentResult("SUCCESS", "PayPal payment processed", generateTransactionId());
    }
    
    @Override
    public boolean supports(PaymentMethod method) {
        return method == PaymentMethod.PAYPAL;
    }
    
    private void validatePayPalAccount(String email) {
        // PayPal validation logic
        if (email == null || !email.contains("@")) {
            throw new InvalidPaymentException("Invalid PayPal email");
        }
    }
    
    private String generateTransactionId() {
        return "PP_" + System.currentTimeMillis();
    }
}

// Service using polymorphism
@Service
public class PaymentService {
    
    private final List<PaymentProcessor> processors;
    
    public PaymentService(List<PaymentProcessor> processors) {
        this.processors = processors;
    }
    
    public PaymentResult processPayment(PaymentRequest request) {
        PaymentProcessor processor = processors.stream()
            .filter(p -> p.supports(request.getPaymentMethod()))
            .findFirst()
            .orElseThrow(() -> new UnsupportedPaymentMethodException("Payment method not supported"));
        
        return processor.processPayment(request);
    }
}

```

### Controller Polymorphism
```java
@RestController
@RequestMapping("/api/employees")
public class EmployeeController {
    
    @Autowired
    private EmployeeRepository employeeRepository;
    
    @GetMapping("/{id}/salary")
    public ResponseEntity<SalaryResponse> getEmployeeSalary(@PathVariable Long id) {
        Employee employee = employeeRepository.findById(id)
            .orElseThrow(() -> new EmployeeNotFoundException("Employee not found"));
        
        // Polymorphic behavior - different calculation based on actual type
        BigDecimal totalSalary = employee.calculateTotalSalary();
        
        return ResponseEntity.ok(new SalaryResponse(
            employee.getId(),
            employee.getName(),
            totalSalary,
            employee.getClass().getSimpleName()
        ));
    }
}

```

## Composition
Composition represents a "has-a" relationship where one class contains instances of other classes as components.

### User-Role Composition
```java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String username;
    private String email;
    
    // Composition: User HAS-A Profile
    @OneToOne(cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JoinColumn(name = "profile_id")
    private UserProfile profile;
    
    // Composition: User HAS-MANY Roles
    @ManyToMany(fetch = FetchType.EAGER)
    @JoinTable(
        name = "user_roles",
        joinColumns = @JoinColumn(name = "user_id"),
        inverseJoinColumns = @JoinColumn(name = "role_id")
    )
    private Set<Role> roles = new HashSet<>();
    
    // Composition: User HAS-MANY Addresses
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Address> addresses = new ArrayList<>();
    
    // Constructor
    public User(String username, String email) {
        this.username = username;
        this.email = email;
        this.profile = new UserProfile(); // Composition initialization
    }
    
    // Composition methods
    public void addRole(Role role) {
        roles.add(role);
        role.getUsers().add(this);
    }
    
    public void removeRole(Role role) {
        roles.remove(role);
        role.getUsers().remove(this);
    }
    
    public void addAddress(Address address) {
        addresses.add(address);
        address.setUser(this);
    }
    
    public boolean hasRole(String roleName) {
        return roles.stream()
            .anyMatch(role -> role.getName().equals(roleName));
    }
    
    // Getters and setters
    public UserProfile getProfile() { return profile; }
    public Set<Role> getRoles() { return roles; }
    public List<Address> getAddresses() { return addresses; }
}

@Entity
@Table(name = "user_profiles")
public class UserProfile {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String firstName;
    private String lastName;
    private LocalDate dateOfBirth;
    private String phoneNumber;
    
    // Constructors, getters, and setters
    public String getFullName() {
        return firstName + " " + lastName;
    }
}

@Entity
@Table(name = "addresses")
public class Address {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String street;
    private String city;
    private String state;
    private String zipCode;
    private String country;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;
    
    // Constructors, getters, and setters
}
```

## Loose Coupling
Loose coupling reduces dependencies between components, making the system more flexible and maintainable.

### Interface Based Loose Coupling
```java
// Interface for loose coupling
public interface NotificationService {
    void sendNotification(String recipient, String message, NotificationType type);
}

// Multiple implementations
@Service
@Qualifier("emailNotification")
public class EmailNotificationService implements NotificationService {
    
    @Override
    public void sendNotification(String recipient, String message, NotificationType type) {
        // Email sending logic
        System.out.println("Sending email to: " + recipient + " - " + message);
    }
}

@Service
@Qualifier("smsNotification")
public class SmsNotificationService implements NotificationService {
    
    @Override
    public void sendNotification(String recipient, String message, NotificationType type) {
        // SMS sending logic
        System.out.println("Sending SMS to: " + recipient + " - " + message);
    }
}

// Service using loose coupling
@Service
public class UserRegistrationService {
    
    private final UserRepository userRepository;
    private final NotificationService notificationService;
    
    // Constructor injection for loose coupling
    public UserRegistrationService(
            UserRepository userRepository,
            @Qualifier("emailNotification") NotificationService notificationService) {
        this.userRepository = userRepository;
        this.notificationService = notificationService;
    }
    
    public User registerUser(UserRegistrationDto dto) {
        User user = new User(dto.getUsername(), dto.getEmail());
        User savedUser = userRepository.save(user);
        
        // Loosely coupled notification
        notificationService.sendNotification(
            savedUser.getEmail(),
            "Welcome to our platform!",
            NotificationType.WELCOME
        );
        
        return savedUser;
    }
}

```

## Dependency Injection (DI)

Dependency Injection is Spring's core feature that manages object creation and dependency resolution automatically.

### Constructor Injection
Constructor injection provides dependencies through the class constructor when the object is created. This is the **recommended approach** in Spring Boot applications.

```java
@Service
public class UserService {
    
    private final UserRepository userRepository;
    private final EmailService emailService;
    private final ValidationService validationService;
    
    // Constructor injection - @Autowired optional since Spring 4.3 for single constructor
    public UserService(UserRepository userRepository, 
                      EmailService emailService, 
                      ValidationService validationService) {
        this.userRepository = userRepository;
        this.emailService = emailService;
        this.validationService = validationService;
    }
    
    public User createUser(UserDto userDto) {
        validationService.validate(userDto);
        User user = new User(userDto.getUsername(), userDto.getEmail());
        User savedUser = userRepository.save(user);
        emailService.sendWelcomeEmail(savedUser.getEmail());
        return savedUser;
    }
}
```

#### Key Characteristics
**Immutability**: Dependencies are marked as `final`, ensuring they cannot be changed after object creation
**Mandatory Dependencies**: All dependencies must be provided during object instantiation, guaranteeing fully initialized objects
**Fail-Fast Behavior**: Missing dependencies are detected at application startup, not at runtime.
**Thread Safety**: Immutable dependencies make the class inherently thread-safe.

#### Benefits
- **Testability**: Easy to create instances with mock dependencies in unit tests
- **Clear Dependencies**: Constructor signature explicitly shows all required dependencies
- **Prevents Null Dependencies**: Impossible to have null dependencies if constructor completes successfully
- **Framework Independence**: Works without Spring annotations in tests

## Setter Injection
Setter injection provides dependencies through setter methods after object creation using a no-argument constructor.

```java
@Service
public class NotificationService {
    
    private EmailService emailService;
    private SmsService smsService;
    private PushNotificationService pushService;
    
    // No-argument constructor required
    public NotificationService() {}
    
    @Autowired
    public void setEmailService(EmailService emailService) {
        this.emailService = emailService;
    }
    
    @Autowired
    public void setSmsService(SmsService smsService) {
        this.smsService = smsService;
    }
    
    @Autowired(required = false) // Optional dependency
    public void setPushService(PushNotificationService pushService) {
        this.pushService = pushService;
    }
    
    public void sendNotification(String message, NotificationType type) {
        switch (type) {
            case EMAIL:
                if (emailService != null) emailService.send(message);
                break;
            case SMS:
                if (smsService != null) smsService.send(message);
                break;
            case PUSH:
                if (pushService != null) pushService.send(message);
                break;
        }
    }
}
```

#### Key Characteristics
**Optional Dependencies**: Can mark dependencies as optional using `@Autowired(required = false).
**Mutable Dependencies**: Dependencies can be changed after object creation by calling setters again.
**Partial Initialization**: Object can exist in partially initialized state if some setters aren't called.
**Flexible Configuration**: Allows reconfiguration of dependencies at runtime.

#### Use Cases
- **Optional Dependencies**: When some dependencies are not always required
- **Circular Dependencies**: Can help resolve circular dependency issues
- **Legacy Code Integration**: Easier to retrofit into existing codebases
- **Configuration Changes**: When dependencies might need to change during application lifecycle


## Field Injection
Field injection directly injects dependencies into class fields using annotations, bypassing constructors and setters.

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @Autowired
    private UserService userService;
    
    @Autowired
    private UserMapper userMapper;
    
    @Autowired
    private ValidationService validationService;
    
    @PostMapping
    public ResponseEntity<UserDto> createUser(@Valid @RequestBody CreateUserDto dto) {
        validationService.validateCreateRequest(dto);
        User user = userService.createUser(dto);
        UserDto userDto = userMapper.toDto(user);
        return ResponseEntity.status(HttpStatus.CREATED).body(userDto);
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<UserDto> getUser(@PathVariable Long id) {
        User user = userService.findById(id);
        UserDto userDto = userMapper.toDto(user);
        return ResponseEntity.ok(userDto);
    }
}

```

#### Key Characteristics
**Reflection-Based**: Uses reflection to inject dependencies, which can impact performance.
**Framework Dependency**: Tightly couples code to Spring framework annotations.
**Hidden Dependencies**: Dependencies are not visible in class API, making them harder to discover.
**Testing Challenges**: Difficult to inject mock dependencies in unit tests without Spring context.

#### Limitations
- **No Immutability**: Cannot use `final` fields
- **Testing Complexity**: Requires Spring test context or reflection for testing
- **Hidden Complexity**: Dependencies not obvious from class interface
- **Null Pointer Risk**: No guarantee dependencies are injected before use

## Comparison Summary

| Aspect                     | Constructor  | Setter          | Field                  |
| -------------------------- | ------------ | --------------- | ---------------------- |
| **Immutability**           | ✓ Supported  | ✗ Not supported | ✗ Not supported        |
| **Mandatory Dependencies** | ✓ Enforced   | ✗ Optional      | ✗ Optional             |
| **Testing**                | ✓ Easy       | ⚠️ Moderate     | ✗ Difficult            |
| **Fail-Fast**              | ✓ At startup | ⚠️ At runtime   | ⚠️ At runtime          |
| **Framework Coupling**     | ✓ Low        | ⚠️ Medium       | ✗ High                 |
| **Code Clarity**           | ✓ High       | ⚠️ Medium       | ✗ Low                  |
| **Performance**            | ✓ Best       | ⚠️ Good         | ⚠️ Reflection overhead |
