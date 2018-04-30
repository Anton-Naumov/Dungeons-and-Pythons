import json
from enemy import Enemy
from weapon import Weapon
from spell import Spell


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
