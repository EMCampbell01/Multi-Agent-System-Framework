from typing import TYPE_CHECKING
import matplotlib.pyplot as plt
import asyncio

if TYPE_CHECKING:
    from multi_agent_system_framework.environment.environment import Environment
    from multi_agent_system_framework.agent.agent import Agent

async def visualize_ant_simulation(environment: 'Environment'):
    plt.ion()
    fig, ax = plt.subplots()
    fig.suptitle("Ant Simulation")

    while True:
        
        ax.clear()
        ax.set_xlim(0, environment.size[0])
        ax.set_ylim(0, environment.size[1])
        ax.set_aspect('equal', adjustable='box')
        ax.set_xticks([])
        ax.set_yticks([])
        
        # First, plot the trails (ensure trails are drawn first)
        for entity in environment.entities.values():
            if type(entity).__name__ == 'Item' and entity.item_type == 'trail':
                pos_1 = entity.position
                pos_2 = entity.data.get('food direction')
                if pos_1 and pos_2:
                    x_start, y_start = pos_1
                    x_end, y_end = pos_2
                    ax.plot([x_start, x_end], [y_start, y_end], 'r-', linewidth=1)
        
        # Then, plot other entities like nests, food, and ants
        for entity in environment.entities.values():
            if type(entity).__name__ == 'Item':
                
                if entity.item_type == 'ant nest':
                    x, y = entity.position
                    ax.plot(x, y, '^', color='black', markersize=10)
                    food_delivered = entity.data.get('food count')
                    ax.text(0, 0 + 0.9, (" Food delivered to nest: " + str(food_delivered)), fontsize=10, color='red', ha='left')

                elif entity.item_type == 'food':
                    count = entity.inventory.get('food')
                    x, y = entity.position
                    ax.plot(x, y, 'go')
                    ax.text(x + 0.1, y + 0.1, str(count), fontsize=10, color='black', ha='center')
                    
            # Plot ants as black dots
            if type(entity).__name__ == 'AntAgent':
                x, y = entity.position
                ax.plot(x, y, 'ko')
                if entity.inventory.contains('food'):
                    ax.plot(x, y, 'go', markersize=4)

        plt.draw()
        plt.pause(0.1)
        await asyncio.sleep(0.01)
