import unittest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from hero import Hero
from spell import Spell
from weapon import Weapon
from exceptions import NotEquippedError, NotEnoughManaError


class TestsHero(unittest.TestCase):
    def setUp(self):
        self.hero1 = Hero(
            name='Toni',
            title='Pythonslayer',
            health=250,
            mana=1000,
            mana_regeneration_rate=25,
        )

        self.hero2 = Hero(
            name="Bron",
            title="Dragonslayer",
            health=100,
            mana=100,
            mana_regeneration_rate=2
        )

        self.spell = Spell(name="Fireball", damage=30, mana_cost=110, cast_range=2)
        self.weapon = Weapon(name="The Axe of Destiny", damage=20)

    def test_init_working_correctly(self):
        with self.subTest('hero1'):
            self.assertEqual(self.hero1._name, 'Toni')
            self.assertEqual(self.hero1._title, 'Pythonslayer')
            self.assertEqual(self.hero1._health, 250)
            self.assertEqual(self.hero1._max_health, 250)
            self.assertEqual(self.hero1._mana, 1000)
            self.assertEqual(self.hero1._max_mana, 1000)
            self.assertEqual(self.hero1._mana_regeneration_rate, 25)
            self.assertEqual(self.hero1._weapon, None)
            self.assertEqual(self.hero1._spell, None)

    def test_known_as(self):
        with self.subTest('hero1'):
            self.assertEqual(self.hero1.known_as(), 'Toni the Pythonslayer')

        with self.subTest('hero2'):
            self.assertEqual(self.hero2.known_as(), 'Bron the Dragonslayer')

    def test_can_cast(self):
        with self.subTest('spell is None'):
            self.assertFalse(self.hero1.can_cast())

        with self.subTest('when mana is not enough'):
            self.hero2._spell = self.spell

            self.assertFalse(self.hero2.can_cast())

        with self.subTest('when mana is not enough'):
            self.hero1._spell = self.spell

            self.assertTrue(self.hero1.can_cast())

    def test_attack_raises_exceptions_correctly(self):
        with self.subTest('when by == weapon and hero\'s weapon is None'):
            with self.assertRaises(NotEquippedError):
                self.hero1.attack(by='weapon')

        with self.subTest('when by == spell and hero\'s spell is None'):
            with self.assertRaises(NotEquippedError):
                self.hero1.attack(by='spell')

        with self.subTest('when by is not \'weapon\' or \'spell\''):
            with self.assertRaises(TypeError):
                self.hero1.attack(by='foot')

        with self.subTest('when spell costs more then current mana'):
            with self.assertRaises(NotEnoughManaError):
                self.hero1.learn(self.spell)
                for x in range(0, 20):
                    self.hero1.attack(by='spell')

    def test_attack_returns_correct_damage(self):
        with self.subTest('\'by\' == \'spell\''):
            self.hero1._spell = self.spell
            damage = self.hero1.attack(by='spell')

            self.assertEqual(damage, 30)
            self.assertEqual(self.hero1._mana, 890)

        with self.subTest('\'by\' == \'weapon\''):
            self.hero2._weapon = self.weapon
            damage = self.hero2.attack(by='weapon')

            self.assertEqual(damage, 20)

    def test_eq_returns_false_when_hero1_super_different_than_hero2_super(self):
        hero3 = Hero(
            name="Bron",
            title="Dragonslayer",
            health=100,
            mana=100,
            mana_regeneration_rate=2
        )

        hero3.learn(self.spell)

        self.assertNotEqual(self.hero2, hero3)

    def test_eq_returns_false_when_hero1_has_different_attr_than_hero2_super(self):
        hero3 = Hero(
            name="Toni",
            title="Dragonslayer",
            health=100,
            mana=100,
            mana_regeneration_rate=2
        )

        self.assertNotEqual(self.hero2, hero3)

    def test_eq_returns_true_when_super_and_all_attrs_are_the_same(self):
        hero3 = Hero(
            name="Bron",
            title="Dragonslayer",
            health=100,
            mana=100,
            mana_regeneration_rate=2
        )

        self.assertEqual(self.hero2, hero3)

    def test_to_json(self):
        self.hero1.learn(self.spell)
        expected = {
            'name': 'Toni',
            'title': 'Pythonslayer',
            'mana_regeneration_rate': 25,
            'health': 250,
            'mana': 1000,
            'weapon': None,
            'spell': self.spell.to_json()
        }

        self.assertDictEqual(self.hero1.to_json(), expected)

    def test_from_json(self):
        self.hero1.equip(self.weapon)
        json_dict = {
            'name': 'Toni',
            'title': 'Pythonslayer',
            'mana_regeneration_rate': 25,
            'health': 250,
            'mana': 1000,
            'weapon': self.weapon.to_json(),
            'spell': None
        }

        self.assertEqual(self.hero1, Hero.from_json(json_dict))


if __name__ == '__main__':
    unittest.main()
