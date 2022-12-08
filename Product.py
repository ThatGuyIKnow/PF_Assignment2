class Product():
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