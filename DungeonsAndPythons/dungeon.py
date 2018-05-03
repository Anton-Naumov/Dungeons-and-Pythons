import json
from enemy import Enemy
from weapon import Weapon
from spell import Spell
from fight import Fight


class Dungeon:
    def __init__(self, json_info):
        self._map = [list(line) for line in json_info["map"]]
        self.add_enemies(json_info["enemies"])
        self.add_treasures(json_info["treasures"])
        self._hero = None
        self._hero_pos = None

    def get_map(self):
        string = []

        for line in self._map:
            string.append(''.join(line))

        return "".join(string)

    def print_map(self):
        print(self.get_map())

    def spawn(self, hero):
        for row in range(len(self._map)):
            for col in range(len(self._map[row])):
                if str(self._map[row][col]) == 'S':
                    self._map[row][col] = hero
                    self._hero = hero
                    self._hero_pos = (row, col)
                    return True
        return False

    directions = {
        'left': (0, -1),
        'right': (0, 1),
        'down': (1, 0),
        'up': (-1, 0)
    }

    def move_hero(self, direction):
        new_pos_x = self._hero_pos[0] + self.directions[direction][0]
        new_pos_y = self._hero_pos[1] + self.directions[direction][1]

        if self._map[new_pos_x][new_pos_y] == '#' or new_pos_x < 0 or new_pos_y < 0 or\
           new_pos_x >= len(self._map) or new_pos_y >= len(self._map[0]):
            return False
        elif self._map[new_pos_x][new_pos_y] == '.':
            self._map[self._hero_pos[0]][self._hero_pos[1]] = '.'
            self._map[new_pos_x][new_pos_y] = self._hero
            self._hero_pos = new_pos_x, new_pos_y
        elif isinstance(self._map[new_pos_x][new_pos_y], Enemy):
            Fight(self, self._map[new_pos_x][new_pos_y], (new_pos_x, new_pos_y)).fight()
        else:  # treasure
            self.hero_open_treasure((new_pos_x, new_pos_y))
        return True

    def enemy_move(self, enemy_pos, direction):
        new_pos_x = enemy_pos[0] + self.directions[direction][0]
        new_pos_y = enemy_pos[1] + self.directions[direction][1]

        assert isinstance(self._map[enemy_pos[0]][enemy_pos[1]], Enemy)

        if self._map[new_pos_x][new_pos_y] == '#' or new_pos_x < 0 or new_pos_y < 0 or\
           new_pos_x >= len(self._map) or new_pos_y >= len(self._map[0]):
            raise Exception('Enemy can\'t step there!')

        self._map[new_pos_x][new_pos_y] = self._map[enemy_pos[0]][enemy_pos[1]]
        self._map[enemy_pos[0]][enemy_pos[1]] = '.'
        return new_pos_x, new_pos_y

    def hero_open_treasure(self, pos_of_treasure):
        treasure = self._map[pos_of_treasure[0]][pos_of_treasure[1]]
        if type(treasure) is dict:
            if treasure['type'] == 'health':
                self._hero.take_healing(treasure['amount'])
            elif treasure['type'] == 'mana':
                self._hero.take_mana(treasure['amount'])
        elif type(treasure) is Weapon:
            self._hero.equip(treasure)
        elif type(treasure) is Spell:
            self._hero.learn(treasure)
        else:
            raise Exception('No treasure on that pos!')

    def add_enemies(self, enemies):
        for pos_str, enemy_dict in enemies.items():
            pos = self.extract_pos(pos_str)

            if self._map[pos[0]][pos[1]] != 'E':
                raise Exception('No enemy on pos ({}, {}) on the map!'.format(pos[0], pos[1]))

            try:
                self._map[pos[0]][pos[1]] = Enemy.from_json(enemy_dict)
            except Exception as e:
                raise ValueError('Error parsing enemy on pos ({}, {})!'.format(pos[0], pos[1]))

    def add_treasures(self, treasures):
        for pos_str, treasure_dict in treasures.items():
            pos = self.extract_pos(pos_str)

            if self._map[pos[0]][pos[1]] != 'T':
                raise Exception('No T on pos ({}, {}) on the map!'.format(pos[0], pos[1]))

            try:
                self._map[pos[0]][pos[1]] = self.extract_treasure(treasure_dict)
            except Exception as e:
                raise ValueError('Error parsing T on pos ({}, {})!'.format(pos[0], pos[1]))

    def extract_treasure(self, treasure_dict):
        if treasure_dict["class"] == 'Weapon':
            return Weapon.from_json(treasure_dict)

        if treasure_dict["class"] == 'Spell':
            return Spell.from_json(treasure_dict)

        if treasure_dict["class"] == 'Potion':
            return treasure_dict

        raise Exception('Invalid treasure_dict!')

    def extract_pos(self, string_with_pos):
        parts = string_with_pos.split(',')
        if len(parts) != 2 or parts[0].isdigit() is False or parts[1].isdigit() is False:
            raise TypeError('Invalid pos for enemy!')

        x, y = int(parts[0]), int(parts[1])
        if (x < 0 or x >= len(self._map)) or\
           ((len(self._map) > 0) and (y < 0 or y > len(self._map[0]))):
            raise TypeError('Invalid pos for enemy!')

        return x, y

    @staticmethod
    def get_json_dict(file_name):
        with open(file_name, 'r') as f:
            json_dict = json.load(f)
        return json_dict


if __name__ == '__main__':
    dungeon = Dungeon(Dungeon.get_json_dict('levels/level01.json'))
