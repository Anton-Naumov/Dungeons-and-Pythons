from hero import Hero
from exceptions import NotEquippedError, OutOfRangeError


class Fight:
    def __init__(self, *, dungeon, enemy, enemy_pos):
        self.dungeon = dungeon

    @property
    def hero(self):
        return self.dungeon._hero

    @property
    def enemy(self):
        return self.dungeon._enemy

    def fight(self):
        print(f'A fight is started between our {self.hero} and {self.enemy}')
        # TODO:Enemy has to move near hero
        while(True):
            if self.hero.is_alive():
                self.player_makes_move(self.hero)
            else:
                print("Hero is dead!Game over.")
                return False

            if self.enemy.is_alive():
                self.player_makes_move(self.enemy)
            else:
                print("Enemy is dead!")
                return True

    def direction_to_enemy(self, direction_vector=True):
        direction_x = self.dungeon.hero_pos[0] - self.enemy_pos[0]
        if direction_vector:
            if direction_x != 0:
                direction_x /= abs(direction_x)

            direction_y = self.hero_pos[1] - self.enemy_pos[1]
            if direction_y != 0:
                direction_y /= abs(direction_y)

        return (direction_x, direction_y)

    def range_between(self):
        range_pair = self.direction_to_enemy(direction_vector=False)
        return max(abs(range_pair[0]), abs(range_pair[1]))

    def player_makes_move(self, player):
        range_ = self.range_between()
        try:
            damage = self.player.make_better_attack(range_)
        except OutOfRangeError:
            print(f'{player.__class__.__name__} out of range.{player.__class__.__name__} moves')
            self.hero_move() if type(player) is Hero else self.enemy_move()
        except NotEquippedError:
            print("Hero cant attack")
        else:
            self.enemy.take_damage(damage)
            print(f'{player.__class__.__name__} deals {damage} dmg to enemy.')

    def hero_move(self):
        direction = self.direction_to_enemy()
        for key, value in self.dungeon.directions:
            if value == direction:
                self.dungeon.move_hero(key)
                return True

        raise Exception("You should not be here")

    def enemy_move(self):
        direction = self.direction_to_enemy()
        direction = (- direction[0], - direction[1])
        for key, value in self.dungeon.directions:
            if value == direction:
                self.enemy_pos = self.dungeon.enemy_move(self.enemy_pos, key)
                return True

        raise Exception("You should not be here")

    def hero_attack_with_better_weapon(self):
        try:
            return self.hero.pick_better_tool_to_fight()
        except NotEquippedError as exc:
            print(exc)
            return None

    def hero_attacks(self):
        attack_tool = self.hero_attack_with_better_weapon()
        damage = self.hero.attack(by=attack_tool)
        if attack_tool == 'spell':
            print(f'Hero casts {self.hero.spell},hits enemy for {damage} dmg', end='')

        if attack_tool == 'weapon':
            print(f'Hero hits with {self.hero.weapon} for {damage} dmg', end='')
        return damage
