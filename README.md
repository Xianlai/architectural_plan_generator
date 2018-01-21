# NAR_Highrise plan:
In this project, we are trying to implement an algorithm to automate the process of highrise floor plan design *(just core area for now)*. 

**Inputs:**
  1. Bounding box of floor
  2. number of floors (to determine # of elevators)
  3. ceiling height (to dertermine # of runs for staircase)

**Outputs:**
  1. Walls including the location of end points, the opening type and location.
  2. Stats of each room including area, ratio, adjacency list etc.
  3. Stats of plan including area, maximun escaping distance, core area etc.

# Dataset Collecting Phase
The dataset are abstracted from human designed highrise floor plans.


# Function Model Learning Phase
In this phase, we make use of dataset and learn the statistical model of highrise plan in general.

### Function model
The function model is the joint distribution of all variables in our input dataset. For now, the variables are all discrete.


### The use of function model:
- The variables and their corresponding domains studied in this joint distribution will serve as the pool of random drawing when initiating states.

- this joint distribution will be used as part of objective function together with physical constraints and code constraints. A state has higher probability in this joint distribution will have a higher objective value.

**features:**
- room_description
- room_id
- room_type
- room_area
- room_car
- room_adjacentRoom
- room_adjacentType
- room_location *locate the room in the given bbox*
- room_n_sametype
- floor_id
- floor_bbox
- floor_area
- floor_ratio


# Plan Searching Phase

### Objectives
We want to generate a bunch of highrise floor plans that comply to function model, physical constraints, code constraints and financial benefits.

**Function model**:
As we said, the higher objective value will be assigned to a plan achieve higher probability in the joint distribution defined by function model.

**Physical constraints**:
- The walls should not overlapping or intrude into other rooms.
- The room should not exceed the bounding box of floor.
- to be added


**Code constraints**:
- maximum escaping distance
- minimum restroom area
- to be added


**Financial benefits**:
- The volumn of material
- The ratio of core versus floor
- Average distance from each room to elevator.
- To be added



The **final objective function** will be a weighted linear combination of these objective values.

### Instances
There are in total three types of objects -**wall, room and plan**- ordered from low to high level exist in plan searching phase.


#### Wall class:
**class** ```Wall(ends, rooms)```    
A wall object is identified by 2 end points, its opening and the 2 rooms it belongs to.

**Inputs:**
    - ends:
    - rooms:

**Attributes:**
    - Wall.id
    - Wall.ends : $[(x\_0, y\_0), (x\_1, y\_1)]$
    - Wall.rooms : which rooms(always 2 rooms) does this wall belong to
    - Wall.normal : The normal direction of wall
    - Wall.thickness : *not in use for now*
    - Wall.opening : \[type, location\]. 
        type $\in {0, 1, 2}$ corresponds to close, window, door.   
        location is the distance from first end point.

**Methods:**
    - add_thickness: add thickness based on wall type.


#### Room class:
**class** ```Room(type, id, walls)```  
A room is identified by a collection of walls. Wall is implemented in Wall class. When initializing, a room always starts from a 3 by 3 square consisted of 4 walls.

**Inputs:**
    - type: room type like hallway, service room, etc.
    - id: room id which should be the same as its index in walls list
    - walls: the walls enclose this room

**Attributes:**
    - walls: the walls it has.
    - type: room type
    - id: room id
    - stats: a dictionary of its properties like area, convexAspect, escapeDist, etc.
    - adjacency: adjacent rooms and corresponding types

**Methods:**
    - update_stats: update the stats of this room given walls


#### Plan class:
**class** ```Plan(type, id, walls)```  
A floor is identified by a collection of Room objects it contains. And it has some associated stats describing its properties like space efficiency, structure efficiency, escape distance etc.

**Inputs:**
    - rm_types: the types of rooms in function model
    - rm_nums: the initial numbers of rooms corresponding to each type. (this 
        number will change in search process)
    - silent: do not print out the searching process

**Attributes:**
- rooms
    Each plan has a list of m dictionaries corresponding to m types in typical highrise like the one below (m depends on how many types are found in learning dataset). Each dictionary contains a number of rooms of same type and could be empty.

```python
[{'type':'mr', 'rooms':[mr_00, mr_01, mr_02], 'number':3},
{'type':'wr', 'rooms':[wr_00, wr_01, wr_02, wr_03], 'number':4},
...]
```

- walls: A flat list of all wall objects. (for plotting)
- boundary: the boundary of plan area
- bbox: the bounding box of this plan
- stats: the stats of this plan
    The stats is consisting of 3 types of properties comes from 3 types of constraints:

    1. functional:
        + structureEfficiency
        + spaceEfficiency
        + ...
        
    2. code:
        + escapeDist
        + ...
    
    3. physical:
        + n_rooms_outOfBoundary
        + n_walls_overlap
- objective: calculated from stats and objective function

**Methods:**
The methods include 
- actions: changing the state of plans
    - swap_room: swap the id and type of 2 rooms
    - split_room(add_wall): add a wall somewhere in the middle
    - remove_room(remove_wall): remove a wall between 2 rooms
    - move_wall
    - move_opening
        move the location of opening on the wall.
    - change_opening
        change the opening type. Possible opening types: {0:'close', 1:'window', 2:'door'}
    - ...

- others: supporting funcitons
    - initialize: initialize the plan based on room types and numbers in functional model.
    - update_stats: Parse the state and return the stats
    - evaluate: Use the objective function to evaluate the stats and return the objective value.
    - plot: extract walls and openings from rooms and plot the plan
    - print_stats: print the stats



### Procedure:
1. **Initiate k plans:** The number of rooms in each type will be initiated with the mode of corresponding distribution. And the walls of these rooms will all be defaut(a 4X4 square).

2. **Find first k successors:** Find all successors result from possible moves and randomly choose one and evaluate against objective function until k successors better than current ones are found.

3. Repeat until stop criteria.

4. Restart l times.

5. Output l plans.





















