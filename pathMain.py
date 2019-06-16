from pathClasses import Point
from PIL import Image, ImageDraw
import re
from random import randint

# open file and store data in lines
file = open("elevation_small.txt")
lines = file.readlines()
file.close()
nest = []
paths = []

# creates a nice list of lists of the individual data points in each line, and removes newlines whilst doing so.
for l in lines:
    clean_line = l[0:(len(l)-1)]
    aline = clean_line.split(" ")
    anotherline = []
    if aline != []:
        for i in aline:
            if i != "":
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

img = Image.new('RGBA', (rows, columns), (0, 77, 64))
img.save("elevation_map_small.png")


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
    x = 1
    y = start_pt
    points_in_path = [(0, start_pt)]
    path_and_change = []
    total_change = 0
    current_elevation = nest[start_pt][0]
    while x < (columns - 2):
        # automatically goes straight forward if neither up-forward or down-forward has less change
        best_choice = (x, y)
        best_y = y 
        
        # checks if up-forward has less change than forward
        if abs((nest[y - 1][x] - current_elevation)) < abs(nest[y][x] - current_elevation):
            # even if up-forward is less than forward, down-forward may still have less change
            if y < (rows - 1) and abs(nest[y - 1][x] - current_elevation) > abs(nest[y + 1][x] - current_elevation):
                best_choice = (x, y + 1)
                best_y = y + 1
            else:
                best_choice = (x, y - 1)
                best_y = y - 1
        # if forward-up has greater or equal elevation change than forward, forward-down may have less change than forward
        elif y < (rows - 1) and abs(nest[y + 1][x] - current_elevation) < abs(nest[y][x] - current_elevation):
            best_choice = (x, y + 1)
            best_y = y + 1
        #sets the current elevation to the elevation at the point pathfinder chooses to move to
        total_change += abs(nest[best_y][x] - current_elevation)
        current_elevation = nest[best_y][x]
        y = best_y
        points_in_path.append(best_choice)
        print(best_choice)
        x += 1

    path_and_change.append(points_in_path)
    path_and_change.append(total_change)
    # stores each path with its total elevation change in paths
    paths.append(path_and_change)
    return points_in_path

# returns the path with the least elevation change
def path_least_change():
    best_path = paths[0]
    for path in paths:
        if path[1] < best_path[1]:
            best_path = path
    return best_path[0]



for x in range(rows):
    for y in range(columns):
        print(f"{x}/{rows - 1}")
        img.putpixel((x, y), (88, 214, 141, (int((nest[y][x] - min_elevation) / (max_elevation - min_elevation) * 255))))
img.save("elevation_map_small.png")


draw = ImageDraw.Draw(img)
for x in range(columns - 1):
    draw.line(pathfinder(x), fill=(243, 156, 18))
draw.line(path_least_change(), fill=(244, 67, 54), width=2)
print(paths)
img.save("elevation_small_paths.png")