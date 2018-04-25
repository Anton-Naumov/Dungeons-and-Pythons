import unittest
from hero import Hero
from spell import Spell
from weapon import Weapon


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

    def test_attack_returns_0(self):
        with self.subTest('when by == weapon and hero\'s weapon is None'):
            self.assertEqual(self.hero1.attack(by='weapon'), 0)

        with self.subTest('when by == spell and hero\'s spell is None'):
            self.assertEqual(self.hero1.attack(by='spell'), 0)

        with self.subTest('when by is not \'weapon\' or \'spell\''):
            self.assertEqual(self.hero1.attack(by='foot'), 0)

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


if __name__ == '__main__':
    unittest.main()
