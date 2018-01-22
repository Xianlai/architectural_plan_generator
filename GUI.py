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

def random_move_x(point):
	point.x = point.x + 5.0

def random_move_y(point):
	point.y = point.y + 5.0	

def move_a_wall(walls):
	#random pick a wall from the list:
	the_wall = random.choice(walls)
	i = walls.index(the_wall)

	#random move the end points of the wall:	
	random.choice([random_move_x, random_move_y])(the_wall[0])
	random.choice([random_move_x, random_move_y])(the_wall[1])

	walls[i] = the_wall

	return (walls)


def draw_walls(walls, canvas):

	for wall in walls:
		wall = Line(wall[0], wall[1])
		wall.draw(canvas)


def main(walls, canvas):
	for i in range(0, 9):
		move_a_wall(walls)
		draw_walls(walls, canvas)
		
		time.sleep(1)

	return (walls)

main(walls, win)

win.getMouse()
win.close()