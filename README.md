# STL Slicer

## Introduction:

Simple code to understand the logic behind softwares used for FDM 3D Printing used by major Cartesian Marlin or Sprinter Firmwares  

STL Slicer gives a simple code to view Layer information of any STL file compiled in ASCII format and also Rectilinear Toolpath of Nozzle movement for FDM printing in Rapid Prototyping

## Files
1. part1.py : 
2. part2.py : 
3. liver.stl : Demo input STL files
4. circle.stl: Demo input 2 STL files

## Setup and How to Run
### Dependencies installation
> Note : Works for Python3.6 or greater

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install libraries.

`pip3 install AST`
`pip3 install matplotlib`

### Trial Run 
```bash=
>$ python3 part1.py
Enter Full File Name: liver.stl
Number of Triangles in Loaded STL File: 38142
Enter the value of Z for Slicing between 13.0746 and 212.808 : 145
```
#### Output 1![](https://i.imgur.com/Pds4Mtz.jpg)

The Rectilinear Toolpath code works for single polygon either concave or convex.. Test case for the layer at z = 200:
```bash=
>$ python3 part2.py
Do you want to proceed with the layer achieved from the previous code for rectilinear are fill (y/n): y
Approximate x dimesion is: 123.3359
Enter the increment value: 2
```
#### Output 2 
The figure shown is the Toolpath Visualisation where the red path represents **Printing action** (Commonly G1) and the Blue path represents **Rapid Transverse** (commonly G0).
![](https://i.imgur.com/EMyubXA.jpg)

Toolpath is saved as a GCode file:

First 10 lines:

```sequenceDiagram
G0 X140.887 Y264.902
G1 X140.887 Y264.902
G1 X142.887 Y269.718
G1 X142.887 Y256.032
G1 X144.887 Y249.557
G1 X144.887 Y279.787
G1 X146.887 Y281.701
G1 X146.887 Y246.494
G1 X148.887 Y245.208
G1 X148.887 Y283.349
```

## License
[MIT](https://choosealicense.com/licenses/mit/)


