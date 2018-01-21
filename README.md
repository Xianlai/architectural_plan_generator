# Architectural Plan Generator
In this project, we are trying to implement an algorithm to automate the process of architectural plan design. The plan could be the whole floor plan or a portion like an apartment or the core area of highrise.

# Synopsis
This project is consisted of 4 parts or problems: datasets collecting, function model learning, objective function learning and searching.

- **Datasets collecting**
    Encode datasets for learning function model from plans designed by human designers.

- **Function model learning**
    Learn a joint distribution called function model from given datasets. The function model contains the probabilities of combinations of random variables like room type, room area, room adjacency etc.

- **Objective function learning**
    Learn the objective function which is a weighted combination of criteria. Besides function model, we use 3 types of other criteria:
    - financial ones like space efficiency, 
    - regulational ones like escape distance,
    - physical ones like number of rooms outside boundary.

- **Searching** 
    initialize a plan and change the state by apply actions like move wall, split room etc. to fit rooms into given boundary.

**Outputs:**
1. Walls including the location of end points, the opening type and location.
2. Stats of rooms including area, ratio, adjacency list etc.
3. Stats of plan including area, maximun escaping distance, core area etc.
4. Objective value

# Dataset Collecting:
The dataset are abstracted from human designed floor plans.


# Function model learning:
In this phase, we make use of dataset and learn the function model of similar plans. The function model is the joint distribution of all variables in our input dataset. For now, the variables are all discrete.

### The use of function model:
The variables and their corresponding domains studied in this joint distribution will serve as the pool of random drawing when initiating states.

this joint distribution will be used as part of objective function together with physical constraints and code constraints. A state has higher probability in this joint distribution will have a higher objective value.

features:
- room_description
- room_id
- room_type
- room_area
- room_car
- room_adjacentRoom
- room_adjacentType
- room_location locate the room in the given bbox
- room_n_sametype
- floor_id
- floor_bbox
- floor_area
- floor_ratio



# Objective function learning
**Function model:**
As we said, the higher objective value will be assigned to a plan achieve higher probability in the joint distribution defined by function model.

**Physical constraints:**
- The walls should not overlapping or intrude into other rooms.
- The room should not exceed the boundary of plan.(heavy penalty)
- to be added

**Regulational requirements:**
- maximum escaping distance
- minimum restroom area
- to be added

**Financial benefits:**
- The volumn of material
- The ratio of core versus floor
- Average distance from each room to elevator.
- To be added

The final objective function will be a weighted linear combination of these objective values.


# Searching
Given the objective function(contains function model, all kinds of constraints for this problem like boundary, local regulations etc.), we want to generate（search for） a plan with high objective value.

### Classes
We represent the instances in this problem as follow:

- **Geometrical Instances:**  
    - **Plan class**: a collect of rooms and some stats. 
    - **Room class**: a collect of walls and some stats. 
    - **Walls**: 2 end points, a opening and some wall properties

- **Non-geometrical Instances**  
    - **Objective class**: objective function and constraints
    - **FunctionModel class**: function model learned from function model learning part.

For geometrical instances, the attributes falls into 2 categories: states and stats. The methods also falls into 2 categories: actions that change the states and supporting methods that generate stats from states.


### Procedure:
- **Initiate k plans:** 
    The number of rooms in each type will be initiated with the mode of corresponding distribution. And the walls of these rooms will all be defaut(a 4X4 square).

- **Find first k successors:** 
    Find all successors result from possible moves and randomly choose one and evaluate against objective function until k successors better than current ones are found.

- **Repeat until stop criteria.**

- **Restart l times.**

- **Output l plans.**















