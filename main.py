import click
import time
import sys
from cli.commands import cli
from load_fixtures import load_fixtures
from services.auth import sign_up, log_in
from utils.cli_helper import (get_masked_input)

# Session state (should eventually move to a class or context object)
CURRENT_USER_ID = None
CURRENT_USERNAME = None


def show_auth_menu():
    """
    Display the authentication menu options to the user.
    """
    click.echo("👤 Welcome to Habit Tracker")
    click.echo("1. Sign Up")
    click.echo("2. Log In")
    click.echo("3. Exit")


def authenticate_user():
    """
    Handling user authentication flow for Habit Tracker.
    Shows a CLI menu that allows the user to sign up or log in.
    Stores the authenticated user's ID and username in global session state.
    Exits the program if the user chooses to quit.
    """
    global CURRENT_USER_ID, CURRENT_USERNAME

    while True:
        show_auth_menu()
        choice = click.prompt("Choose an option", type=int)

        if choice == 1:
            # Sign Up
            username = click.prompt("Choose a username")
            email = click.prompt("Email")
            password = get_masked_input("Choose a password: ")
            user_id, message = sign_up(username, email, password)
            click.echo(message)
            if user_id:
                CURRENT_USER_ID = user_id
                CURRENT_USERNAME = username
                break

        elif choice == 2:
            # Log In
            username = click.prompt("Username")
            password = get_masked_input("Password: ")
            user_id, message = log_in(username, password)
            click.echo(message)
            if user_id:
                CURRENT_USER_ID = user_id
                CURRENT_USERNAME = username
                break

        elif choice == 3:
            # Exit
            click.echo("👋 Goodbye!")
            exit(0)

        else:
            click.echo("❌ Invalid option. Try again.")


def show_main_menu():
    click.echo(f"\n📋 Main Menu (for @{CURRENT_USERNAME})")
    click.echo("1. Create Habit")
    click.echo("2. Delete Habit")
    click.echo("3. List Habits")
    click.echo("4. Check-off Habit")
    click.echo("5. Analyze Habits")
    click.echo("6. Log Out")
    click.echo("7. Exit")


def run_interactive_menu():
    global CURRENT_USER_ID, CURRENT_USERNAME

    while True:
        show_main_menu()
        choice = click.prompt("Choose an option", type=int)

        if choice == 1:
            cli.main(args=["create", "--user-id", str(CURRENT_USER_ID)], standalone_mode=False)

        elif choice == 2:
            cli.main(args=["delete"], standalone_mode=False)

        elif choice == 3:  # List Habits
            while True:
                cli.main(args=["list", "--user-id", str(CURRENT_USER_ID)], standalone_mode=False)
                click.echo("\n7. Back to Main Menu")
                click.echo("8. Exit")
                sub_choice = click.prompt("Choose an option", type=int)
                if sub_choice == 7:
                    break
                elif sub_choice == 8:
                    click.echo("👋 Goodbye!")
                    exit(0)

        elif choice == 4:  # Check-off
            cli.main(args=["checkoff", "--user-id", str(CURRENT_USER_ID)], standalone_mode=False)

        elif choice == 5:  # Analyze
            while True:
                cli.main(args=["analyze", "--user-id", str(CURRENT_USER_ID)], standalone_mode=False)
                click.echo("\n7. Back to Main Menu")
                click.echo("8. Exit")
                sub_choice = click.prompt("Choose an option", type=int)
                if sub_choice == 7:
                    break
                elif sub_choice == 8:
                    click.echo("👋 Goodbye!")
                    exit(0)

        elif choice == 6:  # Log Out
            click.echo("🔐 Logging out", nl=False)
            for _ in range(3):
                time.sleep(0.4)
                click.echo(".", nl=False)
                sys.stdout.flush()
            time.sleep(0.3)
            click.echo("\n")  # move to new line

            CURRENT_USER_ID = None
            CURRENT_USERNAME = None
            authenticate_user()
            continue

        elif choice == 7:
            click.echo("👋 Goodbye!")
            break

        else:
            click.echo("❌ Invalid option. Try again.")

@click.group()
def cli_main():
    """Main CLI entry point."""
    pass

@cli_main.command()
def start():
    """Start the interactive menu loop."""
    authenticate_user()
    run_interactive_menu()

if __name__ == "__main__":
    load_fixtures()         # Load fixture data only if not already in DB
    authenticate_user()     # Prompt login or signup
    run_interactive_menu()  # Personalized habit tracking 🎯
    cli_main()