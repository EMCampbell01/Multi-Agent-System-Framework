# Multi-Agent System Framework
**Development Status: Ongoing**

## Overview
The Multi-Agent System Frameworks provides the building blocks to create a multi-agent system. Enables the creation of multiple agents which interact with each other and a shared environment. Agents act independantly, and run asyncronously. Can be used as a foundadtion for a number of MAS projects such as simulations, distributed problem solving, and IOT systems.

## Core Components
The core components of this framework are:
- Agent
- Environment
- Entities

# Agents

**Agent**
The Agent class is an abstract class that contains the basic outline of any Agent instance. The class contains the basic attributes for all child agents:

- id: A unique id generated on its Instanciation.
- running: A boolean representing if the agent is currently running its process loop.
- environment: A reference to the environment instance shared by all agents.
- state: An AgentState object for managing the agents state.
- sleep_time: The time in seconds between each itteration of the main process loop.

Agent instances are not intended to be created directly via this abstract class, instead the *create_agent* function should be used with an AgentBlueprint

Agents can only exist in the context of the environment, and require a reference to the environment object on their creation to be stored.

The agent is run by calling *run*. This excecutes a loop infinitely until *stop_running* is called. This loop calls the process function every n seconds, where n is *sleep_time*. In the Agent class, the *process* function is empty, and serves only as a placeholder, it will be overriden in its child classes to provide behaviour for the agent.  

**Agent Creation**
To create an Agent instance, first a AgentBlueprint instance should be created. Agent blueprints serve as representation of a Agent child class that can be created via *create_agent*. A blueprint only requires the basic attributes of the Agent class, an attributes dict for the agents state, and a Callable to override *process*. 

Example:
```python
    def hello_world():
        print('hello world')

    hello_world_agent_bp = AgentBlueprint(
        agent_type='HelloWorld',
        process=hello_world,
        sleep_timer=15,
        environment=environment,
        attributes={},
    )

    hello_world_agent = create_agent(hello_world_agent_bp_bp, environment)
```
This example creates a simple agent instance, an agent with no state, that does not interact with its environment, and solely prints "hello world" every 15 seconds.

**Agent State**
An agents state is represented by a AgentState data class object. The only required sub-component of a AgentState is *atttributes*. This is a dict for holding any general data related to an agent.

Additional agent state sub-components can be included optionally. 

- memory: only stores up to a certain volume of data, before replacing oldest input data with newest input data.
- inventory: a dict where each key represents an item held by the agent, and its value the number this item it holds.
- positon: a tuple representing the agents position as an x,y coordinate.

These sub-components are more constrained, but the AgentState class provides methods for working with them 

# Environment

# Entities

## Demo

## Requirements

## Running
