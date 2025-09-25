

import pygame
import random
import math


# --- Constants ---
screen_width = 800
screen_height = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34) # Background color

ORC_ZONE_TOP = screen_height / 2
ORC_ZONE_BOTTOM = screen_height

ELF_ZONE_TOP = 0
ELF_ZONE_BOTTOM = screen_height / 2

#Feel free to adjust these values to change battle dynamics!
ORC_LIFE = 120
ORC_DAMAGE = 15
ELF_LIFE = 100
ELF_DAMAGE = 20

#Please do not change these values, as they are crucial for game balance!
'''
ORC_LIFE = 120
ORC_DAMAGE = 15
ELF_LIFE = 100
ELF_DAMAGE = 20
'''
DOT_SIZE = 10
DOT_SPEED = 0.9
COLLISION_DISTANCE = DOT_SIZE

# --- Pygame Initialization ---
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Epic Battle Simulation") # Set window title
clock = pygame.time.Clock() # For controlling framerate
FPS = 60 # Frames per second

# --- User Input ---
print("This is an epic battle simulator. Please limit the number of total characters to be below 2000.")
try:
    orc_number = int(input("Tell me how many orcs you want: "))
    elf_number = int(input("Tell me how many elves you want: "))
except ValueError:
    print("Invalid input. Please enter numbers. You are now disqualified. ha hA HA")
    pygame.quit()
    exit()

# --- Entity Initialization ---
next_id = 0

orcs = []
for _ in range(orc_number):
    x = random.randint(0, screen_width - DOT_SIZE)
    y = random.randint(ORC_ZONE_TOP, ORC_ZONE_BOTTOM - DOT_SIZE)
    orcs.append({
        'id': next_id,
        'x': x,
        'y': y,
        'target_id': None,
        'is_fighting': False,
        'life': ORC_LIFE
    })
    next_id += 1

elves = []
for _ in range(elf_number): 
    x = random.randint(0, screen_width - DOT_SIZE)
    y = random.randint(ELF_ZONE_TOP, ELF_ZONE_BOTTOM - DOT_SIZE)
    elves.append({
        'id': next_id,
        'x': x,
        'y': y,
        'target_id': None,
        'is_fighting': False,
        'life': ELF_LIFE
    })
    next_id += 1

# --- Initial Target Assignment ---
if elf_number > 0:
    for orc_data in orcs:
        target_elf = random.choice(elves)
        orc_data['target_id'] = target_elf['id']
if orc_number > 0:
    for elf_data in elves:
        target_orc = random.choice(orcs)
        elf_data['target_id'] = target_orc['id']

# --- Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Combat Logic ---
    elves_defeated_ids = set()
    orcs_defeated_ids = set()

    orc_map = {orc['id']: orc for orc in orcs}
    elf_map = {elf['id']: elf for elf in elves}

    # Reset fighting status for all units
    for orc in orcs:
        orc['is_fighting'] = False
    for elf in elves:
        elf['is_fighting'] = False

    # --- ORC MOVING TOWARDS THEIR TARGET ELF ---
    for orc in orcs:
        if orc['id'] in orcs_defeated_ids: # Skip if already marked as defeated this frame
            continue

        target_elf = elf_map.get(orc['target_id'])

        if target_elf and target_elf['id'] not in elves_defeated_ids: # Ensure target exists and is not defeated
            dx = target_elf['x'] - orc['x']
            dy = target_elf['y'] - orc['y']
            distance = math.sqrt(dx**2 + dy**2)

            if distance <= COLLISION_DISTANCE:
                orc['is_fighting'] = True
                target_elf['is_fighting'] = True

                orc['life'] -= ELF_DAMAGE # Orc takes damage from elf
                target_elf['life'] -= ORC_DAMAGE # Elf takes damage from orc

                if orc['life'] <= 0:
                    orcs_defeated_ids.add(orc['id'])

                if target_elf['life'] <= 0:
                    elves_defeated_ids.add(target_elf['id']) 
                    orc['target_id'] = None # Orc's target is defeated
            else:
                if distance > 0:
                    orc['x'] += (dx / distance) * DOT_SPEED
                    orc['y'] += (dy / distance) * DOT_SPEED
        else:
            # If target is gone or already defeated, find a new one
            orc['target_id'] = None
            remaining_elves = [elf for elf in elves if elf['id'] not in elves_defeated_ids]
            if remaining_elves:
                new_target_elf = random.choice(remaining_elves)
                orc['target_id'] = new_target_elf['id']
            else:
                # No more elves, orc wanders randomly
                orc['x'] += random.choice([-DOT_SPEED, 0, DOT_SPEED])
                orc['y'] += random.choice([-DOT_SPEED, 0, DOT_SPEED])

        # Boundary checking for orcs
        orc['x'] = max(0, min(orc['x'], screen_width - DOT_SIZE))
        orc['y'] = max(0, min(orc['y'], screen_height - DOT_SIZE))

    # --- ELF MOVING TOWARDS THEIR TARGET ORC ---
    for elf in elves:
        if elf['id'] in elves_defeated_ids: # Skip if already marked as defeated this frame
            continue

        target_orc = orc_map.get(elf['target_id'])

        if target_orc and target_orc['id'] not in orcs_defeated_ids: # Ensure target exists and is not defeated
            dx = target_orc['x'] - elf['x']
            dy = target_orc['y'] - elf['y']
            distance = math.sqrt(dx**2 + dy**2)

            if distance <= COLLISION_DISTANCE:
                elf['is_fighting'] = True
                target_orc['is_fighting'] = True

                elf['life'] -= ORC_DAMAGE # Elf takes damage from orc
                target_orc['life'] -= ELF_DAMAGE # Orc takes damage from elf

                if elf['life'] <= 0:
                    elves_defeated_ids.add(elf['id'])
                if target_orc['life'] <= 0:
                    orcs_defeated_ids.add(target_orc['id'])
                    elf['target_id'] = None # Elf's target is defeated
            else:
                if distance > 0:
                    elf['x'] += (dx / distance) * DOT_SPEED
                    elf['y'] += (dy / distance) * DOT_SPEED
        else:
            # If target is gone or already defeated, find a new one
            elf['target_id'] = None
            remaining_orcs = [orc for orc in orcs if orc['id'] not in orcs_defeated_ids]
            if remaining_orcs:
                new_target_orc = random.choice(remaining_orcs)
                elf['target_id'] = new_target_orc['id']
            else:
                # No more orcs, elf wanders randomly
                elf['x'] += random.choice([-DOT_SPEED, 0, DOT_SPEED])
                elf['y'] += random.choice([-DOT_SPEED, 0, DOT_SPEED])

        # Boundary checking for elves
        elf['x'] = max(0, min(elf['x'], screen_width - DOT_SIZE)) 
        elf['y'] = max(0, min(elf['y'], screen_height - DOT_SIZE)) 

    # --- Remove defeated units after all calculations for the frame ---
    orcs = [orc for orc in orcs if orc['id'] not in orcs_defeated_ids]
    elves = [elf for elf in elves if elf['id'] not in elves_defeated_ids]

    # --- Check for game over condition ---
    if not orcs:
        print("Elves win! All orcs defeated!")
        running = False
    if not elves:
        print("Orcs win! All elves defeated!")
        running = False
    if not orcs and not elves: # Draw scenario
        print("It's a draw! All units defeated!")
        running = False

    # --- Drawing ---
    screen.fill(GREEN)

    for orc_data in orcs:
        # Draw orc
        pygame.draw.ellipse(screen, BLACK, (orc_data['x'], orc_data['y'], DOT_SIZE, DOT_SIZE))
        #Health bar
        health_bar_width = DOT_SIZE * (orc_data['life'] / ORC_LIFE)
        pygame.draw.rect(screen, (255, 0, 0), (orc_data['x'], orc_data['y'] - 5, health_bar_width, 3))


    for elf_data in elves:
        # Draw elf
        pygame.draw.ellipse(screen, WHITE, (elf_data['x'], elf_data['y'], DOT_SIZE, DOT_SIZE))
        #Heath Bar
        health_bar_width = DOT_SIZE * (elf_data['life'] / ELF_LIFE)
        pygame.draw.rect(screen, (0, 0, 255), (elf_data['x'], elf_data['y'] - 5, health_bar_width, 3))

    pygame.display.flip() 
    clock.tick(FPS)

pygame.quit() 
print("Game over!")
