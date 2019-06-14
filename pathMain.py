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
    nest.append(aline)
    


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
            pt = Point((x, y), val)
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
img.save("elevation_map.png")


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

def get_multiplier(val):
    """returns a float between 0 and 1 that will be used for the A value for a pixel"""
    return int((int(val) - min_elevation) / (max_elevation - min_elevation) * 255)

for x in range(rows):
    for y in range(columns):
        print(f"{x}, {y}")
        img.putpixel((x, y), (30, 132, 73, get_multiplier(from_index_get_val((x, y)))))
img.save("elevation_map.png")


