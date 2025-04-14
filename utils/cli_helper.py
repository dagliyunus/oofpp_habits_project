import sys
import tty
import termios


def get_masked_input(prompt="Password: "):
    """
    Prompt the user for a password input with masked characters (e.g., '*').
    Unlike `getpass.getpass()`, this version provides feedback by printing
    a '*' for each character typed and handles backspace input.
    Parameters:
        prompt (str): The prompt message displayed to the user.
    Returns:
        str: The entered password as a plain string (not masked).
    """
    print(prompt, end='', flush=True)
    password = ""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        # Set terminal to raw mode (no buffering or echo)
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch == '\n' or ch == '\r':
                break
                # Handling backspace (DEL key)
            elif ch == '\x7f':
                if len(password) > 0:
                    password = password[:-1]
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            else:
                password += ch
                # Removing character from display
                sys.stdout.write('*')
                sys.stdout.flush()
    finally:
        # Here restoring original terminal settings
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        # moving to the next line
        print()

    return password