import unittest
from hero import Hero


class TestsHero(unittest.TestCase):
    def setUp(self):
        self.hero1 = Hero(
                            name='Toni',
                            title='Pythonslayer',
                            health=250,
                            mana=1000,
                            mana_regeneration_rate=25,
                            pos=(1, 1)
        )

        self.hero2 = Hero(
                            name="Bron",
                            title="Dragonslayer",
                            health=100,
                            mana=100,
                            mana_regeneration_rate=2
        )

    def test_init_working_correctly(self):
        with self.subTest('hero1'):
            self.assertEqual(self.hero1._name, 'Toni')
            self.assertEqual(self.hero1._title, 'Pythonslayer')
            self.assertEqual(self.hero1._health, 250)
            self.assertEqual(self.hero1._max_health, 250)
            self.assertEqual(self.hero1._mana, 1000)
            self.assertEqual(self.hero1._max_mana, 1000)
            self.assertEqual(self.hero1._mana_regeneration_rate, 25)
            self.assertEqual(self.hero1._pos, (1, 1))
            self.assertEqual(self.hero1._weapon, None)
            self.assertEqual(self.hero1._spell, None)

        with self.subTest('hero2 (no pos given in the constructor)'):
            self.assertEqual(self.hero2._pos, (0, 0))

    def test_known_as(self):
        with self.subTest('hero1'):
            self.assertEqual(self.hero1.known_as(), 'Toni the Pythonslayer')

        with self.subTest('hero2'):
            self.assertEqual(self.hero2.known_as(), 'Bron the Dragonslayer')

    def test_can_cast(self):
        with self.subTest('spell is None'):
            self.assertFalse(self.hero1.can_cast())

        # add test when mana is not enough

        # add test when can_cast is true

    def test_attack_raises_exception(self):
        with self.subTest('when by == weapon and hero\'s weapon is None'):
            with self.assertRaises(
                                      Exception,
                                      msg='The hero must have a weapon to attack with it!'
            ):
                self.hero1.attack(by='weapon')

        with self.subTest('when by == spell and hero\'s spell is None'):
            with self.assertRaises(
                                      Exception,
                                      msg='The hero must have a weapon to attack with it!'
            ):
                self.hero1.attack(by='spell')

        with self.subTest('when by is not \'weapon\' or \'spell\''):
            with self.assertRaises(
                                      Exception,
                                      msg='Invalid argument \'by={by}\''
            ):
                self.hero1.attack(by='foot')

    # add more tests for attack


if __name__ == '__main__':
    unittest.main()
