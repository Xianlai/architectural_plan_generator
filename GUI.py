from graphics import *
import random

point_00 = Point(100, 300)
point_01 = Point(300, 300)
point_02 = Point(300, 100)
point_03 = Point(100, 100)

class Wall(Point):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.type = str("Living Room")
        ##self.length = ((p1.x-p2.x)^2+(p1.y-p2.y)^2)^0.5


wall_00 = Wall(point_00, point_01)
wall_01 = Wall(point_01, point_02)
wall_02 = Wall(point_02, point_03) 
wall_03 = Wall(point_03, point_00)

room_type = ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Corridor"]
room_00 = [wall_00, wall_01, wall_02, wall_03, room_type[1]]

walls = [wall_00, wall_01, wall_02, wall_03]
points = [point_00, point_01, point_02, point_03]
rooms = [room_00]

#create graphic window:
win = GraphWin("My Window", 500, 500)
win.setBackground(color_rgb(255,255,255))

def move_a_wall(walls):
	#random pick a wall from the list:
	the_wall = random.choice(walls)
	i = walls.index(the_wall)

	#to understand if the wall is along x or y:
	if i%2 == 0:
		random.choice([move_up, move_down])(the_wall)
	else:
		random.choice([move_left, move_right])(the_wall)	

	walls[i] = the_wall
	return (walls)


def draw_walls(walls, canvas):

	for wall in walls:
		wall = Line(wall.p1, wall.p2)
		wall.draw(canvas)


def move_left(wall):
	wall.p1.x = wall.p1.x + 20.0
	wall.p2.x = wall.p2.x + 20.0


def move_right(wall):
	wall.p1.x = wall.p1.x - 20.0
	wall.p2.x = wall.p2.x - 20.0


def move_up(wall):
	wall.p1.y = wall.p1.y + 20.0
	wall.p2.y = wall.p2.y + 20.0


def move_down(wall):
	wall.p1.y = wall.p1.y - 20.0
	wall.p2.y = wall.p2.y - 20.0	

def clear(canvas):
    for item in canvas.items[:]:
        item.undraw()
    win.update()

def main(walls, canvas):
	for i in range(0, 9):
		draw_walls(walls, canvas)
		move_a_wall(walls)
		
		time.sleep(1)
		clear(canvas)

	return (walls)

main(walls, win)

win.getMouse()
win.close()