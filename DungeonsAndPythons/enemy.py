from player_mixin import PlayerMixin


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
        if by == 'weapon' and self._weapon is not None:
            return self.__damage + self._weapon.get_damage
        elif by == 'spell' and self._spell is not None:
            if self.can_cast():
                self._mana -= self._spell._mana_cost
                return self.__damage + self._spell.get_damage
            else:
                raise Exception("You dont have enough mana to cast this spell!")
        else:
            return self.__damage

    def take_mana(self):
        # print('You cannot regenerate mana!')
        return False

    def __eq__(self, other):
        return super(Enemy, other).__eq__(self) and\
            self.__damage == other.__damage

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
