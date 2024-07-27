#filing.py
from models import User, Product
from abc import ABC, abstractmethod
from colorama import Fore, Style, init

Delimiter = "````"
init(autoreset=True)

class FileManager(ABC):
    """Abstract base class for file management operations."""

    @abstractmethod
    def read(self):
        """Abstract method to read data from a file."""
        pass

    @abstractmethod
    def write(self, data):
        """Abstract method to write data to a file."""
        pass


class UserFileManager(FileManager):
    """Manages user data file operations."""

    def read(self):
        """Reads user data from 'user_data.txt' file and returns a list of User objects.

        Returns:
            list: A list of User objects read from the file.

        Raises:
            FileNotFoundError: If the 'user_data.txt' file is not found.
        """
        users = []
        try:
            with open("user_data.txt", "r") as file:
                for line in file:
                    user_info = line.strip().split(Delimiter)
                    if len(user_info) == 5:
                        user = User(user_info[0], user_info[1], user_info[2], user_info[3], user_info[4])
                        users.append(user)
        except FileNotFoundError:
            print(f"{Fore.LIGHTRED_EX}User data file not found. No users to read.")
        return users

    def write(self, users):
        """Writes user data to the 'user_data.txt' file.

        Args:
            users (list): A list of User objects to be written to the file.

        Raises:
            Exception: If an error occurs while writing to the file.
        """
        try:
            with open("user_data.txt", "w") as file:
                for user in users:
                    user_data = f"{user.username}{Delimiter}{user.password}{Delimiter}{user.first_name}{Delimiter}{user.last_name}{Delimiter}{user.address}\n"
                    file.write(user_data)
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}Error writing to user data file: {e}")


class ProductFileManager(FileManager):
    """Manages product data file operations."""

    def read(self):
        """Reads product data from the 'product_list.txt' file and returns a list of lists.

        Returns:
            list: A list where each element is a list representing a product with its attributes.
        """
        products = []
        try:
            with open("product_list.txt", "r") as file:
                for line in file.readlines():
                    parts = line.strip().split(",")
                    if len(parts) == 4:
                        product_id, title, price, quantity = parts
                        products.append([product_id, title, price, quantity])
        except FileNotFoundError:
            print(F"{Fore.LIGHTRED_EX}Products data file not found.")
        return products

    def write(self, data):
        """Writes product data to the 'product_list.txt' file and returns newly added products.

        Args:
            data (list): A list of Product objects to be added to the file.

        Returns:
            list: A list of Product objects that were successfully added to the file.
        """
        try:
            existing_products = self.read()
            max_id = len(existing_products)
            new_products = []

            with open("product_list.txt", "a") as file:
                for product in data:
                    if isinstance(product, Product):
                        max_id += 1
                        product.product_id = max_id
                        product_data = f"{product.product_id},{product.title},{product.price},{product.quantity}\n"
                        file.write(product_data)
                        new_products.append(product)
            return new_products
        except FileNotFoundError:
            print(f"{Fore.LIGHTRED_EX}Products data file not found.")
            return []

    def overwrite(self, data):
        """Overwrites product data in the 'product_list.txt' file.

        Args:
            data (list): A list of Product objects or lists representing products to overwrite in the file.
        """
        try:
            with open("product_list.txt", "w") as file:
                for product in data:
                    if isinstance(product, list):
                        product_data = f"{product[0]},{product[1]},{product[2]},{product[3]}\n"
                    elif isinstance(product, Product):
                        product_data = f"{product.product_id},{product.title},{product.price},{product.quantity}\n"
                    file.write(product_data)
        except FileNotFoundError:
            print(f"{Fore.LIGHTRED_EX}Products data file not found.")

    def display_products_from_file(self):
        """Displays products from the 'product_list.txt' file in a formatted table."""
        with open("product_list.txt", 'r') as file:
            lines = file.readlines()

        products = [line.strip().split(',') for line in lines]
        space = "\t" * 7
        # Starting line
        starting_line = f"{space}{Fore.LIGHTCYAN_EX}{'-' *58}{Style.RESET_ALL}"
        print(starting_line)
        # Table Header
        header = (
            f"{space}{Fore.LIGHTBLUE_EX}| {'Product No.':^10} | {'Product':^17} | {'Price':^8} | {'Quantity':^10} |{Style.RESET_ALL}"
        )
        print(header)
        print(f"{space}{Fore.LIGHTCYAN_EX}{'-' * 58}{Style.RESET_ALL}")

        # Table Rows
        for product in products:
            row = (
                f"{space}{Fore.MAGENTA}| {int(product[0]):<11} "
                f"{Fore.MAGENTA}| {product[1]:<17} "
                f"{Fore.MAGENTA}| {int(product[2]):<8} "
                f"{Fore.MAGENTA}| {int(product[3]):<10} |{Style.RESET_ALL}"
            )
            print(row)

        # Closing Line
        closing_line = f"{space}{Fore.LIGHTCYAN_EX}{'-' * 59}{Style.RESET_ALL}"
        print(closing_line)

class HistoryManager:
    """Manages order history file operations."""

    def __init__(self, filename="history.txt"):
        """
        Initializes a HistoryManager instance.

        Args:
            filename (str, optional): The filename to store order history. Defaults to "history.txt".
        """
        self.filename = filename

    def write_order_history(self, username, order_number, order_time, order_amount, items_purchased):
        """
        Writes order history to the file.

        Args:
            username (str): The username associated with the order.
            order_number (str): The order number.
            order_time (str): The time the order was placed.
            order_amount (float): The amount of the order.
            items_purchased (list): List of items purchased, each item should be a string representation.
        """
        try:
            with open(self.filename, "a") as file:
                file.write(
                    f"{username}{Delimiter}{order_number}{Delimiter}{order_time}{Delimiter}{order_amount}{Delimiter}{','.join(items_purchased)}\n")
            print(f"{Fore.LIGHTMAGENTA_EX}Order history recorded successfully.")
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}Error writing to history file: {e}")

    def get_user_history(self, username):
        """
        Gets order history for a specific user.

        Args:
            username (str): The username to retrieve order history for.

        Returns:
            list: A list of dictionaries representing order histories, each containing 'order_number', 'order_time',
                  'order_amount', and 'items_purchased'. Returns None if no order history is found for the user.
        """
        try:
            with open(self.filename, "r") as file:
                histories = []
                for line in file:
                    if line.startswith(username):
                        history_info = line.strip().split(Delimiter)
                        histories.append({
                            "order_number": history_info[1],
                            "order_time": history_info[2],
                            "order_amount": history_info[3],
                            "items_purchased": history_info[4].split(',')
                        })
                if histories:
                    return histories
                else:
                    return None
        except FileNotFoundError:
            print(f"{Fore.LIGHTRED_EX}History data file '{self.filename}' not found.")
            return None

    def display_user_history(self, username):
        """
        Displays order history for a specific user.

        Args:
            username (str): The username to display order history for.
        """
        histories = self.get_user_history(username)
        if histories:
            print(f"Order history for user '{username}':")
            for i, history in enumerate(histories):
                print(f"  Order {i + 1}:")
                print(f"    Order Number: {history['order_number']}")
                print(f"    Order Time: {history['order_time']}")
                print(f"    Order Amount: Rs.{history['order_amount']}")
                print(f"    Items Purchased: {', '.join(history['items_purchased'])}")
                print()  # Ensure spacing after each order
        else:
            print(f"{Fore.LIGHTRED_EX}No order history available for user '{username}'.")
