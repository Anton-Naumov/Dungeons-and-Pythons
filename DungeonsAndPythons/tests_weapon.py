import unittest
from weapon import Weapon


class TestsWeapon(unittest.TestCase):
    def setUp(self):
        self.weapon = Weapon(name="The Axe of Destiny", damage=20)

    def test_eq_(self):
        with self.subTest('Returns false when damages don\'t match'):
            weapon1 = Weapon(name="The Axe of Destiny", damage=50)

            self.assertNotEqual(self.weapon, weapon1)

        with self.subTest('Returns false when names don\'t match'):
            weapon1 = Weapon(name="Sword", damage=20)

            self.assertNotEqual(self.weapon, weapon1)

        with self.subTest('Returns true when both args match'):
            weapon1 = Weapon(name="The Axe of Destiny", damage=20)

            self.assertEqual(self.weapon, weapon1)

    def test_to_json(self):
        expected = {
            'class': 'Weapon',
            'name': 'The Axe of Destiny',
            'damage': 20
        }

        self.assertDictEqual(self.weapon.to_json(), expected)

    def test_from_json(self):
        json_string = {
            'class': 'Weapon',
            'name': 'The Axe of Destiny',
            'damage': 20
        }

        self.assertEqual(Weapon.from_json(json_string), self.weapon)


if __name__ == '__main__':
    unittest.main()
