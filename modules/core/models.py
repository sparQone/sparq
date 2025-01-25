class Model():
    def __init__(self, name=None):
        self.name = name

    def save(self, data):
        print(f"Saving data: {data}")
        