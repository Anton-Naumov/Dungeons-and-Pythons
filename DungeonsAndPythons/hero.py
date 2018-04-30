from player_mixin import PlayerMixin
from exceptions import NotEnoughManaError, NotEquippedError


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
        if by is not None:
            return super(Hero, self).attack(by)
        else:
            raise NotEquippedError("You havent equipped anything")

    def __str__(self):
        return f'{self.known_as()}, {PlayerMixin.__str__(self)}'

    def __repr__(self):
        return str(self)

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
