from hero import Hero
from enemy import Enemy
from exceptions import NotEquippedError, OutOfRangeError, HeroIsDeadError


class Fight:
    def __init__(self, *, dungeon, enemy_pos):
        self.dungeon = dungeon
        self.enemy = self.dungeon.inspect_pos(enemy_pos[0], enemy_pos[1])
        assert isinstance(self.enemy, Enemy)
        self.enemy_pos = enemy_pos

    def fight(self):
        print(f'A fight is started between our {self.dungeon.get_hero()} and {self.enemy}')
        while(True):
            if self.dungeon.get_hero().is_alive():
                self.player_makes_move(self.dungeon.get_hero())
            else:
                raise HeroIsDeadError("Hero is dead!Game over.")

            if self.enemy.is_alive():
                self.player_makes_move(self.enemy)
            else:
                print(f'Hero has: {self.dungeon._hero.get_health()} health left.')
                print("Enemy is dead!")
                return True

    def _direction_to_enemy(self, direction_vector=True):
        direction_x = self.enemy_pos[0] - self.dungeon._hero_pos[0]
        direction_y = self.enemy_pos[1] - self.dungeon._hero_pos[1]
        if direction_vector:
            if direction_x != 0:
                direction_x /= abs(direction_x)

            if direction_y != 0:
                direction_y /= abs(direction_y)

        return (direction_x, direction_y)

    def _range_between(self):
        range_pair = self._direction_to_enemy(direction_vector=False)
        return max(abs(range_pair[0]), abs(range_pair[1]))

    def player_makes_move(self, player):
        range_ = self._range_between()
        try:
            damage = player.make_better_attack(range_)
        except OutOfRangeError:
            print(f'{player.__class__.__name__} out of range.{player.__class__.__name__} moves')
            self.hero_move() if type(player) is Hero else self.enemy_move()
        except NotEquippedError:
            print("Hero cant attack")
        else:
            if type(player) is Hero:
                self.enemy.take_damage(damage)
                print(f'{player.__class__.__name__} deals {damage} dmg to enemy.')
            else:
                self.dungeon._hero.take_damage(damage)
                print(f'{player.__class__.__name__} deals {damage} dmg to hero.')

    def hero_move(self):
        direction = self._direction_to_enemy()
        for key, value in self.dungeon.directions.items():
            if value == direction:
                self.dungeon.move_hero(key)
                return True

        raise Exception("You should not be here")

    def enemy_move(self):
        direction = self._direction_to_enemy()
        direction = (- direction[0], - direction[1])
        for key, value in self.dungeon.directions.items():
            if value == direction:
                self.enemy_pos = self.dungeon.enemy_move(self.enemy_pos, key)
                return True

        raise Exception("You should not be here")
