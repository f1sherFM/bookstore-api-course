"""
Advanced Decorators + Type Hints
Learning: custom decorators, functools, typing, generics
"""

import time
import functools
import logging
from typing import (
    TypeVar, Generic, Callable, Any, Dict, List, Optional, 
    Union, Tuple, Protocol, runtime_checkable
)
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio
import inspect


# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Type Variables for Generic types
T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])
R = TypeVar('R')  # Return type


# 1. TIMER DECORATOR
def timer(func: F) -> F:
    """
    Decorator for measuring function execution time
    Supports both synchronous and asynchronous functions
    """
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                end_time = time.perf_counter()
                execution_time = end_time - start_time
                logger.info(f"⏱️ {func.__name__} executed in {execution_time:.4f} seconds")
        return async_wrapper  # type: ignore
    else:
        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.perf_counter()
                execution_time = end_time - start_time
                logger.info(f"⏱️ {func.__name__} executed in {execution_time:.4f} seconds")
        return sync_wrapper  # type: ignore


# 2. RETRY DECORATOR FOR ERRORS
def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[type, ...] = (Exception,)
) -> Callable[[F], F]:
    """
    Decorator for retrying function on errors
    
    Args:
        max_attempts: Maximum number of attempts
        delay: Initial delay between attempts (seconds)
        backoff: Multiplier for increasing delay
        exceptions: Exception types to retry on
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts - 1:  # Last attempt
                        logger.error(f"❌ {func.__name__} failed to execute after {max_attempts} attempts")
                        raise e
                    
                    logger.warning(f"🔄 {func.__name__} attempt {attempt + 1} failed: {e}")
                    logger.info(f"⏳ Waiting {current_delay:.2f} seconds...")
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            # This code should never execute, but for typing
            if last_exception:
                raise last_exception
                
        return wrapper  # type: ignore
    return decorator


# 3. ADVANCED CACHING DECORATOR
class CacheStats:
    """Cache statistics"""
    def __init__(self) -> None:
        self.hits: int = 0
        self.misses: int = 0
        self.cache_size: int = 0
    
    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0.0
    
    def __str__(self) -> str:
        return f"Cache(hits={self.hits}, misses={self.misses}, hit_rate={self.hit_rate:.1f}%, size={self.cache_size})"


def cache(
    maxsize: Optional[int] = 128,
    ttl: Optional[float] = None,
    typed: bool = False
) -> Callable[[F], F]:
    """
    Advanced caching decorator
    
    Args:
        maxsize: Maximum cache size (None = unlimited)
        ttl: Time to live for entries in seconds (None = forever)
        typed: Distinguish argument types (True/False)
    """
    def decorator(func: F) -> F:
        cache_data: Dict[str, Tuple[Any, float]] = {}
        stats = CacheStats()
        
        def make_key(*args: Any, **kwargs: Any) -> str:
            """Create cache key"""
            key_parts = []
            
            # Add positional arguments
            for arg in args:
                if typed:
                    key_parts.append(f"{type(arg).__name__}:{arg}")
                else:
                    key_parts.append(str(arg))
            
            # Add keyword arguments
            for k, v in sorted(kwargs.items()):
                if typed:
                    key_parts.append(f"{k}={type(v).__name__}:{v}")
                else:
                    key_parts.append(f"{k}={v}")
            
            return "|".join(key_parts)
        
        def is_expired(timestamp: float) -> bool:
            """Check TTL expiration"""
            if ttl is None:
                return False
            return time.time() - timestamp > ttl
        
        def cleanup_expired() -> None:
            """Clean up expired entries"""
            if ttl is None:
                return
            
            current_time = time.time()
            expired_keys = [
                key for key, (_, timestamp) in cache_data.items()
                if current_time - timestamp > ttl
            ]
            
            for key in expired_keys:
                del cache_data[key]
            
            stats.cache_size = len(cache_data)
        
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Clean up expired entries
            cleanup_expired()
            
            # Create key
            cache_key = make_key(*args, **kwargs)
            
            # Check cache
            if cache_key in cache_data:
                value, timestamp = cache_data[cache_key]
                if not is_expired(timestamp):
                    stats.hits += 1
                    logger.debug(f"💾 Cache HIT for {func.__name__}")
                    return value
                else:
                    # Remove expired entry
                    del cache_data[cache_key]
            
            # Calculate value
            stats.misses += 1
            logger.debug(f"🔍 Cache MISS for {func.__name__}")
            result = func(*args, **kwargs)
            
            # Save to cache
            current_time = time.time()
            cache_data[cache_key] = (result, current_time)
            
            # Check cache size
            if maxsize is not None and len(cache_data) > maxsize:
                # Remove oldest entry (simple strategy)
                oldest_key = min(cache_data.keys(), 
                               key=lambda k: cache_data[k][1])
                del cache_data[oldest_key]
            
            stats.cache_size = len(cache_data)
            return result
        
        # Add cache management methods
        wrapper.cache_info = lambda: stats  # type: ignore
        wrapper.cache_clear = lambda: cache_data.clear()  # type: ignore
        
        return wrapper  # type: ignore
    return decorator


# 4. VALIDATION DECORATOR WITH PROTOCOLS
@runtime_checkable
class Validator(Protocol):
    """Protocol for validators"""
    def validate(self, value: Any) -> bool:
        ...
    
    def get_error_message(self, value: Any) -> str:
        ...


class RangeValidator:
    """Number range validator"""
    def __init__(self, min_val: float, max_val: float) -> None:
        self.min_val = min_val
        self.max_val = max_val
    
    def validate(self, value: Any) -> bool:
        return isinstance(value, (int, float)) and self.min_val <= value <= self.max_val
    
    def get_error_message(self, value: Any) -> str:
        return f"Value {value} must be in range [{self.min_val}, {self.max_val}]"


class TypeValidator:
    """Type validator"""
    def __init__(self, expected_type: type) -> None:
        self.expected_type = expected_type
    
    def validate(self, value: Any) -> bool:
        return isinstance(value, self.expected_type)
    
    def get_error_message(self, value: Any) -> str:
        return f"Expected type {self.expected_type.__name__}, got {type(value).__name__}"


def validate_args(**validators: Validator) -> Callable[[F], F]:
    """
    Decorator for function argument validation
    
    Usage:
        @validate_args(
            age=RangeValidator(0, 150),
            name=TypeValidator(str)
        )
        def create_user(name: str, age: int) -> User:
            ...
    """
    def decorator(func: F) -> F:
        # Get function parameter information
        sig = inspect.signature(func)
        param_names = list(sig.parameters.keys())
        
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Create dictionary of all arguments
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Validate each argument
            for param_name, validator in validators.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not validator.validate(value):
                        error_msg = validator.get_error_message(value)
                        raise ValueError(f"Validation of parameter '{param_name}' failed: {error_msg}")
            
            return func(*args, **kwargs)
        
        return wrapper  # type: ignore
    return decorator


# 5. LOGGING DECORATOR WITH CONTEXT
def log_calls(
    level: int = logging.INFO,
    include_args: bool = True,
    include_result: bool = True,
    max_arg_length: int = 100
) -> Callable[[F], F]:
    """
    Decorator for logging function calls
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Prepare argument information
            args_info = ""
            if include_args:
                args_str = ", ".join([
                    str(arg)[:max_arg_length] + ("..." if len(str(arg)) > max_arg_length else "")
                    for arg in args
                ])
                kwargs_str = ", ".join([
                    f"{k}={str(v)[:max_arg_length]}" + ("..." if len(str(v)) > max_arg_length else "")
                    for k, v in kwargs.items()
                ])
                all_args = [args_str, kwargs_str] if args_str and kwargs_str else [args_str or kwargs_str]
                args_info = f"({', '.join(filter(None, all_args))})"
            
            logger.log(level, f"🔵 Calling {func.__name__}{args_info}")
            
            try:
                result = func(*args, **kwargs)
                
                if include_result:
                    result_str = str(result)[:max_arg_length]
                    if len(str(result)) > max_arg_length:
                        result_str += "..."
                    logger.log(level, f"✅ {func.__name__} returned: {result_str}")
                else:
                    logger.log(level, f"✅ {func.__name__} executed successfully")
                
                return result
            
            except Exception as e:
                logger.log(logging.ERROR, f"❌ {func.__name__} raised exception: {e}")
                raise
        
        return wrapper  # type: ignore
    return decorator


# DEMONSTRATION OF ALL DECORATORS
class MathOperations:
    """Class for demonstrating decorators"""
    
    @timer
    @cache(maxsize=50, ttl=10.0)
    @log_calls(include_result=True)
    def fibonacci(self, n: int) -> int:
        """Calculate Fibonacci number with caching"""
        if n <= 1:
            return n
        return self.fibonacci(n - 1) + self.fibonacci(n - 2)
    
    @retry(max_attempts=3, delay=0.1, exceptions=(ValueError, ZeroDivisionError))
    @validate_args(
        a=TypeValidator(float),
        b=TypeValidator(float)
    )
    @timer
    def divide(self, a: float, b: float) -> float:
        """Division with retry on errors"""
        if b == 0:
            raise ZeroDivisionError("Division by zero!")
        return a / b
    
    @cache(maxsize=10)
    @validate_args(
        base=RangeValidator(1, 1000),
        exponent=RangeValidator(0, 10)
    )
    def power(self, base: float, exponent: float) -> float:
        """Power calculation with validation"""
        time.sleep(0.1)  # Simulate heavy computation
        return base ** exponent


# Async functions with decorators
@timer
async def async_operation(duration: float) -> str:
    """Async operation with timing"""
    await asyncio.sleep(duration)
    return f"Operation completed in {duration} seconds"


def demo_decorators() -> None:
    """Demonstration of all decorators"""
    print("🎭 ADVANCED DECORATORS DEMONSTRATION\n")
    
    math_ops = MathOperations()
    
    # 1. Caching + logging
    print("1️⃣ Fibonacci caching:")
    print(f"fibonacci(10) = {math_ops.fibonacci(10)}")
    print(f"fibonacci(10) = {math_ops.fibonacci(10)}")  # From cache
    print(f"Cache info: {math_ops.fibonacci.cache_info()}")
    print()
    
    # 2. Validation + retry
    print("2️⃣ Validation and retry:")
    try:
        result = math_ops.divide(10.0, 2.0)
        print(f"10 / 2 = {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    try:
        math_ops.divide("10", 2.0)  # Type error
    except ValueError as e:
        print(f"Validation error: {e}")
    print()
    
    # 3. Range validation
    print("3️⃣ Range validation:")
    try:
        result = math_ops.power(2.0, 3.0)
        print(f"2^3 = {result}")
        result = math_ops.power(2.0, 3.0)  # From cache
        print(f"2^3 = {result} (from cache)")
    except ValueError as e:
        print(f"Validation error: {e}")
    
    try:
        math_ops.power(2000.0, 3.0)  # Out of range
    except ValueError as e:
        print(f"Validation error: {e}")
    print()


async def demo_async_decorators() -> None:
    """Demonstration of async decorators"""
    print("4️⃣ Async decorators:")
    result = await async_operation(0.5)
    print(f"Result: {result}")


if __name__ == "__main__":
    # Synchronous demonstration
    demo_decorators()
    
    # Asynchronous demonstration
    print("\n" + "="*50)
    asyncio.run(demo_async_decorators())