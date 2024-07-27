#accounts.py
from filing import UserFileManager
from models import User
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

class AccountManager:
    """Manages user accounts including creation, validation, and authentication."""

    def __init__(self):
        """Initializes the AccountManager with a UserFileManager instance."""
        self.user_file_manager = UserFileManager()
        self.users = self.user_file_manager.read()

    def is_username_valid(self, username):
        """
        Checks if the username is valid based on length, characters, and uniqueness.

        Args:
            username (str): The username to validate.

        Returns:
            tuple: A tuple indicating whether the username is valid (bool) and a message (str).

        """
        # Check username length and alphanumeric characters
        if not (4 <= len(username) <= 8):
            return False, "Username must be between 4 and 8 characters long."
        if not username.isalnum():
            return False, "Username must be alphanumeric."
        if username.isdigit():
            return False, "Username cannot be only digits."
        # Check if username already exists
        if any(user.username == username for user in self.users):
            return False, "Username already taken."
        return True, "Valid username."

    def create_account(self, username, password, first_name, last_name, address):
        """
        Creates a new user account if the username and password meet criteria.

        Args:
            username (str): The username for the new account.
            password (str): The password for the new account.
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            address (str): The address of the user.

        Raises:
            ValueError: If the username or password is invalid.

        """
        is_valid, message = self.is_username_valid(username)
        if not is_valid:
            print(Fore.LIGHTRED_EX + message)
            return

        if not self.is_password_valid(password):
            print(Fore.LIGHTRED_EX + "Password must be at least 6 characters long.")
            return

        user = User(username, password, first_name, last_name, address)
        self.users.append(user)
        self.user_file_manager.write(self.users)


    def is_password_valid(self, password):
        """
        Checks if the password meets the minimum length requirement.

        Args:
            password (str): The password to check.

        Returns:
            bool: True if the password meets the length requirement, False otherwise.

        """
        return len(password) >= 6

    def authenticate(self, username, password):
        """
        Authenticates a user based on username and password.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            User or None: The User object if authentication is successful, None otherwise.

        """
        for user in self.users:
            if user.username == username and user.password == password:
                print(Fore.LIGHTGREEN_EX + "Username and Password Authenticated")
                return user
        print(Fore.LIGHTRED_EX + "Invalid credentials.")
        return None



