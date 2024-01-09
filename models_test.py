"""The collections of the tests for the 'models.py' module."""
import pytest

from models import Product, TransactionType, OrderType, Order, Orders


TRANSACTION_TYPE_ERROR_MSG = 'Invalid transaction type. It should be "Buy" or "Sell".'
ORDER_TYPE_ERROR_MSG = 'Invalid order type. It should be "Add" or "Remove".'


@pytest.fixture
def fixture_products() -> dict:
    """Fixture providing a dictionary of products.

    Returns:
        dict: A dictionary where keys are Product objects with name and price attributes,
              and values are corresponding quantities.
    """
    products = {
        Product(name='Banana', price=4.5): 10,
        Product(name='Apple', price=7.2): 9,
        Product(name='Orange', price=2.3): 1,
        Product(name='Lemon', price=1.0): 999,
    }
    return products


@pytest.fixture
def fixture_orders() -> list:
    """Fixture providing a list of Order objects for testing purposes.

     Returns:
         list: A list of Order objects with various products, transaction types, and order types.
     """
    orders = [
        Order({Product('Banana', 99.0): 99}, TransactionType.BUY, OrderType.ADD),
        Order({Product('Apple', 1.0): 1}, TransactionType.BUY, OrderType.ADD),
        Order({Product('Orange', 53.0): 1}, TransactionType.SELL, OrderType.ADD),
        Order({Product('Lemon', 0.1): 9}, TransactionType.SELL, OrderType.ADD),
    ]
    return orders


@pytest.mark.parametrize(
    'transaction_type, order_type',
    (
        (TransactionType.BUY, OrderType.ADD),
        (TransactionType.BUY, OrderType.REMOVE),
        (TransactionType.SELL, OrderType.ADD),
        (TransactionType.SELL, OrderType.REMOVE),
    )
)
def test_valid_order_creation(fixture_products: dict, transaction_type: TransactionType, order_type: OrderType):
    """Test for valid order creation.

    Args:
        fixture_products (dict): A dictionary representing products associated with the order.
        transaction_type (TransactionType): The type of transaction, either Buy or Sell.
        order_type (OrderType): The type of order, either Add or Remove.

    Test the creation of a valid Order object with various transaction types and order types,
    and ensure that the attributes are set correctly.
    """
    order = Order(fixture_products, transaction_type, order_type)

    assert order.products == fixture_products
    assert order.transaction_type == transaction_type
    assert order.order_type == order_type


@pytest.mark.parametrize(
    'transaction_type, order_type, expected_error, expected_message',
    (
        (TransactionType.BUY, 'invalid_order_type', TypeError, ORDER_TYPE_ERROR_MSG),
        (TransactionType.SELL, 'invalid_order_type', TypeError, ORDER_TYPE_ERROR_MSG),
        ('invalid_transaction_type', OrderType.REMOVE, TypeError, TRANSACTION_TYPE_ERROR_MSG),
        ('invalid_transaction_type', OrderType.REMOVE, TypeError, TRANSACTION_TYPE_ERROR_MSG),
    )
)
def test_invalid_order_creation(
        fixture_products: dict,
        transaction_type: TransactionType,
        order_type: OrderType,
        expected_error: Exception,
        expected_message: str
):
    """Test for invalid order creation.

    Args:
        fixture_products (dict): A dictionary representing products associated with the order.
        transaction_type (TransactionType): The type of transaction, either Buy or Sell.
        order_type (OrderType or str): The type of order, either Add or Remove, or an invalid string.
        expected_error (Exception): The expected exception type.
        expected_message (str): The expected error message.

    Test the creation of an Order object with invalid input and verify that the expected exception
    is raised with the correct error message.
    """
    with pytest.raises(expected_error) as error:
        Order(fixture_products, transaction_type, order_type)

    assert error.type == expected_error
    assert str(error.value) == expected_message


def test_add_order_to_orders(fixture_orders: list):
    """Test adding orders to the Orders collection.

    Args:
        fixture_orders (list): A list of Order objects for testing.

    Test adding orders to the Orders collection and verify that the order IDs are assigned correctly,
    and the number of orders in the collection increases accordingly.
    """
    orders = Orders()

    for index, order in enumerate(fixture_orders):
        assert orders._get_next_id() == index + 1
        assert len(orders.orders) == index
        orders.add_order(order)


def test_display_order_with_a_best_price(fixture_orders: list, capsys: pytest.fixture):
    """Test displaying the best orders with various inputs.

    Args:
        fixture_orders (list): A list of Order objects for testing.
        capsys (pytest.fixture): Pytest fixture for capturing stdout.

    Test displaying the best orders for each transaction type based on total price.
    Verify the output matches the expected messages.
    """
    expected_output = 'Best Buy Order: ID = 1, Price = 9801.0\n' \
                      'Best Buy Order: ID = 1, Price = 9801.0\n' \
                      'Best Buy Order: ID = 1, Price = 9801.0\n' \
                      'Best Sell Order: ID = 3, Price = 53.0\n' \
                      'Best Buy Order: ID = 1, Price = 9801.0\n' \
                      'Best Sell Order: ID = 3, Price = 53.0\n'
    orders = Orders()

    for order in fixture_orders:
        orders.add_order(order)
    out, _ = capsys.readouterr()

    assert out == expected_output
