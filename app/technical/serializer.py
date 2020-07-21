import omitempty


class Serializer(object):
    @property
    def value(self):
        dict_values = omitempty(self.__dict__)
        if not dict_values:
            return None
        return self.__dict__
