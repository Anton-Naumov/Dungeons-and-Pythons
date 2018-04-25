class Fight:
    def __init__(
            self,
            *,
            hero,
            hero_pos,
            enemy,
            enemy_pos,
            dungeon_map
    ):
        self._hero = hero
        self._hero_pos = hero_pos
        self._enemy = enemy
        self._enemy_pos = enemy_pos
        self._dungeon_map = dungeon_map

    def fight(self):
        while(self._hero.is_alive() and self._enemy.is_alive()):
            attack_type = self.hero_choose_better_attack()
            if attack_type is None:
                print('Hero hasnt equiped anything!')
            else:
                pass

    def hero_choose_better_attack(self):
        try:
            return self._hero.pick_better_tool_to_fight()
        except Exception as exc:
            print(exc)
            return None

    def hero_attacks(self):
        pass
