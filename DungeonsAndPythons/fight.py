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
            if(self._hero.is_alive()):
                self.hero_attacks()
            else:
                print("You are dead!Game over.")
            if(self._enemy.is_alive()):
                self.enemy_attacks()
            else:
                print("Enemy is dead!")

    def hero_choose_better_attack(self):
        try:
            return self._hero.pick_better_tool_to_fight()
        except Exception:
            return None

    def hero_attacks(self):
        attack_tool = self.hero_choose_better_attack()
        if attack_tool is None:
            return self._hero.attack()
        elif attack_tool == 'spell':
            return self._hero.attack(by='spell')
        return self._hero.attack(by='weapon')
