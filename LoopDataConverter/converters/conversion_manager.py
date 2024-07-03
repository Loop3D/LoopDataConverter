
class ConversionManager:
    def __init__(self):
        self._converters = []

    def add_converter(self, converter):
        self._converters.append(converter)

    def convert(self, data):
        for converter in self._converters:
            if converter.can_convert(data):
                return converter.convert(data)
        raise ValueError('No converter found for data: {}'.format(data))