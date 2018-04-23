class PlayerMixin:
    def __init__(self, *, health, mana):
        self._max_health = self.health
        self._max_mana = self.mana
        self._health = health
        self._mana = mana
        self._weapon = None
        self._spell = None

    def is_alive(self):
        return self._health > 0

    def get_health(self):
        return self._health

    def get_mana(self):
        return self._mana

    def can_cast(self):
        return self._mana > self._spell.mana_cost()

    def take_healing(self, healing_points):
        self._health = max(self._health + healing_points, self._max_health)

    def take_mana(self, mana_points):
        self._mana = max(self._mana + mana_points, self._max_mana)

    def attack(self):
        raise Exception('Not implemented!')

    def take_deamage(self, deamage):
        self._health = max(self._health - deamage, 0)
