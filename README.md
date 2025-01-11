# Multi-Agent System Framework
**Development Status: Ongoing**

## Overview
The Multi-Agent System Framework provides the building blocks to create a multi-agent system. Enables the creation of multiple agents that interact with each other and a shared environment. Agents act independently, and run asynchronously. Can be used as a foundation for a number of MAS projects.

[Watch the demo on YouTube](https://www.youtube.com/watch?v=mkvSidTgCdE)

## Core Components
The core components of this framework are:
- Environment
- Agents
- Items

(Agents and Items are collectively reffered to as *'entities'*)

# Environment

**Environment**

The environment is an object which represents an environment, and data that agents exist within and interact with.

# Agents

**Agent**

The Agent class is an abstract class that contains the basic outline of any Agent instance. The class contains the basic attributes for all child agents:

- id: A unique id generated on its Instantiation.
- running: A boolean representing if the agent is currently running its process loop.
- environment: A reference to the environment instance the agent exists within.
- process_delay: The time in seconds between each iteration of the main process loop. A lower value creates a faster-acting agent.

Agent instances are not intended to be created directly via this abstract class, instead, the *create_agent* class method should be used with an AgentBlueprint

Agents can only exist in the context of an environment, and require a reference to the environment object on their creation to be stored.

The agent is run by calling *run*. This executes a loop infinitely until *stop_running* is called. This loop calls the process function every n seconds, where n is *process_delay*. In the Agent class, the *process* function is empty and serves only as a placeholder, it will be overridden in its child classes to provide behavior for the agent.  

**Agent Creation**

To create an Agent instance, first, a AgentBlueprint must be defined. Agent blueprints serve as a representation of an Agent child class that can be created via the *create_agent* class method. A blueprint only requires the basic attributes of the Agent class:

- agent_type: used to name the child class.
- process: the callable function to overwrite the agent base class *process* method.
- environment: reference to the agent's environment object

Example - Creates a HelloWorldAgent:
```python
    def hello_world():
        print('hello world')

    hello_world_agent_bp = AgentBlueprint(
        agent_type = 'HelloWorld',
        process = hello_world,
        environment = environment,
    )

    hello_world_agent = Agent.create_agent(hello_world_agent_bp, environment)
```
This example creates a simple agent instance, an agent with no state, that does not interact with its environment, and solely prints "hello world" every second.

Agents have additional attributes which are empty by default. Additional attributes:

- Position
- Data
- Process Delay

**Agent Sub-Components**

- Inventory
- Memory
- Clock

# Items

**Item**

Items represent basic entities that exist within an environment. 
They may store state but do not have their own behaviour. They are acted upon by agents

## Demos

**Ant Simulation**

[Watch the demo on YouTube](https://www.youtube.com/watch?v=mkvSidTgCdE)

## Requirements

## Running
