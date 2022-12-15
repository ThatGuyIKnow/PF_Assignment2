from Records import Records
from pages.AbstractPage import AbstractPage


class DisplayOrders(AbstractPage):
    def __init__(self, records: Records) -> None:
        super().__init__()
        self.records = records

    def run(self) -> int:
        print('ORDERS:')
        for order in self.records.orders:
            customer, product, quantity, _, timestamp = order
            print(f'{customer}, {product}, {quantity}, {timestamp}', end='')
        return 0