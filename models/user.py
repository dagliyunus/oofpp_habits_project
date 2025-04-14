class User:
    """
        Represents a user of the Habit Tracker application.
        Attributes:
            user_id (int): Unique identifier for the user.
            username (str): The user's chosen username.
            email (str): Email address of the user.
            password (str): The hashed password of the user.
            created_at (datetime): Timestamp of user account creation.
        """
    def __init__(self, user_id, username, email, password, created_at=None):
        """
        Initialize a new User instance.
        Parameters:
            user_id (int): The ID assigned to the user.
            username (str): The username chosen by the user.
            email (str): The user's email address.
            password (str): The user's password (ideally hashed).
            created_at (Optional[datetime]): Timestamp of creation. Defaults to now().
        """
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at