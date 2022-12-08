
from pages.Menu import Menu
from Records import Records

if __name__ == '__main__':
    records = Records('./data/customers.csv', './data/products.csv')
    menu = Menu(records)
    menu.run()