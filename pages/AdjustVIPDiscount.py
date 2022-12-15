from Records import Records
from pages.AbstractPage import AbstractPage


class AdjustVIPDiscount(AbstractPage):
    def __init__(self, records: Records) -> None:
        self.records = records

    def run(self):
        customer_id = input('Please type the name or ID of the customer you would like to adjust: ')
        customer = self.records.find_customer(customer_id)
        
        if customer is None or not customer.id.startswith('V'):
            print('Invalid customer!')
            return 0
        
        discount_rate = input(f'Please type the new discount rate (Current is {customer.discount_rate}): ')
        if not self.validate_discount_rate(discount_rate):
            print('Invalid discount rate!')

        customer.set_rate(float(discount_rate))
        self.records.update_customer_info(customer)
        return 0


    def validate_discount_rate(self, discout_rate: str):
        try: 
            discount_rate = float(discout_rate)
            if discount_rate < 0 or discount_rate > 1:
                return False
        except:
            return False
        return True