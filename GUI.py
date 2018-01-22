from graphics import *

def main():

	win = GraphWin("My Window", 500, 500)
	win.setBackground(color_rgb(255,255,255))

	Point_01 = Point(100, 300)
	Point_02 = Point(300, 300)
	Point_03 = Point(300, 100)
	Point_04 = Point(100, 100)

	wall_A = Line(Point_01, Point_02) 
	wall_B = Line(Point_02, Point_03) 
	wall_C = Line(Point_03, Point_04) 
	wall_D = Line(Point_04, Point_01) 

	walls = [wall_A, wall_B, wall_C, wall_D]
	Points = [Point_01, Point_02, Point_03, Point_04]

	for wall in walls:
		wall.draw(win)

	win.getMouse()
	win.close()

main()