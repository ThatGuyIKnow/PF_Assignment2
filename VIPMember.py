from Member import Member

class VIPMember(Member):
    _discount_threshold = 1000
    _membership_cost = 200

    def __init__(self, id: str, name: str, value: float = 0, discount_rate: float = 0.1) -> None:
        super().__init__(id, name, value)
        self._discount_rate = discount_rate

    @property
    def discount_rate(self):
        return self._discount_rate

    def get_discount(self, price):
        discount_rate = self.discount_rate
        if price > self._discount_threshold:
            discount_rate += 0.05
        return discount_rate,  price * (1-discount_rate)

    def display_info(self):
        attr = vars(self)
        attr['discount_rate'] = self.discount_rate
        attr['discount_threshold'] = self._discount_threshold
        print(f'Customer: {attr}')

    def set_rate(self, rate):
        self._discount_rate = rate

    @classmethod
    @property
    def membership_cost(cls):
        return cls._membership_cost

    @classmethod
    def set_threshold(cls, threshold):
        cls._discount_threshold = threshold
