class BaseModel:
    def __init__(self, **data):
        for k, v in data.items():
            setattr(self, k, v)
    model_dump = property(lambda self: self.__dict__)
