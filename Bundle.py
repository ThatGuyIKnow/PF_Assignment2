class Bundle():
    def __init__(self, id: str, name: str, products, stock: int, discount: float = 0.2) -> None:
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
        prices = list(map(lambda x: x['price'], self.products))
        if None in prices:
            return None
        return sum(prices) * (1-self.discount)
    
    def __eq__(self, __o: object) -> bool:
        return self._id == __o.id