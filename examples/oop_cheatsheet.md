# 🐍 Advanced OOP in Python - Cheat Sheet

## 🎯 What we learned (9:00-10:30)

### 1. Abstract classes (ABC)
```python
from abc import ABC, abstractmethod

class BaseTask(ABC):
    @abstractmethod
    def get_priority(self):
        pass
```
**Why:** Defines interface that inheritors must implement

### 2. Property decorators
```python
@property
def title(self):
    return self._title

@title.setter  
def title(self, value):
    if not value:
        raise ValueError("Empty title")
    self._title = value
```
**Why:** Controlled access to attributes with validation

### 3. Magic Methods
```python
def __str__(self):      # For users
    return f"{self.title} ({self.status})"

def __repr__(self):     # For developers  
    return f"Task(id={self.id})"

def __eq__(self, other): # Comparison
    return self.id == other.id

def __hash__(self):     # For set/dict
    return hash(self.id)
```

### 4. Multiple inheritance + Mixins
```python
class TimestampMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Important!
        self._updated_at = datetime.now()

class WorkTask(BaseTask, TimestampMixin, AssigneeMixin):
    pass  # Gets functionality from all parents
```
**Rule:** Always use `super()` in mixins!

### 5. Context Managers
```python
class TaskManager:
    def __enter__(self):
        # Resource preparation
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Resource cleanup
        if exc_type is None:
            self.save()  # Success
        else:
            print(f"Error: {exc_val}")  # Error
        return False  # Don't suppress exceptions
```

## 🔥 Key Principles

### MRO (Method Resolution Order)
```python
class A: pass
class B(A): pass  
class C(A): pass
class D(B, C): pass

print(D.__mro__)  # Method search order
```

### Composition vs Inheritance
- **Inheritance:** "is-a" (Task IS-A BaseTask)
- **Composition:** "has-a" (TaskManager HAS-A List[Task])

### SOLID principles
- **S**ingle Responsibility - one class = one responsibility
- **O**pen/Closed - open for extension, closed for modification
- **L**iskov Substitution - inheritors replace parents
- **I**nterface Segregation - many small interfaces
- **D**ependency Inversion - depend on abstractions

## ⚡ Practical Tips

### 1. When to use ABC
```python
# ✅ Good - defines contract
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount): pass

# ❌ Bad - no common interface
class Animal(ABC): pass
```

### 2. Property vs regular attributes
```python
# ✅ Use property for:
@property
def age(self):
    return (datetime.now() - self.birth_date).days // 365

# ❌ Not needed for simple attributes
@property  
def name(self):
    return self._name  # Just use self.name
```

### 3. Mixins should be small
```python
# ✅ Good - single function
class TimestampMixin:
    def update_timestamp(self): pass

# ❌ Bad - too many functions
class EverythingMixin:
    def timestamp(self): pass
    def validate(self): pass  
    def serialize(self): pass
```

## 🎯 Next step: Decorators + Type Hints (10:30-12:00)

Ready to continue? Moving on to creating custom decorators! 🚀