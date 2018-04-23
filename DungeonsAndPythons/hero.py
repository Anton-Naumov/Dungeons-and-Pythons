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
