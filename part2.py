import math
import matplotlib.pyplot as plt
import ast 

# Defining some functions to be used later

# Distance between 2 points a and b
def dist(a,b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

# Checking Intersection of 2 line segments 
def intersect(a,b,c,d):
    # If the 3rd point c(coinciding with d in this case) lies on the line joining a and b
    if c==d:
        if round(dist(a,c),2) + round(dist(b,c),2) == round(dist(a,b),2):
            return True,c
        return False,[]
    a1 = b[1] - a[1]
    b1 = a[0] - b[0]
    c1 = a1*(a[0]) + b1*(a[1])
    
    a2 = d[1] - c[1]
    b2 = c[0] - d[0]
    c2 = a2*(c[0])+ b2*(c[1])
    
    determinant = a1*b2 - a2*b1
    
    #Check for parallel lines, if parallel, they dont Intersect
    if determinant == 0:  
        return False,[] 
        
    # If not parallel, lines will definately intersect, now check if
    # Line segments are intersecting by checking bounds of Intersection
    else:
        x = (b2*c1 - b1*c2)/determinant; 
        y = (a1*c2 - a2*c1)/determinant; 
        if x <= max(a[0],b[0]) and x >= min(a[0],b[0]):
            if y <= max(a[1],b[1]) and y<=max(c[1],d[1]) and y >= min(a[1],b[1]) and y>=min(c[1],d[1]):
                return True,[x,y]
    return False,[]

# To check if a point is inside the given Polygon
# Source: 
def point_inside_polygon(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        c=[x,y]
        a=[p1x,p1y]
        b=[p2x,p2y]
        if round(dist(a,c),1) + round(dist(b,c),1) == round(dist(a,b),1):
            return True
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside
    
    
yesno = input("Do you want to proceed with the layer achieved from previous code for rectilinear area fill (y/n) : ")

# Use Layer data as polygon from Previous data
if yesno == "y" or yesno == "Y":
  fil2 = open("layer_data.txt","r") 
  data = fil2.read() 
  segments = ast.literal_eval(data) 

# Manually Enter Points of New Polygon
elif yesno == "n" or yesno == "N":
  inputcoords = [int(x) for x in input("Enter coordinates of Polygon as x1 y1 x2 y2 x3 y3 ...: ").split()]
  tp = []
  segments = []
  for i in range(0,len(inputcoords),2):
    tp.append([inputcoords[i],inputcoords[i+1]])
  for i in range(len(tp)):
    segments.append([tp[i%len(tp)],tp[(i+1)%len(tp)]])

# Error in inputing y/n
else:
  print("Keystroke of y/n not recognised, proceeding with sample points")    
  segments = [[[0,0],[10,0]],[[10,0],[5,5]],[[5,5],[10,10]],[[10,10],[0,10]],[[0,10],[0,0]]]

points=[i[0] for i in segments]
xs=[i[0] for i in points]

# Defining the Increment value
print("Approximate x dimension is " + str(max(xs) - min(xs)))
delta = input("Enter the Increment value: ")



# Define a Dictionary with key as the x and the values as all the points on the boundary
# at that particular x
dictt={}

# Calculate the Starting point for the toolpath
i=min(xs)
while i <= max(xs):
    for each in segments:
        check,point=intersect(each[0],each[1],[i,each[0][1]],[i,each[1][1]])
        if check:            
            dictt[i]=dictt.get(i,[])+[point]
    i+=float(delta)


# Sort the Dictionary based on x values
finalsort=list(dictt.items())
finalsort.sort(key=lambda x: x[0])

# Define all the points of intersection of rectilinear path with boundary
snake=[]
count=0

# Alternate the Toolpath every round by inverting the intersection points
for i in finalsort:
    lis=i[1]
    lis.sort(key=lambda x: x[1])
    if count%2==0:
        snake.append(lis)
    else:
        snake.append(lis[::-1])
    count+=1

# Setting the Final Coordinates of toolpath in order and also check for concavity
draw=[]
prev=None
for i in snake:
    if len(i)>1:
        for j in range(len(i)-1):
            # The line segment drawn, if its midpoint lies inside, it should be printed
            if point_inside_polygon(i[j][0],(i[j][1]+i[j+1][1])/2,points):
                if prev is not None:
                    if prev[1][0]!=i[1][0] and prev[0]=="G1":
                        draw.append(["G1",prev[2],i[j]])
                draw.append(["G1",i[j],i[j+1]])

            # If the midpoint of the segment lies outside, that segment should not be printed, but traversed    
            else:
                draw.append(["G0",i[j],i[j+1]])
            prev=draw[-1]
    else:
        # Same conditions as above but if segment is a point or a tangent to the polygon
        if point_inside_polygon(i[0][0],i[0][1],points):
            draw.append(["draw",i[0],i[0]])
            if prev is not None:
                    if prev[1][0]!=i[0][0] and prev[0]=="draw":
                        draw.append(["G1",prev[2],i[0]])
        else:
            draw.append(["G0",i[0],i[0]])
        prev=draw[-1]

print("Red is Printing Toolpath (G1) and Blue is Rapid Transverse no printing (G0)")

fig,ax = plt.subplots(figsize=(10, 10)) 
for i in draw:
    if i[0]=="G1":
        ax.plot([i[1][0],i[2][0]], [i[1][1],i[2][1]], c ="red")
    else:
        ax.plot([i[1][0],i[2][0]], [i[1][1],i[2][1]], c ="blue")

ax.set_aspect('equal')
ax.set_title("Visualisation of The Toolpath")
fig.savefig("Toolpath.jpg")
plt.show()


new = []
for i in range(len(draw)):
    new.append([draw[i][0], 'X', round(draw[i][2][0],3), 'Y' , round(draw[i][2][1],3)])

filetoolpath = 'toolpath.gcode'
file = open(filetoolpath, "w")
file = open(filetoolpath, "a")
for i in range(len(draw)):
    file.write(str(draw[i][0]) + " " + "X" + str(round(draw[i][2][0],3)) + " " + "Y" + str(round(draw[i][2][1],3)) + "\n")
file.close()
