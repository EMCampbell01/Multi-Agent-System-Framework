import os
import pygame
import math
import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from multi_agent_system_framework.environment.environment import Environment
    from multi_agent_system_framework.agent.agent import Agent

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set a scaling factor to make the visualization larger
SCALING_FACTOR = 7  # Increase this to make everything appear larger

# Function to calculate the angle of movement between two positions
def calculate_angle(position, previous_position):
    dx = position[0] - previous_position[0]
    dy = position[1] - previous_position[1]
    angle = math.degrees(math.atan2(dy, dx))  # Get the angle in degrees
    return angle

# Visualize ant simulation using Pygame
async def visualize_ant_simulation_py_game(environment: 'Environment'):
    pygame.init()

    # Scale the window size by the scaling factor
    window_size = (environment.size[0] * SCALING_FACTOR, environment.size[1] * SCALING_FACTOR)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Ant Simulation")

    # Use the os module to construct the relative paths for the images
    current_dir = os.path.dirname(__file__)
    background_image_path = os.path.join(current_dir, 'Dirt.png')  # Path to the background
    ant_image_path = os.path.join(current_dir, 'ant.png')  # Path to the ant image

    # Load the ant image as the window icon
    icon_image = pygame.image.load(ant_image_path)
    pygame.display.set_icon(icon_image)  # Set the ant image as the window icon

    # Load the background and ant images for the simulation
    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, window_size)

    ant_image = pygame.image.load(ant_image_path)
    ant_image = pygame.transform.scale(ant_image, (20, 20))  # Resize the ant image (adjust size as needed)

    previous_positions = {}  # Dictionary to store the previous positions of the ants

    # Font setup
    font = pygame.font.SysFont(None, 36)  # You can change font size if needed

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the background image
        screen.blit(background_image, (0, 0))

        # First, draw the trails (ensure trails are drawn first)
        for entity in environment.entities.values():
            if type(entity).__name__ == 'Item' and entity.item_type == 'trail':
                pos_1 = entity.position
                pos_2 = entity.data.get('food direction')
                if pos_1 and pos_2:
                    x_start, y_start = [coord * SCALING_FACTOR for coord in pos_1]
                    x_end, y_end = [coord * SCALING_FACTOR for coord in pos_2]
                    pygame.draw.line(screen, RED, (x_start, y_start), (x_end, y_end), 2)

        # Then, draw other entities like nests, food, and ants
        food_delivered = 0  # Default value
        for entity in environment.entities.values():
            if type(entity).__name__ == 'Item':
                
                if entity.item_type == 'ant nest':
                    x, y = [coord * SCALING_FACTOR for coord in entity.position]
                    pygame.draw.polygon(screen, BLACK, [(x-10, y+10), (x+10, y+10), (x, y-10)])
                    food_delivered = entity.data.get('food count', 0)  # Retrieve food delivered from the nest

                elif entity.item_type == 'food':
                    count = entity.inventory.get('food', 0)
                    x, y = [coord * SCALING_FACTOR for coord in entity.position]
                    pygame.draw.circle(screen, GREEN, (x, y), 5)
                    font = pygame.font.SysFont(None, 24)
                    text = font.render(str(count), True, BLACK)
                    screen.blit(text, (x + 10, y + 10))

            # Draw ants using the ant.png image, with rotation based on direction
            if type(entity).__name__ == 'AntAgent':
                x, y = [coord * SCALING_FACTOR for coord in entity.position]
                
                # Get the previous position of the ant to calculate direction
                previous_position = previous_positions.get(entity, (x, y))
                
                # Calculate the angle of movement
                angle = calculate_angle((x, y), previous_position) - 270  # Adjust by -90 degrees for proper orientation
                
                # Rotate the ant image to face the direction of movement
                rotated_ant_image = pygame.transform.rotate(ant_image, -angle)  # Negative angle for correct rotation
                
                # Update the previous position for the next frame
                previous_positions[entity] = (x, y)
                
                # Draw the rotated ant image centered at the position
                rect = rotated_ant_image.get_rect(center=(x, y))
                screen.blit(rotated_ant_image, rect.topleft)

                # If the ant has food, draw a small green circle
                if entity.inventory.contains('food'):
                    pygame.draw.circle(screen, GREEN, (x, y), 3)

        # Render "Food delivered" counter centered at the top of the screen
        text = font.render(f"Food delivered: {food_delivered}", True, BLACK, WHITE)  # Black text, white background
        text_rect = text.get_rect(center=(window_size[0] // 2, 20))  # Centered horizontally, 20 pixels from the top
        screen.blit(text, text_rect)

        # Update the display
        pygame.display.flip()

        # Frame rate limit and asyncio sleep for smooth animation
        clock.tick(60)  # 60 FPS
        await asyncio.sleep(0.01)

    pygame.quit()


