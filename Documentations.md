# Documentation for Modules in this project
As mentioned in readme file, there are 2 types of classes in this project: geometrical and non-geometrical. 

For geometrical instances, the attributes falls into 2 categories: 

- states:
    The attributes defines the current state of this object.
- stats:
    The attributes that describes the properties like area, objective value of this object. These attributes can be calculated from states attributes.

The methods also falls into 2 categories: 

- actions: 
    The methods change the states attributes.
- supporting methods
    The methods that generate stats from states.

____
## Wall class
The wall class implements the real-world wall objects. It has states attributes including the id, 2 end points, the opening, 2 rooms it belongs to, thickness, material etc. In the searching process, we will abstract it into a line with 1 id, 2 end points, 1 opening and 2 owning rooms. The other attributes will be implemented later when needed in other problems.

**class** ```Wall(id, ends, rooms)```

#### Parameters:     
- **id**: 
    The wall id 

- **ends**: 
    a list of 2 end points. The points should be in order (left, right) or (upper, lower).    

- **rooms**:   
    a list of 2 rooms 

#### Attributes:
- **``self.id``**: 
    The id should be the same as the index of this object in walls list.    

- **``self.ends``**: 
    `[(x0,y0),(x1,y1)]`

- **``self.rooms``**: 
    a list of rooms(always 2 rooms) this wall belongs to 

- **``self.opening``**: 
    `[type, location]`
    type $\in \{0,1,2\}$ corresponds to close, window, door. 
    location is the distance from first end point.

- **``self.type``**: 
    The wall type like glazing, dry wall etc.(Not in use for now.) 

- **``self.stats``**
    The stats of this wall is encoded as a dictionary. The keys include:
    + normalDir: The normal direction of wall
    + thickness: (Not in use for now.) 
    + material: (Not in use for now.) 


#### Methods: 
```python
- self.parse()
```

**``__init__(ends, rooms)``**  
    When initialize, the opening type is always 0 and location is 0.
    
**``parse()``**
    parse the states attributes to get stats attributes.


____
## Room class
The room class implements the real-world room objects. It has states attributes include the id, the enclosing walls, the room function etc. And stats attribtues include room area, convex aspect ratio, etc. When initializing, a room always starts from a 3 by 3 square consisted of 4 walls without openings.

**class** `Room(id, type, walls)` 

#### Parameters: 
- **id**: 
    room id which should be the same as its index in rooms list

- **function**: 
    room function like hallway, service room, etc.

- **walls**: 
    the walls enclose this room

#### Attributes:  
- **``self.id``**: 
    room id  

- **``self.function``**: 
    The room function 

- **``self.walls``**: 
    the walls enclose this room 

- **``self.stats``**: 
    The stats of this room is encoded as a dictionary. The keys include:
    + adjacency: adjacent rooms and corresponding types
    + area
    + convexAspect
    + escapeDist
    + center

#### Methods: 
```python
- self.parse()
```

**``__init__(id, function, walls)``**  

**``self.parse()``**      
    parse the stats of this room given states


-----
## Plan Class
The plan class implements the real-world plan objects. It has states attributes include the rooms in it , its boundary etc. And stats attribtues include total area, space efficiency etc.

**class** `Plan(rm_functions, rm_nums, silent=False)`  

#### Parameters:  
- **rm_functions**: 
    All the room functions exist in function model

- **rm_nums**: 
    the initial numbers of rooms corresponding to each function. (this 
number will change in search process)

- **silent**: 
    do not print out the searching process

#### Attributes: 
- **``self.rooms``**: 
    a list of rooms in this plan

- **``self.boundary``**: 
    the boundary of plan area

- **``self.stats``**: 
    The stats of this plan is encoded as a dictionary. The keys include:
    + rm_functions
    + rm_nums
    + walls: A flat list of all wall objects. (for plotting)
    + structureEfficiency
    + spaceEfficiency
    + escapeDist
    + n_rooms_outOfBoundary
    + n_walls_overlap
    + objective

#### Methods: 
```python
# Actions: changing the state of plans
- self._initialize()
- self.swap_rooms()   
- self.split_room()  
- self.remove_room()  
- self.move_wall()
- self.move_opening()   
- self.change_opening()  

# Supporting methods:
- self.parse()
- self.evaluate()
- self.plot()
- self.print_stats()
```

**``__init__(rm_functions, rm_nums, silent=False)``**  

**``initialize()``**    
    Initialize the plan with given room functions and numbers.

**``swap_rooms()``**    
    Awap the id and type of 2 rooms

**``split_room()``**  
    Add a wall somewhere in the middle of a room. 

**``remove_room()``**  
    Remove a wall between 2 rooms

**``move_wall()``**  
    There are multiple situations in this action  

**``move_opening()``**  
    move the location of opening on the wall. 

**``change_opening()``**    
    change the opening type. Possible opening types: 
    `{0:’close’, 1:’window’, 2:’door’}`
 

**``parse()``**    
    Parse the state and return the stats

**``evaluate()``**    
    Use the objective function to evaluate the stats and return the objective value.

**``plot()``**    
    Plot the rooms' tags, walls and openings.

**``print_stats()``**    
    print the stats



____
## Objectives class
objective function and constraints


____
## FunctionModel class
function model learned from function model learning part.


