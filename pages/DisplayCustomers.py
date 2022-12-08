from Records import Records
from pages.AbstractPage import AbstractPage


class DisplayCustomers(AbstractPage):
    def __init__(self, records: Records) -> None:
        super().__init__()
        self.records = records

    def run(self) -> int:
        self.records.list_customers()
        return 0