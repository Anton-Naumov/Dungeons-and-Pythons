import unittest
from dungeon import Dungeon
from enemy import Enemy
from weapon import Weapon
from spell import Spell


class TestsDungeon(unittest.TestCase):
    def setUp(self):
        self.spell = Spell(name="Fireball", damage=5, mana_cost=20, cast_range=1)
        self.weapon = Weapon(name="The Axe of Destiny", damage=10)
        self.map = [['S', '.', '#', '#', '.', '.', '.', '.', '.', 'T'],
                    ['#', 'T', '#', '#', '.', '.', '#', '#', '#', '.'],
                    ['#', '.', '#', '#', '#', 'E', '#', '#', '#', 'E'],
                    ['#', '.', 'E', '.', '.', '.', '#', '#', '#', '.'],
                    ['#', '#', '#', 'T', '#', 'T', '#', '#', '#', 'G']]

        self.enemies = {
            "2,5": {
                "damage": 10,
                "health": 40,
                "mana": 20,
                "weapon": None,
                "spell": self.spell.to_json()
            },
            "2,9": {
                "damage": 10,
                "health": 40,
                "mana": 20,
                "weapon": self.weapon.to_json(),
                "spell": None
            },
            "3,2": {
                "damage": 10,
                "health": 40,
                "mana": 20,
                "weapon": None,
                "spell": None
            }
          }

        self.treasures = {
            "1,1": {
                "class": "Potion",
                "type": "health",
                "amount": 50
            },
            "3,6": {
                "class": "Potion",
                "type": "mana",
                "amount": 50
            },
            "4,3": {
                "class": "Weapon",
                "name": "Small Axe",
                "damage": 10
            },
            "4,6": {
                'class': "Spell",
                'name': 'Fireball',
                'damage': 30,
                'mana_cost': 50,
                'cast_range': 2
            }
        }

        self.json_data = {
          "map": [
            "S.##.....T",
            "#T##..###.",
            "#.###E###E",
            "#.E...T##.",
            "###T##T##G"
          ],
          "enemies": self.enemies,
          "treasures": self.treasures
        }

        self.dungeon = Dungeon(self.json_data)

    def test_get_map(self):
        expected = 'S.##.....T'\
                   '#T##..###.'\
                   '#.###E###E'\
                   '#.E...###.'\
                   '###T#T###G'
        self.dungeon._map = self.map

        self.assertEqual(self.dungeon.get_map(), expected)

    def test_extract_pos_raises_TypeError(self):
        self.dungeon._map = self.map
        with self.subTest('When given string\'s format is not "digits,digits"'):
            with self.assertRaises(TypeError):
                self.dungeon.extract_pos('abc')

        with self.subTest('When the given coordinates are outsite the map!'):
            with self.assertRaises(TypeError):
                self.dungeon.extract_pos('-1,5')
            with self.assertRaises(TypeError):
                self.dungeon.extract_pos('1,-5')
            with self.assertRaises(TypeError):
                self.dungeon.extract_pos('10,1')
            with self.assertRaises(TypeError):
                self.dungeon.extract_pos('1,15')

    def test_extract_pos_returns_correct_pos(self):
        self.dungeon._map = self.map

        self.assertEqual(self.dungeon.extract_pos('1,1'), (1, 1))
        self.assertEqual(self.dungeon.extract_pos('0,0'), (0, 0))
        self.assertEqual(self.dungeon.extract_pos('4,9'), (4, 9))
        self.assertEqual(self.dungeon.extract_pos('2,3'), (2, 3))

    def test_add_enemies_raises_exception(self):
        self.dungeon._map = self.map

        with self.subTest('When pos of an enemy is invalid!'):
            enemies = {
                "abc": {
                  "deamage": 10,
                  "health": 40,
                  "mana": 20,
                  "weapon": None,
                  "spell": None
                }
            }

            with self.assertRaises(TypeError):
                self.dungeon.add_enemies(enemies)

        with self.subTest('When pos is not marked with \"E\" on the map!'):
            enemies = {
                "0,1": {
                  "damage": 10,
                  "health": 40,
                  "mana": 20,
                  "weapon": None,
                  "spell": None
                }
            }

            with self.assertRaises(Exception):
                self.dungeon.add_enemies(enemies)

        with self.subTest('When an error occurs parsing an enemy! (Enemy with no damage)'):
            enemies = {
                "2,5": {
                  "health": 40,
                  "mana": 20,
                  "weapon": None,
                  "spell": None
                }
            }

            with self.assertRaises(ValueError):
                self.dungeon.add_enemies(enemies)

    def test_add_enemies_adds_enemies_correctly(self):
        self.dungeon._map = self.map
        self.dungeon.add_enemies(self.enemies)
        enemy1 = Enemy.from_json(self.enemies['2,5'])
        enemy2 = Enemy.from_json(self.enemies['2,9'])
        enemy3 = Enemy.from_json(self.enemies['3,2'])

        expected = [['S', '.', '#', '#', '.', '.', '.', '.', '.', 'T'],
                    ['#', 'T', '#', '#', '.', '.', '#', '#', '#', '.'],
                    ['#', '.', '#', '#', '#', enemy1, '#', '#', '#', enemy2],
                    ['#', '.', enemy3, '.', '.', '.', '#', '#', '#', '.'],
                    ['#', '#', '#', 'T', '#', 'T', '#', '#', '#', 'G']]

        self.assertEqual(self.dungeon._map, expected)

    def test_extract_treasure_returns_correct_object(self):
        with self.subTest('With weapon'):
            w_dict = {
              "class": "Weapon",
              "name": "The Axe of Destiny",
              "damage": 10
            }

            self.assertEqual(self.dungeon.extract_treasure(w_dict), self.weapon)

        with self.subTest('With spell'):
            s_dict = {
              "class": "Spell",
              "name": "Fireball",
              "damage": 5,
              "mana_cost": 20,
              "cast_range": 1
            }

            self.assertEqual(self.dungeon.extract_treasure(s_dict), self.spell)

        with self.subTest('With health or mana potion'):
            health_potion = {
              "class": "Potion",
              "type": "mana",
              "amount": 50
            }

            self.assertEqual(self.dungeon.extract_treasure(health_potion), health_potion)

            mana_potion = {
              "class": "Potion",
              "type": "mana",
              "amount": 50
            }

            self.assertEqual(self.dungeon.extract_treasure(mana_potion), mana_potion)

    def test_extract_treasure_raises_exception_on_invalid_class(self):
        invalid_class_dict = {
            'class': 'Computer'
        }

        with self.assertRaises(Exception):
            self.dungeon.extract_treasure(invalid_class_dict)


if __name__ == '__main__':
    unittest.main()
