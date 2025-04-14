from datetime import datetime
from collections import defaultdict


def get_most_missed_habits(habit_logs):
    """
    Analyze habit logs and return a sorted list of habits by how often they were missed.
    Parameters:
        habit_logs (list[dict]): A list of habit check-off logs. Each log is expected to
                             contain 'habit_id' and a 'missed' boolean flag.
    Returns:
        list[tuple[int, int]]: A list of (habit_id, missed_count) tuples, sorted by missed count in descending order.
    """
    missed_counts = defaultdict(int)
    # Counting missed checkoffs per habit
    for log in habit_logs:
        if log.get('missed'):
            missed_counts[log['habit_id']] += 1
    # Returning sorted list of (habit_id, count) by most missed
    return sorted(missed_counts.items(), key=lambda x: x[1], reverse=True)

def get_longest_streak(habit_logs):
    """
    Calculate the longest streak (consecutive days) for each habit and return the habit with the highest streak.
    Parameters:
        habit_logs (list[dict]): A list of habit check-off logs. Each log must contain 'habit_id' and 'completed_at'.
    Returns:
        tuple[int, int] or None: A tuple (habit_id, longest_streak_days) for the habit with the longest streak,
                                 or None if no streak data is available.
    """
    streaks = defaultdict(int)
    logs_by_habit = defaultdict(list)
    # Grouping logs by habit and convert timestamps
    for log in habit_logs:
        habit_id = log['habit_id']
        completed_at = datetime.fromisoformat(log['completed_at'])
        logs_by_habit[habit_id].append(completed_at)
    # Calculating max streak per habit
    for habit_id, timestamps in logs_by_habit.items():
        timestamps.sort()
        streak = max_streak = 1
        for i in range(1, len(timestamps)):
            # Checking if current completion is exactly 1 day after previous
            if (timestamps[i] - timestamps[i - 1]).days == 1:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 1
        streaks[habit_id] = max_streak
    # Returning the habit with the highest streak
    if streaks:
        return max(streaks.items(), key=lambda x: x[1])
    return None


def get_habits_by_period(habits, period='daily'):
    """
    Filter a list of habits by their frequency period.
    Parameters:
        habits (list[dict]): A list of habit dictionaries, each expected to include a 'frequency' key.
        period (str): The desired frequency to filter by ('daily' or 'weekly'). Defaults to 'daily'.
    Returns:
        list[dict]: A list of habits that match the specified period.
    """
    # Return habits that match the given frequency (default: daily)
    return [habit for habit in habits if habit.get('frequency') == period]


def calculate_streaks(logs):
    """
    Calculate the current streak of consecutive daily completions based on check-off logs.
    Parameters:
        logs (list[dict]): A list of log entries, each containing a 'completed_at' timestamp in '%Y-%m-%d %H:%M:%S' format.
    Returns:
        int: The number of consecutive days the habit was completed, starting from the most recent date.
    """
    if not logs:
        return 0
    # Sorting logs in reverse chronological order
    logs = sorted(logs, key=lambda x: x['completed_at'], reverse=True)
    # Starting with the most recent log
    streak = 1
    for i in range(1, len(logs)):
        # Parsing datetime strings
        d1 = datetime.strptime(logs[i - 1]['completed_at'], "%Y-%m-%d %H:%M:%S")
        d2 = datetime.strptime(logs[i]['completed_at'], "%Y-%m-%d %H:%M:%S")
        # Checking for exactly 1 day difference
        if (d1 - d2).days == 1:
            streak += 1
        else:
            # Streak is broken here
            break

    return streak