from weapon import Weapon
from spell import Spell
from exceptions import NotEnoughManaError, NotEquippedError, OutOfRangeError


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

    def can_cast(self, range_=0):
        return self._spell is not None and\
            self._mana >= self._spell.mana_cost and\
            self._spell.cast_range > range_

    def take_healing(self, healing_points):
        if self.is_alive() is False:
            return False

        self._health = min(self._health + healing_points, self._max_health)
        return True

    def take_mana(self, mana_points):
        self._mana = min(self._mana + mana_points, self._max_mana)

    def take_damage(self, damage):
        self._health = max(self._health - damage, 0)

    def equip(self, weapon):
        self._weapon = weapon

    def learn(self, spell):
        self._spell = spell

    def __eq__(self, other):
        if sum([obj._weapon is None for obj in [self, other]]) == 1 or\
           sum([obj._spell is None for obj in [self, other]]) == 1:
            return False

        return self._health == other._health and\
            self._max_health == other._max_health and\
            self._mana == other._mana and\
            self._max_mana == other._max_mana and\
            self._weapon == other._weapon and\
            self._spell == other._spell

    def __str__(self):
        return f'health={self._health},mana={self._mana}'

    def __repr__(self):
        return str(self)

    def to_json(self):
        return {
            'health': self._health,
            'mana': self._mana,
            'weapon': self._weapon.to_json() if self._weapon is not None else None,
            'spell': self._spell.to_json() if self._spell is not None else None
        }

    @classmethod
    def from_json(cls, json_dict):
        player = PlayerMixin(health=json_dict['health'], mana=json_dict['mana'])

        weapon = Weapon.from_json(json_dict['weapon']) if json_dict['weapon'] is not None\
            else None
        spell = Spell.from_json(json_dict['spell']) if json_dict['spell'] is not None\
            else None
        player.equip(weapon)
        player.learn(spell)

        return player

    @property
    def weapon(self):
        return self._weapon

    @property
    def spell(self):
        return self._spell

    # TODO: write test
    def make_better_attack(self, range_):
        if range_ > 0:
            if self.can_cast(range_):
                return self.attack(by='spell')
            else:
                raise OutOfRangeError
        else:
            if not self.can_cast() and self.weapon is None:
                raise NotEquippedError
            elif self.can_cast() and self.weapon is not None:
                if self.spell.get_damage > self.weapon.get_damage:
                    return self.attack(by='spell')
                else:
                    return self.attack(by='weapon')
            elif not self.can_cast():
                return self.attack(by='weapon')
            else:
                return self.attack(by='spell')

    def attack(self, by=None):
        if by == 'weapon':
            if self._weapon is not None:
                return self._weapon.get_damage
            else:
                raise NotEquippedError("You havent equipped a weapon")

        if by == 'spell':
            if self._spell is None:
                raise NotEquippedError("You havent learned a spell")
            elif self.can_cast():
                self._mana -= self._spell.mana_cost
                return self._spell.get_damage
            else:
                raise NotEnoughManaError("You dont have enough mana")

        if by is not None:
            raise TypeError("Wrong 'by' type")

        return 0
