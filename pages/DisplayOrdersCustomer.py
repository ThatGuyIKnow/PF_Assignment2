from Records import Records
from pages.AbstractPage import AbstractPage


class DisplayOrdersCustomer(AbstractPage):
    def __init__(self, records: Records) -> None:
        super().__init__()
        self.records = records

    def run(self) -> int:

        
        customer_id = input('Please type the name or ID of the customer you would like to view orders of: ')
        customer = self.records.find_customer(customer_id)
        if customer is None:
            print(f'Invalid customer!')
            return 0

        print('ORDERS:')
        for order in self.records.orders:
            if order.customer == customer.id:
                order_customer, product, quantity, _, timestamp = order
                print(f'{order_customer}, {product}, {quantity}, {timestamp}', end='')
        return 0