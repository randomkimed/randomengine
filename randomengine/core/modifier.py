# randomengine.core > modifier

class Modifier:
    def __init__(self):
        self.owner = None
        self.__dirty = set()

    def START(self):
        pass

    def AWAKE(self):
        pass

    def UPDATE(self):
        pass

    def LATE_UPDATE(self):
        pass

    def FIXED_UPDATE(self):
        pass

    def EXIT(self):
        pass

    def DIRTY(self, field: str):
        self.__dirty.add(field)

    def IS_DIRTY(self, field: str):
        return field in self.__dirty

    @staticmethod
    def DIRTY_UPDATE(fields: str | list[str], strict: bool = False):
        def decorator(method):
            def wrapper(self, *args, **kwargs):
                if isinstance(fields, str):
                    dirty = self.IS_DIRTY(fields)
                else:
                    check = [self.IS_DIRTY(field) for field in fields]
                    dirty = all(check) if strict else any(check)

                if dirty:
                    result = self.func(*args, **kwargs)
                    self.__dirty.clear()
                    return result
            return wrapper
        return decorator