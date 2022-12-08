
from pages.Menu import Menu
from Records import Records

def run():
    try: 
        records = Records('./data/customers.csv', './data/products.csv')
    except IOError as e:
        print('Error retrieving data from customers/products. The following error was recorded: ' + str(e))
        return
    menu = Menu(records)
    menu.run()

if __name__ == '__main__':
    run()