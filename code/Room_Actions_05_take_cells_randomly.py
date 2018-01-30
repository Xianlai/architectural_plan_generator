from graphics import *
import pandas as pd
import ast
import random
from random import randrange
from itertools import groupby

#------read excel file generated by GH------#

raw_data = pd.read_excel("GH_To_Excel_Single_test_01.xlsx")

#add column for evaluation scores
#raw_data["score_01"] = 0
#raw_data["score_02"] = 0

#raw_data.to_csv("GH_To_Excel_10_edit.csv")

df = raw_data

number_of_room = 5
num_of_row = df.shape[0]
num_of_column = df.shape[1]
#print (num_of_row, num_of_column)


#------define cell class based on the "x, y" data read from excel------#

class Cell:
	# def __init__(self, x, y, size, options=["outline","width","fill"]):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		# self.pt = None
		# self.size = size
		# self.option = options

	#get the corner points
	def get_rec(self, size, x_offset, y_offset):
		top_left = Point(x_offset + self.x*size - size/2, y_offset + self.y*size - size/2)
		top_right = Point(x_offset + self.x*size + size/2, y_offset + self.y*size - size/2)
		bottom_left = Point(x_offset + self.x*size - size/2, y_offset + self.y*size + size/2)
		bottom_right = Point(x_offset + self.x*size + size/2, y_offset + self.y*size + size/2)
		rec = Rectangle(top_left, bottom_right)
		return rec

	#transfer x,y information to the point coordinates on screen
	def xy2point(x,y):
		pass


#------define cell class based on the "x, y" data read from excel------#
class Room:


	def __init__(self, cells, index):
		self.cells = cells
		self.i = index


	@property
	def area(self):
		num_cells = len(self.cells)
		return num_cells


	#------remove a cell from it's belonging room------#
	def remove_cell(self, cell):
		self.cells.remove(cell)
		return


	def wall_move_up(self):
		for cell in self.wall_top:
			new_cell = Cell(cell.x, cell.y-1)
			self.cells.append(new_cell)
		return self.cells


	def wall_move_down(self):
		for cell in self.wall_bottom:
			new_cell = Cell(cell.x, cell.y+1)
			self.cells.append(new_cell)
		return self.cells


	def wall_move_left(self):
		for cell in self.wall_left:
			new_cell = Cell(cell.x-1, cell.y)
			self.cells.append(new_cell)
		return self.cells


	def wall_move_right(self):
		for cell in self.wall_right:
			new_cell = Cell(cell.x+1, cell.y)
			self.cells.append(new_cell)
		return self.cells


	@property
	def wall_top(self):
		wall_top = []
		for cell in self.cells:
			if cell.y == self.min_y:
				wall_top.append(cell)
		return wall_top


	@property
	def wall_bottom(self):
		wall_bottom = []
		for cell in self.cells:
			if cell.y == self.max_y:
				wall_bottom.append(cell)
		return wall_bottom


	@property
	def wall_left(self):
		wall_left = []
		for cell in self.cells:
			if cell.x == self.min_x:
				wall_left.append(cell)
		return wall_left


	@property
	def wall_right(self):
		wall_right = []
		for cell in self.cells:
			if cell.x == self.max_x:
				wall_right.append(cell)
		return wall_right


	@property
	def all_x(self):
		all_x = []
		for cell in self.cells:
			x = cell.x
			all_x.append(x)
		return all_x


	@property
	def max_x(self):
		return max(self.all_x)


	@property
	def min_x(self):
		return min(self.all_x)


	@property
	def all_y(self):
		all_y = []
		for cell in self.cells:
			y = cell.y
			all_y.append(y)
		return all_y


	@property
	def max_y(self):
		return max(self.all_y)


	@property
	def min_y(self):
		return min(self.all_y)
	
		
def rooms_in_each_iteration(iteration):

	#iterate through each column(room), generate rooms and cells
	rooms_in_each_iteration = []
	for i in range(number_of_room):
		cells_in_each_room = []
		cells_parsing = ast.literal_eval(iteration[i])
		
		for j in range(len(cells_parsing)):
			x = cells_parsing[j][0]
			y = cells_parsing[j][1]
			cell = Cell(x, y)
			cells_in_each_room.append(cell)
			# print ("x = " + str(cell.x) + ", " + "y = " + str(cell.y))

		room = Room(cells_in_each_room, i)
		rooms_in_each_iteration.append(room)
#	print (rooms_in_each_iteration)
#	print (rooms_in_each_iteration[1].cells[0].x, rooms_in_each_iteration[1].cells[0].y)
	return rooms_in_each_iteration


#------get all cells for reference------#
def get_all_cells(rooms):
	all_cells = []
	for room in rooms:
		for cell in room.cells:
			all_cells.append(cell)
	return all_cells


#------compare cells if they are in the same location------#
def compare_cells(cell_1, cell_2):
	if (cell_1.x == cell_2.x and cell_1.y == cell_2.y):
		return True
	else: return False


def adjacent_cells(cell_1, cell_2):
	test_list = []
	test_list.append(cell_1.x == (cell_2.x - 1) and (cell_1.y == cell_2.y))
	test_list.append(cell_1.x == (cell_2.x + 1) and (cell_1.y == cell_2.y))
	test_list.append(cell_1.y == (cell_2.y - 1) and (cell_1.x == cell_2.x))
	test_list.append(cell_1.y == (cell_2.y + 1) and (cell_1.x == cell_2.x))
	if True in test_list:
		return True
	else: return False


#------to test a cell see if it's within the boundary------#
def cell_in_boudnary(cell_to_test, all_cells):
	test_list = []
	for cell in all_cells:
		test_list.append(compare_cells(cell_to_test, cell))
	if False in test_list:
		return False
	else: return True


#------pick a room------#
def pick_room(rooms):
	random_index = randrange(0, len(rooms))
	room_picked = rooms[random_index]
	del rooms[random_index]
	return room_picked


def draw_room(room, canvas):
	cell_in_room = get_all_cells([room])
	index = room.i
	# draw cells
	color = color_rgb(50*index, 255-50*index, 255-10*index)
	for cell in cell_in_room:
		rec = cell.get_rec(20, 100, 100)
		rec.draw(canvas)
		rec.setFill(color)


def pick_walls_from_cells(cells):
	walls = []

	pass



def expand_room(picked_room, other_rooms):

	cells_pr = get_all_cells([picked_room])

	cells_next_to_room = []
	count = 0
	for cell in cells_pr:
		for room in other_rooms:
			for cell_to_test in room.cells:
				if adjacent_cells(cell, cell_to_test):
					if random.choice([True, False, False, False, False]):
						picked_room.cells.append(cell_to_test)
						room.remove_cell(cell_to_test)
						count += 1
	print (str(count) + " cells has been updated")

	return


def iteration_action(all_rooms, canvas):

	# randomly pick a room for next step
	picked_room = pick_room(all_rooms)
	other_rooms = all_rooms
	cells_pr = get_all_cells([picked_room])

	time.sleep(1)

	expand_room(picked_room, other_rooms)
	draw_room(picked_room, canvas)

	all_rooms.append(picked_room)

	return all_rooms


#------evalutation each iteration------#
def evalutate_iteration(iteration):
	evalucate_area(iteration)
	pass

	def evalucate_area(iteration):
		pass

	def evalucate_aspect_ratio(iteration):
		pass

#------go through each iteration------#

for iteration in range(num_of_row):
	#TODO: do evalutation fuctions
	pass


def draw_cell(cell, canvas):
	rec = cell.get_rec()
	rec.draw(canvas)

def clear(canvas):
    for item in canvas.items[:]:
        item.undraw()
    win.update()


def main():
	#------initiate graphic window------#

	win_width = 500
	win_height = 500

	win = GraphWin("My Window", win_width, win_height)
	win.setBackground(color_rgb(255,255,255))


	#------working on one row/iteration------#
	iteration = df.iloc[(0)]
	# print (iteration)

	# get all rooms in current iteration
	all_rooms = rooms_in_each_iteration(iteration)
	# get all cells, this is also define the boudary for overall space
	all_cells = get_all_cells(all_rooms)

	for room in all_rooms:
		draw_room(room, win)

	for i in range(20):
		iteration_action(all_rooms, win)
		

	win.getMouse()
	win.close()
	

if __name__ == "__main__":
    main()

