# 🎭 Decorators + Type Hints - Cheat Sheet

## 🎯 What we learned (10:30-12:00)

### 1. Custom decorators

#### Basic template
```python
import functools
from typing import TypeVar, Callable, Any

F = TypeVar('F', bound=Callable[..., Any])

def my_decorator(func: F) -> F:
    @functools.wraps(func)  # Preserves function metadata
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Logic before execution
        result = func(*args, **kwargs)
        # Logic after execution
        return result
    return wrapper  # type: ignore
```

#### Decorator with parameters
```python
def retry(max_attempts: int = 3) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
        return wrapper  # type: ignore
    return decorator
```

#### Universal decorator (sync + async)
```python
def timer(func: F) -> F:
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            print(f"Time: {time.perf_counter() - start:.4f}s")
            return result
        return async_wrapper  # type: ignore
    else:
        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            print(f"Time: {time.perf_counter() - start:.4f}s")
            return result
        return sync_wrapper  # type: ignore
```

### 2. Advanced Type Hints

#### Generic types
```python
from typing import TypeVar, Generic, List

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> T:
        return self._items.pop()

# Usage
int_stack: Stack[int] = Stack()
str_stack: Stack[str] = Stack()
```

#### Protocols (structural typing)
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...
    
    @property
    def area(self) -> float: ...

class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius
    
    def draw(self) -> str:
        return f"Circle({self.radius})"
    
    @property
    def area(self) -> float:
        return 3.14 * self.radius ** 2

# Circle automatically conforms to Drawable!
def render(shape: Drawable) -> None:
    print(shape.draw())

circle = Circle(5)
render(circle)  # Works!
```

#### Union and Literal
```python
from typing import Union, Literal

# Union - one of the types
ID = Union[int, str]

# Literal - specific values
Status = Literal["pending", "completed", "failed"]
HttpMethod = Literal["GET", "POST", "PUT", "DELETE"]

def process_request(method: HttpMethod, status: Status) -> None:
    # IDE knows exact possible values!
    pass
```

#### TypedDict
```python
from typing import TypedDict, Optional

class UserDict(TypedDict):
    id: int
    name: str
    email: str
    age: Optional[int]

# Use as regular dict, but with type checking
user: UserDict = {
    "id": 1,
    "name": "John",
    "email": "john@example.com",
    "age": 30
}
```

#### Callable types
```python
from typing import Callable

# Function that takes int and returns str
Processor = Callable[[int], str]

def apply_processor(data: List[int], proc: Processor) -> List[str]:
    return [proc(item) for item in data]

# Usage
result = apply_processor([1, 2, 3], lambda x: f"Item {x}")
```

### 3. Combining decorators and types

```python
from typing import TypeVar, Callable, Any, cast
import functools

F = TypeVar('F', bound=Callable[..., Any])

def validate_types(func: F) -> F:
    """Decorator for runtime type validation"""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Get type annotations
        hints = get_type_hints(func)
        
        # Validate arguments
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        
        for name, value in bound.arguments.items():
            if name in hints:
                expected_type = hints[name]
                if not isinstance(value, expected_type):
                    raise TypeError(f"Argument {name} must be {expected_type}")
        
        return func(*args, **kwargs)
    
    return cast(F, wrapper)

# Usage
@validate_types
def add_numbers(a: int, b: int) -> int:
    return a + b
```

## 🔥 Practical patterns

### 1. Decorator class
```python
class RateLimiter:
    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self.calls: List[float] = []
    
    def __call__(self, func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            now = time.time()
            # Clean old calls
            self.calls = [call for call in self.calls if now - call < self.period]
            
            if len(self.calls) >= self.max_calls:
                raise Exception("Rate limit exceeded")
            
            self.calls.append(now)
            return func(*args, **kwargs)
        
        return wrapper  # type: ignore

# Usage
@RateLimiter(max_calls=5, period=60.0)  # 5 calls per minute
def api_call() -> str:
    return "API response"
```

### 2. Context Manager + Generic
```python
from typing import ContextManager, TypeVar, Generic
from contextlib import contextmanager

T = TypeVar('T')

class ResourceManager(Generic[T]):
    def __init__(self, resource: T) -> None:
        self.resource = resource
    
    def __enter__(self) -> T:
        print(f"Acquiring {type(self.resource).__name__}")
        return self.resource
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        print(f"Releasing {type(self.resource).__name__}")

# Usage
with ResourceManager("database_connection") as db:
    print(f"Using {db}")
```

### 3. Async decorators with typing
```python
from typing import Awaitable, TypeVar, Callable

AsyncF = TypeVar('AsyncF', bound=Callable[..., Awaitable[Any]])

def async_retry(max_attempts: int = 3) -> Callable[[AsyncF], AsyncF]:
    def decorator(func: AsyncF) -> AsyncF:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
        return wrapper  # type: ignore
    return decorator
```

## ⚡ Best practices

### Type Hints
- ✅ Use `from __future__ import annotations` for forward references
- ✅ Prefer `list[int]` over `List[int]` (Python 3.9+)
- ✅ Use `Optional[T]` instead of `Union[T, None]`
- ✅ Apply `Protocol` for duck typing
- ❌ Don't overuse `Any` - better use `object`

### Decorators
- ✅ Always use `@functools.wraps`
- ✅ Support both sync and async functions
- ✅ Add management methods (cache_clear, stats)
- ✅ Make decorators composable
- ❌ Don't change function signature unnecessarily

## 🎯 Next step: FastAPI (13:00-15:00)

Ready to create modern API with automatic documentation? 🚀