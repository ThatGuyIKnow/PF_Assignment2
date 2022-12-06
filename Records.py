from Customer import Customer
from Member import Member
from Product import Product
from VIPMember import VIPMember


class Records():
    def __init__(self, customer_file_path: str, product_file_path: str) -> None:
        self.customer_file_path = customer_file_path
        self.product_file_path = product_file_path
        self.customers = self.read_customers()
        self.products = self.read_products()
    
    def read_customers(self):
        customers = self.csv_reader(self.customer_file_path)
        create_customer = lambda args: self.__create_customer(*args)
        return list(map(create_customer, customers))
    
    def __create_customer(self, id: str, name: str, discount_rate: str, value: str):
        customer_type = id[0]
        discount_rate = float(discount_rate)
        value = int(value)
        if customer_type == 'C':
            return Customer(id, name, value)
        elif customer_type == 'M':
            return Member(id, name, value)
        elif customer_type == 'V':
            return VIPMember(id, name, value, discount_rate)


    def read_products(self):
        products = self.csv_reader(self.product_file_path)
        create_product = lambda args: self.__create_product(*args)
        return list(map(create_product, products))


    def __create_product(self, id: str, name: str, price: str, quantity: str):
        price = float(price)
        quantity = int(quantity)
        return Product(id, name, price, quantity)

    def csv_reader(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                for line in f:
                    yield line.split(', ')
        except FileNotFoundError:
            print('Customer data file not found. Exiting...')

    def find_customer(self, query: str, search_in_name: bool):
        return self.find_in_customers_or_products(query, search_in_name, self.customers)

    def find_product(self, query: str, search_in_name: bool):
        return self.find_in_customers_or_products(query, search_in_name, self.products)
    
    def find_in_customers_or_products(self, query: str, search_in_name: bool, list):
        field = lambda x: x.name if search_in_name else lambda x: x.id
        index = list(map(field, list)).index(query)
        return list[index]

    def list_customers(self, format_string='{0}, {1}, {2}, {3}'):
        print('CUSTOMERS: ')
        for customer in self.customers:
            print(format_string.format(customer))

    def list_products(self, format_string='{0}, {1}, {2}, {3}'):
        print('PRODUCTS: ')
        for product in self.products:
            print(format_string.format(product))