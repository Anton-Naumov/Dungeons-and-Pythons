from weapon import Weapon
from spell import Spell
from dungeon import Dungeon
from hero import Hero
from exceptions import YouWin, HeroIsDeadError


class GameMenu:
    options = {
        '1': lambda inst: inst.dungeon.move_hero('left'),
        '2': lambda inst: inst.dungeon.move_hero('right'),
        '3': lambda inst: inst.dungeon.move_hero('up'),
        '4': lambda inst: inst.dungeon.move_hero('down'),
        '5': lambda inst: inst.option_attack_from_distance()
    }
    levels = """
        level01
        level02
    """
    menu = """
    1)Move left
    2)Move right
    3)Move up
    4)Move down
    5)Attack from distance in some way
    6)Quit game
    """

    def __init__(self):
        self.dungeon = None
        self.hero = None
        self.name = 'Unnamed'

    def enter_name(self):
        name = input('Welcome to the game!\nPlease enter a username:')
        print('Great job!')
        self.name = name

    def choose_level(self):
        import re
        pattern = re.compile("level0[1-2]")
        print(self.levels)
        level_name = input("Choose a level of the game\n:")
        while(not pattern.match(level_name)):
            print(self.levels)
            level_name = input("Please enter correct level\n:")

        return Dungeon.get_json_dict(f'levels/{level_name}.json')

    def setup_game(self):
        level = self.choose_level()

        self.hero = Hero(
            name=self.name,
            title=level["hero_title"],
            health=level['hero_health'],
            mana=level['hero_mana'],
            mana_regeneration_rate=level['mana_regeneration']
        )
        self.hero.equip(Weapon.from_json(level['hero_weapon']))
        self.hero.learn(Spell.from_json(level['hero_spell']))
        self.dungeon = Dungeon(level)
        self.dungeon.spawn(self.hero)

    def play(self):
        while(True):
            print(self.menu)
            print(f'{self.dungeon._hero}\n')
            self.dungeon.print_map()
            option = input('Choose an option:')
            print()
            if option == '6':
                return
            while option not in self.options.keys():
                print('Invalid option! Try again.')
                option = input('Choose an option:')
            try:
                self.options[option](self)
            except YouWin as e:
                print(e)
                return
            except HeroIsDeadError as e:
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
