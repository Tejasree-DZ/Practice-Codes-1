class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print("Creating new instance")
        else:
            print("Using existing instance")
        return cls._instance

    def __init__(self, name):
        self.name = name

    def show_name(self):
        print(f"Singleton object name: {self.name}")


if __name__ == "__main__":
    obj1 = Singleton("Object 1")
    obj2 = Singleton("Object 2")

    print("obj1 is obj2?", obj1 is obj2)

    obj1.show_name()
    obj2.show_name()