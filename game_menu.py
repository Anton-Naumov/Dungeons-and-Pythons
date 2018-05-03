from dungeon import Dungeon
from hero import Hero


class GameMenu:
    options = {
        '1': lambda inst: inst.dungeon.move_hero('left'),
        '2': lambda inst: inst.dungeon.move_hero('right'),
        '3': lambda inst: inst.dungeon.move_hero('up'),
        '4': lambda inst: inst.dungeon.move_hero('down'),
        '5': lambda inst: inst.option_attack_from_distance()
    }

    menu = """
                1)Move left
                2)Move right
                3)Move up
                4)Move down
                5)Attack from distance in some way
    """

    def __init__(self):
        self.dungeon = None
        self.hero = None
        self.name = None

    def enter_name(self):
        name = input('Welcome to the game!Please enter a username')
        print('Great job!')
        self.name = name

    def setup_game(self):
        json_info = Dungeon.get_json_dict('levels/level01.json')
        self.hero = Hero(
            self.name,
            json_info["hero_title"],
            json_info['hero_health'],
            json_info['hero_mana'],
            json_info['hero_mana_regeneration']
        )
        self.hero.equip(json_info['hero_weapon'])
        self.hero.learn(json_info['hero_spell'])
        self.dungeon = Dungeon(json_info)
        self.dungeon.spawn(self.hero)

    def play(self):
        while(True):
            print(self.menu)
            option = input('Choose an option:')
            try:
                self.options[option](self)
            except Exception:
                print('Game Over!')
                return

    def option_attack_from_distance(self):
        direction = input('Enter a direction')
        self.dungeon.attack_from_distance(direction)


def main():
    menu = GameMenu()
    menu.enter_name()
    menu.setup_game()
    menu.play()


if __name__ == "__main__":
    main()
