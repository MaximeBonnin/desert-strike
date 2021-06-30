import pygame
import os
from random import randint
from units import *
# from buttons import *

COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "gray": (225, 225, 225),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "dark gray": (25, 25, 25),
    "light blue": (173, 216, 230),
}

win_w, win_h = 600, 600
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(os.path.join("sounds", "epic_music.mp3"))
window = pygame.display.set_mode((win_w, win_h))
padding = 10
BUTTONS = []
FIELD = []
TILES = {
    "stone": pygame.image.load(os.path.join("images", "map tiles", f"stone_tile.png")),
    "sand": pygame.image.load(os.path.join("images", "map tiles", f"sand_tile.png"))
}
NORMAL_FONT = pygame.font.SysFont(None, 25)


one_sec_event = pygame.USEREVENT + 0
round_start_event = pygame.USEREVENT + 1
win_event = pygame.USEREVENT + 2
SOUNDS = {
    "slash": pygame.mixer.Sound(os.path.join("sounds", "slash.mp3")),
    "trumpet": pygame.mixer.Sound(os.path.join("sounds", "trumpet.mp3")),
    "cannon": pygame.mixer.Sound(os.path.join("sounds", "cannon.mp3")),
    "arrow": pygame.mixer.Sound(os.path.join("sounds", "arrow.mp3")),
    "marching": pygame.mixer.Sound(os.path.join("sounds", "marching.mp3"))
}
#TODO maybe make this into a json?
UNIT_TYPES = {
    "melee": {
        "name": "melee",
        "speed": 1,
        "range": 1,
        "attack": 1,
        "attack_speed": 2,
        "max_hp": 5,
        "hp": 5,
        "sound": SOUNDS["slash"]
    },
    "archer": {
        "name": "archer",
        "speed": 1,
        "range": 2,
        "attack": 1,
        "attack_speed": 2,
        "max_hp": 2,
        "hp": 2,
        "sound": SOUNDS["arrow"]
    },
    "tower": {
        "name": "tower",
        "speed": 0,
        "range": 3,
        "attack": 2,
        "attack_speed": 1,
        "max_hp": 50,
        "hp": 50,
        "sound": SOUNDS["cannon"]
    }
}


class Button:
    def __init__(self, x, y, surface, offset, purpose=(1, "spawn", "melee")):
        self.purpose = purpose
        self.surface = surface
        self.x = x
        self.y = y
        self.w = surface.get_width() - 2*padding
        self.h = 32
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.g_rect = pygame.Rect(self.x +offset[0], self.y +offset[1], 100, 32)
        # img = pygame.image.load(os.path.join("images", "units", f"{purpose[2]}{purpose[0]}.png"))
        # self.img = pygame.transform.scale(img, (32, 32))
        self.color = COLORS["black"]
        self.text = f"Spawn {purpose[2]}"
        self.title = NORMAL_FONT.render(self.text, True, COLORS["white"])

        BUTTONS.append(self)
        pygame.draw.rect(self.surface, self.color, self.rect)

    def clicked(self):
        out_of_frame = - 100
        return Unit(32*out_of_frame, 32*out_of_frame, UNIT_TYPES[self.purpose[2]],
                    self.purpose[0], is_ghost=True, FIELD_list=FIELD)

    def mouseover(self):
        if self.g_rect.collidepoint(pygame.mouse.get_pos()):
            self.color = COLORS["dark gray"]
            return True
        else:
            self.color = COLORS["black"]
            return False

def make_buttons(surface, x_y_offset=(0, 0)):
    index = 0
    for i in UNIT_TYPES.keys():
        if i != "tower":
            Button(padding, padding + index*(32+padding),
                   surface, x_y_offset, purpose=(1, "spawn", i))
            index += 1

class Tile:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col*32+padding
        self.y = row*32+padding
        self.w, self.h = 32, 32
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.has_unit = False
        self.color = COLORS["blue"]
        self.is_spawn = False
        self.check_is_spawn()
        self.find_img()

    def check_is_spawn(self):
        # TODO make this not have hardcoded field len
        if self.row in [0, 1, 2]:
            self.is_spawn = 1
            self.color = COLORS["red"]
        elif self.row in [14, 15, 16]:
            self.is_spawn = 2
            self.color = COLORS["red"]

    def change_has_unit(self, unit):
        if self.has_unit:
            self.has_unit = False
        else:
            self.has_unit = unit

    def find_img(self):
        if self.is_spawn:
            self.img = pygame.transform.scale(TILES["stone"], (32, 32))
        else:
            self.img = pygame.transform.scale(TILES["sand"], (32, 32))

def make_field_list():
    w, h = 11, 17
    field_list = []
    for row in range(h):
        r = []
        for col in range(w):
            new_tile = Tile(row, col)
            r.append(new_tile)
        field_list.append(r)
    return field_list

def draw_bg():
    field_w, field_h = 400 - padding * 2, win_h - padding * 2
    field = pygame.Surface((field_w, field_h))
    field.fill(COLORS["light blue"])

    for row in FIELD:
        for tile in row:
            # pygame.draw.rect(field, tile.color, tile.rect)
            field.blit(tile.img, (tile.x, tile.y))

    draw_units(field)

    window.blit(field, (padding, padding))
    return field

def draw_legend(field, x_y):
    x, y = x_y
    legend_w, legend_h = win_w - field.get_width() - 2*padding, win_h
    legend = pygame.Surface((legend_w, legend_h))
    legend.fill(COLORS["gray"])

    for button in BUTTONS:
        if button.g_rect.collidepoint(pygame.mouse.get_pos()):
            button.mouseover()
        else:
            button.mouseover()
        pygame.draw.rect(legend, button.color, button.rect)
        legend.blit(button.title, (button.x, button.y))
    window.blit(legend, (x, y))
    return legend

def draw_window():
    window.fill(COLORS["dark gray"])
    field = draw_bg()
    draw_legend(field, (field.get_width() + padding*2, 0))
    pygame.display.update()

def setup_game():
    window.fill(COLORS["dark gray"])
    field = draw_bg()
    legend = draw_legend(field, (field.get_width() + padding * 2, 0))
    pygame.display.update()
    make_buttons(legend, (field.get_width() + padding*2, 0))

    global FIELD
    FIELD = make_field_list()

    # upper tower
    r, c = 5, 3
    Unit(r * 32, c * 32, UNIT_TYPES["tower"], faction=1, is_ghost=False, FIELD_list=FIELD)

    # lower tower
    r, c = 5, 13
    Unit(r * 32, c * 32, UNIT_TYPES["tower"], faction=2, is_ghost=False, FIELD_list=FIELD)

def run_round():
    if len(UNITS) > len(UNIT_COPIES):
        for unit in UNITS:
            unit_copy = Unit(unit.x-padding, unit.y-padding, unit.type, unit.faction, is_ghost=False)

    for copy in UNIT_COPIES:
        copy.act()

def main():
    clock = pygame.time.Clock()
    FPS = 60
    running = True
    setup_game()
    playtime = 0
    round = 0
    new_unit = False
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()

    ev = pygame.event.Event(one_sec_event)
    pygame.event.post(ev)

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # for mouse button 1
                    for button in BUTTONS:
                        if button.g_rect.collidepoint(event.pos):
                            new_unit = button.clicked()  # new unit selected
                elif event.button == 3:
                    if new_unit:
                        for row in FIELD:
                            for tile in row:
                                if tile.rect.collidepoint(event.pos) and tile.is_spawn:
                                    new_unit.x, new_unit.y = tile.x, tile.y
                                    new_unit.update_rects()
                                    new_unit.faction = tile.is_spawn
                                    new_unit.find_img()
                                    # make it spawn right unit
                                    new_unit = False  # unselect new unit

            elif event.type == one_sec_event:
                playtime += 1
                if playtime % 5 == 0:
                    print(f"Time until next round: {20-playtime}")
                if playtime == 20:
                    e = pygame.event.Event(round_start_event)
                    pygame.event.post(e)
                    playtime = 0

                pygame.time.set_timer(one_sec_event, 1000)
                if UNIT_COPIES:
                    for copy in UNIT_COPIES:
                        copy.act(FIELD)

            elif event.type == round_start_event:
                sound = SOUNDS["trumpet"]
                sound.set_volume(0.2)
                sound.play()
                print("Round starting...")
                for unit in UNITS:
                    Unit(unit.x - padding, unit.y - padding, unit.type, unit.faction, is_ghost=False, FIELD_list=FIELD)
            elif event.type == win_event:
                print("Game should end now.")
                pygame.time.wait(10*1000)


        draw_window()


if __name__ == "__main__":
    main()