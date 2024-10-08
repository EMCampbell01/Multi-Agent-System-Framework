import matplotlib.pyplot as plt
import asyncio

async def visualize_ant_simulation(environment, ants):
    plt.ion()
    fig, ax = plt.subplots()
    fig.suptitle("Ant Simulation")

    while True:
        
        ax.clear()
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.set_aspect('equal', adjustable='box')
        ax.set_xticks([])
        ax.set_yticks([])

        # Draw trails as thin green lines
        food_trail_entities = environment.state.get_entities_of_type('food trail')
        for trail in food_trail_entities:
            start = trail.position
            end = trail.data['end']
            ax.plot([start[0], end[0]], [start[1], end[1]], color='green', linewidth=0.5)

        # Plot ants as black dots
        for ant in ants:
            position = ant.state.get_position()
            ax.plot(position[0], position[1], 'ko')
            
        # Plot food as green dots
        food_entities = environment.state.get_entities_of_type('food')
        for food in food_entities:
            ax.plot(food.position[0], food.position[1], 'go')

        # Plot nest as brown square
        nest_entities = environment.state.get_entities_of_type('nest')
        for nest in nest_entities:
            ax.plot(nest.position[0], nest.position[1], '^', color='black', markersize=10)

        plt.draw()
        plt.pause(0.1)
        await asyncio.sleep(0.1)