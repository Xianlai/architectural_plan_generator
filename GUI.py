from graphics import *
import copy
import random
import math


class Wall:
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2


	def wall_len(p1, p2):
		length = math.sqrt(math.pow(p2.x - p1.x, 2) + math.pow(p2.y - p1.y, 2))
		return length


	def wall_xy(p1, p2):
		if (p1.x == p2.x):
			wall_xy = "vertical"
		elif (p1.y == p2.y):
			wall_xy = "horizontal"
		else:
			wall_xy = "diagonal"
		return wall_xy


	def wall_move_type(self):
				
		return random.choice(["0", "1", "2"])


class Room:
	def __init__(self, walls, room_type):
		self.walls = walls
		self.type = room_type
#		self.area = calculate_room_area(self)

	"""
	walls is a list that contents all walls that enclose this room IN ORDER(conterclockwise, from bottom)
	room_types is a list that that contents types of the wall as strings
	"""

	def calculate_room_area(room):
		walls = room.walls
		area = 0.0
		for wall in walls:
			area = 0.5 * abs(wall.p1.x*wall.p2.y - wall.p2.x*wall.p1.y)
			area += area
		return area


#starting points
point_00 = Point(100, 300)
point_01 = Point(300, 300)
point_02 = Point(300, 200)
point_03 = Point(300, 100)
point_04 = Point(100, 100)
point_05 = Point(100, 200)

#create walls using Wall Class
wall_00 = Wall(point_00, point_01)
wall_01 = Wall(point_01, point_02)
wall_02 = Wall(point_02, point_03) 
wall_03 = Wall(point_03, point_04)
wall_04 = Wall(point_04, point_05)
wall_05 = Wall(point_05, point_00)
wall_06 = Wall(point_05, point_02)

#default values for room types in list
room_types = ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Corridor"]

#create rooms using Room Class
room_00 = Room([wall_00, wall_01, wall_06, wall_05], room_types[1])
room_01 = Room([wall_06, wall_02, wall_03, wall_04], room_types[2])

#create lists for points, walls and rooms
points = [point_00, point_01, point_02, point_03, point_04, point_05]
walls = [wall_00, wall_01, wall_02, wall_03, wall_04, wall_05, wall_06]
rooms = [room_00, room_01]

#create graphic window:
win = GraphWin("My Window", 500, 500)
win.setBackground(color_rgb(255,255,255))


def move_a_wall(walls):

	#random pick a wall from the list:
	the_wall = random.choice(walls)
	i = walls.index(the_wall)
	j = the_wall.wall_move_type()

	move_types[str(j)](the_wall)
	print (the_wall.wall_xy)


	return (walls)

		#try to go through each type of move, until it's working
# 		for j in range(3):
# 			move_types[str(j)](the_wall)
# 			walls[i] = the_wall

# 			#test if this step cause any problem:
# 			if(test_a_move(walls)):
# 				walls[i] = the_wall
# 				print(str(test_a_move(walls)))
# 				loop = False
# 				print("test success, exit loop")
# 				break
# 			else:
# 				#UNDO previous move
# 				print ("will try some other type of move")
# 				continue

# 			if(j == 2):
# 				print ("faile to operate all types of moves, will select another wall.")
# 				count_down -= 1
# 					del pickable_walls[i]

# 		if (count_down == 1):	
# 			loop = False
# 			print("nothing to select from, exit loop")


#test out if previous move cause any "diagonal" wall
# def test_a_move(walls):

# 	wall_test_list = []

# 	for wall in walls:
# 		if (wall.wall_xy != "diagonal"):
# 			wall_test = False			
# 		else:
# 			wall_test = True
# 		wall_test_list.append(wall_test)

# 	#print out the test result as a list
# 	print ('[%s]' % ','.join(map(str, wall_test_list)))

# 	if all(wall_test_list):
# 		return True
# 	else:
# 		return False


def move_type_00(wall):
	print("operate move_type_00")
	if (wall.wall_xy == "horizontal"):
		random.choice([move_U_typ_00, move_D_typ_00])(wall)
	elif(wall.wall_xy == "vertical"):
		random.choice([move_L_typ_00, move_R_typ_00])(wall)
	else:
		random.choice([move_L_typ_00, move_R_typ_00, move_U_typ_00, move_D_typ_00])(wall)
		return	


def move_type_01(wall):
	print("operate move_type_01")
	if (wall.wall_xy == "horizontal"):
		random.choice([move_U_typ_00, move_D_typ_00])(wall)
	elif(wall.wall_xy == "vertical"):
		random.choice([move_L_typ_00, move_R_typ_00])(wall)
	else:
		random.choice([move_L_typ_00, move_R_typ_00, move_U_typ_00, move_D_typ_00])(wall)
		return
	

def move_type_02(wall):
	print("operate move_type_02")


def move_L_typ_00(wall):
	wall.p1.x = wall.p1.x + 20.0
	wall.p2.x = wall.p2.x + 20.0


def move_R_typ_00(wall):
	wall.p1.x = wall.p1.x - 20.0
	wall.p2.x = wall.p2.x - 20.0


def move_U_typ_00(wall):
	wall.p1.y = wall.p1.y + 20.0
	wall.p2.y = wall.p2.y + 20.0


def move_D_typ_00(wall):
	wall.p1.y = wall.p1.y - 20.0
	wall.p2.y = wall.p2.y - 20.0	

#define a dictionary dispatcher to test through different types of moves
move_types = {'0': move_type_00, '1': move_type_01, '2': move_type_02}


def draw_walls(walls, canvas):

	for wall in walls:
		wall = Line(wall.p1, wall.p2)
		wall.draw(canvas)


def clear(canvas):
    for item in canvas.items[:]:
        item.undraw()
    win.update()


def main(room, walls, canvas):
	for i in range(0, 29):
		draw_walls(walls, canvas)
		move_a_wall(walls)

		area = room.calculate_room_area()

		text1 = Text(Point(350,400), "Room Area is " + str(area))
		text1.setSize(9)
		text1.draw(win)
		
		time.sleep(0.5)
		clear(canvas)

	return (walls)

main(room_00, walls, win)


win.getMouse()
win.close()