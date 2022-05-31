# Purpose: Gameplay child class that inherits from State class, controls main game mechanics such as customer and recipe generating and cooking 

"""
To do list:

- Add return button to each cooking screen that goes back to restaurant
- Will need to make another state for being in the kitchen because buttons don't work after screen flipped

"""
import random, time
from states.state import State
from button import Button
from assets.assets import * 

class Restaurant(State):

    def __init__(self, game):
        State.__init__(self, game)
        
        self.possible_recipes =  {
            "Burger": {
                "Cook Patty": "Flip at the right time!",
                "Slice Tomato": "Click two points to make a slice.",
                "Assemble Burger": "Put the ingredients of the burger together"
            },
            "Pizza": {
                "Roll Dough": "Scroll your mouse to move the rolling pin back and forth until the dough is rolled.",
                "Add Toppings": "Drag the toppings to the pizza.",
                "Place in Oven": "Put the pizza in the oven"
            },
            "Stew": {
                "Cut vegetables": "",
                "": "",
                "": "",
            },
            "Fried Chicken": {
                "": "",
                "": "",
                "": "",
            }
        }

        self.set_order()

    def generate_order(self): 
        selected = random.choice(list(self.possible_recipes.keys()))
        return(selected, self.possible_recipes[selected])

    def generate_customer(self):
        possible_customers = [customer_1, customer_2, customer_3]
        return random.choice(possible_customers) 

    def set_order(self):
        returned = self.generate_order()
        self.selected_customer = self.generate_customer()
        self.selected_recipe = returned[0]
        self.game.current_recipe = self.selected_recipe

    def update(self, actions):
        if actions["menu"]:
            main_menu = self.game.state_stack[0]
            main_menu.enter_state()

        if actions["recipe"]:
            self.set_order()

        if actions["cooking"]:
            new_state = Kitchen(self.game)
            new_state.enter_state()

    def render(self, surface):

        surface.fill(WHISTLES_GOLD)
        self.game.draw_image(self.selected_customer, 1, surface, self.game.GAME_X / 2, 100)
        self.game.draw_image(restaurant_counter, 1, surface, self.game.GAME_X / 2, 105)
        self.game.draw_image(speech_bubble, 1, surface, self.game.GAME_X/ 2 + 60, self.game.GAME_Y / 2 - 50)
        self.show_order(surface)

        if return_button.draw(surface):
            self.game.actions["menu"] = True

        if decline_order_button.draw(surface):
            self.game.actions["recipe"] = True

        if confirm_order_button.draw(surface):
            self.game.actions["cooking"] = True

        
    def show_order(self, surface):  # MUST BE INSIDE OF LOOP
        
        icon_position = self.game.GAME_X/ 2 + 60, self.game.GAME_Y / 2 - 57
        
        if self.selected_recipe == "Burger":
            self.game.draw_image(burger_icon, 1, surface, icon_position[0], icon_position[1])

        elif self.selected_recipe == "Pizza":
            self.game.draw_image(pizza_icon, 1, surface, icon_position[0], icon_position[1])

        elif self.selected_recipe == "Stew":
            self.game.draw_image(stew_icon, 1, surface, icon_position[0], icon_position[1])

        elif self.selected_recipe == "Fried Chicken":
            self.game.draw_image(chicken_icon, 1, surface, icon_position[0], icon_position[1])


class Kitchen(State):

    def __init__(self, game):
        State.__init__(self, game)

        self.current_recipe = self.game.current_recipe
        self.countdown_triggered = False
        self.countdown_completed = False
        self.rating_triggered = False
        self.ingredient_rating = None
        self.total_rating = 0
        self.next_step = False

        self.countdown = {

            3: False,
            2: False,
            1: False

        }

        self.burger_patty_speed = 0.15
        self.burger_patty_pos = 0
        self.stop_button_posx, self.stop_button_posy = self.game.GAME_X / 4, self.game.GAME_Y / 5
        self.stop_button_velx, self.stop_button_vely = 1,1
        
        self.step_1 = True
        self.step_2 = False
        self.step_3 = False

        self.cooking_done = False

    def update(self, actions):
        if actions["menu"]:
            main_menu = self.game.state_stack[0]
            main_menu.enter_state()

        if self.countdown_triggered:
            current_time = pygame.time.get_ticks()
            
            if current_time - self.button_time >= 100 and current_time - self.button_time < 1100:
                self.countdown[3] = True
            if current_time - self.button_time >= 1100 and current_time - self.button_time < 2100:
                self.countdown[2] = True
                self.countdown[3] = False
            if current_time - self.button_time >= 2100 and current_time - self.button_time < 3100:
                self.countdown[2] = False
                self.countdown[1] = True
            if current_time - self.button_time >= 3100 and current_time - self.button_time < 4100:
                self.countdown[1] = False
            if current_time - self.button_time >= 4100 and current_time - self.button_time < 5100:
                self.countdown_triggered = False
                self.countdown_completed = True

        if self.cooking_done:
            if pygame.time.get_ticks() > self.completed_time + 3000:
                self.rating_triggered = True
                if pygame.time.get_ticks() > self.completed_time + 6000:
                    self.next_step = True

    def render(self, surface):

        if self.current_recipe == "Burger":
            self.cook_burger(surface)

        elif self.current_recipe == "Pizza":
            self.cook_pizza(surface) 

        elif self.current_recipe == "Stew":
            self.cook_stew(surface)

        elif self.current_recipe == "Fried Chicken":
            self.cook_chicken(surface)

    def cook_burger(self, surface):

        def cook_patty(surface):
            self.game.draw_image(kitchen_grill, 1, surface, self.game.GAME_X / 4, self.game.GAME_Y / 2)
            self.game.draw_image(green_instruction_panel, 1, surface, self.game.GAME_X / 2 + self.game.GAME_X / 4, self.game.GAME_Y / 2)
            self.game.draw_image(cooking_papa, 1, surface, 215, 128)
            self.game.draw_image(papa_speech, 1, surface, 275, 110)

            # Changes the text in cooking papa's speech bubble depending on the conditions

            if not self.cooking_done:
                
                self.game.draw_text(surface, "FLIP AT THE", MINIMAL_FONT, NOBLE_BLACK, 275, 95)
                self.game.draw_text(surface, "RIGHT TIME!", MINIMAL_FONT, NOBLE_BLACK, 275, 110)

            if self.cooking_done:

                if (self.burger_patty_pos >= 0 and self.burger_patty_pos <= 40) or self.burger_patty_pos > 90:
                    self.game.draw_text(surface, "TRY BETTER", MINIMAL_FONT, NOBLE_BLACK, 275, 95)
                    self.game.draw_text(surface, "NEXT TIME!", MINIMAL_FONT, NOBLE_BLACK, 275, 110)
                    self.ingredient_rating = 1

                elif (self.burger_patty_pos > 40 and self.burger_patty_pos <= 50) or (self.burger_patty_pos > 80 and self.burger_patty_pos <= 90):
                    self.game.draw_text(surface, "GOOD JOB!", MINIMAL_FONT, NOBLE_BLACK, 275, 95)
                    self.game.draw_text(surface, "DOING GREAT!", MINIMAL_FONT, NOBLE_BLACK, 275, 110)
                    self.ingredient_rating = 2

                elif self.burger_patty_pos > 50 and self.burger_patty_pos <= 80:
                    self.game.draw_text(surface, "PERFECT!", MINIMAL_FONT, NOBLE_BLACK, 275, 95)
                    self.game.draw_text(surface, "EXCELLENT JOB", MINIMAL_FONT, NOBLE_BLACK, 276, 110)
                    self.ingredient_rating = 3

                self.total_rating += self.ingredient_rating                

            self.game.draw_image(cooking_bar, 1, surface, self.game.GAME_X / 2 + self.game.GAME_X / 4, self.game.GAME_Y / 4)

            self.trigger_countdown(surface)

            if self.countdown_completed:
                
                stop_button = Button(self.stop_button_posx, self.stop_button_posy, flip_button, 1)

                self.stop_button_posx += self.stop_button_velx
                self.stop_button_posy += self.stop_button_vely

                if self.stop_button_posx >= self.game.GAME_X / 2 - 9 or self.stop_button_posx <= 9:
                    self.stop_button_velx *= -1

                if self.stop_button_posy >= self.game.GAME_Y / 2 - 28 or self.stop_button_posy <= 5:
                    self.stop_button_vely *= -1

                if stop_button.draw(surface):
                    self.cooking_done = True
                    self.completed_time = pygame.time.get_ticks()
                    self.burger_patty_speed, self.stop_button_velx, self.stop_button_vely = 0, 0, 0

                self.game.draw_image(cooking_arrow, 1, surface, self.game.GAME_X / 2 + self.game.GAME_X / 4 - 65 + self.burger_patty_pos, self.game.GAME_Y / 4 + 10)
                
                self.burger_patty_pos += self.burger_patty_speed

                # Stops the cooking arrow when it reaches the end of the bar
                if self.burger_patty_pos >= 135:
                    self.burger_patty_speed, self.stop_button_velx, self.stop_button_vely = 0, 0, 0

                # Draw the appropriate patty depending on the cooking arrow position
                elif self.burger_patty_pos >= 0 and self.burger_patty_pos <= 40:
                    self.game.draw_image(raw_patty, 1, surface, self.game.GAME_X / 4, 135)

                elif self.burger_patty_pos > 40 and self.burger_patty_pos <= 90:
                    self.game.draw_image(cooked_patty, 1, surface, self.game.GAME_X / 4, 135)

                elif self.burger_patty_pos > 90:
                    self.game.draw_image(burned_patty, 1, surface, self.game.GAME_X / 4, 135)

                if self.rating_triggered:
                    self.rating_screen(surface, green_background, "COOK PATTY")
                    
                    if self.next_step:
                        self.reset_status(1)

        def cut_tomato(surface):
            self.game.draw_image(cutting_board, 1, surface, self.game.GAME_X / 4, self.game.GAME_Y / 2)
            self.game.draw_image(green_instruction_panel, 1, surface, self.game.GAME_X / 2 + self.game.GAME_X / 4, self.game.GAME_Y / 2)
            self.game.draw_image(cooking_papa, 1, surface, 215, 128)
            self.game.draw_image(papa_speech, 1, surface, 275, 110)

            if not self.cooking_done:
                
                self.game.draw_text(surface, "SLICE AT THE", MINIMAL_FONT, NOBLE_BLACK, 275, 95)
                self.game.draw_text(surface, "RIGHT TIME!", MINIMAL_FONT, NOBLE_BLACK, 275, 110)

            if self.cooking_done:

                if (self.burger_patty_pos >= 0 and self.burger_patty_pos <= 40) or self.burger_patty_pos > 90:
                    self.game.draw_text(surface, "TRY BETTER", MINIMAL_FONT, NOBLE_BLACK, 275, 95)
                    self.game.draw_text(surface, "NEXT TIME!", MINIMAL_FONT, NOBLE_BLACK, 275, 110)
                    self.ingredient_rating = 1

                elif (self.burger_patty_pos > 40 and self.burger_patty_pos <= 50) or (self.burger_patty_pos > 80 and self.burger_patty_pos <= 90):
                    self.game.draw_text(surface, "GOOD JOB!", MINIMAL_FONT, NOBLE_BLACK, 275, 95)
                    self.game.draw_text(surface, "DOING GREAT!", MINIMAL_FONT, NOBLE_BLACK, 275, 110)
                    self.ingredient_rating = 2

                elif self.burger_patty_pos > 50 and self.burger_patty_pos <= 80:
                    self.game.draw_text(surface, "PERFECT!", MINIMAL_FONT, NOBLE_BLACK, 275, 95)
                    self.game.draw_text(surface, "EXCELLENT JOB", MINIMAL_FONT, NOBLE_BLACK, 276, 110)
                    self.ingredient_rating = 3

                self.total_rating += self.ingredient_rating
    
            self.game.draw_image(cooking_bar, 1, surface, self.game.GAME_X / 2 + self.game.GAME_X / 4, self.game.GAME_Y / 4)

            self.trigger_countdown(surface)

            if self.countdown_completed:
                
                stop_button = Button(self.game.GAME_X, 80, flip_button, 1)
                self.game.draw_image(whole_tomato, 1, surface, self.game.GAME_X / 4, 135)

                if stop_button.draw(surface):
                    self.cooking_done = True
                    self.completed_time = pygame.time.get_ticks()

                if self.rating_triggered:
                    self.rating_screen(surface, green_background, "SLICE TOMATO")
                    
                    if self.next_step:
                        self.reset_status(2)

        def assemble_burger(surface):
            self.game.draw_image(cutting_board, 1, surface, self.game.GAME_X / 4, self.game.GAME_Y / 2)
            self.game.draw_image(green_instruction_panel, 1, surface, self.game.GAME_X / 2 + self.game.GAME_X / 4, self.game.GAME_Y / 2)
            self.game.draw_image(cooking_papa, 1, surface, 215, 128)
            self.game.draw_image(papa_speech, 1, surface, 275, 110)
            

        surface.fill(FANCY_MOSS)
        
        if self.step_1:
            cook_patty(surface)
        elif self.step_2:
            cut_tomato(surface)
        elif self.step_3:
            assemble_burger(surface)
        
    def cook_pizza(self, surface):

        def roll_dough(surface):
            self.game.draw_image(cutting_board, 1, surface, self.game.GAME_X / 4, self.game.GAME_Y / 2)

        def add_sauce(surface):
            pass

        def add_toppings(surface):
            pass

        surface.fill(MINERAL_RED)
        if self.step_1:
            roll_dough(surface)
        elif self.step_2:
            add_sauce(surface)
        elif self.step_3:
            add_toppings(surface)

    def cook_stew(self, surface):

        def step_1(surface):
            pass

        def step_2(surface):
            pass

        def step_3(surface):
            pass

        surface.fill(KASHMIR_PINK)
        step_1(surface)
        step_2(surface)
        step_3(surface)

    def cook_chicken(self, surface):

        def step_1(surface):
            pass

        def step_2(surface):
            pass

        def step_3(surface):
            pass

        surface.fill(WARM_CROISSANT)
        step_1(surface)
        step_2(surface)
        step_3(surface)

    def rating_screen(self, surface, background_image, step_name):
        self.game.draw_image(background_image, 1, surface, self.game.GAME_X / 2, self.game.GAME_Y / 2)
        self.game.draw_text(surface, str(step_name), MARIO_FONT, NOBLE_BLACK, self.game.GAME_X / 2, self.game.GAME_Y / 4)
        self.game.draw_text(surface, str(self.ingredient_rating), MARIO_FONT, NOBLE_BLACK, self.game.GAME_X / 2, self.game.GAME_Y / 2)

    def reset_status(self, current_step):
        self.cooking_done = False
        self.countdown_triggered = False
        self.countdown_completed = False
        self.rating_triggered = False
        self.ingredient_rating = None
        self.next_step = False

        if current_step == 1:
            self.step_1 = False
            self.step_2 = True

        elif current_step == 2:
            self.step_2 = False
            self.step_3 = True

        elif current_step == 3:
            self.step_3 = False

    def trigger_countdown(self, surface):
        start_button = Button(self.game.GAME_X / 2, self.game.GAME_Y / 2, start, 1)
                
        if not self.countdown_triggered and not self.countdown_completed:
            if start_button.draw(surface):
                self.button_time = pygame.time.get_ticks()
                self.countdown_triggered = True

        if self.countdown[3]:
            self.game.draw_image(countdown_3, 1, surface, self.game.GAME_X / 4, self.game.GAME_Y / 2)

        elif self.countdown[2]:
            self.game.draw_image(countdown_2, 1, surface, self.game.GAME_X / 4, self.game.GAME_Y / 2)

        elif self.countdown[1]:
            self.game.draw_image(countdown_1, 1, surface, self.game.GAME_X / 4, self.game.GAME_Y / 2)
            






