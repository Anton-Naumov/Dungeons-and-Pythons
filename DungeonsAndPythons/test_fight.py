import unittest
from weapon import Weapon
from spell import Spell
from dungeon import Dungeon
from hero import Hero
from enemy import Enemy
from fight import Fight
from exceptions import HeroIsDeadError


class FightTests(unittest.TestCase):
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
        self.map = [['.', '.', '#', '#', '.', 'S', '.', '.', '.', 'T'],
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

        self.json_data = {
          "map": self.map,
          "enemies": self.enemies,
          "treasures": self.treasures
        }

        self.dungeon = Dungeon(self.json_data)
        self.dungeon.spawn(self.hero)

        self.fight = Fight(dungeon=self.dungeon, enemy_pos=(2, 5))

    def test_init_initializing_correctly(self):
        self.assertEqual(self.fight.dungeon, self.dungeon)
        self.assertEqual(self.fight.enemy, Enemy.from_json(self.enemies['2,5']))
        self.assertEqual(self.fight.enemy_pos, (2, 5))

    def test_init_raises_Assertion_error_when_there_is_no_enemy_on_the_given_pos(self):
        with self.assertRaises(AssertionError):
            Fight(dungeon=self.dungeon, enemy_pos=(0, 1))

    def test__range_between(self):
        self.assertEqual(self.fight._range_between(), 2)

    def test__direction_to_enemy_without_arguments(self):
        with self.subTest('Hero is up from enemy'):
            self.assertEqual(self.fight._direction_to_enemy(), (1, 0))

        with self.subTest('Hero is down from enemy'):
            self.fight.dungeon._hero_pos = (3, 5)

            self.assertEqual(self.fight._direction_to_enemy(), (-1, 0))

    def test__direction_to_enemy_with_argument(self):
        self.fight.enemy_pos = (3, 2)
        with self.subTest('Hero is left from enemy'):
            self.fight.dungeon._hero_pos = (3, 1)
            self.assertEqual(self.fight._direction_to_enemy(False), (0, 1))

        with self.subTest('Hero is right from enemy'):
            self.fight.dungeon._hero_pos = (3, 5)

            self.assertEqual(self.fight._direction_to_enemy(False), (0, -3))

    def test_hero_move_moves_hero_on_the_map_towards_enemy(self):
        self.fight.hero_move()

        self.assertEqual(self.fight.dungeon._map[1][5], self.hero)

    def test_enemy_move_moves_enemy_on_the_map_towards_hero(self):
        self.fight.enemy_move()

        self.assertEqual(self.fight.dungeon._map[1][5], self.fight.enemy)
        self.assertEqual(self.fight.enemy_pos, (1, 5))

    def test_player_makes_move_one_of_the_players_move_when_hero_has_to_move(self):
        self.fight.player_makes_move(self.dungeon._hero)

        self.assertEqual(self.fight.dungeon._map[1][5], self.hero)

    def test_player_makes_move_one_of_the_players_move_when_enemy_has_to_move(self):
        self.fight.player_makes_move(self.fight.enemy)

        self.assertEqual(self.fight.dungeon._map[1][5], self.fight.enemy)

    def test_player_makes_move_hero_attacks(self):
        self.fight.dungeon._hero.learn(self.spell)
        self.fight.enemy_move()
        self.fight.player_makes_move(self.fight.dungeon._hero)

        self.assertEqual(self.fight.enemy.get_health(), 35)

    def test_player_makes_move_enemy_attacks(self):
        self.fight.hero_move()
        self.fight.player_makes_move(self.fight.enemy)

        self.assertEqual(self.fight.dungeon._hero.get_health(), 85)

    def test_fight(self):
        spell = Spell(name="Fireball", damage=20, mana_cost=4, cast_range=1)
        self.fight.dungeon._hero.learn(spell)
        print()
        self.fight.dungeon.print_map()
        self.fight.fight()

        self.assertEqual(self.fight.dungeon._hero.get_health(), 85)
        self.assertEqual(self.fight.dungeon._hero_pos, (1, 5))
        self.assertFalse(self.fight.enemy.is_alive())

    def test_fight_hero_is_dead(self):
        self.hero._health = 10
        with self.assertRaises(HeroIsDeadError):
            self.fight.fight()


if __name__ == '__main__':
    unittest.main()
