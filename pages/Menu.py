
from Records import Records
from pages.AbstractPage import AbstractPage
from pages.DisplayCustomers import DisplayCustomers
from pages.DisplayProducts import DisplayProducts
from pages.ExitPage import ExitPage
from pages.PlaceOrderPage import PlaceOrderPage


class Menu(AbstractPage):
    def __init__(self, records: Records) -> None:
        super().__init__()
        self.records = records
        self.menu_items = [
            ('Place order', PlaceOrderPage(self.records)),
            ('Display customers', DisplayCustomers(self.records)),
            ('Display products', DisplayProducts(self.records)),
            ('Exit', ExitPage()),
            ]

    def run(self):
        while self.__display_menu() == 0:
            pass
        return 1

    def __display_menu(self):
        for index, (title, _) in enumerate(self.menu_items, 1):
            print(f'[{index}] {title}')
        choice = input('Please select a menu option: ')
        choice = int(choice)
        return self.menu_items[choice-1][1].run()
        