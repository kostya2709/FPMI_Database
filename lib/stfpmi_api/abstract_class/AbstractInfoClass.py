class AbstractInfoClass:
    """ Abstract class to get information.
        It provides some methods which are used by classes that inherit this class."""

    """ List of available attributes"""
    available_attr = []

    @classmethod
    def initialize(cls, initial_values: dict, __object):
        """Receives the dictionary like {key : value},
        checks whether 'key' is a name of an available attribute
        (which are listed in 'available_attr'). If so, it initializes
        the attribute with the 'value', otherwise it raises an exception.

        Arguments:
            cls             a class, inherited from this one.
            initial_values  dictionary in the format {'attribute name' : 'desired attribute value'}.
            __object        the proper object of class 'cls' which needs to be initialized.

        Exception:
            RunTimeError    input data are incorrect, a 'key' in the dictionary 'initial_values'
                            does not correspond to any attribute listed in 'available attributes' field.
        """
        for attr in cls.available_attr:
            setattr(__object, attr, None)

        for key, value in initial_values.items():
            if key in cls.available_attr:
                setattr(__object, key, value)
            else:
                raise RuntimeError(f"Unexpected attribute in {cls.__name__}: {key}")

    def __str__(self):
        """String representation of the object in the format:

        'attribute name 1': 'attribute 1 value'
        'attribute name 2': 'attribute 2 value'
        ...
        'attribute name n': 'attribute n value'
        'attribute name k':
            'attribute name j': 'attribute j value'
            ...
            'attribute name i': 'attribute i value'
        """
        dashes = 60
        return dashes * "-" + "\n" + add_attr_str(self, 1) + dashes * "-" + "\n"


def add_attr_str(obj, tab_num):
    result = ""
    for key, value in obj.__dict__.items():
        result += tab_num * "\t" + str(key) + ": "
        if hasattr(value, "__dict__"):
            result += "\n"
            result += add_attr_str(value, tab_num + 1)
        elif isinstance(value, list):
            result += "\n"
            for i in value:
                result += "\n" + add_attr_str(i, tab_num + 1)
            result += "\n"
        else:
            result += str(value) + "\n"
    return result


if __name__ == "__main__":
    pass
