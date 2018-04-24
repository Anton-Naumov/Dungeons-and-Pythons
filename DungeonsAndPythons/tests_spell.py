import unittest
from spell import Spell


class TestsSpell(unittest.TestCase):
    def setUp(self):
        self.spell = Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2)

    def test_init_(self):
        self.assertEqual(self.spell._name, 'Fireball')
        self.assertEqual(self.spell._damage, 30)
        self.assertEqual(self.spell._mana_cost, 50)
        self.assertEqual(self.spell._cast_range, 2)

    def test_str_(self):
        expected = 'Spell Fireball: damage - 30, mana_cost - 50, cast_range - 2'

        self.assertEqual(str(self.spell), expected)

    def test_eq_returns_true(self):
        spell1 = Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2)

        self.assertEqual(self.spell, spell1)

    def test_eq_returns_false(self):
        with self.subTest('when one attribute is different'):
            spell1 = Spell(name="Frostbolt", damage=30, mana_cost=50, cast_range=2)

            self.assertNotEqual(self.spell, spell1)

        with self.subTest('when two attributes are different'):
            spell1 = Spell(name="Frostbolt", damage=35, mana_cost=50, cast_range=2)

            self.assertNotEqual(self.spell, spell1)

        with self.subTest('when three attributes are different'):
            spell1 = Spell(name="Frostbolt", damage=35, mana_cost=75, cast_range=2)

            self.assertNotEqual(self.spell, spell1)

        with self.subTest('when four attributes are different'):
            spell1 = Spell(name="Frostbolt", damage=35, mana_cost=75, cast_range=10)

            self.assertNotEqual(self.spell, spell1)

    def test_to_json(self):
        expected = {
            'name': 'Fireball',
            'damage': 30,
            'mana_cost': 50,
            'cast_range': 2
        }

        self.assertEqual(self.spell.to_json(), expected)

    def test_from_json(self):
        json_dict = {
            'name': 'Fireball',
            'damage': 30,
            'mana_cost': 50,
            'cast_range': 2
        }

        self.assertEqual(Spell.from_json(json_dict), self.spell)


if __name__ == '__main__':
    unittest.main()
