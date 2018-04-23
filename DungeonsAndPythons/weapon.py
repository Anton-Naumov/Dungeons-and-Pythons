class Weapon:
    def __init__(self, *, name, damage):
        self.__name = name
        self.__damage = damage

    @property
    def get_name(self):
        return self.__name

    @property
    def get_damage(self):
        return self.__damage

    def __eq__(self, other):
        return self.__name == other.__name and\
            self.__damage == other.__damage

    def __str__(self):
        return f'{self.__name} with damage:{self.__damage}'

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.__str__())
