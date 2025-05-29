To create a basic API in SpringBoot 

1. Entity(Database Mapping) Model(Application Model) DTO(data transfer objects for abstraction)
2. Repo(has interfaces which extend the JpaRepository<Model, Long>)
3. Service(Has functions that contains logic of the application uses the repo functions)
4. Controller(Controls the mapping of the apis)

Example project.

### Application
```java
package com.insane.uncurable;

  

import org.springframework.boot.SpringApplication;

import org.springframework.boot.autoconfigure.SpringBootApplication;

import org.springframework.boot.autoconfigure.domain.EntityScan;

  

@SpringBootApplication

@EntityScan(basePackages = "com.insane.uncurable.models")

public class UncurableApplication {
	
	  
	
	public static void main(String[] args) {
	
		SpringApplication.run(UncurableApplication.class, args);
	
	}
	
	  

}
```

### Controller
```java
//BookController.java
package com.insane.uncurable.controllers;

  

import com.insane.uncurable.models.BookModel;

import com.insane.uncurable.services.BookService;

  

import org.springframework.web.bind.annotation.*;

  

import java.util.List;

  

@RestController

@RequestMapping("/api/books")

public class BookController {

private final BookService service;

  

public BookController(BookService service) {

this.service = service;

}

  

@GetMapping

public List<BookModel> getAll() {

return service.getAll();

}

  

@GetMapping("/{id}")

public BookModel get(@PathVariable Long id) {

return service.get(id);

}

  

@PostMapping

public BookModel add(@RequestBody BookModel book) {

return service.add(book);

}

  

@PutMapping("/{id}")

public BookModel update(@PathVariable Long id, @RequestBody BookModel book) {

return service.update(id, book);

}

  

@DeleteMapping("/{id}")

public void delete(@PathVariable Long id) {

service.delete(id);

}

  

@PatchMapping("/{id}/quantity")

public BookModel updateQty(@PathVariable Long id, @RequestParam int qty) {

return service.updateQuantity(id, qty);

}

}
```

### Repository
```java
//BookRepository.java
package com.insane.uncurable.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import org.springframework.stereotype.Repository;

  

import com.insane.uncurable.models.BookModel;

  

@Repository

public interface BookRepository extends JpaRepository<BookModel, Long> {

}
```

### Service
```java
//BookService.java
package com.insane.uncurable.services;

  

import com.insane.uncurable.models.BookModel;

import com.insane.uncurable.repository.BookRepository;

  

import org.springframework.stereotype.Service;

import java.util.List;

  

@Service

public class BookService {

private final BookRepository repo;

  

public BookService(BookRepository repo) {

this.repo = repo;

}

  

public List<BookModel> getAll() {

return repo.findAll();

}

  

public BookModel get(Long id) {

return repo.findById(id).orElse(null);

}

  

public BookModel add(BookModel book) {

return repo.save(book);

}

  

public BookModel update(Long id, BookModel book) {

BookModel existing = repo.findById(id).orElse(null);

if (existing == null) return null;

existing.setTitle(book.getTitle());

existing.setAuthor(book.getAuthor());

existing.setQuantity(book.getQuantity());

return repo.save(existing);

}

  

public void delete(Long id) {

repo.deleteById(id);

}

  

public BookModel updateQuantity(Long id, int qty) {

BookModel book = repo.findById(id).orElse(null);

if (book == null) return null;

book.setQuantity(qty);

return repo.save(book);

}

}
```

### Model

```java
//BookModel.java
package com.insane.uncurable.models;

  

import jakarta.persistence.Entity;

import jakarta.persistence.Table;

import jakarta.persistence.Id;

import jakarta.persistence.GeneratedValue;

import jakarta.persistence.GenerationType;

import lombok.Getter;

import lombok.Setter;

  

@Entity

@Table(name = "books")

@Getter

@Setter

public class BookModel {

@Id

@GeneratedValue(strategy = GenerationType.IDENTITY)

private Long id;

private String title;

private String author;

private String isbn;

private int quantity;

  

public BookModel() {

}

  

public BookModel(String title, String author, String isbn) {

this.title = title;

this.author = author;

this.isbn = isbn;

}

}
```

