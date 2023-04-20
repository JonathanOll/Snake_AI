from random import choice, randint, uniform
import sys
from time import time
from const import *
import pygame
from ai import NeuralNetwork, Generation
import sys

sys.setrecursionlimit(999999999)

class Controller:

    def __init__(self, table={}, network=None):
        
        self.pressing = []
        self.pressed = []
        self.released = []
        self.table = table
        if network:
            self.network = network
        else:
            self.network = None
    
    def update(self, inputs=None):
        if self.network:

            res = self.network.forward(inputs)

            best = 0
            for i in range(1, 4):
                if res[i] > res[best]:
                    best = i
            
            self.pressed.clear()
            self.pressed.append(DIR_STR[best])
        
        for key in self.table.keys():
            if pygame.key.get_pressed()[key]:
                    self.press(key)
            else:
                self.release(key)

    def press(self, key):
        if self.table[key] not in self.pressing:
            self.pressed.append(self.table[key])
            self.pressing.append(self.table[key])
        elif self.table[key] in self.pressed:
            self.pressed.remove(self.table[key])

    def release(self, key):
        if self.table[key] in self.pressing:
            self.pressing.remove(self.table[key])
            self.released.append(self.table[key])
        elif self.table[key] in self.released:
            self.released.remove(self.table[key])

class Game:

    GAME_COUNT = 0

    def __init__(self, generation=None, controller=None, reset=False):
        
        if not reset:
            self.id = Game.GAME_COUNT
            Game.GAME_COUNT += 1
        self.running = True
        self.alive_tick = 0
        self.tick_without_growing = 0

        if generation:
            self.generation = generation
        elif not reset:
            self.generation = None

        if controller and not reset:
            self.controller = controller
        elif not reset and not generation:
            self.controller = Controller()
        elif not reset and generation:
            self.controller = Controller(network=generation.get_current_ind())
        elif reset and self.generation:
            self.controller = Controller(network=self.generation.next_ind())

        self.apples = []
        self.free_spaces = [ (x, y) for x in range(MAP_WIDTH) for y in range(MAP_HEIGHT) ]

        self.snake = [ (MAP_WIDTH // 2, MAP_HEIGHT // 2),
                       (MAP_WIDTH // 2, MAP_HEIGHT // 2 + 1) ]
        self.free_spaces.remove((MAP_WIDTH // 2, MAP_HEIGHT // 2))
        self.free_spaces.remove((MAP_WIDTH // 2, MAP_HEIGHT // 2 + 1))
        self.snake_dir = 0

        self.clock = {"tick": time()}

    def is_pos_valid(self, *args):
        if len(args) == 1:
            x, y = args[0]
        else:
            x, y = args[0], args[1]

        return (0 <= x < MAP_WIDTH) and (0 <= y < MAP_HEIGHT)

    def end(self):

        self.running = False
        
        if self.controller.network is not None:

            self.controller.network.fitness = 10 * len(self.snake) ** 2
            
            self.__init__(reset=True)
            self.run()

    def gen_apple(self):

        if len(self.free_spaces) == 0 : return
        
        apple_pos = choice(self.free_spaces)
        self.apples.append(apple_pos)
        self.free_spaces.remove(apple_pos)
    
    def gen_apples(self):

        for i in range(min(len(self.free_spaces), MAX_APPLE - len(self.apples))):

            self.gen_apple()

    def forward(self):
        
        new_pos = (self.snake[0][0] + DIR[self.snake_dir][0], 
        self.snake[0][1] + DIR[self.snake_dir][1])

        if new_pos not in self.apples:
            self.free_spaces.append(self.snake.pop())
        else:
            self.apples.remove(new_pos)
            self.gen_apple()
            self.tick_without_growing = 0

        if not self.is_pos_valid(new_pos) or new_pos in self.snake:
            self.end()
            return
        
        self.snake.insert(0, new_pos)

        if new_pos in self.free_spaces:
            self.free_spaces.remove(new_pos)

    def tick(self):

        # action de l'IA

        if self.controller.network:

            self.controller.update(self.get_inputs())
        
        # mise à jour de la direction

        for i in range(len(DIR_STR)):
            
            if DIR_STR[i] in self.controller.pressed:
                
                self.snake_dir = STR_TO_DIR[DIR_STR[i]]

        # mise à jour de la position

        self.forward()
        
        # verification de l'état du jeu

        if len(self.snake) >= MAP_HEIGHT * MAP_WIDTH or self.tick_without_growing > TICK_WITHOUT_GROWING_LIMIT:

            self.end()
        
        self.alive_tick += 1
        self.tick_without_growing += 1
    
    def get_inputs(self): 
        inputs = []

        base_x, base_y = self.snake[0]

        # Détection des obstacles

        for dir in DIR8:
            res = 0
            x, y, (dx, dy) = base_x, base_y, dir
            x += dx
            y += dy

            while self.is_pos_valid(x, y) and (x, y) not in self.snake:
                x += dx
                y += dy
                res += 1
            
            inputs.append(res)
        
        # Détection des pommes

        for dir in DIR8:
            res = 0
            x, y, (dx, dy) = base_x, base_y, dir

            while True:
                if (x, y) in self.apples:
                    break
                x += dx
                y += dy
                res += 1
                if not self.is_pos_valid(x, y):
                    res = -1
                    break
            
            inputs.append(res)

        return inputs

    def paint(self, surface=None, base_pos=(0, 0)):

        if surface == None and self.screen: surface = self.screen

        surface.fill((0, 0, 0))

        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                
                if (x, y) in self.snake : 
                    coef = 1 - (self.snake.index((x, y)) / len(self.snake)) * 0.7
                    color = tuple(coef * SNAKE_CELL_COLOR[i] for i in range(3))
                elif (x, y) in self.apples: 
                    color = APPLE_CELL_COLOR
                else: color = BACKGROUND_COLOR
                pygame.draw.rect(surface, color, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        if not self.running:
            text = self.font.render("Game over", False, GAME_OVER_COLOR)
            self.screen.blit(text, (MAP_WIDTH * CELL_SIZE // 2 - text.get_width() // 2, MAP_HEIGHT * CELL_SIZE // 2 - text.get_height() // 2))

        if self.generation:
            text = self.font.render("Game #" + str(self.generation.current_index()), False, GAME_ID_COLOR)
            self.screen.blit(text, (MAP_WIDTH * CELL_SIZE // 2 - text.get_width() // 2, MAP_HEIGHT * CELL_SIZE + 5))

        if self.controller.network:
            self.controller.network.paint(self.screen, NN_DISPLAY_RECT)

        pygame.display.flip()
    
    def init_window(self):

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake")
        pygame.font.init()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 30)
    
    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit()
        if not self.running and "ok" in self.controller.pressed:
            self.__init__(reset=True)
            self.run()

    def run(self):

        self.gen_apples()

        while True:

            self.handle_event()

            if not self.controller.network:
                self.controller.update()


            for d in DIR_STR:
                if d in self.controller.pressed and (STR_TO_DIR[d] + self.snake_dir) % 2 != 0:
                    self.snake_dir = STR_TO_DIR[d]
            
            if self.running and time() - self.clock["tick"] >= TICK_DELAY:
                self.clock["tick"] = time()
                self.tick()
                self.paint()



# game = Game(controller=Controller({pygame.K_UP: "up", pygame.K_RIGHT: "right", pygame.K_DOWN: "down", pygame.K_LEFT: "left", pygame.K_SPACE: "ok"}))
# game = Game(controller=Controller(network=NeuralNetwork(), table={pygame.K_SPACE: "ok"}))
game = Game(generation=Generation())

game.init_window()
game.run()

        

        
        
    
        







