import unittest
from dungeon import Dungeon
from enemy import Enemy
from weapon import Weapon
from spell import Spell
from hero import Hero


class TestsDungeon(unittest.TestCase):
    def setUp(self):
        self.spell = Spell(name="Fireball", damage=5, mana_cost=20, cast_range=1)
        self.weapon = Weapon(name="The Axe of Destiny", damage=10)
        self.hero = Hero(
            name="Bron",
            title="Dragonslayer",
            health=100,
            mana=100,
            mana_regeneration_rate=2
        )
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

        self.enemy1 = Enemy.from_json(self.enemies['2,5'])
        self.enemy2 = Enemy.from_json(self.enemies['2,9'])
        self.enemy3 = Enemy.from_json(self.enemies['3,2'])

        self.treasures = {
            "1,1": {
                "class": "Potion",
                "type": "mana",
                "amount": 50
            },
            "0,9": {
                "class": "Potion",
                "type": "health",
                "amount": 50
            },
            "4,3": {
                "class": "Weapon",
                "name": "The Axe of Destiny",
                "damage": 10
            },
            "4,5": {
                'class': "Spell",
                'name': 'Fireball',
                'damage': 5,
                'mana_cost': 20,
                'cast_range': 1
            }
        }

        self.tr1 = self.treasures['0,9']
        self.tr2 = self.treasures['1,1']
        self.tr3 = Weapon.from_json(self.treasures['4,3'])
        self.tr4 = Spell.from_json(self.treasures['4,5'])

        self.json_data = {
          "map": [
            "S.##.....T",
            "#T##..###.",
            "#.###E###E",
            "#.E...###.",
            "###T#T###G"
          ],
          "enemies": self.enemies,
          "treasures": self.treasures
        }

        self.dungeon = Dungeon(self.json_data)

    def test_init_adds_everything_on_the_map(self):
        expected_map = [['S', '.', '#', '#', '.', '.', '.', '.', '.', self.tr1],
                        ['#', self.tr2, '#', '#', '.', '.', '#', '#', '#', '.'],
                        ['#', '.', '#', '#', '#', self.enemy1, '#', '#', '#', self.enemy2],
                        ['#', '.', self.enemy3, '.', '.', '.', '#', '#', '#', '.'],
                        ['#', '#', '#', self.tr3, '#', self.tr4, '#', '#', '#', 'G']]

        self.assertEqual(self.dungeon._map, expected_map)
        self.assertEqual(self.dungeon._hero, None)
        self.assertEqual(self.dungeon._hero_pos, None)

    def test_get_map(self):
        expected = 'S.##.....T\n'\
                   '#T##..###.\n'\
                   '#.###E###E\n'\
                   '#.E...###.\n'\
                   '###T#T###G\n'
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

        expected = [['S', '.', '#', '#', '.', '.', '.', '.', '.', 'T'],
                    ['#', 'T', '#', '#', '.', '.', '#', '#', '#', '.'],
                    ['#', '.', '#', '#', '#', self.enemy1, '#', '#', '#', self.enemy2],
                    ['#', '.', self.enemy3, '.', '.', '.', '#', '#', '#', '.'],
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

    def test_add_treasures_raises_exception(self):
        self.dungeon._map = self.map
        with self.subTest('When the pos of a treasure is invalid!'):
            treasures = {
                "20,20": {
                    "class": "Potion",
                    "type": "mana",
                    "amount": 50
                }
            }
            with self.assertRaises(TypeError):
                self.dungeon.add_treasures(treasures)

        with self.subTest('When the pos of a treasure is not marked on the map with T!'):
            treasures = {
                "0,0": {
                    "class": "Potion",
                    "type": "mana",
                    "amount": 50
                }
            }
            with self.assertRaises(Exception):
                self.dungeon.add_treasures(treasures)

        with self.subTest('When an error occurs parsing the treasure!'):
            treasures = {
                "1,1": {
                    "class": "Chest",
                    "type": "mana",
                    "amount": 1000
                }
            }
            with self.assertRaises(Exception):
                self.dungeon.add_treasures(treasures)

    def test_add_treasures_adds_treasures_correctly(self):
        self.dungeon._map = self.map

        expected_map = [['S', '.', '#', '#', '.', '.', '.', '.', '.', self.tr1],
                        ['#', self.tr2, '#', '#', '.', '.', '#', '#', '#', '.'],
                        ['#', '.', '#', '#', '#', 'E', '#', '#', '#', 'E'],
                        ['#', '.', 'E', '.', '.', '.', '#', '#', '#', '.'],
                        ['#', '#', '#', self.tr3, '#', self.tr4, '#', '#', '#', 'G']]

        self.dungeon.add_treasures(self.treasures)

        self.assertEqual(self.dungeon._map, expected_map)

    def test_spawn_returns_False_when_there_is_no_spawning_point_on_the_map(self):
        self.dungeon._map[0][0] = '.'

        self.assertFalse(self.dungeon.spawn(self.hero))

    def test_spawn_spawns_hero_on_the_first_pos_marked_with_S(self):
        self.dungeon.spawn(self.hero)

        self.assertEqual(self.dungeon._map[0][0], self.hero)
        self.assertEqual(self.dungeon._hero, self.hero)
        self.assertEqual(self.dungeon._hero_pos, (0, 0))

    def test_move_hero_with_is_Fight_True_and_enemy_on_the_new_position(self):
        self.dungeon._map[1][5] = self.hero
        self.dungeon._hero = self.hero
        self.dungeon._hero_pos = (1, 5)
        self.dungeon.move_hero('down', True)

        self.assertEqual(self.dungeon._hero_pos, (2, 5))

    def test_move_hero_returns_False(self):
        self.dungeon.spawn(self.hero)

        with self.subTest('When trying to move outside the map!'):
            self.assertEqual(self.dungeon.move_hero('up'), False)

        with self.subTest('When trying to move in a wall!'):
            self.assertFalse(self.dungeon.move_hero('down'))

    def test_move_hero_returns_True_and_moves_hero_when_the_field_he_moves_on_is_free(self):
        self.dungeon.spawn(self.hero)

        self.assertTrue(self.dungeon.move_hero('right'))
        self.assertEqual(self.dungeon._map[0][0], '.')

    def test_move_hero_on_fied_with_treasure_opens_treasure(self):
        self.dungeon._hero = self.hero
        self.dungeon._hero_pos = (0, 8)
        self.dungeon._map[0][8] = self.hero
        self.dungeon._hero.take_damage(50)

        self.dungeon.move_hero('right')

        self.assertEqual(self.dungeon._hero.get_health(), 100)

    def test_enemy_move_throws_exception(self):
        with self.subTest('When there is no enemy on the given position'):
            with self.assertRaises(AssertionError):
                self.dungeon.enemy_move((1, 1), 'left')

        with self.subTest('When the enemy will move outside the map'):
            with self.assertRaises(Exception):
                self.dungeon.enemy_move((2, 9), 'right')

        with self.subTest('When the enemy will move in a wall'):
            with self.assertRaises(Exception):
                self.dungeon.enemy_move((2, 9), 'left')

    def test_enemy_move_moves_enemy(self):
        new_pos_of_enemy = self.dungeon.enemy_move((2, 9), 'up')

        self.assertEqual(new_pos_of_enemy, (1, 9))
        self.assertEqual(self.dungeon._map[2][9], '.')

    def test_hero_open_treasure(self):
        self.dungeon.spawn(self.hero)

        with self.subTest('When treasure is a health potion'):
            self.dungeon._hero.take_damage(50)
            self.assertEqual(self.dungeon._hero.get_health(), 50)
            self.dungeon.hero_open_treasure((0, 9))
            self.assertEqual(self.dungeon._hero.get_mana(), 100)

        with self.subTest('When treasure is a mana potion'):
            self.dungeon._hero.learn(self.spell)
            self.dungeon._hero.attack(by='spell')

            self.assertEqual(self.dungeon._hero.get_mana(), 80)
            self.dungeon.hero_open_treasure((1, 1))
            self.assertEqual(self.dungeon._hero.get_mana(), 100)

        with self.subTest('When treasure is a weapon'):
            self.dungeon.hero_open_treasure((4, 3))
            self.assertEqual(self.dungeon._hero.weapon, self.weapon)

        with self.subTest('When treasure is a spell'):
            self.dungeon.hero_open_treasure((4, 5))
            self.assertEqual(self.dungeon._hero.spell, self.spell)

    def test_attack_from_distance(self):
        self.dungeon._hero = self.hero
        self.dungeon._hero_pos = (3, 1)
        self.dungeon._map[3][1] = self.hero
        self.dungeon._hero.learn(self.spell)

        with self.subTest('attack empty space'):
            self.assertFalse(self.dungeon.attack_from_distance((-1, 0)))

        with self.subTest('attack a wall'):
            with self.assertRaises(Exception):
                self.dungeon.attack_from_distance((0, -1))

        with self.subTest('attack an enemy'):
            self.assertTrue(self.dungeon.attack_from_distance((0, 1)))

    def test_is_pos_on_the_map_returns_false(self):
        self.assertFalse(self.dungeon.is_pos_on_the_map(-1, -1))
        self.assertFalse(self.dungeon.is_pos_on_the_map(10, 1))

    def test_is_pos_on_the_map_returns_true(self):
        self.assertTrue(self.dungeon.is_pos_on_the_map(0, 0))
        self.assertTrue(self.dungeon.is_pos_on_the_map(4, 9))

    def test_inspect_pos_raises_Exception_when_given_pos_is_not_valid(self):
        with self.assertRaises(Exception):
            self.dungeon.inspect_pos(-1, 1)

    def test_inspect_pos_working_correctly(self):
        self.dungeon.spawn(self.hero)
        self.assertEqual(self.dungeon.inspect_pos(0, 0), self.hero)
        self.assertEqual(self.dungeon.inspect_pos(1, 0), '#')
        self.assertEqual(self.dungeon.inspect_pos(1, 1), self.tr2)
        self.assertEqual(self.dungeon.inspect_pos(2, 5), self.enemy1)
        self.assertEqual(self.dungeon.inspect_pos(0, 1), '.')


if __name__ == '__main__':
    unittest.main()
