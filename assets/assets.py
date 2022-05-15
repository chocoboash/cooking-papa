import pygame
from button import Button

pygame.font.init()
pygame.mixer.init()

MARBLE_WHITE = (242, 240, 229)
SILVER_BULLET = (184, 181, 185)
SUVA_GREY = (134, 129, 136)
DIGITAL_GREY = (100, 99, 101)
NIGHT_GREY = (69, 68, 79)
MAGIC_NIGHT = (58, 56, 88)
NOBLE_BLACK = (33, 33, 35)
OBSIDIAN_BLACK = (53, 43, 66)
PALACE_ARMS = (67, 67, 106)
BLUE_SONKI = (75, 128, 202)
ARCTIC_OCEAN = (104, 194, 211)
YUCCA_CREAM = (162, 220, 199)
WHISTLES_GOLD = (237, 225, 158)
DESERT_CARAVAN = (211, 160, 104)
MINERAL_RED = (180, 82, 82)
MEDICINE_MAN = (106, 83, 110)
SOVEREIGN = (75, 65, 88)
SEQUOIA = (128, 73, 58)
TUSCAN_SOIL = (167, 123, 91)
WARM_CROISSANT = (229, 206, 180)
SOFT_FERN = (194, 211, 104)
BROCCOLI = (138, 176, 96)
GREEN_HOUR = (86, 123, 121)
DEEP_EVERGREEN = (78, 88, 74)
FERN_SHADE = (123, 114, 67)
FANCY_MOSS = (178, 180, 126)
KASHMIR_PINK = (237, 200, 196)
CARNATION_ROSE = (207, 138, 203)
PURPLE_STONE = (95, 85, 106)

# Fonts
NEXA_FONT = pygame.font.Font("assets/fonts/Nexa-Trial-Regular.ttf", 15)
DAYDREAM_FONT = pygame.font.Font("assets/fonts/Daydream.ttf", 15)
YOSTER_FONT = pygame.font.Font("assets/fonts/yoster.ttf", 15)
MARIO_FONT = pygame.font.Font("assets/fonts/Mario-Kart-DS.ttf", 20)

# Main Menu Assets
game_logo = pygame.image.load("assets/images/titles/cookingPapaPlaceholderTitle.png")
play_button = pygame.image.load("assets/images/icons/play_button.png")
shop_button = pygame.image.load("assets/images/icons/shop_button.png")
quit_button = pygame.image.load("assets/images/icons/quit_button.png")

placeholder_button = pygame.image.load("assets/images/icons/buttonPlaceholder.png")
return_arrow = pygame.image.load("assets/images/icons/return_arrow.png")
gold_icon = pygame.image.load("assets/images/icons/coin.png")
check_mark = pygame.image.load("assets/images/icons/check_mark.png")

# Kitchen assets
restaurant_counter = pygame.image.load("assets/images/images/restaurant_counter.png")
kitchen_grill = pygame.image.load("assets/images/images/kitchen_grill.png")

# Burger
raw_burger_patty = pygame.image.load("assets/images/images/raw_burger_patty.png")

# Reocurring buttons
return_button = Button(20, 20, return_arrow, 1)
check_button = Button(300, 20, check_mark, 1)