"""
Advanced Type Hints in Python
Learning: Generic, Protocol, Union, Literal, TypedDict, and much more
"""

from typing import (
    # Basic types
    List, Dict, Set, Tuple, Optional, Union, Any, Callable,
    # Advanced types
    TypeVar, Generic, Protocol, runtime_checkable,
    # Special types
    Literal, Final, ClassVar, TypedDict, NamedTuple,
    # For working with functions
    Awaitable, Coroutine, AsyncGenerator, Generator,
    # For validation
    get_type_hints, get_origin, get_args
)
from typing_extensions import Self, ParamSpec, Concatenate
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from collections.abc import Sequence, Mapping
import json


# 1. GENERIC TYPES
T = TypeVar('T')  # Any type
K = TypeVar('K')  # Key type
V = TypeVar('V')  # Value type
P = ParamSpec('P')  # Parameters


class Stack(Generic[T]):
    """Typed stack"""
    
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        """Add element"""
        self._items.append(item)
    
    def pop(self) -> T:
        """Extract element"""
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items.pop()
    
    def peek(self) -> Optional[T]:
        """Look at top element"""
        return self._items[-1] if self._items else None
    
    def is_empty(self) -> bool:
        """Check if empty"""
        return len(self._items) == 0
    
    def size(self) -> int:
        """Stack size"""
        return len(self._items)
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __iter__(self) -> Generator[T, None, None]:
        """Iterate over stack (top to bottom)"""
        for item in reversed(self._items):
            yield item


class Cache(Generic[K, V]):
    """Typed cache"""
    
    def __init__(self, max_size: int = 100) -> None:
        self._data: Dict[K, V] = {}
        self._max_size = max_size
    
    def get(self, key: K) -> Optional[V]:
        """Get value by key"""
        return self._data.get(key)
    
    def set(self, key: K, value: V) -> None:
        """Set value"""
        if len(self._data) >= self._max_size and key not in self._data:
            # Remove first element (simple strategy)
            first_key = next(iter(self._data))
            del self._data[first_key]
        
        self._data[key] = value
    
    def delete(self, key: K) -> bool:
        """Delete key"""
        if key in self._data:
            del self._data[key]
            return True
        return False
    
    def clear(self) -> None:
        """Clear cache"""
        self._data.clear()
    
    def keys(self) -> List[K]:
        """Get all keys"""
        return list(self._data.keys())
    
    def values(self) -> List[V]:
        """Get all values"""
        return list(self._data.values())


# 2. PROTOCOLS - Structural typing
@runtime_checkable
class Drawable(Protocol):
    """Protocol for drawable objects"""
    
    def draw(self) -> str:
        """Draw object"""
        ...
    
    @property
    def area(self) -> float:
        """Object area"""
        ...


@runtime_checkable
class Serializable(Protocol):
    """Protocol for serializable objects"""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        ...
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        """Create from dictionary"""
        ...


class Circle:
    """Circle - implements Drawable"""
    
    def __init__(self, radius: float) -> None:
        self.radius = radius
    
    def draw(self) -> str:
        return f"Circle with radius {self.radius}"
    
    @property
    def area(self) -> float:
        return 3.14159 * self.radius ** 2


class Rectangle:
    """Rectangle - implements Drawable and Serializable"""
    
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
    
    def draw(self) -> str:
        return f"Rectangle {self.width}x{self.height}"
    
    @property
    def area(self) -> float:
        return self.width * self.height
    
    def to_dict(self) -> Dict[str, Any]:
        return {"width": self.width, "height": self.height}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        return cls(data["width"], data["height"])


# 3. UNION AND LITERAL TYPES
class Status(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# Literal for value constraints
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]

# Union for alternative types
ID = Union[int, str]  # ID can be number or string
JSONValue = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]


# 4. TYPEDDICT FOR STRUCTURED DICTIONARIES
class UserDict(TypedDict):
    """Typed user dictionary"""
    id: int
    name: str
    email: str
    age: Optional[int]
    is_active: bool


class ConfigDict(TypedDict, total=False):  # total=False - all fields optional
    """Configuration (all fields optional)"""
    host: str
    port: int
    debug: bool
    timeout: float


# 5. NAMEDTUPLE WITH TYPES
class Point(NamedTuple):
    """Point in 2D space"""
    x: float
    y: float
    
    def distance_to(self, other: 'Point') -> float:
        """Distance to another point"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


class Color(NamedTuple):
    """RGB color"""
    red: int
    green: int
    blue: int
    alpha: float = 1.0
    
    def to_hex(self) -> str:
        """Convert to HEX"""
        return f"#{self.red:02x}{self.green:02x}{self.blue:02x}"


# 6. DATACLASS WITH ADVANCED TYPING
@dataclass(frozen=True)  # Immutable dataclass
class Product:
    """Product in store"""
    id: int
    name: str
    price: float
    category: str
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # ClassVar - class variable, not instance
    _next_id: ClassVar[int] = 1
    
    def __post_init__(self) -> None:
        """Validation after creation"""
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if not self.name.strip():
            raise ValueError("Name cannot be empty")


@dataclass
class Order:
    """Order"""
    id: int
    user_id: int
    products: List[Product]
    status: Status = Status.PENDING
    created_at: Optional[str] = None
    
    @property
    def total_price(self) -> float:
        """Total order price"""
        return sum(product.price for product in self.products)
    
    def add_product(self, product: Product) -> None:
        """Add product"""
        self.products.append(product)
    
    def remove_product(self, product_id: int) -> bool:
        """Remove product by ID"""
        for i, product in enumerate(self.products):
            if product.id == product_id:
                del self.products[i]
                return True
        return False


# 7. FUNCTIONS WITH ADVANCED TYPING
def process_items(
    items: Sequence[T],  # Sequence - more general type than List
    processor: Callable[[T], V],  # Processing function
    filter_func: Optional[Callable[[T], bool]] = None  # Optional filter
) -> List[V]:
    """
    Process items with function
    
    Args:
        items: Sequence of items
        processor: Function to process each item
        filter_func: Optional filtering function
    
    Returns:
        List of processed items
    """
    filtered_items = items
    if filter_func:
        filtered_items = [item for item in items if filter_func(item)]
    
    return [processor(item) for item in filtered_items]


def create_cache_factory() -> Callable[[], Cache[str, Any]]:
    """Factory for creating caches"""
    def factory() -> Cache[str, Any]:
        return Cache[str, Any](max_size=50)
    return factory


# Overload for functions with different signatures
from typing import overload

@overload
def get_user_info(user_id: int) -> UserDict:
    ...

@overload  
def get_user_info(user_id: str) -> UserDict:
    ...

def get_user_info(user_id: ID) -> UserDict:
    """Get user information by ID"""
    # In reality, this would be a DB query
    return UserDict(
        id=int(user_id) if isinstance(user_id, str) else user_id,
        name="Test User",
        email="test@example.com",
        age=25,
        is_active=True
    )


# 8. ASYNC TYPES
async def fetch_data(url: str) -> Dict[str, Any]:
    """Async data fetching"""
    # Simulate HTTP request
    await asyncio.sleep(0.1)
    return {"url": url, "status": "success"}


async def process_urls(urls: List[str]) -> AsyncGenerator[Dict[str, Any], None]:
    """Async generator for processing URLs"""
    for url in urls:
        data = await fetch_data(url)
        yield data


# 9. FUNCTIONS FOR WORKING WITH TYPES
def analyze_type(obj: Any) -> Dict[str, Any]:
    """Analyze object type"""
    obj_type = type(obj)
    
    return {
        "type": obj_type.__name__,
        "module": obj_type.__module__,
        "mro": [cls.__name__ for cls in obj_type.__mro__],
        "is_generic": hasattr(obj_type, "__origin__"),
        "origin": getattr(obj_type, "__origin__", None),
        "args": getattr(obj_type, "__args__", ()),
    }


def validate_protocol(obj: Any, protocol: type) -> bool:
    """Check if object conforms to protocol"""
    return isinstance(obj, protocol)


# DEMONSTRATION
def demo_type_hints() -> None:
    """Advanced type hints demonstration"""
    print("🔍 ADVANCED TYPE HINTS DEMONSTRATION\n")
    
    # 1. Generic types
    print("1️⃣ Generic types:")
    int_stack: Stack[int] = Stack()
    int_stack.push(1)
    int_stack.push(2)
    int_stack.push(3)
    
    print(f"Stack: {list(int_stack)}")
    print(f"Top element: {int_stack.peek()}")
    
    str_cache: Cache[str, str] = Cache()
    str_cache.set("key1", "value1")
    str_cache.set("key2", "value2")
    print(f"Cache: {str_cache.get('key1')}")
    print()
    
    # 2. Protocols
    print("2️⃣ Protocols:")
    circle = Circle(5.0)
    rectangle = Rectangle(4.0, 3.0)
    
    shapes: List[Drawable] = [circle, rectangle]
    for shape in shapes:
        print(f"{shape.draw()}, area: {shape.area}")
    
    print(f"Circle is Drawable: {validate_protocol(circle, Drawable)}")
    print(f"Rectangle is Serializable: {validate_protocol(rectangle, Serializable)}")
    print()
    
    # 3. TypedDict
    print("3️⃣ TypedDict:")
    user: UserDict = {
        "id": 1,
        "name": "Ivan Petrov",
        "email": "ivan@example.com",
        "age": 30,
        "is_active": True
    }
    print(f"User: {user['name']}, age: {user['age']}")
    
    config: ConfigDict = {"host": "localhost", "port": 8000}
    print(f"Configuration: {config}")
    print()
    
    # 4. NamedTuple and dataclass
    print("4️⃣ NamedTuple and dataclass:")
    point1 = Point(0.0, 0.0)
    point2 = Point(3.0, 4.0)
    print(f"Distance between points: {point1.distance_to(point2)}")
    
    color = Color(255, 128, 0)
    print(f"Color: {color.to_hex()}")
    
    product = Product(1, "Laptop", 50000.0, "Electronics", ["computer", "work"])
    order = Order(1, 123, [product])
    print(f"Order total: {order.total_price}")
    print()
    
    # 5. Functions with typing
    print("5️⃣ Functions with typing:")
    numbers = [1, 2, 3, 4, 5]
    squared = process_items(
        numbers,
        lambda x: x ** 2,
        lambda x: x % 2 == 0  # Only even numbers
    )
    print(f"Squares of even numbers: {squared}")
    
    user_info = get_user_info(123)
    print(f"User info: {user_info['name']}")
    print()
    
    # 6. Type analysis
    print("6️⃣ Type analysis:")
    cache_analysis = analyze_type(str_cache)
    print(f"Cache analysis: {cache_analysis}")


async def demo_async_types() -> None:
    """Async types demonstration"""
    print("7️⃣ Async types:")
    
    urls = ["http://example.com", "http://google.com", "http://github.com"]
    
    async for data in process_urls(urls):
        print(f"Processed URL: {data}")


if __name__ == "__main__":
    demo_type_hints()
    print("\n" + "="*50)
    asyncio.run(demo_async_types())