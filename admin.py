#admin.py
from colorama import init, Fore, Style
from filing import ProductFileManager, UserFileManager, HistoryManager
from models import Product, User

# Initialize colorama
init(autoreset=True)

class Admin:
    """Represents an administrator with a username and password."""
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self, password):
        """Checks if the provided password matches the admin's password."""
        return self.password == password


class AdminManager:
    """Manages administrative tasks such as product management, user management, and order viewing."""

    def __init__(self):
        """Initializes AdminManager with necessary file managers and history manager."""
        self.admin_file = "admin data.txt"  # File storing admin credentials (if used)
        self.product_manager = ProductFileManager()
        self.user_manager = UserFileManager()
        self.history_manager = HistoryManager()

    def authenticate_admin(self, username, password):
        """
        Authenticates an admin based on provided username and password.

        Args:
            username (str): The username of the admin.
            password (str): The password of the admin.

        Returns:
            Admin or None: An Admin object if authentication is successful, otherwise None.
        """
        try:
            with open(self.admin_file, "r") as file:
                for line in file:
                    admin_info = line.strip().split(",")
                    if len(admin_info) == 2 and admin_info[0] == username and admin_info[1] == password:
                        return Admin(username, password)
        except FileNotFoundError:
            print(Fore.LIGHTRED_EX + "Admin data file not found.")
        return None

    def add_product(self, title, price, quantity):
        """
        Adds a new product with the given title and price.

        Args:
            title (str): The title of the product.
            price (float): The price of the product.
        """
        product = Product(title, price, quantity)
        self.product_manager.write([product])
        print(Fore.LIGHTGREEN_EX + f"Product '{title}' added successfully.")

    def edit_product(self, product_index, new_title, new_price, new_quantity):
        """
        Edits an existing product's title and price based on its index.

        Args:
            product_index (int): The index of the product to edit.
            new_title (str): The new title for the product.
            new_price (float): The new price for the product.
            new_quantity (int): The new quantity for the product
        """
        products = self.product_manager.read()
        # Adjust for zero-based indexing
        zero_based_index = product_index - 1
        if 0 <= zero_based_index < len(products):
            product_id = products[zero_based_index][0]
            products[zero_based_index] = [product_id, new_title, new_price, new_quantity]
            self.product_manager.overwrite(products)
            print(Fore.LIGHTGREEN_EX + f"Product {product_index} updated successfully.")
        else:
            print(Fore.LIGHTRED_EX + "Invalid product index.")
    def delete_product(self, product_number):
        """
        Deletes a product based on its product number and updates the product numbers.

        Args:
            product_number (str): The product number to delete.
        """
        products = self.product_manager.read()
        print(Fore.YELLOW + f"Products before deletion: {products}")

        found_product = None
        for product in products:
            if product[0] == str(product_number):
                found_product = product
                break

        if found_product:
            products.remove(found_product)
            print(Fore.LIGHTGREEN_EX + f"Product '{found_product[1]}' deleted successfully.")

            for index, product in enumerate(products):
                product[0] = str(index + 1)

            self.product_manager.overwrite(products)

            updated_products = self.product_manager.read()
            print(Fore.YELLOW + f"Products after deletion and re-numbering: {updated_products}")
        else:
            print(Fore.LIGHTRED_EX + "Invalid product number.")


    def view_users(self):
        """Displays all registered users."""
        users = self.user_manager.read()
        if users:
            # Print table header
            header = f"{Fore.BLUE}{'Username':<15}{'First Name':<15}{'Last Name':<15}{'Address':<20}{Style.RESET_ALL}"
            print(header)
            print('-' * len(header) + Fore.LIGHTCYAN_EX)

            # Print table rows
            for user in users:
                row = (
                    f"{Fore.MAGENTA}{user.username:<15}{user.first_name:<15}{user.last_name:<15}{user.address:<20}{Style.RESET_ALL}")
                print(row)
        else:
            print(Fore.CYAN + "No users available." + Style.RESET_ALL)
    def view_orders(self, user_manager):
        """
        Displays all orders for each user.

        Args:
            user_manager (UserManager): An instance of UserManager to access user data.
        """
        users = user_manager.read()
        if not users:
            print(Fore.LIGHTRED_EX + "No users available.")
            return

        for user in users:
            histories = self.history_manager.get_user_history(user.username)
            if histories:
                print(Fore.CYAN + f"Order history for {Fore.LIGHTGREEN_EX}{user.username}{Style.RESET_ALL}:")
                for i, history in enumerate(histories):
                    print(Fore.MAGENTA + f"  Order {i + 1}:")
                    print(Fore.MAGENTA + f"    Order Number: {Fore.LIGHTMAGENTA_EX}{history['order_number']}{Style.RESET_ALL}")
                    print(Fore.MAGENTA + f"    Order Time: {Fore.LIGHTMAGENTA_EX}{history['order_time']}{Style.RESET_ALL}")
                    print(Fore.MAGENTA + f"    Order Amount: {Fore.LIGHTMAGENTA_EX}Rs.{history['order_amount']}{Style.RESET_ALL}")
                    print(Fore.MAGENTA + "    Items Purchased:")
                    for item in history['items_purchased']:
                        print(Fore.MAGENTA + f"      - {Fore.LIGHTMAGENTA_EX}{item}{Style.RESET_ALL}")
            else:
                print(Fore.LIGHTRED_EX + f"No orders found for {user.username}.")

        print(Fore.CYAN + "All orders displayed.")

    def display_products(self):
        """Displays all products available."""
        self.product_manager.display_products_from_file()




















