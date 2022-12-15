from Customer import Customer
from Product import Product
import datetime

class Order():
    # def __init__(self, customer: Customer|str, product: Product|str, quantity: int) -> None:
    #     if isinstance(customer, Customer):
    #         self.customer_name = customer.name
    #     else:
    #         self.customer_name = customer
        
    #     if isinstance(product, Product):
    #         self.product_name = product.name
    #     else:
    #         self.product_name = product
        
    #     self.quantity = quantity
    
    
    def __init__(self, customer: str, product: str, quantity: int, purchased_VIP: bool = False, timestamp = datetime.datetime.now()) -> None:
        self.customer = customer
        self.product = product
        self.quantity = quantity
        self.purchased_VIP = purchased_VIP
        self.timestamp = timestamp


    def __iter__(self):
        i = [self.customer, self.product, self.quantity, self.purchased_VIP, self.timestamp]
        for v in i:
            yield v

    @property
    def total_price(self):
        return self.product.price * self.quantity

    