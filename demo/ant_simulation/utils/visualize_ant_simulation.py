import os
import pygame
import math
import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from multi_agent_system_framework.environment.environment import Environment
    from multi_agent_system_framework.agent.agent import Agent

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

SCALING_FACTOR = 7

def calculate_angle(position, previous_position):
    dx = position[0] - previous_position[0]
    dy = position[1] - previous_position[1]
    angle = math.degrees(math.atan2(dy, dx))
    return angle

# Visualize ant simulation using Pygame
async def visualize_ant_simulation(environment: 'Environment'):
    pygame.init()
    
    # Load images
    current_dir = os.path.dirname(__file__)
    ant_image_path = os.path.join(current_dir, 'ant.png')
    background_image_path = os.path.join(current_dir, 'Dirt.png')
    icon_image = pygame.image.load(ant_image_path)
    ant_image = pygame.image.load(ant_image_path)
    ant_image = pygame.transform.scale(ant_image, (20, 20))
    background_image = pygame.image.load(background_image_path)
        
    # Setup window
    window_size = (environment.size[0] * SCALING_FACTOR, environment.size[1] * SCALING_FACTOR)
    background_image = pygame.transform.scale(background_image, window_size)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Ant Simulation")
    pygame.display.set_icon(icon_image)
    font = pygame.font.SysFont(None, 36)

    clock = pygame.time.Clock()
    previous_positions = {}
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Render the background image
        screen.blit(background_image, (0, 0))

        # Render trails
        for entity in environment.entities.values():
            if type(entity).__name__ == 'Item' and entity.item_type == 'trail':
                pos_1 = entity.position
                pos_2 = entity.data.get('food direction')
                if pos_1 and pos_2:
                    x_start, y_start = [coord * SCALING_FACTOR for coord in pos_1]
                    x_end, y_end = [coord * SCALING_FACTOR for coord in pos_2]
                    pygame.draw.line(screen, RED, (x_start, y_start), (x_end, y_end), 2)

        # Render other entities
        food_delivered = 0
        for entity in environment.entities.values():
            if type(entity).__name__ == 'Item':
                
                # Render nest
                if entity.item_type == 'ant nest':
                    x, y = [coord * SCALING_FACTOR for coord in entity.position]
                    pygame.draw.polygon(screen, BLACK, [(x-10, y+10), (x+10, y+10), (x, y-10)])
                    food_delivered = entity.data.get('food count', 0)

                # Render food
                elif entity.item_type == 'food':
                    count = entity.inventory.get('food', 0)
                    x, y = [coord * SCALING_FACTOR for coord in entity.position]
                    pygame.draw.circle(screen, GREEN, (x, y), 5)
                    font = pygame.font.SysFont(None, 24)
                    text = font.render(str(count), True, BLACK)
                    screen.blit(text, (x + 10, y + 10))

            # Render ants
            if type(entity).__name__ == 'AntAgent':
                
                x, y = [coord * SCALING_FACTOR for coord in entity.position]
                
                previous_position = previous_positions.get(entity, (x, y))
                angle = calculate_angle((x, y), previous_position) - 270
                rotated_ant_image = pygame.transform.rotate(ant_image, -angle)
                
                previous_positions[entity] = (x, y)
                
                rect = rotated_ant_image.get_rect(center=(x, y))
                screen.blit(rotated_ant_image, rect.topleft)

                # Render carried food
                if entity.inventory.contains('food'):
                    pygame.draw.circle(screen, GREEN, (x, y), 3)

        # Render food delivered counter
        text = font.render(f"Food delivered: {food_delivered}", True, BLACK, WHITE)  # Black text, white background
        text_rect = text.get_rect(center=(window_size[0] // 2, 20))  # Centered horizontally, 20 pixels from the top
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)  # 60 FPS
        await asyncio.sleep(0.01)

    pygame.quit()
