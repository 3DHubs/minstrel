from .patching import patch


class Mock:

    base = None
    derivatives = None
    objects = None
    transport_configs = None

    def __init__(self, transport_configs, base, derivatives):
        self.transport_configs = transport_configs
        self.base = base
        self.derivatives = derivatives

        self.generate_objects()

    def generate_objects(self):
        self.objects = [self.base]
        for derivative in self.derivatives:
            dct = self.base.copy()
            if 'merge' in derivative:
                dct.update(derivative['merge'])
            if 'patches' in derivative:
                dct = patch(self.base, derivative['patches'])
            self.objects.append(dct)
