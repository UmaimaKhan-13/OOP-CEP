from colorama import Fore, Style, init
from filing import ProductFileManager, UserFileManager, HistoryManager
from admin import AdminManager
from accounts import AccountManager
import time
from datetime import datetime
from models import User
from abc import ABC

# Initialize Colorama
init()

class Displayable(ABC):
    """
    Base class for objects that can be displayed.
    """
    def display(self):
        raise NotImplementedError("Subclasses must implement this method")

class CartItem(Displayable):
    """
    Represents an item in the shopping cart.
    """
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def display(self):
        return f"{Fore.LIGHTCYAN_EX}{self.quantity} x {self.product[1]} (Rs. {self.product[2]})"

class Cart:
    """
    Represents a shopping cart.
    """
    def __init__(self, username):
        self.username = username
        self.items = []
        self.bill = 0

    def add_product(self, product, quantity):
        for item in self.items:
            if item.product == product:
                item.quantity += quantity
                self.bill += int(product[2]) * quantity
                break
        else:
            self.items.append(CartItem(product, quantity))
            self.bill += int(product[2]) * quantity

    def remove_product(self, product, quantity):
        for item in self.items:
            if item.product == product:
                if item.quantity > quantity:
                    item.quantity -= quantity
                    self.bill -= int(product[2]) * quantity
                else:
                    self.items.remove(item)
                    self.bill -= int(product[2]) * item.quantity
                break

    def display(self):
        for item in self.items:
            print(item.display())
        print(f"{Fore.LIGHTYELLOW_EX}Total bill: Rs.{self.bill}{Style.RESET_ALL}")

class Order(Displayable):
    """
    Represents an order.
    """
    def __init__(self, cart):
        self.items = cart.items[:]
        self.bill = cart.bill
        self.time = ""

    def display(self):
        for item in self.items:
            print(item.display())
        print(f"{Fore.GREEN}Total bill: Rs.{self.bill}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Order time: {self.time}{Style.RESET_ALL}")

class Admin(User):
    """
    Represents an admin user.
    """
    def __init__(self, username, password):
        super().__init__(username, password)

    def login(self, password):
        return self.password == password

class ShoppingApp:
    """
    Main application class for the shopping app.
    """
    def __init__(self):
        self.account_manager = AccountManager()
        self.product_manager = ProductFileManager()
        self.user_manager = UserFileManager()
        self.admin_manager = AdminManager()
        self.history_manager = HistoryManager()

    def main_menu(self, account):
        cart = Cart(account.username)

        while True:
            print(f"{Fore.CYAN}SELECTION:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}1. Display products{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}2. Add product to cart{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}3. Remove product from cart{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}4. Display cart{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}5. Display history{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}6. Proceed to checkout{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}7. Quit{Style.RESET_ALL}")

            try:
                choice = int(input(f"{Fore.LIGHTGREEN_EX}Enter your choice: {Style.RESET_ALL}"))
                print()

                if choice == 1:
                    self.product_manager.display_products_from_file()
                    print()
                elif choice == 2:
                    """Adds a product to the cart and ensures the quantity does not exceed available stock."""
                    products = self.product_manager.read()
                    self.product_manager.display_products_from_file()
                    try:
                        product_number = int(input(f"{Fore.LIGHTMAGENTA_EX}Enter the product no.: {Style.RESET_ALL}"))
                        product = products[product_number - 1]
                        available_quantity = int(product[3])
                        quantity = int(input(f"{Fore.LIGHTMAGENTA_EX}Enter product quantity: {Style.RESET_ALL}"))

                        if quantity > available_quantity:
                            print(
                                f"{Fore.LIGHTRED_EX}Cannot add {quantity} {product[1]}(s) to the cart. Only {available_quantity} available.{Style.RESET_ALL}")
                        else:
                            cart.add_product(product, quantity)
                            print()
                            print(f"{Fore.LIGHTGREEN_EX}{quantity} {product[1]}(s) added to cart.{Style.RESET_ALL}")
                            # Update the quantity in the product list
                            product[3] = str(available_quantity - quantity)
                            self.product_manager.overwrite(products)
                    except (IndexError, ValueError):
                        print(f"{Fore.LIGHTBLUE_EX}Invalid product number or quantity. Please try again.{Style.RESET_ALL}")
                elif choice == 3:
                    for i, item in enumerate(cart.items):
                        print(f"Item {i + 1}: {item.display()}")
                    try:
                        item_number = int(input(f"{Fore.LIGHTGREEN_EX}Enter the item no.: {Style.RESET_ALL}"))
                        if item_number < 1 or item_number > len(cart.items):
                            print(f"{Fore.RED}Invalid item number.{Style.RESET_ALL}")
                        else:
                            item = cart.items[item_number - 1]
                            print(f"Selected Item: {item.display()}")
                            print(f"Current Quantity in Cart: {item.quantity}")

                            quantity = int(input(f"{Fore.LIGHTGREEN_EX}Enter product quantity to remove: {Style.RESET_ALL}"))

                            if quantity > item.quantity:
                                print(
                                    f"{Fore.LIGHTRED_EX}Error: Quantity to remove ({quantity}) exceeds quantity in cart ({item.quantity}).{Style.RESET_ALL}")
                            else:
                                cart.remove_product(item.product, quantity)
                                print(
                                    f"{Fore.LIGHTMAGENTA_EX}{quantity} {item.product[1]}(s) removed from cart.{Style.RESET_ALL}")
                    except (IndexError, ValueError):
                        print(f"{Fore.RED}Invalid item number or quantity. Please try again.{Style.RESET_ALL}")
                elif choice == 4:
                    cart.display()
                elif choice == 5:
                    if isinstance(account, User):
                        self.history_manager.display_user_history(account.username)
                    else:
                        print(f"{Fore.LIGHTRED_EX}No transactions done previously.{Style.RESET_ALL}")
                elif choice == 6:
                    if cart.bill == 0:
                        print(f"{Fore.LIGHTRED_EX}Add some products to cart first.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.LIGHTMAGENTA_EX}Proceeding to checkout...{Style.RESET_ALL}")
                        cart.display()
                        print()

                        print(f"{Fore.MAGENTA}Account holder: {cart.username}{Style.RESET_ALL}")

                        users = self.user_manager.read()
                        current_user = None
                        for user in users:
                            if user.username == cart.username:
                                current_user = user
                                break

                        if current_user is None:
                            print(f"{Fore.LIGHTRED_EX}User not found. Cannot proceed with checkout.{Style.RESET_ALL}")
                            continue

                        delivery_address = input(f"{Fore.CYAN}Enter your delivery address: {Style.RESET_ALL}")

                        if delivery_address == current_user.address:
                            print(f"{Fore.LIGHTGREEN_EX}Delivery address: {delivery_address}{Style.RESET_ALL}")
                            print()
                            confirmation = input(f"{Fore.LIGHTGREEN_EX}Press 'y' or 'Y' to confirm: {Style.RESET_ALL}")
                            if confirmation in ('y', 'Y'):
                                print()
                                print(f"{Fore.LIGHTMAGENTA_EX}Order will be delivered in 2 days.{Style.RESET_ALL}")
                                print()

                                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                order_number = str(int(time.time()))
                                order_amount = cart.bill
                                items_purchased = [item.display() for item in cart.items]

                                self.history_manager.write_order_history(
                                    cart.username,
                                    order_number,
                                    current_time,
                                    order_amount,
                                    items_purchased
                                )

                                cart = Cart(cart.username)
                                print()
                                print(f"{Fore.LIGHTCYAN_EX}Checkout successful. Thank you :){Style.RESET_ALL}")
                                print()
                            else:
                                print(f"{Fore.LIGHTRED_EX}Checkout canceled.{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.LIGHTRED_EX}Delivery address does not match. Please enter the correct address.{Style.RESET_ALL}")

                elif choice == 7:
                    quit()
                else:
                    print(f"{Fore.RED}Invalid choice entered.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please enter a number corresponding to the menu options.{Style.RESET_ALL}")

    def admin_menu(self):
        while True:
            print(f"{Fore.LIGHTCYAN_EX}ADMIN PANEL:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}1. Add product{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}2. Edit product{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}3. Delete product{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}4. View users{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}5. View orders{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}6. Display products{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}7. Logout{Style.RESET_ALL}")

            try:
                choice = int(input(f"{Fore.GREEN}Enter your choice: {Style.RESET_ALL}"))
                print()

                if choice == 1:
                    title = input(f"{Fore.GREEN}Enter product title: {Style.RESET_ALL}")
                    price = input(f"{Fore.GREEN}Enter product price: {Style.RESET_ALL}")
                    quantity = input(f"{Fore.GREEN}Enter product quantity: {Style.RESET_ALL}")
                    self.admin_manager.add_product(title, price, quantity)
                    print(f"{Fore.GREEN}Product added successfully.{Style.RESET_ALL}")
                elif choice == 2:
                    self.product_manager.display_products_from_file()
                    try:
                        product_index = int(input(f"{Fore.GREEN}Enter the product number to edit: {Style.RESET_ALL}"))
                        new_title = input(f"{Fore.GREEN}Enter new product name: {Style.RESET_ALL}")
                        new_price = input(f"{Fore.GREEN}Enter new product price: {Style.RESET_ALL}")
                        new_quantity = input(f"{Fore.GREEN}Enter new product quantity: {Style.RESET_ALL}")
                        self.admin_manager.edit_product(product_index, new_title, new_price, new_quantity)
                        print(f"{Fore.GREEN}Product updated successfully.{Style.RESET_ALL}")
                    except (IndexError, ValueError):
                        print(f"{Fore.RED}Invalid product number or details.{Style.RESET_ALL}")
                elif choice == 3:
                    self.product_manager.display_products_from_file()
                    try:
                        product_number = int(input(f"{Fore.GREEN}Enter the product number to delete: {Style.RESET_ALL}"))
                        self.admin_manager.delete_product(product_number)
                        print(f"{Fore.GREEN}Product deleted successfully.{Style.RESET_ALL}")
                    except (IndexError, ValueError):
                        print(f"{Fore.RED}Invalid product number.{Style.RESET_ALL}")
                elif choice == 4:
                    self.admin_manager.view_users()
                elif choice == 5:
                    self.admin_manager.view_orders(self.user_manager)
                elif choice == 6:
                    self.product_manager.display_products_from_file()
                elif choice == 7:
                    break
                else:
                    print(f"{Fore.RED}Invalid choice entered.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please enter a number corresponding to the menu options.{Style.RESET_ALL}")

def main():
    """
    Main function to start the shopping app.

    This function initializes the shopping app and provides an interface for users and admins to log in,
    register, or quit the application. It loops to continuously accept user input until the user chooses to quit.
    """
    print(f"""
           {Fore.BLUE}{Style.BRIGHT}
                               ===============================================
                                                 WELCOME TO
                                               SHOPPING APP 🛒
                               ===============================================
           {Style.RESET_ALL}
                               {Fore.LIGHTMAGENTA_EX}Your one-stop shop for everything!{Style.RESET_ALL}
              """)
    app = ShoppingApp()

    while True:
        space = "\t"*8
        print(f"\t\t\t\t\t\t{Fore.LIGHTBLUE_EX}Choose from the given options :)")
        print(f"{space}{Fore.LIGHTCYAN_EX}1. Register{Style.RESET_ALL}")
        print(f"{space}{Fore.LIGHTCYAN_EX}2. Login{Style.RESET_ALL}")
        print(f"{space}{Fore.LIGHTCYAN_EX}3. Admin Login{Style.RESET_ALL}")
        print(f"{space}{Fore.LIGHTCYAN_EX}4. Exit{Style.RESET_ALL}")
        print()

        try:
            choice = int(input(f"{space}{Fore.LIGHTYELLOW_EX}Enter your choice: {Style.RESET_ALL}"))
            print()

            if choice == 1:
                # User registration
                username = input(Fore.LIGHTMAGENTA_EX + "Enter new username: " + Style.RESET_ALL)

                # Check if username is valid and available
                is_valid, message = app.account_manager.is_username_valid(username)
                if not is_valid:
                    print(Fore.LIGHTRED_EX + f"Error: {message}" + Style.RESET_ALL)
                    continue

                password = input(Fore.LIGHTMAGENTA_EX + "Enter password: " + Style.RESET_ALL)

                # Check if password is valid
                if not app.account_manager.is_password_valid(password):
                    print(Fore.LIGHTRED_EX + "Error: Password must be at least 6 characters long." + Style.RESET_ALL)
                    continue

                # Collect user details
                first_name = input(Fore.LIGHTMAGENTA_EX + "Enter your first name: " + Style.RESET_ALL)
                last_name = input(Fore.LIGHTMAGENTA_EX + "Enter your last name: " + Style.RESET_ALL)
                address = input(Fore.LIGHTMAGENTA_EX + "Enter your address: " + Style.RESET_ALL)

                try:
                    # Create a new user account
                    app.account_manager.create_account(username, password, first_name, last_name, address)
                    print(Fore.LIGHTGREEN_EX + "Registration successful." + Style.RESET_ALL)
                    print()
                except ValueError as e:
                    # Handle errors during account creation
                    print(Fore.LIGHTRED_EX + f"Error: {e}" + Style.RESET_ALL)
            elif choice == 2:
                username = input(f"{Fore.LIGHTMAGENTA_EX}Enter username: {Style.RESET_ALL}")
                password = input(f"{Fore.LIGHTMAGENTA_EX}Enter password: {Style.RESET_ALL}")

                account = app.account_manager.authenticate(username, password)
                if account:
                    print(f"{Fore.LIGHTGREEN_EX}Login successful.{Style.RESET_ALL}")
                    print()
                    app.main_menu(account)
                else:
                    print(f"{Fore.LIGHTRED_EX}Invalid username or password.{Style.RESET_ALL}")
            elif choice == 3:
                admin_username = input(f"{Fore.LIGHTMAGENTA_EX}Enter admin username: {Style.RESET_ALL}")
                admin_password = input(f"{Fore.LIGHTMAGENTA_EX}Enter admin password: {Style.RESET_ALL}")

                if app.admin_manager.authenticate_admin(admin_username, admin_password):
                    print(f"{Fore.LIGHTGREEN_EX}Admin login successful.{Style.RESET_ALL}")
                    print()
                    app.admin_menu()
                else:
                    print(f"{Fore.LIGHTRED_EX}Invalid admin username or password.{Style.RESET_ALL}")
            elif choice == 4:
                break
            else:
                print(f"{Fore.LIGHTRED_EX}Invalid choice entered.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.LIGHTRED_EX}Invalid input. Please enter a number corresponding to the menu options.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()






