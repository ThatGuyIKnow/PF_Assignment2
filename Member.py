from Customer import Customer


class Member(Customer):
    _discount_rate = 0.05

    def __init__(self, id: str, name: str, value: float = 0) -> None:
        super().__init__(id, name, value)
    
    def get_discount(self, price):
        new_price = price * (1 - self.discount_rate)
        return (self.discount_rate, new_price)

    @property
    def discount_rate(self):
        return Member._discount_rate

    @classmethod
    def set_rate(cls, rate):
        cls._discount_rate = rate
    