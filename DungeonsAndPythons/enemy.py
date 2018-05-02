from player_mixin import PlayerMixin
from exceptions import NotEnoughManaError, NotEquippedError


class Enemy(PlayerMixin):
    def __init__(
        self,
        *,
        health,
        mana,
        damage,
    ):
        super().__init__(health=health, mana=mana)
        self.__damage = damage

    def attack(self, *, by=None):
        if by is not None:
            return super(Enemy, self).attack(by) + self.__damage
        else:
            return self.__damage

    def take_mana(self):
        # print('You cannot regenerate mana!')
        return False

    def __eq__(self, other):
        return super(Enemy, other).__eq__(self) and\
            self.__damage == other.__damage

    def __str__(self):
        return f'Enemy({PlayerMixin.__str__(self)}, damage={self.__damage})'

    def __repr__(self):
        return str(self)

    def to_json(self):
        json_dict = {
            'damage': self.__damage
        }

        json_dict.update(super().to_json())

        return json_dict

    @classmethod
    def from_json(cls, json_dict):
        enemy = cls(
            health=json_dict['health'],
            mana=json_dict['mana'],
            damage=json_dict['damage']
        )

        base_class_hero = PlayerMixin.from_json(json_dict)

        enemy.equip(base_class_hero._weapon)
        enemy.learn(base_class_hero._spell)

        return enemy

    def make_better_attack(range_):
        try:
            return super(Enemy, self).make_better_attack(range_)
        except NotEquippedError:
            return self.attack()
