#models.py
from colorama import init, Fore, Style
# Initialize colorama
init(autoreset=True)

class User:
    """
    Represents a user with basic information.

    Attributes:
        username (str): The username of the user.
        password (str): The password associated with the user account.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        address (str): The address of the user.
    """

    def __init__(self, username, password, first_name, last_name, address):
        """
        Initializes a User object with provided attributes.

        Args:
            username (str): The username of the user.
            password (str): The password associated with the user account.
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            address (str): The address of the user.
        """
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.address = address

    def __str__(self):
        """
        Returns a string representation of the User object.

        Returns:
            str: A string containing username, full name, and address of the user.
        """
        return (f"{Fore.CYAN}Username: {Fore.GREEN}{self.username}{Style.RESET_ALL}, "
                f"{Fore.CYAN}Name: {Fore.GREEN}{self.first_name} {self.last_name}{Style.RESET_ALL}, "
                f"{Fore.CYAN}Address: {Fore.GREEN}{self.address}{Style.RESET_ALL}")

class Product:
    """
    Represents a product with a title and price.

    Attributes:
        title (str): The title or name of the product.
        price (float): The price of the product.
    """

    def __init__(self, title, price, quantity=0, product_id=None):
        """
        Initializes a Product object with provided attributes.

        Args:
            title (str): The title or name of the product.
            price (float): The price of the product.
            quantity (int): The quantity of the product
            product_id : The product number of the product
        """
        self.title = title
        self.price = price
        self.quantity = quantity
        self.product_id = product_id


    def __str__(self):
        """
        Returns a string representation of the Product object.

        Returns:
            str: A string containing the title and price of the product.
        """
        return (f"{Fore.CYAN}Product: {Fore.GREEN}{self.title}{Style.RESET_ALL}, "
                f"{Fore.CYAN}Price: {Fore.GREEN}Rs{self.price:.2f}{Style.RESET_ALL}")















