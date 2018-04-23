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
                    pos=(0, 0)
    ):
        super().__init__(health=health, mana=mana)
        self._name = name
        self._title = title
        self._mana_regeneration_rate = mana_regeneration_rate
        self._pos = pos

    def known_as(self):
        return f'{self._name} the {self._title}'

    def can_cast(self):
        return self._spell is not None and self._mana >= self._spell.mana_const()

    def attack(self, *, by):
        if by == 'weapon':
            if self._weapon is not None:
                return self._weapon.get_damege
            else:
                raise Exception('The hero must have a weapon to attack with it!')

        if by == 'spell':
            if self._spell is not None and self.can_cast():
                self._mana -= self._spell.mana_cost()
                return self._spell.get_damage
            else:
                raise Exception('The hero must learn a spell before using it!')

        raise Exception(f'Invalid argument \'by={by}\'')
