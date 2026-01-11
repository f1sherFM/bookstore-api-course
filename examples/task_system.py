"""
Task Management System - Advanced OOP
Learning: ABC, multiple inheritance, property, magic methods, context managers
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional, Dict, Any
import json


class TaskStatus(Enum):
    """Task statuses"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"


class Priority(Enum):
    """Task priorities"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


# Abstract base class
class BaseTask(ABC):
    """Abstract base class for all tasks"""
    
    def __init__(self, title: str, description: str = ""):
        self._title = title
        self._description = description
        self._created_at = datetime.now()
        self._status = TaskStatus.TODO
        self._id = id(self)  # Simple ID based on memory address
    
    @property
    def title(self) -> str:
        """Title getter"""
        return self._title
    
    @title.setter
    def title(self, value: str) -> None:
        """Title setter with validation"""
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        self._title = value.strip()
    
    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, value: str) -> None:
        self._description = value.strip()
    
    @property
    def status(self) -> TaskStatus:
        return self._status
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def id(self) -> int:
        return self._id
    
    @abstractmethod
    def get_priority(self) -> Priority:
        """Abstract method - each task type defines its own priority"""
        pass
    
    @abstractmethod
    def estimate_duration(self) -> timedelta:
        """Abstract method - execution time estimate"""
        pass
    
    def start(self) -> None:
        """Start task execution"""
        if self._status == TaskStatus.TODO:
            self._status = TaskStatus.IN_PROGRESS
        else:
            raise ValueError(f"Cannot start task with status {self._status.value}")
    
    def complete(self) -> None:
        """Complete task"""
        if self._status == TaskStatus.IN_PROGRESS:
            self._status = TaskStatus.DONE
        else:
            raise ValueError(f"Cannot complete task with status {self._status.value}")
    
    def cancel(self) -> None:
        """Cancel task"""
        if self._status in [TaskStatus.TODO, TaskStatus.IN_PROGRESS]:
            self._status = TaskStatus.CANCELLED
        else:
            raise ValueError(f"Cannot cancel task with status {self._status.value}")
    
    # Magic methods
    def __str__(self) -> str:
        """String representation for users"""
        return f"{self.title} ({self.status.value})"
    
    def __repr__(self) -> str:
        """String representation for developers"""
        return f"{self.__class__.__name__}(id={self.id}, title='{self.title}', status='{self.status.value}')"
    
    def __eq__(self, other) -> bool:
        """Task comparison by ID"""
        if not isinstance(other, BaseTask):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash for use in sets and dictionaries"""
        return hash(self.id)


# Mixins for additional functionality
class TimestampMixin:
    """Mixin for tracking change timestamps"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._updated_at = datetime.now()
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    def _update_timestamp(self) -> None:
        """Update timestamp"""
        self._updated_at = datetime.now()


class AssigneeMixin:
    """Mixin for assigning executor"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._assignee: Optional[str] = None
    
    @property
    def assignee(self) -> Optional[str]:
        return self._assignee
    
    @assignee.setter
    def assignee(self, value: Optional[str]) -> None:
        self._assignee = value
        if hasattr(self, '_update_timestamp'):
            self._update_timestamp()


# Concrete task classes with multiple inheritance
class SimpleTask(BaseTask, TimestampMixin):
    """Simple task"""
    
    def __init__(self, title: str, description: str = "", priority: Priority = Priority.MEDIUM):
        super().__init__(title, description)
        self._priority = priority
    
    def get_priority(self) -> Priority:
        return self._priority
    
    def estimate_duration(self) -> timedelta:
        # Simple task - 30 minutes to 2 hours depending on priority
        base_hours = {
            Priority.LOW: 0.5,
            Priority.MEDIUM: 1,
            Priority.HIGH: 1.5,
            Priority.URGENT: 2
        }
        return timedelta(hours=base_hours[self._priority])


class WorkTask(BaseTask, TimestampMixin, AssigneeMixin):
    """Work task with assignee"""
    
    def __init__(self, title: str, description: str = "", assignee: Optional[str] = None):
        super().__init__(title, description)
        self.assignee = assignee
    
    def get_priority(self) -> Priority:
        # Work tasks have high priority by default
        return Priority.HIGH
    
    def estimate_duration(self) -> timedelta:
        # Work tasks usually take more time
        return timedelta(hours=4)


class UrgentTask(BaseTask, TimestampMixin, AssigneeMixin):
    """Urgent task"""
    
    def __init__(self, title: str, description: str = "", deadline: Optional[datetime] = None):
        super().__init__(title, description)
        self._deadline = deadline or (datetime.now() + timedelta(hours=24))
    
    @property
    def deadline(self) -> datetime:
        return self._deadline
    
    @property
    def is_overdue(self) -> bool:
        """Check if overdue"""
        return datetime.now() > self._deadline and self.status != TaskStatus.DONE
    
    def get_priority(self) -> Priority:
        return Priority.URGENT
    
    def estimate_duration(self) -> timedelta:
        return timedelta(hours=1)


# Context Manager for working with tasks
class TaskManager:
    """Task manager with context manager functionality"""
    
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[BaseTask] = []
        self._in_context = False
    
    def add_task(self, task: BaseTask) -> None:
        """Add task"""
        self.tasks.append(task)
    
    def get_task_by_id(self, task_id: int) -> Optional[BaseTask]:
        """Find task by ID"""
        return next((task for task in self.tasks if task.id == task_id), None)
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[BaseTask]:
        """Get tasks by status"""
        return [task for task in self.tasks if task.status == status]
    
    def get_overdue_tasks(self) -> List[UrgentTask]:
        """Get overdue tasks"""
        return [task for task in self.tasks 
                if isinstance(task, UrgentTask) and task.is_overdue]
    
    # Context Manager methods
    def __enter__(self):
        """Context entry - load tasks from file"""
        print(f"📂 Loading tasks from {self.filename}")
        self._in_context = True
        try:
            self._load_tasks()
        except FileNotFoundError:
            print("📝 File not found, creating new task list")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context exit - save tasks to file"""
        if exc_type is None:
            print(f"💾 Saving tasks to {self.filename}")
            self._save_tasks()
        else:
            print(f"❌ Error: {exc_val}, tasks not saved")
        self._in_context = False
        return False  # Don't suppress exceptions
    
    def _load_tasks(self) -> None:
        """Load tasks from file (simplified version)"""
        # In a real project, this would be deserialization
        pass
    
    def _save_tasks(self) -> None:
        """Save tasks to file (simplified version)"""
        # In a real project, this would be serialization
        task_data = []
        for task in self.tasks:
            task_data.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status.value,
                'type': task.__class__.__name__,
                'created_at': task.created_at.isoformat()
            })
        
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(task_data, f, ensure_ascii=False, indent=2)
    
    def __len__(self) -> int:
        """Number of tasks"""
        return len(self.tasks)
    
    def __iter__(self):
        """Iterate over tasks"""
        return iter(self.tasks)


# Demonstration of all features
def demo():
    """Advanced OOP demonstration in Python"""
    print("🚀 Advanced OOP in Python Demonstration\n")
    
    # Create different types of tasks
    simple = SimpleTask("Learn Python", "OOP basics", Priority.HIGH)
    work = WorkTask("Write report", "Quarterly report", "Ivan Petrov")
    urgent = UrgentTask("Fix bug", "Critical bug in production")
    
    print("📋 Created tasks:")
    print(f"1. {simple} - Priority: {simple.get_priority().name}")
    print(f"2. {work} - Assignee: {work.assignee}")
    print(f"3. {urgent} - Deadline: {urgent.deadline.strftime('%Y-%m-%d %H:%M')}")
    print()
    
    # Context Manager demonstration
    print("🔄 Working with Context Manager:")
    with TaskManager("demo_tasks.json") as manager:
        manager.add_task(simple)
        manager.add_task(work)
        manager.add_task(urgent)
        
        print(f"Total tasks: {len(manager)}")
        
        # Work with tasks
        simple.start()
        work.start()
        work.complete()
        
        print("\n📊 Statistics:")
        print(f"TODO: {len(manager.get_tasks_by_status(TaskStatus.TODO))}")
        print(f"In progress: {len(manager.get_tasks_by_status(TaskStatus.IN_PROGRESS))}")
        print(f"Completed: {len(manager.get_tasks_by_status(TaskStatus.DONE))}")
        
        # Check overdue
        overdue = manager.get_overdue_tasks()
        if overdue:
            print(f"⚠️ Overdue tasks: {len(overdue)}")
    
    print("\n✅ Demonstration completed!")
    
    # Magic methods demonstration
    print("\n🎭 Magic Methods:")
    print(f"str(simple): {str(simple)}")
    print(f"repr(simple): {repr(simple)}")
    print(f"simple == work: {simple == work}")
    print(f"hash(simple): {hash(simple)}")


if __name__ == "__main__":
    demo()