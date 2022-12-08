
from pages.AbstractPage import AbstractPage

class ExitPage(AbstractPage):
    def __init__(self) -> None:
        super().__init__()
    
    def run(self) -> int:
        print('Thank you for using the Console-Mart System. See you another time!')
        return 1