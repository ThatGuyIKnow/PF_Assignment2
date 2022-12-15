from Records import Records
from VIPMember import VIPMember
from pages.AbstractPage import AbstractPage


class AdjustVIPThreshold(AbstractPage):
    def __init__(self, records: Records) -> None:
        self.records = records

    def run(self):
        discount_threshold = input(f'Please type the VIP threshold (Current is {VIPMember.discount_threshold}): ')
        while not self.validate_discount_threshold(discount_threshold):
            print('Invalid discount rate!')
            discount_threshold = input(f'Please type the VIP threshold (Current is {VIPMember.discount_threshold}): ')

        VIPMember.set_threshold(float(discount_threshold))
        return 0


    def validate_discount_threshold(self, discount_threshold: str):
        try: 
            discount_threshold = float(discount_threshold)
            if discount_threshold <= 0:
                return False
        except:
            return False
        return True