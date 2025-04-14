from datetime import datetime
from typing import List, Dict

class Habit:
    """
    Represents a habit tracked by a user.
    Attributes:
        habit_id (int): Unique identifier for the habit.
        user_id (int): The ID of the user who owns the habit.
        name (str): Name of the habit.
        frequency (str): Frequency of the habit ('daily' or 'weekly').
        description (str): Optional description of the habit.
        deadline_time (Optional[datetime]): Deadline for the habit, if any.
        created_at (datetime): Timestamp when the habit was created.
        logs (List[Dict]): Optional in-memory log list for testing purposes.
    """
    def __init__(self, habit_id, user_id, name, frequency, description, deadline_time, created_at=None):
        """
        Initialize a Habit instance.
        Parameters:
            habit_id (int): The ID of the habit.
            user_id (int): The ID of the user.
            name (str): The name of the habit.
            frequency (str): Frequency ('daily' or 'weekly').
            description (str): A short description of the habit.
            deadline_time (Optional[datetime]): The deadline time, if any.
            created_at (Optional[datetime]): Creation timestamp. Defaults to now().
        """
        self.habit_id = habit_id
        self.user_id = user_id
        self.name = name
        self.frequency = frequency
        self.description = description
        self.deadline_time = deadline_time
        self.created_at = created_at or datetime.now()
        # Only used in memory for testing
        self.logs: List[Dict] = []

    def add_checkoff(self):
        """
        Record a check-off for the habit (e.g., mark it as completed today).
        Calls a storage manager function to persist this data.
        """
        from repository.storage_manager import save_checkoff
        save_checkoff(self.habit_id, self.user_id)

    def was_missed(self):
        """
        Determine whether the habit was missed based on its deadline.
        Returns:
         bool: True if missed, False otherwise.
        """
        from repository.storage_manager import check_if_missed
        return check_if_missed(self.habit_id, self.deadline_time)

    def calculate_streaks(self):
        """
        Calculate the current streak of consecutive completions for the habit.
        Returns:
         int: The number of consecutive completions.
        """
        from repository.storage_manager import load_checkoffs_for_habit
        from analytics.analytics_module import calculate_streaks
        logs = load_checkoffs_for_habit(self.habit_id)
        return calculate_streaks(logs)