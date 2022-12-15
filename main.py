
import sys
from pages.Menu import Menu
from Records import Records

def run():
    try: 
        args = ['./data/customers.csv', './data/products.csv', './data/orders.csv']
        
        c_args = sys.argv[1:4]
        arg_length = len(c_args)
        if arg_length > 0:
            args[:arg_length] = c_args
        
        records = Records(*args)
    except IOError as e:
        print('Error retrieving data from customers/products. The following error was recorded: ' + str(e))
        return
    menu = Menu(records)
    menu.run()

if __name__ == '__main__':
    run()