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
        raise Exception('Not implemented method \"can_cast\"!')

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
<<<<<<< HEAD
=======

    def equip(self, weapon):
        self._weapon = weapon

    def learn(self, spell):
        self._spell = spell
>>>>>>> e5053c1f77df548920f1432d04083b2a7929f07c
