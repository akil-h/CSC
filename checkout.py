
# An order qualifies for express checkout if does not have more items than
# the EXPRESS_LIMIT
EXPRESS_LIMIT = 8

def express_checkout(product_to_quantity: dict[str, int]) -> bool:
    """Return True if and only if the grocery order in product_to_quantity
    qualifies for the express checkout. product_to_quantity maps products
    to the numbers of those items in the grocery order.
    
    >>> express_checkout({'banana': 3, 'soy milk': 1, 'peanut butter': 1})
    True
    >>> express_checkout({'banana': 3, 'soy milk': 1, 'twinkie': 5})
    False
    """
    num_items = 0
    for key in product_to_quantity:
        num_items = num_items + product_to_quantity[key]
    return num_items < EXPRESS_LIMIT