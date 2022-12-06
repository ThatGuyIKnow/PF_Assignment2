class Customer():
    _discount_rate = 0.

    def __init__(self, id: str, name: str, value: int = 0) -> None:
        self._id = id
        self._name = name
        self._value = value

    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @property
    def value(self):
        return self._value

    @classmethod
    @property
    def discount_rate(cls):
        return cls._discount_rate


    def get_discount(self, price):
        return self.discount_rate, price

    def display_info(self):
        attr = vars(self)
        attr['discount_rate'] = self.discount_rate
        print(f'Customer: {attr}')


    def __eq__(self, __o: object) -> bool:
            return self._id == __o.id