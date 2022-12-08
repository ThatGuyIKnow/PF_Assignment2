

class AbstractPage():
    def __init__(self) -> None:
        if type(self) is AbstractPage:
            raise RuntimeError("Cannot instantiate abstract class")

    def run(self) -> int:
        pass
