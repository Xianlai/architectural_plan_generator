# Architectural Plan Generator
In this project, we are trying to implement an agent to automate the process of architectural plan design. The agent could be used in different scales from a apartment to a urban design. And can be used in a nested way. For example, we can first use it to generate boundaries of apartments for a residential floor plan and then use it for layouts inside apartment as well.

# Synopsis
This project is consisted of 4 phases or problems: **datasets collecting**, **criteria learning/encoding**, **objective function learning** and finally **searching**.

- **Datasets collecting**
    Encode datasets and features from human designed architectural plans.

- **Criteria learning/encoding**
    We have 2 types of criteria: 
    - one kind is **uncertain ones** like the area, adjacency, connecting etc which are not obvious which value is the best. The best value depends on the values of all other uncertain criteria. This type of criteria should be learned.
    
    - The other kind is **centain ones** like space efficiency, regulation which it's obvious. For example, the bigger efficiency, the better; it's better to satisfy the regulation. This type of criteria can be encoded.

- **Objective function learning**
    Then we use linear combination of the criteria learned or encoded above to evaluate the state of plan and produce a score that can be used to guide the search process. But we still need to learn the weights.

- **Searching** 
    Initialize a plan and then strategically change the state by apply actions like expand, split, merge, swap rooms etc to achieve a better score calculated by objective function.

# Dataset Collecting
pass

# Criteria Learning and Encoding
## Uncertain Criteria
The uncertain part of those criteria can be learned from datasets collected in the first phase. The result is a joint distribution called function model contains the probabilities of combinations of random variables like room type, room area, room adjacency etc. 

### The use of function model:
The variables and their corresponding domains studied in this joint distribution can serve as the pool of random drawing when initiating states.

This joint distribution will be used as part of objective function together with physical constraints and code constraints. A state has higher probability in this joint distribution will have a higher objective value.

Possible random variables:
    + room_type
    + room_area
    + room_car
    + room_adjacentRoom
    + room_adjacentType
    + room_location locate the room in the given bbox
    + room_n_sametype
    + floor_bbox
    + floor_area
    + floor_ratio

## Certain Criteria
The rest can be encoded by human designers using domain knowledge. At this point of time, we temporarily skip the data collecting phase and encode all the criteria manually.

In general, we use 3 types of certain criteria:
- **Physical constraints:**
    - The walls should not overlapping or intrude into other rooms.
    - The room should not exceed the boundary of plan.(heavy penalty)
    - to be added

- **Regulational requirements:**
    + maximum escaping distance
    + minimum restroom area
    + to be added

- **Financial benefits:**
    + The volumn of material
    + The ratio of core versus floor
    + Average distance from each room to elevator.
    + To be added


# Objective function learning
The final objective function will be a weighted linear combination of these objective values. The weightings vary. For some hard constraints like regulational one and physical ones, we should assign a high weighting to them so the agent will satisfy them prior to other soft constraints like area, space efficiency. 


# Searching
Given the objective function, we want to find a plan state with high objective value. We can use different searching strategies in local search domain.

# Script Files

**architectural_plan_generator.py**: This is the entry point of this project. Run this file to get agent started.

- **Geometrical Classes:**  
    - **Plan.py**: The file implements plan objects and associated methods.
    - **Room.py**: The file implements room objects and associated methods. 
    - **Grid.py**: The file implements grid objects and associated methods
    - **Wall.py**: The file implements wall objects and associated methods

- **Non-geometrical Classes**  
    - **ObjectiveFunction.py**: objective function and constraints
    - **FunctionModel.py**: function model learned from criteria learning part.
    - **Transition.py**: the class implements the transition model and available actions.


For details of classes, see [Documentations](https://github.com/Xianlai/architectural_plan_generator/blob/Xianlai/Documentations.md)

















