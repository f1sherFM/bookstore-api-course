"""
Practical exercises for advanced OOP
Try to complete these exercises on your own!
"""

from task_system import *
from datetime import datetime, timedelta


def practice_1_custom_task():
    """
    EXERCISE 1: Create your own task type
    
    Create a PersonalTask class that:
    - Inherits from BaseTask and TimestampMixin
    - Has an additional category field (string)
    - Priority depends on category:
      * "health" -> URGENT
      * "family" -> HIGH  
      * "hobby" -> LOW
      * everything else -> MEDIUM
    - Execution time: 2 hours for all
    """
    print("🎯 EXERCISE 1: Create PersonalTask")
    print("Hint: class PersonalTask(BaseTask, TimestampMixin):")
    print("Need to implement get_priority() and estimate_duration()")
    print()


def practice_2_custom_manager():
    """
    EXERCISE 2: Extend TaskManager
    
    Add methods:
    - get_tasks_by_priority(priority: Priority) -> List[BaseTask]
    - get_tasks_by_assignee(assignee: str) -> List[BaseTask]
    - get_completion_rate() -> float (percentage of completed tasks)
    """
    print("🎯 EXERCISE 2: Extend TaskManager")
    print("Add new methods for filtering and statistics")
    print()


def practice_3_decorators():
    """
    EXERCISE 3: Create decorators for tasks
    
    Create decorators:
    - @log_task_changes - logs status changes
    - @validate_task - validates data
    - @auto_assign - automatically assigns executor
    """
    print("🎯 EXERCISE 3: Create decorators")
    print("Decorators should work with start(), complete(), cancel() methods")
    print()


def practice_4_advanced_context():
    """
    EXERCISE 4: Advanced Context Manager
    
    Create DatabaseTaskManager that:
    - Connects to database on context entry
    - Starts transaction
    - On success - commits transaction
    - On error - rolls back transaction
    - Closes connection on exit
    """
    print("🎯 EXERCISE 4: DatabaseTaskManager")
    print("Use try/except in __exit__ for transaction handling")
    print()


# Solutions (uncomment to check)

class PersonalTask(BaseTask, TimestampMixin):
    """Solution for exercise 1"""
    
    def __init__(self, title: str, description: str = "", category: str = "general"):
        super().__init__(title, description)
        self.category = category
    
    def get_priority(self) -> Priority:
        priority_map = {
            "health": Priority.URGENT,
            "family": Priority.HIGH,
            "hobby": Priority.LOW
        }
        return priority_map.get(self.category.lower(), Priority.MEDIUM)
    
    def estimate_duration(self) -> timedelta:
        return timedelta(hours=2)


class ExtendedTaskManager(TaskManager):
    """Solution for exercise 2"""
    
    def get_tasks_by_priority(self, priority: Priority) -> List[BaseTask]:
        return [task for task in self.tasks if task.get_priority() == priority]
    
    def get_tasks_by_assignee(self, assignee: str) -> List[BaseTask]:
        return [task for task in self.tasks 
                if hasattr(task, 'assignee') and task.assignee == assignee]
    
    def get_completion_rate(self) -> float:
        if not self.tasks:
            return 0.0
        completed = len(self.get_tasks_by_status(TaskStatus.DONE))
        return (completed / len(self.tasks)) * 100


def log_task_changes(func):
    """Solution for exercise 3 - logging decorator"""
    def wrapper(self, *args, **kwargs):
        old_status = self.status
        result = func(self, *args, **kwargs)
        new_status = self.status
        if old_status != new_status:
            print(f"📝 Task '{self.title}': {old_status.value} -> {new_status.value}")
        return result
    return wrapper


def demo_solutions():
    """Demonstration of solutions"""
    print("🎓 SOLUTIONS DEMONSTRATION\n")
    
    # Exercise 1
    print("✅ Exercise 1 - PersonalTask:")
    health_task = PersonalTask("Go to doctor", category="health")
    hobby_task = PersonalTask("Read book", category="hobby")
    
    print(f"Health: {health_task.get_priority().name}")
    print(f"Hobby: {hobby_task.get_priority().name}")
    print()
    
    # Exercise 2
    print("✅ Exercise 2 - ExtendedTaskManager:")
    with ExtendedTaskManager("extended_demo.json") as manager:
        manager.add_task(health_task)
        manager.add_task(hobby_task)
        
        work_task = WorkTask("Code review", assignee="Anna")
        manager.add_task(work_task)
        work_task.start()
        work_task.complete()
        
        print(f"Urgent tasks: {len(manager.get_tasks_by_priority(Priority.URGENT))}")
        print(f"Anna's tasks: {len(manager.get_tasks_by_assignee('Anna'))}")
        print(f"Completion rate: {manager.get_completion_rate():.1f}%")
    print()
    
    # Exercise 3
    print("✅ Exercise 3 - Logging decorator:")
    
    # Apply decorator to methods
    SimpleTask.start = log_task_changes(SimpleTask.start)
    SimpleTask.complete = log_task_changes(SimpleTask.complete)
    
    demo_task = SimpleTask("Demo task")
    demo_task.start()
    demo_task.complete()


if __name__ == "__main__":
    print("📚 PRACTICAL OOP EXERCISES\n")
    
    practice_1_custom_task()
    practice_2_custom_manager()
    practice_3_decorators()
    practice_4_advanced_context()
    
    print("=" * 50)
    demo_solutions()