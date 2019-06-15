from pathClasses import Point
from PIL import Image
import re

# open file and store data in lines
file = open("elevation_small.txt")
lines = file.readlines()
file.close()
nest = []

# creates a nice list of lists of the individual data points in each line, and removes newlines whilst doing so.
for l in lines:
    clean_line = l[0:(len(l)-1)]
    aline = clean_line.split(" ")
    anotherline = []
    for i in aline:
        anotherline.append(int(i))
    nest.append(anotherline)
    


def init_data(nest):
    """takes data from nested list, 
    initializes each data pt as a Point object,
    adds each of these objects to a list,
    returns the list"""
    data = []
    y = 0
    for row in nest:
        x = 0
        for val in row:
            pt = Point((x, y), int(val))
            data.append(pt)
            x +=1
        y += 1
    return data

def from_index_get_val(index):
    for o in data:
        if o.pt == index:
            return o.val




data = init_data(nest)
rows = len(nest)
columns = len(nest[0])

img = Image.new('RGBA', (rows, columns), 'white')
img.save("elevation_map2.png")


# finds the lowest and highest elevation in the field
min_elevation = data[0].val
max_elevation = data[0].val
for o in data:
    if o.val < min_elevation:
        min_elevation = o.val
    elif o.val > max_elevation:
        max_elevation = o.val
max_elevation = int(max_elevation)
min_elevation = int(min_elevation)


def pathfinder(start_pt):
    """takes a starting y value.
    from there, finds the lowest elevation out of (x+1, y-1), (x+1, y), and (x+1, y+1).
    steps to that point and repeats the process"""
    x = 0
    points_in_path = [(0, start_pt)]
    y = start_pt
    while x < columns:
        best_choice = (x + 1, y)
        if from_index_get_val((x + 1, y - 1)) < from_index_get_val(best_choice):
            best_choice = (x +1, y - 1)
            y = y - 1
        elif from_index_get_val((x + 1, y + 1)) < from_index_get_val(best_choice):
            best_choice = (x + 1, y + 1)
            y = y + 1
        points_in_path.append(best_choice)
        x += 1
    return points_in_path

# class Path:
#     def __init__(self, list_indexes, total_change):
#         self.list_indexes = list_indexes
#         self.total_change = total_change

#     def get_total_change(self):
#         change = 0
#         index = 0
#         for i in list_indexes:
            

# apath = Path(pathfinder(start_pt), <elevation_change_for_path>


for x in range(rows):
    for y in range(columns):
        print(f"{x}, {y}")
        img.putpixel((x, y), (30, 132, 73, (int((nest[y][x] - min_elevation) / (max_elevation - min_elevation) * 255))))
img.save("elevation_map2.png")



