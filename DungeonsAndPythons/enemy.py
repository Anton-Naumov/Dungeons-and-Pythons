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

    def can_cast(self):
        return self._spell is not None and self._mana >= self._spell.mana_cost

    def attack(self, *, by=None):
        if by == 'weapon' and self._weapon is not None:
            return self.__damage + self._weapon.get_damage
        elif by == 'spell' and self._spell is not None:
            if self.can_cast():
                self._mana -= self._spell._mana_cost
                return self.__damage + self._spell.get_damage
            else:
                raise Exception
        else:
            return self.__damage

    def take_mana(self):
        # print('You cannot regenerate mana!')
        return False
