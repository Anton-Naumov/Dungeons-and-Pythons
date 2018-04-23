import unittest
from enemy import Enemy
from weapon import Weapon
from spell import Spell


class EnemyTests(unittest.TestCase):
    def setUp(self):
        self.e = Enemy(health=100, mana=100, damage=50)
        w = Weapon(name='The Axe of Destiny', damage=20)
        s = Spell(name='Fireball', damage=30, mana_cost=60, cast_range=2)

        self.e.equip(w)
        self.e.equip(s)

    def test_can_cast(self):
        self.assertTrue(self.e.can_cast())
        self.e.__mana = 30
        self.assertFalse(self.e.can_cast())

    def test_attack(self):
        self.assertEquals(self.e.attack(), 50)
        self.assertEquals(self.e.attack(by='weapon'), 70)
        self.assertEquals(self.e.attack(by='spell'), 80)
        with self.assertRaises(Exception):
        	self.e.attack(by='spell')

    def test_take_mana(self):
        self.assertFalse(self.e.take_mana())


if __name__ == '__main__':
    unittest.main()
