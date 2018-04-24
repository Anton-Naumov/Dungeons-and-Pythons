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

    def can_cast(self):
        return self._spell is not None and self._mana >= self._spell.mana_cost

    def attack(self, *, by):
        if by == 'weapon':
            if self._weapon is not None:
                return self._weapon.get_damage
            else:
                raise Exception('The hero must have a weapon to attack with it!')

        if by == 'spell':
            if self._spell is not None and self.can_cast():
                self._mana -= self._spell.mana_cost
                return self._spell.get_damage
            else:
                raise Exception('The hero hasn\'t learned a spell yet or doesn\''
                                'have enough mana!')

        raise Exception(f'Invalid argument \'by={by}\'')
