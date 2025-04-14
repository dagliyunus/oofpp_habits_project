USAGE GUIDE – CLI Command Annotations (commands.py)

✅ @click.group()

This decorator defines a command group, acting as the main entry point for my CLI application. 
It allows multiple subcommands (like create, delete, analyze, etc.) to be logically grouped under a single CLI interface. 
I typically use this for organizing commands in a modular way:

@click.group()
def cli():
"""Main command group for Habit Tracker CLI."""
pass

Usage in terminal:

python main.py create
python main.py list

✅ @cli.command()

This decorator registers a subcommand to the main command group defined by @click.group(). 
Each subcommand implements one CLI action (e.g., creating a habit, checking off a task, listing habits):

@cli.command()
def list():
"""Lists all habits for the user."""
...

Now this can be executed from the terminal as:

python main.py list

✅ @click.option()

Defines an option or flag that can be passed from the command line. 
It’s used to capture user input and pass it into the function as arguments. 
This can be used for optional values like --user-id, --verbose, or even default parameters:

@click.option('--user-id', required=True, help='ID of the user.')

Called from terminal as:

python main.py list --user-id 1

