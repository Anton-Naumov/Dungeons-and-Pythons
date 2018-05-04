from weapon import Weapon
from spell import Spell
from dungeon import Dungeon
from hero import Hero
from exceptions import YouWin


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
        self.name = 'Unnamed'

    def enter_name(self):
        name = input('Welcome to the game!\nPlease enter a username:')
        print('Great job!')
        self.name = name

    def setup_game(self):
        json_info = Dungeon.get_json_dict('levels/level01.json')
        self.hero = Hero(
            name=self.name,
            title=json_info["hero_title"],
            health=json_info['hero_health'],
            mana=json_info['hero_mana'],
            mana_regeneration_rate=json_info['mana_regeneration']
        )
        self.hero.equip(Weapon.from_json(json_info['hero_weapon']))
        self.hero.learn(Spell.from_json(json_info['hero_spell']))
        self.dungeon = Dungeon(json_info)
        self.dungeon.spawn(self.hero)

    def play(self):
        while(True):
            print(self.menu)
            self.dungeon.print_map()
            option = input('Choose an option:')
            while option not in self.options.keys():
                print('Invalid option! Try again.')
                option = input('Choose an option:')
            try:
                self.options[option](self)
            except YouWin as e:
                print(e)
                return
            except Exception as exc:
                print(exc)

    def option_attack_from_distance(self):
        direction = input('Enter a direction:')
        self.dungeon.attack_from_distance(direction)


def main():
    game_menu = GameMenu()
    game_menu.enter_name()
    game_menu.setup_game()
    game_menu.play()


if __name__ == '__main__':
    main()
