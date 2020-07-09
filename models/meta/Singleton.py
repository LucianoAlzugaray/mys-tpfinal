class Singleton(type):
    _instances = []

    def __call__(cls, *args, **kwargs):
        if len(cls._instances) == 0:
            cls._instances.append(super(Singleton, cls).__call__(*args, **kwargs))
        return cls._instances[0]