import pygame
import random
import time
pygame.init() #initialization

screen_height = 800 
screen_width = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#Classes
class Unit():
    def __init__(self, life, attack_num, position, color, speed = 0.9, radius = 10, vision_range = 100):
        self.life = life
        self.attack_num = attack_num
        self.speed = speed
        self.position = pygame.Vector2(position)
        self.color = color
        self.radius = radius
        self.vision_range = vision_range
        self.target = None
    
    def is_alive(self):
        return self.life > 0

    def take_damage(self, amount):
        self.life -= amount
        if self.life < 0:
            self.life = 0
    
    def move_towards(self, target_position):
        target_pos = pygame.Vector2(target_position)
        direction = target_pos - self.position
        distance = direction.length()
        if distance > 0:
            direction = direction.normalize()
            self.position += direction * self.speed
    
    def attack_enemy(self, enemy):
        enemy.take_damage(self.attack_num)

    
    def find_nearest_enemy(self, enemies):
        visible_enemies = []
        for enemy in enemies:
            distance = (enemy.position - self.position).length()
            if distance <= self.vision_range and enemy.is_alive():
                visible_enemies.append((distance, enemy))
        
        if visible_enemies:
            visible_enemies.sort(key=lambda x: x[0])
            self.target = visible_enemies[0][1]
        else:
            self.target = None
    
    def update(self, enemies):
        if not self.is_alive():
            return
        
        self.find_nearest_enemy(enemies)
        
        if self.target:
            distance = (self.target.position - self.position).length()
            if distance <= self.radius * 2:
                self.attack_enemy(self.target)
            else:
                self.move_towards(self.target.position)

class UnitGroup():
    def __init__(self, color, num_units, unit_stats, spawn_area):
        self.color = color
        self.units = []
        self.spawn_area = spawn_area

        for _ in range(num_units):
            x = random.randint(spawn_area[0][0], spawn_area[1][0])
            y = random.randint(spawn_area[0][1], spawn_area[1][1])
            position = (x, y)

        unit = Unit(
            life = unit_stats['life'],
            attack_num = unit_stats ['attack'],
            position = position,
            color = color,
            speed = unit_stats.get('speed', 0.9),
            radius = unit_stats.get('radius', 10),
            vision_range = unit_stats.get('vision_range', 100)
        )
        self.units.append(unit)
    
    def alive_units(self):
        return [unit for unit in self.units if unit.is_alive()]
    
    def update(self, enemy_units):
        for unit in self.alive_units():
            unit.update(enemy_units)
    
    def draw(self, screen):
        for unit in self.alive_units():
            pygame.draw.circle(screen, unit.color, (int(unit.position.x), int(unit.position.y)), unit.radius)

class BattleField():
    ...

class Game():
    def __init__(self):
        self.army_number = None

    def start_simulation(self):
        print()
        print("This is an Epic Battle Simulator!")
        print("__________________________________")

        valid_choices = ['2', '3', '4']
        army_number = ''


        while army_number not in valid_choices:
            army_number = input("Choose how many armies you want on the battle field (2-4): ").strip()

            if army_number in valid_choices:
                print(f"{army_number} armies will fight each other!")
                self.army_number = int(army_number)
                break
            else:
                print("Invalid input, please try again.")


        army_names = ["Orcs", "Humans", "Elves", "Dwarves"]

        selected_armies = random.sample(army_names, int(self.army_number))

        if self.army_number == 2:
            print(f"The armies fighting are: {selected_armies[0]} and {selected_armies[1]}")
        elif self.army_number == 3:
            print(f"The armies fighting are: {selected_armies[0]}, {selected_armies[1]}, and {selected_armies[2]}")
        elif self.army_number == 4:
            print(f"The armies fighting are: {selected_armies[0]}, {selected_armies[1]}, {selected_armies[2]}, and {selected_armies[3]}")

