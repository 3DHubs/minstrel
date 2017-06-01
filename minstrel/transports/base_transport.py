class Transport:

    def __init__(self, config):
        pass

    def write(self, dct):
        pass

    def read(self, *args, **kwargs):
        raise NotImplementedError('Cannot read from {}.'
                                  .format(self.__class__.__name__))
