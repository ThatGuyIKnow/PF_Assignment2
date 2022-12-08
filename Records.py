import os
from Customer import Customer
from Member import Member
from Order import Order
from Product import Product
from VIPMember import VIPMember


class Records():
    def __init__(self, customer_file_path: str, product_file_path: str) -> None:
        self.customer_file_path = customer_file_path
        self.product_file_path = product_file_path
        try:
            self.customers = self.read_customers()
            self.products = self.read_products()
        except Exception as e:
            raise IOError(e) from e
        self.next_customer_id = self.get_last_customer_id() + 1
        self.next_product_id = self.get_last_product_id() + 1

    def read_customers(self):
        customers = self.csv_reader(self.customer_file_path)
        create_customer = lambda args: self.__create_customer(*args)
        return list(map(create_customer, customers))
    
    def __create_customer(self, id: str, name: str, discount_rate: str, value: str):
        customer_type = id[0]
        discount_rate = float(discount_rate)
        value = float(value)
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
        except FileNotFoundError as e:
            print('Customer data file not found. Exiting...')
            raise e

    def find_customer(self, query: str, search_in_name: bool = False):
        customer = self.find_in_customers_or_products(query, search_in_name, self.customers)
        if customer is None:
            return None
        return customer

    def find_product(self, query: str, search_in_name: bool = False):
        product = self.find_in_customers_or_products(query, search_in_name, self.products)
        if product is None:
            return None
        return product

    def find_in_customers_or_products(self, query: str, search_in_name: bool, arr_list):
        field = lambda x: x.name if search_in_name else lambda x: x.id
        try:
            index = list(map(field, arr_list)).index(query)
            return arr_list[index]
        except ValueError:
            return None

    def list_customers(self, format_string='{0}, {1}, {2}, {3}'):
        print('CUSTOMERS: ')
        for customer in self.customers:
            print(format_string.format(customer.id, customer.name, customer.discount_rate, customer.value))

    def list_products(self, format_string='{0}, {1}, {2}, {3}'):
        print('PRODUCTS: ')
        for product in self.products:
            print(format_string.format(product.id, product.name, product.price, product.stock))


    def get_last_customer_id(self):
        if len(self.customers) == 0:
            return 0
        return int(self.customers[-1].id[1:])

    def get_last_product_id(self):
        if len(self.products) == 0:
            return 0
        return int(self.products[-1].id[1:])

    def __save_customer(self, customer: Customer):
        try:
            with open(self.customer_file_path, 'a', encoding='utf-8') as f:
                f.write(f'{customer.id}, {customer.name}, {customer.discount_rate}, {customer.value}\n')
        except IOError as e:
            print('Error saving customer to file. Exitting...')
            raise e
        self.customers.append(customer)

    def create_new_customer(self, name: str, member_type: str = 'C'):
        if member_type == 'C':
            customer = Customer(member_type+str(self.next_customer_id), name)
        elif member_type == 'M':
            customer = Member(member_type+str(self.next_customer_id), name)
        elif member_type == 'V':
            customer = VIPMember(member_type+str(self.next_customer_id), name)
        self.next_customer_id += 1;
        self.__save_customer(customer)
        return customer


    def execute_order(self, order: Order):
        customer, product, quantity, purchased_VIP = order
        customer.value += customer.get_discount(order.total_price)[1]
        if purchased_VIP:
            customer.value += VIPMember.membership_cost
        
        product.stock -= quantity

        self.update_customer_info(customer)
        self.update_product_info(product)
    
    def update_customer_info(self, customer: Customer):
        temp_file_path, file_extension = os.path.splitext(self.customer_file_path)
        temp_file_path += '_temp' + file_extension
        with open(self.customer_file_path, 'r+', encoding='utf-8') as f:
            with open(temp_file_path, 'w', encoding='utf-8') as f_new:
                for line in f:
                    if line.startswith(customer.id):
                        id, name, discount_rate, value = customer
                        f_new.write(f'{id}, {name}, {discount_rate}, {value}\n')
                    else:
                        f_new.write(line)

        os.replace(temp_file_path, self.customer_file_path)

    
    def update_product_info(self, product: Product):
        temp_file_path, file_extension = os.path.splitext(self.product_file_path)
        temp_file_path += '_temp' + file_extension
        with open(self.product_file_path, 'r+', encoding='utf-8') as f:
            with open(temp_file_path, 'w', encoding='utf-8') as f_new:
                for line in f:
                    if line.startswith(product.id):
                        id, name, price, stock = product
                        f_new.write(f'{id}, {name}, {price}, {stock}\n')
                    else:
                        f_new.write(line+'\n')
        
        os.replace(temp_file_path, self.product_file_path)