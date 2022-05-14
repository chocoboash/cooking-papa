import pygame, math

from states.main_menu import Main_Menu

class Game: 
    
        def __init__(self):
            pygame.init()
            self.GAME_X, self.GAME_Y = 320, 180
            self.SCREEN_X, self.SCREEN_Y = 1280, 720
            self.game_canvas = pygame.Surface((self.GAME_X, self.GAME_Y))
            self.screen = pygame.display.set_mode((self.SCREEN_X, self.SCREEN_Y))
            pygame.display.set_caption("Cooking Papa")
            self.running, self.playing = True, True
            self.actions = {"menu": False, "start": False, "shop": False, "quit": False}
            self.clock = pygame.time.Clock()
            self.state_stack = []
            self.load_states()

        def game_loop(self):
            while self.playing:
                self.get_events()
                self.update()
                self.render()

        def get_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.actions["quit"]:
                    self.running = False
                    self.playing = False

        def update(self):
            self.state_stack[-1].update(self.actions)

        def render(self):
            self.state_stack[-1].render(self.game_canvas)
            self.screen.blit(pygame.transform.scale(self.game_canvas, (self.SCREEN_X, self.SCREEN_Y)), (0, 0))
            pygame.display.flip()
            self.clock.tick(60)

        def draw_text(self, surface, text, font, color, px, py):
            text_obj = font.render(text, True, color)
            text_rect = text_obj.get_rect()
            text_rect.center = (px, py)
            surface.blit(text_obj, text_rect)

        def draw_image(self, image, scale, surface, px, py):
            image_rect = image.get_rect()
            image_scaled = pygame.transform.scale(image, (image_rect.right * scale, image_rect.bottom * scale))
            image_rect.x, image_rect.y = image.get_width(), image.get_height()
            surface.blit(image_scaled, image_scaled.get_rect(center = (px, py)))

        def gradient_rect(self, surface, top_color, bottom_color, target_rect):
            color_rect = pygame.Surface((2, 2))
            pygame.draw.line(color_rect, top_color, (0, 0), (1, 0))            
            pygame.draw.line(color_rect, bottom_color, (0, 1), (1, 1))
            color_rect = pygame.transform.smoothscale(color_rect, (target_rect.width, target_rect.height))
            surface.blit(color_rect, target_rect)  

        def load_states(self):
            self.main_menu = Main_Menu(self)
            self.state_stack.append(self.main_menu)

        def reset_keys(self):
            for action in self.actions:
                self.actions[action] = False

if __name__ == "__main__":
    game = Game()
    while game.running:
        game.game_loop()

    
        

