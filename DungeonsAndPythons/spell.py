class Spell:
    def __init__(self, *, name, damage, mana_cost, cast_range):
        self._name = name
        self._damage = damage
        self._mana_cost = mana_cost
        self._cast_range = cast_range

    @property
    def get_name(self):
        return self._name

    @property
    def get_damage(self):
        return self._damage

    @property
    def mana_cost(self):
        return self._mana_cost

    @property
    def cast_range(self):
        return self._cast_range

    def __str__(self):
        return f'Spell {self._name}: damage - {self._damage}, '\
               f'mana_cost - {self._mana_cost}, cast_range - {self._cast_range}'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self._name == other._name and\
           self._damage == other._damage and\
           self._mana_cost == other._mana_cost and\
           self._cast_range == other._cast_range

    def to_json(self):
        return {
            'class': 'Spell',
            'name': self._name,
            'damage': self._damage,
            'mana_cost': self._mana_cost,
            'cast_range': self._cast_range
        }

    @classmethod
    def from_json(cls, json_dict):
        return cls(
            name=json_dict['name'],
            damage=json_dict['damage'],
            mana_cost=json_dict['mana_cost'],
            cast_range=json_dict['cast_range']
        )
