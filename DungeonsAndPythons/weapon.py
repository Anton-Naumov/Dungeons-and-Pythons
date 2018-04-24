class Weapon:
    def __init__(self, *, name, damage):
        self._name = name
        self._damage = damage

    @property
    def get_name(self):
        return self._name

    @property
    def get_damage(self):
        return self._damage

    def __eq__(self, other):
        return self._name == other._name and\
            self._damage == other._damage

    def __str__(self):
        return f'{self._name} with damage:{self._damage}'

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.__str__())

    def to_json(self):
        return {
            'name': self._name,
            'damage': self._damage
        }

    @classmethod
    def from_json(cls, json_dict):
        return cls(
            name=json_dict['name'],
            damage=json_dict['damage']
        )
