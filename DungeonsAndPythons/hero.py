from player_mixin import PlayerMixin


class Hero(PlayerMixin):
    def __init__(
        self,
        *,
        name,
        title,
        health,
        mana,
        mana_regeneration_rate,
    ):
        super().__init__(health=health, mana=mana)
        self._name = name
        self._title = title
        self._mana_regeneration_rate = mana_regeneration_rate

    def known_as(self):
        return f'{self._name} the {self._title}'

    def attack(self, *, by):
        if by == 'weapon' and self._weapon is not None:
            return self._weapon.get_damage

        if by == 'spell' and self._spell is not None and self.can_cast():
                self._mana -= self._spell.mana_cost
                return self._spell.get_damage

        return 0

    def __eq__(self, other):
        return super(Hero, other).__eq__(self) and\
            self._name == other._name and\
            self._title == other._title and\
            self._mana_regeneration_rate == other._mana_regeneration_rate

    def to_json(self):
        json_dict = {
            'name': self._name,
            'title': self._title,
            'mana_regeneration_rate': self._mana_regeneration_rate
        }

        json_dict.update(super().to_json())

        return json_dict

    @classmethod
    def from_json(cls, json_dict):
        hero = cls(
            name=json_dict['name'],
            title=json_dict['title'],
            health=json_dict['health'],
            mana=json_dict['mana'],
            mana_regeneration_rate=json_dict['mana_regeneration_rate'],
        )

        base_class_hero = PlayerMixin.from_json(json_dict)

        hero.equip(base_class_hero._weapon)
        hero.learn(base_class_hero._spell)

        return hero
