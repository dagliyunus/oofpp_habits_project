from datetime import datetime
from typing import List, Dict, Optional


class HabitTestable:
    """
     A mock version of the Habit class for testing purposes.
     Simulates habit behavior (e.g., check-offs, streaks, missed deadlines)
     without interacting with a database. Useful for unit testing and logic validation.
     """
    def __init__(
            self,
            habit_id: int,
            user_id: int,
            name: str,
            frequency: str,
            description: Optional[str] = None,
            deadline_time: Optional[datetime] = None,
            created_at: Optional[datetime] = None
    ):
        """
        Initialize a testable Habit instance with optional log simulation.
        Parameters:
            habit_id (int): The ID of the habit.
            user_id (int): The ID of the user who owns this habit.
            name (str): Name of the habit.
            frequency (str): Frequency of the habit ('daily', 'weekly').
            description (Optional[str]): Description of the habit.
            deadline_time (Optional[datetime]): Deadline for habit completion.
            created_at (Optional[datetime]): Creation timestamp. Defaults to now.
        """
        self.habit_id = habit_id
        self.user_id = user_id
        self.name = name
        self.frequency = frequency
        self.description = description
        self.deadline_time = deadline_time
        self.created_at = created_at or datetime.now()
        self.logs: List[Dict] = []

    def add_checkoff(self, date: Optional[datetime] = None):
        """
       Simulate a successful check-off for the habit.
       Parameters:
        date (Optional[datetime]): The timestamp for the check-off. Defaults to now.
       """
        date = date or datetime.now()
        self.logs.append({'completed_at': date, 'missed': False})

    def was_missed(self) -> bool:
        """
        Simulate a missed check-off if current time exceeds deadline.
        Returns:
            bool: True if missed, False otherwise.
        """
        now = datetime.now()
        if self.deadline_time and now > self.deadline_time:
            self.logs.append({'completed_at': now, 'missed': True})
            return True
        return False

    def calculate_streaks(self) -> int:
        """
       Calculate the current streak of consecutive non-missed days.
       Returns:
        int: Length of the current check-off streak.
       """
        if not self.logs:
            return 0

        # Extracting and sorting successful logs here.
        sorted_logs = sorted(
            [log['completed_at'] for log in self.logs if not log['missed']],
            reverse=True
        )
        streak = 1
        for i in range(1, len(sorted_logs)):
            if (sorted_logs[i - 1] - sorted_logs[i]).days == 1:
                streak += 1
            else:
                break
        return streak