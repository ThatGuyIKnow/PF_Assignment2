from Customer import Customer
from Product import Product


class Order():
    def __init__(self, customer: Customer|str, product: Product|str, quantity: int) -> None:
        if isinstance(customer, Customer):
            self.customer_id = customer.id
        else:
            self.customer_id = customer
        
        if isinstance(product, Product):
            self.product_id = Product.id
        else:
            self.product_id = product
        
        self.quantity = quantity
    
    