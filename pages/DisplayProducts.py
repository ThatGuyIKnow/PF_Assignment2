from Records import Records
from pages.AbstractPage import AbstractPage


class DisplayProducts(AbstractPage):
    def __init__(self, records: Records) -> None:
        super().__init__()
        self.records = records

    def run(self) -> int:
        self.records.list_products()
        return 0