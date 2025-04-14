from models.habits import Habit
from repository.storage_manager import (
    save_habit,
    delete_habit,
    load_all_habits,
    save_checkoff,
    load_checkoffs_for_habit,
)


def create_habit(user_id, name, frequency, description, deadline_time):
    """
    Create a new Habit instance and persist it to the database.
    Parameters:
        user_id (int): The ID of the user who owns the habit.
        name (str): Name of the habit.
        frequency (str): Frequency of the habit ('daily' or 'weekly').
        description (str): A brief description of the habit.
        deadline_time (datetime): The deadline by which the habit should be completed.
    Returns:
        Habit: The newly created Habit instance.
    """
    habit = Habit(
        habit_id=None,
        user_id=user_id,
        name=name,
        frequency=frequency,
        description=description,
        deadline_time=deadline_time,
    )
    # Saving the habit to the database
    save_habit(habit)
    return habit


def remove_habit(habit_id):
    """
    Delete a habit from the database by its ID.
    Parameters:
        habit_id (int): The ID of the habit to delete.
    """
    delete_habit(habit_id)


def get_user_habits(user_id):
    """
     Retrieve all habits associated with a specific user.
     Parameters:
         user_id (int): The ID of the user whose habits will be retrieved.
     Returns:
        List[Dict]: A list of habit dictionaries.
     """
    return load_all_habits(user_id)


def checkoff_habit(habit_id, user_id):
    """
    Record a check-off entry for a specific habit and user.
    Parameters:
        habit_id (int): The ID of the habit to be checked off.
        user_id (int): The ID of the user performing the check-off.
    """
    save_checkoff(habit_id, user_id)


def get_checkoffs(habit_id):
    """
    Retrieve all check-off logs for a given habit.
    Parameters:
        habit_id (int): The ID of the habit whose logs are requested.
    Returns:
        List[Dict]: A list of check-off log entries as dictionaries.
    """
    return load_checkoffs_for_habit(habit_id)