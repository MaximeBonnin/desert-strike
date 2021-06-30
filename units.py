import pygame
import os
import desert_strike as ds

UNITS = []
UNIT_COPIES = []
BLOOD_IMG = pygame.image.load(os.path.join("images", "blood.png"))

class Unit:
    def __init__(self, x, y, type, faction, is_ghost, FIELD_list):
        self.x = x+ds.padding
        self.y = y+ds.padding
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        if is_ghost == False:
            self.on_tile(FIELD_list)
        self.color = ds.COLORS["green"]
        self.type = type
        self.speed = self.type["speed"]
        self.attack = self.type["attack"]
        self.hp = self.type["hp"]
        self.max_hp = self.type["max_hp"]
        self.sound = self.type["sound"]
        self.faction = faction  # 1 is top player cuz its easier rn
        self.range = self.type["range"]
        self.range_rect = pygame.Rect(self.x-self.range*32, self.y-self.range*32, 32*(1+self.range*2), 32*(1+self.range*2))
        self.is_ghost = is_ghost
        self.aggro_range = 5  # shit how do I do any of this
        self.find_img()
        if self.is_ghost:
            self.img.set_alpha(100)
            UNITS.append(self)
        elif not self.is_ghost:
            UNIT_COPIES.append(self)
        else:
            print("This should not happen")

    def hp_bar(self):
        text = f"HP: {self.hp}/{self.max_hp}"
        text_img = ds.NORMAL_FONT.render(text, True, ds.COLORS["green"])
        hp_bar = pygame.surface.Surface((text_img.get_width(), text_img.get_height()))
        hp_bar.fill(ds.COLORS["white"])
        hp_bar.blit(text_img, (0, 0))
        return hp_bar

    def find_img(self):
        img = pygame.image.load(os.path.join("images", "units", f"{self.type['name']}{self.faction}.png"))
        self.img = pygame.transform.scale(img, (32, 32))
        if self.is_ghost:
            self.img.set_alpha(100)

    def update_rects(self):
        self.rect.update(self.x, self.y, 32, 32)
        self.range_rect.update(self.x - self.range*32, self.y - self.range*32, 32 * (1 + self.range * 2),
                               32 * (1 + self.range * 2))

    def on_tile(self, FIELD_list):
        for row in FIELD_list:
            for tile in row:
                if self.rect.colliderect(tile.rect):
                    tile.change_has_unit(self)
                    self.tile = tile
                    return self.tile

    def mouseover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        else:
            return False

    def die(self):
        self.is_ghost = True
        self.img = pygame.transform.scale(BLOOD_IMG, (32, 32))
        self.img.set_colorkey(ds.COLORS["black"])
        self.tile.change_has_unit(self)
        print(f"{self.type['name']} died.")
        if self.type["name"] is "tower":
            if self.faction == 1:
                print("Player 2 wins!")
            else:
                print("Player 1 wins!")
            pygame.event.Event(ds.win_event)

    def attack_target(self, target):
        print(f"{self.type['name']} attacking {target.type['name']} ({target.hp}/{target.max_hp})")
        target.hp -= self.attack
        if target.hp <= 0:
            target.die()
            sound = self.sound
            sound.set_volume(0.1)
            sound.play()

    def can_attack(self):
        for target in UNIT_COPIES:
            if target != self and target.faction != self.faction:
                if self.range_rect.colliderect(target.rect) and not target.is_ghost:
                    return target
        return False  # should return target if yes and False if no

    def can_move(self, FIELD_list):
        # l_bound = 0+padding, r_bound = 32*10+padding, u_bound = 0+padding, lw_bound = 16*32
        options = []
        if self.faction == 1 and self.y < 13*32+ds.padding:
            front = (self.x, self.y + 32)
            options.append(front)
        elif self.faction == 2 and self.y > 3*32+ds.padding:
            front = (self.x, self.y - 32)
            options.append(front)
        else:
            pass
        if self.x < 32*10+ds.padding:
            right = (self.x+32, self.y)
            options.append(right)
        if self.x > 0 + ds.padding:
            left = (self.x-32, self.y)
            options.append(left)

        for opt in options:
            for row in FIELD_list:
                for tile in row:
                    if not tile.has_unit and tile.rect.collidepoint(opt):
                        return opt
        return False

    def move(self, FIELD_list):
        old_tile = self.tile
        self.x, self.y = self.can_move(FIELD_list)  # should not have errors, cuz doesnt get called when empty
        self.update_rects()
        self.tile = self.on_tile(FIELD_list)
        old_tile.change_has_unit(self)

    def act(self, FIELD_list):
        if self.is_ghost == False:  # should only be called on non-ghost anyway
            if self.can_attack():
                self.attack_target(self.can_attack())

            elif self.can_move(FIELD_list) and self.speed:
                self.move(FIELD_list)
        else:
            pass

def draw_units(field):
    for unit in UNITS:
        field.blit(unit.img, (unit.x, unit.y))

    for copy in UNIT_COPIES:
        if copy.mouseover():
            # pygame.draw.rect(field, ds.COLORS["red"], copy.range_rect)
            # pygame.draw.rect(field, ds.COLORS["green"], copy.rect)
            field.blit(copy.img, (copy.x, copy.y))
            field.blit(copy.hp_bar(), (copy.rect.centerx-copy.hp_bar().get_width()//2,
                                       copy.y-copy.hp_bar().get_height()))
        else:
            field.blit(copy.img, (copy.x, copy.y))
