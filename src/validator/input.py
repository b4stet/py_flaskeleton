class InputValidator():
    def __init__(self):
        pass

    def check_mandatory(self, value, field_name):
        if value is None:
            raise KeyError('Missing {} field.'.format(field_name))

    def check_type(self, value, expected_type):
        if not isinstance(value, expected_type):
            raise TypeError('Expected {} type, got {}.'.format(expected_type.__name__, type(value)))
