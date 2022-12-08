
from Customer import Customer
from Order import Order
from Product import Product
from Records import Records
from VIPMember import VIPMember
from pages.AbstractPage import AbstractPage


class PlaceOrderPage(AbstractPage):
    def __init__(self, records: Records) -> None:
        super().__init__()
        self.records = records

    def run(self):
        
        name = input('Please enter your name: ')
        customer = self.records.find_customer(name, search_in_name=True)

        product = self.ask_for_product()

        quantity = self.ask_for_quantity(product)

        new_member_type = None
        if customer is None:
            signed_for, customer = self.ask_for_membership(name)
            order = Order(customer, product, quantity, new_member_type == 'V')
        else:
            order = Order(customer, product, quantity)

        self.records.execute_order(order)
        
        if new_member_type == 'V':
            customer.value += VIPMember.membership_cost

        self.print_order(order)

        print('Thank you for shopping at Console-Mart!')

        return 0
        
    
    def ask_for_membership(self, name: str):
        member_choice = input('We can see that you are not a member. Would you like to sign up for membership (Y/N): ').upper()

        while member_choice not in ['Y', 'N']:
            member_choice = input('Invalid answer. Please enter (Y/N): ').upper()


        if member_choice == 'N':
            return 'C', self.records.create_new_customer(name, 'C')

        print('Please select with membership type you would like to sign up for.')
        member_type = input('Regular Member or VIP (M/V): ').upper()
        while member_type not in ['M', 'V']:
            member_type = input('Invalid answer. Please enter (M/V): ').upper()
        
        customer = self.records.create_new_customer(name, member_type)

        print('Thank you for signing up!')
        return member_type, customer


    def ask_for_product(self):
        product_name = input('Please enter product name: ')
        product = self.records.find_product(product_name, search_in_name=True)
        while product is None:
            product_name = input('Product could not be found. Please enter a valid product name: ')
            product = self.records.find_product(product_name, search_in_name=True)

            if product.stock == 0:
                print("Product is out of stock. Please choose another product.")
                product = None
        return product


    def ask_for_quantity(self, product: Product):
        quantity = input('Enter the amount you would like to purchase: ')
        
        while not (self.validate_quantity(quantity) and int(quantity) <= product.stock):
            quantity = input(f'{quantity} is an invalid amount. There are {product.stock} {product.name}(s) in stock. Please enter a valid amount: ')
        quantity = int(quantity)
            
        return quantity

    def validate_quantity(self, quantity: str):
        try:
            quantity = int(quantity)
            if quantity < 1:
                return False
            return True
        except:
            return False

    def print_order(self, order: Order):
        discount_rate, total_cost = order.customer.get_discount(order.total_price)

        print(order, order.customer, order.product)
        print(
            f'''
            {order.customer.name} purchase {order.quantity} x {order.product.name}
            Unit Price:     {order.product.price} (AUD)
            {order.customer.name} gets a discount of {discount_rate} %
            ''')
        
        if order.purchased_VIP:
            print(f'\t    Membership price:   {VIPMember.membership_cost} (AUD)\n')
            total_cost += VIPMember.membership_cost
        print(f'\t    Total price:    {total_cost} (AUD)')
