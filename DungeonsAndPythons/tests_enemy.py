import unittest
from enemy import Enemy
from weapon import Weapon
from spell import Spell


class EnemyTests(unittest.TestCase):
    def setUp(self):
        self.e = Enemy(health=100, mana=100, damage=50)
        self.w = Weapon(name='The Axe of Destiny', damage=20)
        self.s = Spell(name='Fireball', damage=30, mana_cost=60, cast_range=2)

        self.e.equip(self.w)
        self.e.learn(self.s)

    def test_can_cast(self):
        self.assertTrue(self.e.can_cast())
        self.e._mana = 29
        self.assertFalse(self.e.can_cast())

    def test_attack(self):
        self.assertEqual(self.e.attack(by='weapon'), 70)
        self.assertEqual(self.e.attack(by='spell'), 80)
        with self.assertRaises(Exception):
            self.e.attack(by='spell')

    def test_take_mana(self):
        self.assertFalse(self.e.take_mana())

    def test_eq_returns_false_when_enemy1_super_different_than_enemy2_super(self):
        enemy1 = Enemy(health=100, mana=100, damage=50)
        enemy2 = Enemy(health=200, mana=100, damage=50)

        self.assertNotEqual(enemy1, enemy2)

    def test_eq_returns_false_when_enemy1_damage_different_than_enemy2_damage(self):
        enemy1 = Enemy(health=100, mana=100, damage=50)
        enemy2 = Enemy(health=100, mana=100, damage=75)

        self.assertNotEqual(enemy1, enemy2)

    def test_eq_returns_true_when_supers_are_equal_and_damages_are_equal(self):
        enemy1 = Enemy(health=100, mana=100, damage=50)
        enemy2 = Enemy(health=100, mana=100, damage=50)

        self.assertEqual(enemy1, enemy2)

    def test_to_json(self):
        expected = {
            'damage': 50,
            'health': 100,
            'mana': 100,
            'weapon': self.w.to_json(),
            'spell': self.s.to_json()
        }

        self.assertDictEqual(self.e.to_json(), expected)

    def test_from_json(self):
        json_dict = {
            'damage': 50,
            'health': 100,
            'mana': 100,
            'weapon': self.w.to_json(),
            'spell': self.s.to_json()
        }

        self.assertEqual(self.e, Enemy.from_json(json_dict))


if __name__ == '__main__':
    unittest.main()
