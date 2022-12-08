class Customer():
    _discount_rate = 0.

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

    @property
    def discount_rate(self):
        return Customer._discount_rate


    def get_discount(self, price):
        return self.discount_rate, price

    def display_info(self):
        attr = vars(self)
        attr['discount_rate'] = self.discount_rate
        print(f'Customer: {attr}')


    def __eq__(self, __o: object) -> bool:
            return self._id == __o.id