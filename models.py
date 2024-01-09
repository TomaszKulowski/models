"""models.py - Module containing data models for the application.

Classes:
    - Product: Class representing a product with a name and price.
    - TransactionType: Enumeration for transaction types (Buy or Sell).
    - OrderType: Enumeration for order types (Add or Remove).
    - Order: Class representing an order for a set of products with transaction and order types.
    - Orders: Class representing a collection of orders with methods to manage and display orders.

Usage:
    Example usage of the module:

    from models import Product, TransactionType, OrderType, Order, Orders

    # Create a product
    banana = Product(name='Banana', price=4.5)

    # Define transaction and order types
    buy_transaction = TransactionType.BUY
    add_order = OrderType.ADD

    # Create an order
    order = Order(products={banana: 10}, transaction_type=buy_transaction, order_type=add_order)

    # Create a collection of orders
    orders_collection = Orders()

    # Add an order to the collection. The sum of buy/sell orders with the best price is displayed at each step.
    orders_collection.add_order(order)
"""
from enum import Enum


class Product:
    """Class representing a product.

    Attributes:
        name (str): The name of the product.
        price (float): The price of the product.
    """
    def __init__(self, name: str, price: float):
        """Initialize a Product object.

        Args:
            name (str): The name of the product.
            price (float): The price of the product.
        """
        self.name = name
        self.price = price


class TransactionType(Enum):
    """Enumeration for transaction types: Buy or Sell."""
    BUY = 'Buy'
    SELL = 'Sell'


class OrderType(Enum):
    """Enumeration for order types: Add or Remove."""
    ADD = 'Add'
    REMOVE = 'Remove'


class Order:
    """Class representing an order for a product.

    Attributes:
        products (dict): A dictionary representing the products associated with the order.
            Format: {'name'(str): price(float),...}
        transaction_type (TransactionType): The type of transaction, either Buy or Sell.
        order_type (OrderType): The type of order, either Add or Remove.

    Raises:
        TypeError: If an invalid transaction_type or order_type is provided.
    """
    def __init__(self, products: dict, transaction_type: TransactionType, order_type: OrderType):
        """

        Args:
            products (dict): A dictionary representing the products associated with the order.
                Format: {product(Product): quantity(int), ...}
            transaction_type (TransactionType): The type of transaction, either Buy or Sell.
            order_type (OrderType): The type of order, either Add or Remove.
        """
        if transaction_type not in TransactionType.__members__.values():
            raise TypeError('Invalid transaction type. It should be "Buy" or "Sell".')
        if order_type not in OrderType.__members__.values():
            raise TypeError('Invalid order type. It should be "Add" or "Remove".')

        self.products = products
        self.transaction_type = transaction_type
        self.order_type = order_type


class Orders:
    """Class representing a collection of orders.

    Attributes:
        orders (dict): A dictionary containing orders, where keys are order IDs and values are Order objects.

    Methods:
        _get_next_id(): Private method to get the next available order ID.
        add_order(order: Order): Adds a new order to the collection.
        display_order_with_a_best_price(): Displays the best order for each transaction type based on total price.
    """
    def __init__(self):
        """Initialize an Orders object with an empty orders dictionary."""
        self.orders = {}

    def _get_next_id(self) -> int:
        """Private method to get the next available order ID.

        Returns:
            int: The next available order ID.
        """
        return len(self.orders) + 1

    def add_order(self, order: Order):
        """Add a new order to the collection.

         Args:
             order (Order): The Order object to be added.
         """
        self.orders[self._get_next_id()] = order
        self.display_order_with_a_best_price()

    def display_order_with_a_best_price(self):
        """Display the best order for each transaction type based on total price."""
        result = {}
        for order_id, order in self.orders.items():
            total_sum = 0
            for product, quantity in order.products.items():
                total_sum += quantity * product.price

            if not result.get(order.transaction_type):
                result[order.transaction_type] = [order_id, total_sum]
            else:
                if result[order.transaction_type][1] < total_sum:
                    result[order.transaction_type] = [order_id, total_sum]

        for transaction_type, details in result.items():
            print(f'Best {transaction_type.value} Order: ID = {details[0]}, Price = {details[1]}')
