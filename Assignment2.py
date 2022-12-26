import sys
import datetime
import os


class Customer:
    """
    The class representing a customer.

    Args:
        id (str): The unique string of the customer
        name (str): The unique name of the customer
        value (float, optional): The amount of money the customer has spent

    Attributes:
        id (str): The unique string of the customer
        name (str): The unique name of the customer
        value (float, optional): The amount of money the customer has spent
        discount_rate (float, static): The discount available to the customer

    """

    _discount_rate = 0.0

    def __init__(self, id: str, name: str, value: float = 0) -> None:
        self._id = id
        self._name = name
        self.value = value

    def __iter__(self):
        i = [self.id, self.name, self.discount_rate, self.value]
        for v in i:
            yield v

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @classmethod
    @property
    def discount_rate(cls):
        return cls._discount_rate

    def get_discount(self, price):
        """
        Calculates the discounted price and returns it along with the discount rate
        Args:
            price (float): The price to discount
        Returns:
            tuple of (float, float): The applied discount rate and price, respectively
        """
        return self.discount_rate, price

    def display_info(self):
        """
        Displays all information of the customer to the console
        Args:
            None
        Returns:
            None
        """
        attr = vars(self)
        attr["discount_rate"] = self.discount_rate
        print(f"Customer: {attr}")

    def __eq__(self, __o: object) -> bool:
        return self._id == __o.id


class Member(Customer):
    """
    The class representing a member. A member is a subclass of customer, which have signed up for the
    membership program.

    Args:
        id (str): The unique string of the member
        name (str): The unique name of the member
        value (float, optional): The amount of money the member has spent

    Attributes:
        id (str): The unique string of the member
        name (str): The unique name of the member
        value (float, optional): The amount of money the member has spent
        discount_rate (float, static): The discount available to the member
    """

    _discount_rate = 0.05

    def __init__(self, id: str, name: str, value: float = 0) -> None:
        super().__init__(id, name, value)

    def get_discount(self, price):
        """
        Calculates the discounted price and returns it along with the discount rate
        Args:
            price (float): The price to discount
        Returns:
            tuple of (float, float): The applied discount rate and price, respectively
        """
        new_price = price * (1 - self.discount_rate)
        return self.discount_rate, new_price

    @classmethod
    def set_rate(cls, rate):
        """
        Changes the discount rate of the Member class
        Args:
            rate (float): The new discount rate
        Returns:
            None
        """
        cls._discount_rate = rate


class VIPMember(Member):
    """
    The class representing a VIPMember. A VIPMember is a subclass of Member, which have signed up for the
    VIP version of the membership program.

    Args:
        id (str): The unique string of the VIP
        name (str): The unique name of the VIP
        value (float, optional): The amount of money the VIP has spent
        discount_rate (float, optional): The discount rate to apply

    Attributes:
        id (str): The unique string of the VIP
        name (str): The unique name of the VIP
        value (float, optional): The amount of money the VIP has spent
        discount_rate (float): The discount available to the VIP
        discount_threshold (float, static): The discount threshold for the VIP
    """

    _discount_threshold = 1000.0
    _membership_cost = 200.0

    def __init__(
        self, id: str, name: str, value: float = 0, discount_rate: float = 0.1
    ) -> None:
        super().__init__(id, name, value)
        self._discount_rate = discount_rate

    def display_info(self):
        """
        Displays all relevant information about the VIP to the console
        Args:
            None
        Returns:
            None
        """
        attr = vars(self)
        attr["discount_rate"] = self.discount_rate
        attr["discount_threshold"] = self._discount_threshold
        print(f"Customer: {attr}")

    def set_rate(self, rate):
        """
        Changes the discount rate of the instance
        Args:
            rate (float): The new discount rate
        Returns:
            None
        """
        self._discount_rate = rate

    @classmethod
    @property
    def membership_cost(cls):
        return cls._membership_cost

    @property
    def discount_rate(self):
        return self._discount_rate

    @classmethod
    @property
    def discount_threshold(cls):
        return cls._discount_threshold

    def get_discount(self, price):
        """
        Calculates the discounted price and returns it along with the discount rate
        Args:
            price (float): The price to discount
        Returns:
            tuple of (float, float): The applied discount rate and price, respectively
        """
        discount_rate = self.discount_rate
        if price > self._discount_threshold:
            discount_rate += 0.05
        new_price = price * (1 - discount_rate)
        return discount_rate, new_price

    @classmethod
    def set_threshold(cls, threshold):
        cls._discount_threshold = threshold


class Product:
    """
    The class representing a product.

    Args:
        id (str): The unique string of the product
        name (str): The unique name of the product
        price (float): The price of the product
        stock (int): The amount of product in stock

    Attributes:
        id (str): The unique string of the product
        name (str): The unique name of the product
        price (float): The price of the product
        stock (int): The amount of product in stock
    """

    def __init__(self, id: str, name: str, price: float, stock: int) -> None:
        self._id = id
        self._name = name
        self.price = price
        self.stock = stock

    def __iter__(self):
        i = [self.id, self.name, self.price, self.stock]
        for v in i:
            yield v

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def __eq__(self, __o: object) -> bool:
        return self._id == __o.id


class Bundle:
    """
    The class representing a bundle of products. Is cheaper than buying the products
    individually, as a discount is applied to the sum of the products in the bundle.

    Args:
        id (str): The unique string of the product
        name (str): The unique name of the product
        price (float): The price of the product
        stock (int): The amount of product in stock
        discount (float, optional): The discount to apply to the bundle

    Attributes:
        id (str): The unique string of the product
        name (str): The unique name of the product
        price (float): The price of the product
        stock (int): The amount of product in stock
        discount (float): The discount to apply to the bundle

    """

    def __init__(
        self, id: str, name: str, products, stock: int, discount: float = 0.2
    ) -> None:
        self._id = id
        self._name = name
        self.products = products
        self.stock = stock
        self.discount = discount

    def __iter__(self):
        i = [self.id, self.name, self.products, self.stock]
        for v in i:
            yield v

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        """
        The price property.
        Calculates the price of the bundle by gathering the prices of all the
        individual products and then applying the discount.
        Args:
            None
        Returns:
            None
        """
        prices = list(map(lambda x: x["price"], self.products))
        if None in prices:
            return None
        return sum(prices) * (1 - self.discount)

    def __eq__(self, __o: object) -> bool:
        return self._id == __o.id


class Order:
    """
    The class representing a order from a customer to buy a certain product.

    Args:
        customer (str): The unique id of the customer who bought the product
        product (str): The unique id of the product that has been bought
        quantity (int): The quantity of product
        purchase_VIP (bool, optional): Did the customer sign up for VIP in the purchase
        timestamp (datetime, optional): The time of purchase

    Attributes:
        customer (str): The unique id of the customer who bought the product
        product (str): The unique id of the product that has been bought
        quantity (int): The quantity of product
        purchase_VIP (bool): Did the customer sign up for VIP in the purchase
        timestamp (datetime): The time of purchase

    """

    def __init__(
        self,
        customer: str,
        product: str,
        quantity: int,
        purchased_VIP: bool = False,
        timestamp=datetime.datetime.now(),
    ) -> None:
        self.customer = customer
        self.product = product
        self.quantity = quantity
        self.purchased_VIP = purchased_VIP
        self.timestamp = timestamp

    def __iter__(self):
        i = [
            self.customer,
            self.product,
            self.quantity,
            self.purchased_VIP,
            self.timestamp,
        ]
        for v in i:
            yield v

    @property
    def total_price(self):
        return self.product.price * self.quantity


class PersistentStorageManager:
    """
    The persistent storage manager. Helper class for the Records class. Its purpose is to
    seperate the responsibility of keeping track of management of the persistent storage
    from the Records class. Has no internal knowledge of the state of the program.

    Args:
        customer_file_path (str): The file path to the customer storage file
        product_file_path (str): The file path to the product storage file
        orders_file_path (str, optional): The file path to the orders storage file
    Attributes:
        customer_file_path (str): The file path to the customer storage file
        product_file_path (str): The file path to the product storage file
        orders_file_path (str): The file path to the orders storage file
    """

    def __init__(
        self,
        customer_file_path: str,
        product_file_path: str,
        orders_file_path: str = None,
    ) -> None:
        self.customer_file_path = customer_file_path
        self.product_file_path = product_file_path
        self.orders_file_path = orders_file_path

    def read_customers(self):
        """
        Reads all customers from persistent storage and returns them as
        a list of Customer instances.
        Args:
            None
        Returns:
            list of Customer: A list of customers in persistent storage
        """
        customers = self.csv_reader(self.customer_file_path)

        def create_customer(args):
            return self.__create_customer(*args)

        return list(map(create_customer, customers))

    def __create_customer(self, id: str, name: str, discount_rate: str, value: str):
        """
        Deserializes the customer, represented as strings, into a
        Customer/Member/VIPMember instance.
        Args:
            id (str): The id of the customer
            name (str): The name of the customer
            discount_rate (str): The discount rate for the customer
            value (str): The amount spent by the customer
        Returns:
            customer (Customer|Member|VIPMember): The customer instance
        """
        customer_type = id[0]
        discount_rate = float(discount_rate)
        value = float(value)
        if customer_type == "C":
            return Customer(id, name, value)
        elif customer_type == "M":
            return Member(id, name, value)
        elif customer_type == "V":
            return VIPMember(id, name, value, discount_rate)

    def read_products(self):
        """
        Reads the products from persistent storage.
        Args:
            None
        Returns:
            list of Product: The list of products from persisten storage
        """
        products = self.csv_reader(self.product_file_path)
        product_list = [
            self.__create_product(*args) for args in products if args[0][0] == "P"
        ]
        return product_list

    def read_bundles(self, product_list):
        """
        Reads the bundles from persistent storage. Uses product_list to reference bundle's
        product ids to product instances.

        Args:
            product_list (list of Product): The list used to reference bundle's product ids
        Returns:
            list of Bundle: The list of Bundles from persistent storage
        """
        products = self.csv_reader(self.product_file_path)
        bundle_list = [
            self.__create_bundle(product_list, args)
            for args in products
            if args[0][0] == "B"
        ]
        return bundle_list

    def __create_product(self, id: str, name: str, price: str, stock: str):
        """
        Deserializes the product, represented as strings, into a
        Product instance.
        Args:
            id (str): The id of the product
            name (str): The name of the product
            price (str): The price of the product
            stock (str): The quantity in stock
        Returns:
            product (Product): The product instance
        """
        if not price.strip() == "":
            price = float(price)
        else:
            price = None
        stock = int(stock)
        return Product(id, name, price, stock)

    def __create_bundle(self, product_list, args):
        """
        Deserializes the bundle, represented as strings, into a
        Bundle instance. Uses an args list to represent the necessary information.
        The list should be of the format: [id, name, product_id_1, ..., product_id_n, stock]
        Args:
            product_list (list of Product): Products used to create bundle
            args (list of str): Arguments used to create bundle
        Returns:
            bundle (Bundle): The bundle instance
        """
        id = args[0]
        name = args[1]
        bundle = args[2:-1]
        products = [
            {"id": p.id, "price": p.price} for p in product_list if p.id in bundle
        ]
        stock = int(args[-1])
        return Bundle(id, name, products, stock)

    def read_orders(self):
        """
        Reads the orders from persistent storage.
        Args:
            None
        Returns:
            list of Orders: List of Orders from persistent storage
        """
        orders = []
        with open(self.orders_file_path, "r", encoding="utf-8") as f:
            for line in f:
                args = line.split(", ")
                customer, product, quantity, timestamp = args
                orders.append(Order(customer, product, quantity, timestamp=timestamp))
        return orders

    def csv_reader(self, file_path):
        """
        A CSV file format reader generator. Takes a file path and reads a new line
        when called.

        Args:
            file_path (str): The path to the CSV formatted file
        Returns:
            list of str: The list of comma-seperated values on current line
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    yield line.split(", ")
        except FileNotFoundError as e:
            print("Customer data file not found. Exiting...")
            raise e

    def save_customer(self, customer: Customer):
        """
        Appends a new customer to persistent storage in a CSV format. Follows the format
        "id, name, discount_rate, value".

        Args:
            customer (Customer): The customer which to append
        Returns:
            None
        """
        try:
            with open(self.customer_file_path, "a", encoding="utf-8") as f:
                f.write(
                    f"{customer.id}, {customer.name}, {customer.discount_rate}, {customer.value}\n"
                )
        except IOError as e:
            print("Error saving customer to file. Exitting...")
            raise e

    def update_customer_info(self, customer: Customer):
        """
        Updates customer info in persistent storage. Relevant for updating value or
        discount_rate. The customer is identified by their id and the remainding
        information in the Customer instance replaces the persistent information.

        Works by copying the old file to a new file, whilest updating the customer
        information on the fly. When the information has been updated, the old file
        is replaced by the new.

        Args:
            customer (Customer): The customer to update
        Returns:
            None
        """
        temp_file_path, file_extension = os.path.splitext(self.customer_file_path)
        temp_file_path += "_temp" + file_extension
        with open(self.customer_file_path, "r+", encoding="utf-8") as f:
            with open(temp_file_path, "w", encoding="utf-8") as f_new:
                for line in f:
                    if line.startswith(customer.id):
                        id, name, discount_rate, value = customer
                        f_new.write(f"{id}, {name}, {discount_rate}, {value}\n")
                    else:
                        f_new.write(line)

        os.replace(temp_file_path, self.customer_file_path)

    def update_product_info(self, product: Product):
        """
        Updates product info in persistent storage. Relevant for updating price or
        stock. The prouct is identified by its id and the remainding
        information in the Product instance replaces the persistent information.

        Works by copying the old file to a new file, whilest updating the customer
        information on the fly. When the information has been updated, the old file
        is replaced by the new.

        Args:
            product (Product): The product to update
        Returns:
            None
        """
        temp_file_path, file_extension = os.path.splitext(self.product_file_path)
        temp_file_path += "_temp" + file_extension
        with open(self.product_file_path, "r+", encoding="utf-8") as f:
            with open(temp_file_path, "w", encoding="utf-8") as f_new:
                for line in f:
                    if line.startswith(product.id):
                        self.write_product_to_file(product, f_new)
                    else:
                        f_new.write(line)

        os.replace(temp_file_path, self.product_file_path)

    def write_product_to_file(self, product: Product, file):
        """
        Write a comma-seperated serialized version of the product
        to a file. Useful for seperating Bundles and Products,
        which follow two different formats.

        Args:
            product (Product): The product which to write
            file (File): A file opened in write mode
        Returns:
            None
        """
        if product.id.startswith("P"):
            id, name, price, stock = product
            file.write(f"{id}, {name}, {price}, {stock}\n")
        elif product.id.startswith("B"):
            id, name, products, stock = product
            product_ids = [p["id"] for p in products]
            products = ", ".join(product_ids)
            file.write(f"{id}, {name}, {products}, {stock}\n")

    def save_order(self, order: Order):
        """
        Appends a new order to persistent storage in a CSV format. Follows the format
        "customer id, product id, quantity, timestamp"

        Args:
            order (Order): The order which to append
        Returns:
            None
        """
        if self.orders_file_path is None:
            return
        with open(self.orders_file_path, "a", encoding="utf-8") as f:
            f.write(
                f"{order.customer.id}, {order.product.id}, {order.quantity}, {order.timestamp}\n"
            )


class Records:
    """
    The class which maintains the main state. The records responsibility is keep track of
    a main state, which is kept between purchases as well as in persistent storage.
    The persistent storage is managed by a PersistentStorageManager.

    Args:
        customer_file_path (str): The file path to the customer storage file
        product_file_path (str): The file path to the product storage file
        orders_file_path (str, optional): The file path to the orders storage file
    Attributes:
        next_customer_id (int): The next available unique customer id number
        next_product_id (int): The next available unqieu product id number
    """

    def __init__(
        self,
        customer_file_path: str,
        product_file_path: str,
        orders_file_path: str = None,
    ) -> None:
        self._storage_manager = PersistentStorageManager(
            customer_file_path, product_file_path, orders_file_path
        )
        try:
            self.customers = self._storage_manager.read_customers()
            self.products = self._storage_manager.read_products()
            self.products += self._storage_manager.read_bundles(self.products)
        except Exception as e:
            raise IOError(e) from e
        try:
            self.orders = self._storage_manager.read_orders()
        except Exception:
            print("Cannot load the order file. Run as if there is no order previously.")
            self.orders = []

        self.next_customer_id = self.get_last_customer_id() + 1
        self.next_product_id = self.get_last_product_id() + 1

    def find_customer(self, query: str, search_in_name: bool = None):
        """
        Searches for a customer in the self.customer. If not specified,
        will search by both name and id (In that order). 

        Args:
            query (str): The id/name to seach for
            search_in_name (bool, optional): Whether to seach in name only
        Returns:
            Customer|None: The customer found. If none found, return None.
        """
        if search_in_name is not None:
            return self.find_in_customers_or_products(
                query, search_in_name, self.customers
            )

        customer = self.find_in_customers_or_products(query, True, self.customers)
        if customer is None:
            customer = self.find_in_customers_or_products(query, False, self.customers)
        return customer

    def find_product(self, query: str, search_in_name: bool = False):
        """
        Searches for a product in the product_list. If not specified,
        will search by both name and id (In that order). 

        Args:
            query (str): The id/name to seach for
            search_in_name (bool, optional): Whether to seach in name only
        Returns:
            Customer|None: The product found. If none found, return None.
        """
        if search_in_name is not None:
            return self.find_in_customers_or_products(
                query, search_in_name, self.products
            )

        product = self.find_in_customers_or_products(query, True, self.products)
        if product is None:
            product = self.find_in_customers_or_products(query, False, self.products)
        return product

    def find_in_customers_or_products(self, query: str, search_in_name: bool, arr_list):
        """
        Searches for a customer/product in a given list by either name or id.

        Args:
            query (str): The id/name to seach for
            search_in_name (bool): Whether to seach in name
            arr_lst (list of Product / List of Customer): The list to search in
        Returns:
            Customer|Product|None: The instance found. If none found, return None.
        """
        field = (lambda x: x.name) if search_in_name else (lambda x: x.id)
        try:
            index = list(map(field, arr_list)).index(query)
            return arr_list[index]
        except ValueError:
            return None

    def list_customers(self):
        """
        Prints to customers to the console.

        Args:
            None
        Returns:
            None
        """
        print("CUSTOMERS: ")
        for customer in self.customers:
            print(
                "{}, {}, {:.2f}, {:.2f}".format(
                    customer.id, customer.name, customer.discount_rate, customer.value
                )
            )

    def list_products(self):
        """
        Prints to products/bundles to the console.

        Args:
            None
        Returns:
            None
        """
        print("PRODUCTS: ")
        for product in self.products:
            if product.id.startswith("P"):
                print(
                    "{}, {}, {:.2f}, {}".format(
                        product.id, product.name, product.price, product.stock
                    )
                )
            elif product.id.startswith("B"):
                product_ids = [p["id"] for p in product.products]
                product_ids = ", ".join(product_ids)
                print(
                    "{}, {}, {}, {:.2f}, {}".format(
                        product.id,
                        product.name,
                        product_ids,
                        product.price,
                        product.stock,
                    )
                )

    def get_last_customer_id(self):
        """
        Gets the last customer interger id found in the 
        self.customer.

        Args:
            None
        Returns:
            last id (int): The id from the last customer
        """
        if len(self.customers) == 0:
            return 0
        return int(self.customers[-1].id[1:])

    def get_last_product_id(self):
        """
        Gets the last product interger id found in the 
        self.products.

        Args:
            None
        Returns:
            last id (int): The id from the last product
        """
        if len(self.products) == 0:
            return 0
        return int(self.products[-1].id[1:])

    def create_new_customer(self, name: str, member_type: str = "C"):
        """
        Creates a new Customer/Member/VIPMember and saves them
        in persistent storage.

        Args:
            name (str): The name of the customer
            member_type (str['C' | 'M' | 'V']): The membership type of the customer
        Returns:
            customer (Customer|Member|VIPMember): The newly created member
        """
        if member_type == "C":
            customer = Customer(member_type + str(self.next_customer_id), name)
        elif member_type == "M":
            customer = Member(member_type + str(self.next_customer_id), name)
        elif member_type == "V":
            customer = VIPMember(member_type + str(self.next_customer_id), name)
        self.next_customer_id += 1
        self._storage_manager.save_customer(customer)
        self.customers.append(customer)
        return customer

    def execute_order(self, order: Order):
        """
        Updates all information neccesary when the customer completes an order.
        I.e. updates product, customer and order information in both volite and
        persistent storage.

        Args:
            order (Order): The order which to execute
        Returns:
            None
        """
        customer, product, quantity, purchased_VIP, _ = order
        customer.value += customer.get_discount(order.total_price)[1]
        if purchased_VIP:
            customer.value += VIPMember.membership_cost

        product.stock -= quantity

        self._storage_manager.update_customer_info(customer)
        self._storage_manager.update_product_info(product)
        self._storage_manager.save_order(order)

    def update_customer_info(self, customer: Customer):
        self._storage_manager.update_customer_info(customer)

class AbstractPage:
    """
    The AbstractPage class. Uses the command pattern.

    Args:
        None
    Attributes:
        None
    """
    def __init__(self) -> None:
        if type(self) is AbstractPage:
            raise RuntimeError("Cannot instantiate abstract class")

    def run(self) -> int:
        pass


class AdjustVIPDiscount(AbstractPage):
    """
    The AdjustVIPDiscount class. Inherits from the AbstractPage class.
    Allows users to adjust the discount rate for an individual VIPMember.

    Args:
        None
    Attributes:
        None
    """
    def __init__(self, records: Records) -> None:
        self.records = records

    def run(self):
        customer_id = input(
            "Please type the name or ID of the customer you would like to adjust: "
        )
        customer = self.records.find_customer(customer_id)

        if customer is None or not customer.id.startswith("V"):
            print("Invalid customer!")
            return 0

        discount_rate = input(
            f"Please type the new discount rate (Current is {customer.discount_rate}): "
        )
        if not self._validate_discount_rate(discount_rate):
            print("Invalid discount rate!")

        customer.set_rate(float(discount_rate))
        self.records.update_customer_info(customer)
        return 0

    def _validate_discount_rate(self, discount_rate: str):
        """
        Validates that the discount rate is a string which can be converted to a integer
        which is between 0 and 1, exclusive.

        Args:
            discount_rate (str): The discount rate to validate
        Returns:
            is_valid (bool): Is the discount rate string proper
        """
        try:
            discount_rate = float(discount_rate)
            if discount_rate < 0 or discount_rate > 1:
                return False
        except:
            return False
        return True


class AdjustVIPThreshold(AbstractPage):
    """
    The AdjustVIPThreshold class. Inherits from the AbstractPage class.
    Allows users to adjust the discount threshold for the VIPMember class.

    Args:
        None
    Attributes:
        None
    """
    def __init__(self, records: Records) -> None:
        self.records = records

    def run(self):
        discount_threshold = input(
            f"Please type the VIP threshold (Current is {VIPMember.discount_threshold}): "
        )
        while not self._validate_discount_threshold(discount_threshold):
            print("Invalid discount rate!")
            discount_threshold = input(
                f"Please type the VIP threshold (Current is {VIPMember.discount_threshold}): "
            )

        VIPMember.set_threshold(float(discount_threshold))
        return 0

    def _validate_discount_threshold(self, discount_threshold: str):
        """
        Validates that the discount threshold is a string which can be converted to a positive integer.

        Args:
            discount_threshold (str): The discount threshold to validate
        Returns:
            is_valid (bool): Is the discount rate string proper
        """
        try:
            discount_threshold = float(discount_threshold)
            if discount_threshold <= 0:
                return False
        except:
            return False
        return True


class DisplayCustomers(AbstractPage):
    """
    The DisplayCustomers class. Inherits from the AbstractPage class.
    Displays all customer information to the console for all customers.

    Args:
        None
    Attributes:
        None
    """
    def __init__(self, records: Records) -> None:
        super().__init__()
        self.records = records

    def run(self) -> int:
        self.records.list_customers()
        return 0


class DisplayOrders(AbstractPage):
    """
    The DisplayOrders class. Inherits from the AbstractPage class.
    Displays all order information to the console for all orders.

    Args:
        None
    Attributes:
        None
    """
    def __init__(self, records: Records) -> None:
        super().__init__()
        self.records = records

    def run(self) -> int:
        print("ORDERS:")
        for order in self.records.orders:
            customer, product, quantity, _, timestamp = order
            print(f"{customer}, {product}, {quantity}, {timestamp}", end="")
        return 0


class DisplayOrdersCustomer(AbstractPage):
    """
    The DisplayOrdersCustomer class. Inherits from the AbstractPage class.
    Displays all orders to the console for a single customer.

    Args:
        None
    Attributes:
        None
    """
    def __init__(self, records: Records) -> None:
        super().__init__()
        self.records = records

    def run(self) -> int:

        customer_id = input(
            "Please type the name or ID of the customer you would like to view orders of: "
        )
        customer = self.records.find_customer(customer_id)
        if customer is None:
            print(f"Invalid customer!")
            return 0

        print("ORDERS:")
        for order in self.records.orders:
            if order.customer == customer.id:
                order_customer, product, quantity, _, timestamp = order
                print(f"{order_customer}, {product}, {quantity}, {timestamp}", end="")
        return 0


class DisplayProducts(AbstractPage):
    """
    The DisplayProducts class. Inherits from the AbstractPage class.
    Displays all product information to the console for all products.

    Args:
        None
    Attributes:
        None
    """
    def __init__(self, records: Records) -> None:
        super().__init__()
        self.records = records

    def run(self) -> int:
        self.records.list_products()
        return 0


class ExitPage(AbstractPage):
    """
    The ExitPage class. Inherits from the AbstractPage class.
    Exit the application by returning a exit code.

    Args:
        None
    Attributes:
        None
    """
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> int:
        print("Thank you for using the Console-Mart System. See you another time!")
        return 1


class PlaceOrderPage(AbstractPage):
    """
    The PlaceOrderPage class. Inherits from the AbstractPage class.
    Allows customers to purchase a quantity of items by supplying their
    name or id, the products name or id, and the quantity.

    During the process the customer, if new, is also prompted whether they
    would like to sign up for a membership or VIP membership.

    Args:
        None
    Attributes:
        None
    """
    def __init__(self, records: Records) -> None:
        super().__init__()
        self.records = records

    def run(self):

        name = input("Please enter your name: ")
        customer = self.records.find_customer(name, search_in_name=True)

        product = self._ask_for_product()
        if product is None:
            return 0

        quantity = self._ask_for_quantity(product)

        new_member_type = None
        if customer is None:
            new_member_type, customer = self._ask_for_membership(name)
            order = Order(customer, product, quantity, new_member_type == "V")
        else:
            order = Order(customer, product, quantity)

        self.records.execute_order(order)

        if new_member_type == "V":
            customer.value += VIPMember.membership_cost

        self._print_order(order)

        print("Thank you for shopping at Console-Mart!")

        return 0

    def _ask_for_membership(self, name: str):
        """
        Prompts the user to join the membership program. If yes, the user will be asked the type (Member or VIPMember).
        Also creates the Customer|Member|VIPMember instance and saves it, regardless of answer to membership prompt.

        Args:
            name (str): The name of the customer
        Returns:
            customer (Customer): The newly created customer
        """
        member_choice = input(
            "We can see that you are not a member. Would you like to sign up for membership (Y/N): "
        ).upper()

        while member_choice not in ["Y", "N"]:
            member_choice = input("Invalid answer. Please enter (Y/N): ").upper()

        if member_choice == "N":
            return "C", self.records.create_new_customer(name, "C")

        print("Please select with membership type you would like to sign up for.")
        member_type = input("Regular Member or VIP (M/V): ").upper()
        while member_type not in ["M", "V"]:
            member_type = input("Invalid answer. Please enter (M/V): ").upper()

        customer = self.records.create_new_customer(name, member_type)

        print("Thank you for signing up!")
        return member_type, customer

    def _ask_for_product(self):
        """
        Prompts the user for a product. Then retrieves and validates set product. If product
        does not exist or is invalid (No pricing or out of stock), the user will be prompted
        for a new product. This is until a valid product is supplied.

        Args:
            None
        Returns:
            product (Product): The found product
        """
        product_name = input("Please enter product name or ID: ")
        product = self.records.find_product(product_name)

        if not (product is None or self._validate_product(product)):
            return None

        while product is None:
            product_name = input(
                "Product could not be found. Please enter a valid product name or ID: "
            )

            product = self.records.find_product(product_name, search_in_name=True)
            if product is None:
                product = self.records.find_product(product_name)

            if not (product is None or self._validate_product(product)):
                return None
        return product

    def _validate_product(self, product: Product):
        """
        Validate that the product is in stock and has valid pricing.

        Args:
            product (Product): The product to validate
        Returns:
            is_valid (bool): Whether the product is valid
        """
        if product.stock == 0:
            print("Product is out of stock. Please choose another product.")
            return False
        if product.price is None or product.price <= 0:
            print(
                f"Product has an invalid pricing of {product.price}. Returning to menu..."
            )
            return False
        return True

    def _ask_for_quantity(self, product: Product):
        """
        Prompts the user for a quantity of product to buy. 

        Args:
            product (Product): The product being bought
        Returns:
            quanity (int): The amount of product asked for
        """
        quantity = input("Enter the amount you would like to purchase: ")

        while not (self._validate_quantity(quantity) and int(quantity) <= product.stock):
            quantity = input(
                f"{quantity} is an invalid amount. There are {product.stock} {product.name}(s) in stock. Please enter a valid amount: "
            )
        quantity = int(quantity)

        return quantity

    def _validate_quantity(self, quantity: str):
        """
        Validates that a given string can be converted into a positive integer.

        Args:
            quantity (str): The string to validate
        Returns:
            is_valid (bool): Whether the string is valid
        """
        try:
            quantity = int(quantity)
            if quantity < 1:
                return False
            return True
        except:
            return False

    def _print_order(self, order: Order):
        """
        Prints the order to the screen at the end of the transaction.

        Args:
            order (Order): The order to print
        Returns:
            None
        """
        discount_rate, total_cost = order.customer.get_discount(order.total_price)

        print(order, order.customer, order.product)
        print(
            f"""
            {order.customer.name} purchase {order.quantity} x {order.product.name}
            Unit Price:     {order.product.price} (AUD)
            {order.customer.name} gets a discount of {discount_rate} %
            """
        )

        if order.purchased_VIP:
            print(f"\t    Membership price:   {VIPMember.membership_cost} (AUD)\n")
            total_cost += VIPMember.membership_cost
        print(f"\t    Total price:    {total_cost} (AUD)")


class Menu(AbstractPage):
    """
    The Menu class. Inherits from the AbstractPage class.
    Is the overarching menu in which users can access all options in the
    program. If any sub-pages returns anything but a 0, will terminate the program.

    Args:
        None
    Attributes:
        None
    """
    def __init__(self, records: Records) -> None:
        super().__init__()
        self.records = records
        self.menu_items = [
            ("Place order", PlaceOrderPage(self.records)),
            ("Display customers", DisplayCustomers(self.records)),
            ("Display products", DisplayProducts(self.records)),
            ("Display orders", DisplayOrders(self.records)),
            ("Display customer orders", DisplayOrdersCustomer(self.records)),
            ("Adjust VIP discount rate", AdjustVIPDiscount(self.records)),
            ("Adjust VIP discount threshold", AdjustVIPThreshold(self.records)),
            ("Exit", ExitPage()),
        ]

    def run(self):
        while self.__display_menu() == 0:
            pass
        return 0

    def __display_menu(self):
        """
        Prints the menu to the screen.

        Args:
            None
        Returns:
            None
        """
        for index, (title, _) in enumerate(self.menu_items, 1):
            print(f"[{index}] {title}")
        choice = None
        while not self._validate_choice(choice):
            choice = input("Please select a menu option: ")
        
        choice = int(choice)
        return self.menu_items[choice - 1][1].run()

    def _validate_choice(self, choice: str):
        """
        Validates that a given string can be converted into a positive integer,
        that is less than the number of menu options.

        Args:
            quantity (str): The string to validate
        Returns:
            is_valid (bool): Whether the string is valid
        """
        try:
            choice = int(choice)
            if choice < 1 or choice > len(self.menu_items):
                return False
            return True
        except:
            return False

def run():
    try:
        args = ["./data/customers.csv", "./data/products.csv", "./data/orders.csv"]

        c_args = sys.argv[1:4]
        arg_length = len(c_args)
        if arg_length > 0:
            args[:arg_length] = c_args

        records = Records(*args)
    except IOError as e:
        print(
            "Error retrieving data from customers/products. The following error was recorded: "
            + str(e)
        )
        return
    menu = Menu(records)
    menu.run()


if __name__ == "__main__":
    run()
