class PlayerMixin:
    def __init__(self, *, health, mana):
        self._health = health
        self._max_health = self._health
        self._mana = mana
        self._max_mana = self._mana
        self._weapon = None
        self._spell = None

    def is_alive(self):
        return self._health > 0

    def get_health(self):
        return self._health

    def get_mana(self):
        return self._mana

    def can_cast(self):
        return self._spell is not None and self._mana >= self._spell.mana_cost

    def take_healing(self, healing_points):
        if self.is_alive() is False:
            return False

        self._health = min(self._health + healing_points, self._max_health)
        return True

    def take_mana(self, mana_points):
        self._mana = min(self._mana + mana_points, self._max_mana)

    def attack(self, *, by):
        raise Exception('Not implemented mothod \"attack\"!')

    def take_damage(self, damage):
        self._health = max(self._health - damage, 0)

    def equip(self, weapon):
        self._weapon = weapon

    def learn(self, spell):
        self._spell = spell

    @property
    def weapon(self):
        return self._weapon

    @property
    def spell(self):
        return self._spell

    # TODO: write test
    def pick_better_tool_to_fight(self):
        if self._spell is None and self._weapon is None:
            raise Exception('You havent equiped anything!')
        elif self._spell is None and self._weapon is not None:
            return 'weapon'
        elif self._spell is not None and self._weapon is None:
            return 'spell'
        elif self._spell.get_damage >= self._weapon.get_damage:
            return 'spell'
        else:
            return 'weapon'
