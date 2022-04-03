# Planarity
Plane fitting tool written in Python.


## Required packages

 - Numpy
 - Scipy
 - Scikit-spatial
 - Matplotlib

## Example

Sample dataset, all dimensions in mm.
```
# X Y Z
0.0 0.0 0.0
-7.046 7.426 -0.015
0.458 7.417 -0.003
8.559 7.412 0.004
8.554 -2.200 0.017
3.709 -2.205 0.009
0.476 -2.209 0.006
-6.935 -2.214 0.007
```

Results are:
```
Plane rotation:
  X: -0.053°, -0.925 µm/mm
  Y: +0.078°, +1.367 µm/mm

Plane orientation:
  Direction: -34.081°
       Tilt: +0.095°

Deviation from fitted plane:
  Max: +0.006 mm
  Min: -0.005 mm
  RMS: +0.003 mm
  MAD: +0.003 mm
```