import os
from Bundle import Bundle
from Customer import Customer
from Member import Member
from Order import Order
from Product import Product
from VIPMember import VIPMember


class Records():
    def __init__(self, customer_file_path: str, product_file_path: str, orders_file_path: str) -> None:
        self.customer_file_path = customer_file_path
        self.product_file_path = product_file_path
        self.orders_file_path = orders_file_path
        try:
            self.customers = self.read_customers()
            self.products = None
            self.read_products()
        except Exception as e:
            raise IOError(e) from e
        try:
            self.orders = self.read_orders()
        except Exception:
            print('Cannot load the order file. Run as if there is no order previously.')
            self.orders = []
        
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
        product_list = [self.__create_product(*args) for args in products if args[0][0] == 'P']
        self.products = product_list

        products = self.csv_reader(self.product_file_path)
        bundle_list = [self.__create_bundle(args) for args in products if args[0][0] == 'B']
        self.products += bundle_list
        print(bundle_list[0].products)
        

    def __create_product(self, id: str, name: str, price: str, quantity: str):
        if not price.strip() == '':
            price = float(price)
        else:
            price = None
        quantity = int(quantity)
        return Product(id, name, price, quantity)

    def __create_bundle(self, args):
        id = args[0]
        name = args[1]
        products = list(map(self.find_product, args[2:-1]))
        products = [{'id': p.id, 'price': p.price} for p in products]
        stock = int(args[-1])
        print(args[2:-1])
        return Bundle(id, name, products, stock)

    def read_orders(self):
        orders = []
        with open(self.orders_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                args = line.split(', ')
                customer, product, quantity, timestamp = args
                orders.append(Order(customer, product, quantity, timestamp=timestamp))
        return orders

    def csv_reader(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                for line in f:
                    yield line.split(', ')
        except FileNotFoundError as e:
            print('Customer data file not found. Exiting...')
            raise e

    
    def find_customer(self, query: str, search_in_name: bool = None):
        if search_in_name is not None:
            return self.find_in_customers_or_products(query, search_in_name, self.customers)

        customer = self.find_in_customers_or_products(query, True, self.customers)
        if customer is None:
            customer = self.find_in_customers_or_products(query, False, self.customers)
        return customer

    def find_product(self, query: str, search_in_name: bool = False):
        if search_in_name is not None:
            return self.find_in_customers_or_products(query, search_in_name, self.products)

        product = self.find_in_customers_or_products(query, True, self.products)
        if product is None:
            product = self.find_in_customers_or_products(query, False, self.products)
        return product

    def find_in_customers_or_products(self, query: str, search_in_name: bool, arr_list):
        field = (lambda x: x.name) if search_in_name else (lambda x: x.id)
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
            if product.id.startswith('P'):
                print(format_string.format(product.id, product.name, product.price, product.stock))
            elif product.id.startswith('B'):
                product_ids = [p['id'] for p in product.products]
                product_ids = ', '.join(product_ids)
                print(format_string.format(product.id, product.name, product_ids, product.stock))
                


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
        customer, product, quantity, purchased_VIP, _ = order
        customer.value += customer.get_discount(order.total_price)[1]
        if purchased_VIP:
            customer.value += VIPMember.membership_cost
        
        product.stock -= quantity

        self.update_customer_info(customer)
        self.update_product_info(product)
        self.append_order(order)
    
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
                        self.write_product_to_file(product, f_new)
                    else:
                        f_new.write(line)
        
        os.replace(temp_file_path, self.product_file_path)

    
    def write_product_to_file(self, product: Product, file):
        if product.id.startswith('P'):
            id, name, price, stock = product
            file.write(f'{id}, {name}, {price}, {stock}\n')
        elif product.id.startswith('B'):
            id, name, products, stock = product
            product_ids = [p['id'] for p in products]
            products = ', '.join(product_ids)
            print(product_ids)
            file.write(f'{id}, {name}, {products}, {stock}\n')

    def append_order(self, order: Order):
        with open(self.orders_file_path, 'a', encoding='utf-8') as f:
            f.write(f'{order.customer.id}, {order.product.id}, {order.quantity}, {order.timestamp}\n')
