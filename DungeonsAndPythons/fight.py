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

    @property
    def hero(self):
        return self._hero

    @property
    def enemy(self):
        return self._enemy

    def fight(self):
        print(f'A fight is started between our {self._hero} and {self._enemy}')
        # TODO:Enemy has to move near hero
        while(True):
            if self.hero.is_alive():
                damage = self.hero_attacks()
                self.enemy.take_damage(damage)
                print(f'Enemy health is {self.enemy.get_health()}')
            else:
                print("Hero is dead!Game over.")
                return False

            if self.enemy.is_alive():
                damage = self.enemy_attacks()
                self.hero.take_damage(damage)
                print(f'Hero health is {self.hero.get_health()}')
            else:
                print("Enemy is dead!")
                return True

    def hero_choose_better_attack(self):
        try:
            return self.hero.pick_better_tool_to_fight()
        except NotEquippedError as exc:
            print(exc)
            return None

    def hero_attacks(self):
        attack_tool = self.hero_choose_better_attack()
        damage = self.hero.attack(by=attack_tool)
        if attack_tool == 'spell':
            print(f'Hero casts {self.hero.spell},hits enemy for {damage} dmg', end='')

        if attack_tool == 'weapon':
            print(f'Hero hits with {self.hero.weapon} for {damage} dmg', end='')
        return damage
