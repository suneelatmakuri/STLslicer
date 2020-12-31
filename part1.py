import math
import matplotlib.pyplot as plt
import re
import ast 

filestl = input("Enter Full File Name: ")

fil = open(filestl) 
Lines = fil.readlines() 
  
normals=[]
vertices=[]
for line in Lines: 
    lis = re.split(" +",line)
    for i in range(len(lis)):
        if lis[i] == "normal":
            normals.append([float(j) for j in lis[i+1:] if re.search("\d+",j)])
            break
        if lis[i] == "vertex":
            vertices.append([float(j) for j in lis[i+1:] if re.search("\d+",j)])
            break

groups=[]
for i in range(0,len(vertices),3):
    lis = [vertices[i],vertices[i+1],vertices[i+2]]
    lis.sort(key=lambda x: x[2])
    groups.append(lis)

print("Numer of Triangles in Loaded STL File: ",len(groups))

zs = []
for i in range(len(groups)):
  for j in range(3):
    zs.append(groups[i][j][2])  

zslice = float(input("Enter the value of Z for Slicing between " + str(min(zs)) + " and " + str(max(zs)) + " : "))

layer = []
for face in range(len(groups)):
  x1 = groups[face][0][0]
  x2 = groups[face][1][0]
  x3 = groups[face][2][0]
  y1 = groups[face][0][1]
  y2 = groups[face][1][1]
  y3 = groups[face][2][1]
  z1 = groups[face][0][2]
  z2 = groups[face][1][2]
  z3 = groups[face][2][2]

  if z1 < zslice and zslice < z3:
    if z1!=z3 and z2!=z3:
      if zslice > groups[face][1][2]:
        layer.append([[ x3 + (x2-x3)*((zslice - z3)/(z2-z3)) ,y3 + (y2-y3)*((zslice - z3)/(z2-z3)) ] ,[ x3 + (x1-x3)*((zslice - z3)/(z1-z3)), y3 + (y1-y3)*((zslice - z3)/(z1-z3)) ]])   
    if z1!=z2 and z1!=z3:  
      if zslice < groups[face][1][2]:
        layer.append([[ x2 + (x1-x2)*((zslice - z2)/(z1-z2)) ,y2 + (y1-y2)*((zslice - z2)/(z1-z2)) ] ,[ x3 + (x1-x3)*((zslice - z3)/(z1-z3)), y3 + (y1-y3)*((zslice - z3)/(z1-z3)) ]])   
    if z1!=z3:  
      if zslice == groups[face][1][2]:
        layer.append([[ x3 + (x1-x3)*((zslice - z3)/(z1-z3)), y3 + (y1-y3)*((zslice - z3)/(z1-z3)) ], [x2, y2]])
    if z1==z2 and z2==zslice:
      layer.append([[x1,y1],[x2,y2]])
    if z2==z3 and z2==zslice:
      layer.append([[x2,y2],[x3,y3]])

# Writing these Segments to a file for Later use
file_layer = 'layer_data.txt' 
file = open(file_layer, "w")
file.write(str(layer))
file.close()

fig,ax = plt.subplots(figsize=(10,10)) 

for i in range(len(layer)):  
  ax.plot([layer[i][0][0], layer[i][1][0]], [layer[i][0][1], layer[i][1][1]] , c = 'k')

ax.set_aspect('equal') 
fig.savefig("layer.jpg")
plt.show()

