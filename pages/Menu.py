
from Records import Records


class AbstractPage():
    def __init__(self) -> None:
        if type(self) is AbstractPage:
            raise RuntimeError("Cannot instantiate abstract class")

    def run(self) -> int:
        pass

class Menu(AbstractPage):
    def __init__(self, records: Records) -> None:
        super().__init__()
        self.records = records
        self.menu_items = [
            ('Place order', AbstractPage()),
            ('Display customers', AbstractPage()),
            ('Display products', AbstractPage()),
            ('Exit', AbstractPage()),
            ]

    def run(self):
        while self.__display_menu() == 0:
            pass
        return 1

    def __display_menu(self):        
        for index, title, _ in self.menu_items:
            print(f'[{index]} {title}')
        choice = input('Please select a menu option: ')
        return self.menu_items[choice].run()
        
        