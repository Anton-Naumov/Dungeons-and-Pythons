from weapon import Weapon
from spell import Spell


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

<<<<<<< HEAD
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
=======
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
>>>>>>> 55d292b64ebd1b10eee2da407ff453e57e8b433c
