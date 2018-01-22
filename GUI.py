from graphics import *
import random


Point_01 = Point(100, 300)
Point_02 = Point(300, 300)
Point_03 = Point(300, 100)
Point_04 = Point(100, 100)

wall_A = [Point_01, Point_02] 
wall_B = [Point_02, Point_03]
wall_C = [Point_03, Point_04] 
wall_D = [Point_04, Point_01]

walls = [wall_A, wall_B, wall_C, wall_D]
Points = [Point_01, Point_02, Point_03, Point_04]

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
		wall = Line(wall[0], wall[1])
		wall.draw(canvas)


def move_left(wall):
	wall[0].x = wall[0].x + 20.0
	wall[1].x = wall[1].x + 20.0


def move_right(wall):
	wall[0].x = wall[0].x - 20.0
	wall[1].x = wall[1].x - 20.0


def move_up(wall):
	wall[0].y = wall[0].y + 20.0
	wall[1].y = wall[1].y + 20.0


def move_down(wall):
	wall[0].y = wall[0].y - 20.0
	wall[1].y = wall[1].y - 20.0	

def clear(canvas):
    for item in canvas.items[:]:
        item.undraw()
    win.update()

def main(walls, canvas):
	for i in range(0, 19):
		draw_walls(walls, canvas)
		move_a_wall(walls)
		
		time.sleep(1)
		clear(canvas)

	return (walls)

main(walls, win)

win.getMouse()
win.close()