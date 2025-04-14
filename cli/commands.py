import click
from services.habit_service import (
    create_habit,
    remove_habit,
    get_user_habits,
    checkoff_habit,
)
from analytics.analytics_module import (
    get_longest_streak,
    get_most_missed_habits,
)
from repository.storage_manager import (
    load_all_habits,
    load_checkoffs_for_habit,
)
from datetime import datetime


@click.group()
def cli():
    """
    Habit Tracker CLI
    This is the root command group for the Habit Tracker command-line interface.
    """
    pass


@cli.command()
@click.option('--user-id', prompt='User ID', type=int)
@click.option('--name', prompt='Habit name')
@click.option('--frequency', prompt='Frequency (daily/weekly)', type=click.Choice(['daily', 'weekly']))
@click.option('--description', prompt='Description', default='')
@click.option('--deadline', prompt='Deadline (YYYY-MM-DD HH:MM)', default='')
def create(user_id, name, frequency, description, deadline):
    """
    Create a new habit for a specific user.
    Parameters:
        user_id (int): ID of the user creating the habit.
        name (str): Name of the habit.
        frequency (str): Frequency of the habit ('daily' or 'weekly').
        description (str): Optional description of the habit.
        deadline (str): Optional deadline in 'YYYY-MM-DD HH:MM' format.
    """
    # Convert the deadline string to a datetime object if provided
    deadline_time = datetime.strptime(deadline, "%Y-%m-%d %H:%M") if deadline else None
    # Call the habit creation logic
    habit = create_habit(user_id, name, frequency, description, deadline_time)
    # Provide feedback to the user
    click.echo(f"✅ Habit '{habit.name}' created for user {user_id}.")


@cli.command(name="list")
@click.option('--user-id', prompt='User ID', type=int)
def list_habits(user_id):
    """
    List all habits for a specific user.
    Parameters:
        user_id (int): The ID of the user whose habits will be displayed.
    """
    # Fetch habits associated with the use
    habits = get_user_habits(user_id)
    if not habits:
        click.echo("📭 No habits found.")
    else:
        click.echo(f"📋 Habits for user {user_id}:")
        for habit in habits:
            click.echo(f"[{habit['habit_id']}] {habit['name']} ({habit['frequency']})")


@cli.command()
@click.option('--habit-id', prompt='Habit ID', type=int)
def delete(habit_id):
    """
    Delete a specific habit by its ID.
    Parameters:
        habit_id (int): The ID of the habit to be deleted.
    """
    # Remove the habit from the system
    remove_habit(habit_id)
    # Inform the user about the deletion
    click.echo(f"🗑️ Habit {habit_id} deleted.")


@cli.command()
@click.option('--habit-id', prompt='Habit ID', type=int)
@click.option('--user-id', prompt='User ID', type=int)
def checkoff(habit_id, user_id):
    """
    Mark a habit as completed for a specific user.
    Parameters:
        habit_id (int): The ID of the habit to be checked off.
        user_id (int): The ID of the user completing the habit.
    """
    # Register the habit check-off action
    checkoff_habit(habit_id, user_id)
    # Confirm the action to the user
    click.echo(f"✅ Habit {habit_id} checked off for user {user_id}.")


@cli.command()
@click.option('--user-id', prompt='User ID', type=int)
def analyze(user_id):
    """
     Analyze habit performance data for a specific user.
     Parameters:
        user_id (int): The ID of the user whose habits will be analyzed.
     This command loads all habits and check-off logs for the user,
     calculates the longest completion streak, and identifies the most missed habits.
     """
    # Load all habits for the user
    habits = load_all_habits(user_id)
    # Collect all check-off logs across all habits
    all_logs = []
    for habit in habits:
        logs = load_checkoffs_for_habit(habit['habit_id'])
        all_logs.extend(logs)
    # Analyze the longest completion streak
    longest_streak = get_longest_streak(all_logs)
    # Analyze most frequently missed habits
    missed_habits = get_most_missed_habits(all_logs)

    click.echo("📊 Analytics Summary:")

    if longest_streak:
        click.echo(f"🔥 Longest streak: Habit {longest_streak[0]} → {longest_streak[1]} days")
    else:
        click.echo("No streak data available.")

    if missed_habits:
        click.echo("⏰ Most missed habits:")
        for habit_id, count in missed_habits:
            click.echo(f" Habit {habit_id} missed {count} times")
    else:
        click.echo("✅ No missed habits.")