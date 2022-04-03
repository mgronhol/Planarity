#!/usr/bin/env python3

import math

import matplotlib.pyplot as plt

from skspatial.objects import Points, Plane
from skspatial.plotting import plot_3d
from scipy.spatial.transform import Rotation as R



def fit_plane( planepoints, removeOffset = True, scaleX = 1.0, scaleY = 1.0, scaleZ = 1.0 ):


    # Use first point as zero reference
    zOffset = planepoints[0][2]
    if not removeOffset:
        zOffset = 0.0
    
    # Scale and remove z offset from data
    fitpoints = [ [p[0] * scaleX , p[1] * scaleY, (p[2] - zOffset) * scaleZ ] for p in planepoints ]
    

    # Separate per axis
    Xs = [fp[0] for fp in fitpoints]
    Ys = [fp[1] for fp in fitpoints]



    fitpoints = Points( fitpoints )

    plane = Plane.best_fit( fitpoints )
    
    # Remove singularity if plane too close to flat along axis
    if plane.normal[2] > (1-1e-10):
        phi = 0.0
        theta = 0.0
    else:
        # Compute tilt and direction
        phi = math.acos( plane.normal[2] )
        theta = math.atan2( plane.normal[0] / math.sin( phi ), plane.normal[1] / math.sin(phi) )
    

    # Resolve X and Y angles 
    r = R.from_euler( "YZ", [theta, phi] )
    eangles = r.as_euler( "XZY", degrees = True)

    # Compute data centre and span
    cx = (max(Xs) + min(Xs)) / 2
    cy = (max(Ys) + min(Ys)) / 2

    span = (min(Xs), min(Ys), max(Xs), max(Ys))

    return {"euler": eangles[:2], "orient": [(phi*180/math.pi), (theta*180/math.pi)], "plane": plane, "points": fitpoints, "span": span, "centre": (cx, cy)}


def difference_from_plane( points, plane ):
    out = []
    for point in points:
        dZ  = plane.distance_point_signed( point )
        out.append( [point[0], point[1], dZ ] )
    
    return out



def plot_plane( result ):
    plt.close('all')
    _, ax = plot_3d(
        result["points"].plotter(),
        result["plane"].plotter(alpha=0.2, lims_x=(result["span"][0] - result["centre"][0], result["span"][2] - result["centre"][0]), lims_y=(result["span"][1] - result["centre"][1], result["span"][3] - result["centre"][1]) ),
    )
    
    ax.set_ylabel( "Y" )
    ax.set_xlabel( "X" )
    ax.set_zlabel( "Z" )
    


    plt.show( block = False )

def plot_two_planes( plane0, plane1 ):
    plt.close('all')
    _, ax = plot_3d(
        plane0["points"].plotter(),
        plane0["plane"].plotter(alpha=0.2, lims_x=(plane0["span"][0] - plane0["centre"][0], plane0["span"][2] - plane0["centre"][0]), lims_y=(plane0["span"][1] - plane0["centre"][1], plane0["span"][3] - plane0["centre"][1]) ),
        plane1["plane"].plotter(alpha=0.2, lims_x=(plane0["span"][0] - plane0["centre"][0]*0, plane0["span"][2] - plane0["centre"][0]*0), lims_y=(plane0["span"][1] - plane0["centre"][1]*0, plane0["span"][3] - plane0["centre"][1]*0) ),
    )
    
    ax.set_ylabel( "Y" )
    ax.set_xlabel( "X" )
    ax.set_zlabel( "Z" )
    
    plt.show( block = False )
