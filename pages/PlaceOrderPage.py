
from Customer import Customer
from Order import Order
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

        product_name = input('Please enter product name: ')
        product = self.records.find_product(product_name, search_in_name=True)

        quantity = input('Enter the amount you would like to purchase: ')
        quantity = int(quantity)

        if product.stock < quantity:
            print(f'Sorry. There is only {product.stock} product in stock.')
            return 0

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
        if member_choice == 'N':
            return 'C', self.records.create_new_customer(name, 'C')

        print('Please select with membership type you would like to sign up for.')
        member_type = input('Regular Member or VIP (M/V): ').upper()

        customer = self.records.create_new_customer(name, member_type)

        print('Thank you for signing up!')
        return member_type, customer

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