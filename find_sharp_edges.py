#!/usr/local/bin/python3

import math
import argparse

import numpy as np

from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

parser = argparse.ArgumentParser(description='Analyze a manifold mesh to see if it has acute edges.')
parser.add_argument('-t', '--threshold', type=int, default=80, help='The degree in angles that all edges must be greater than (default=80 degrees).')
parser.add_argument('-v', '--view', action="store_true", help='Show a plot of the model instead of analyzing it.')
parser.add_argument('STL_FILE')
args = parser.parse_args()

ANGLE_THRESHOLD = args.threshold
VIEW_PLOT = args.view
STL_FILE = args.STL_FILE

def radians_to_degrees(rad):
    return (rad*180.0)/math.pi

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def get_ordered_segment(v1, v2):
    if v1[0] < v2[0]:
        return (v1, v2)
    elif v2[0] < v1[0]:
        return (v2, v1)
    elif v1[1] < v2[1]:
        return (v1, v2)
    elif v2[1] < v1[1]:
        return (v2, v1)
    elif v1[2] < v2[2]:
        return (v1, v2)
    elif v2[2] < v1[2]:
        return (v2, v1)
    else:
        return (v2, v1)

def get_ordered_segment_tuple(v1, v2):
    segment = get_ordered_segment(v1, v2)
    return (tuple(segment[0]), tuple(segment[1]))

def build_edge_hash(mesh):
    edge_hash = {}
    for i in range(len(mesh.points)):
        AB = get_ordered_segment_tuple(mesh.points[i][0:3], mesh.points[i][3:6])
        AC = get_ordered_segment_tuple(mesh.points[i][0:3], mesh.points[i][6:9])
        BC = get_ordered_segment_tuple(mesh.points[i][3:6], mesh.points[i][6:9])

        tri = (mesh.points[i], mesh.normals[i])

        edge_hash.setdefault(AB, []).append(tri)
        edge_hash.setdefault(AC, []).append(tri)
        edge_hash.setdefault(BC, []).append(tri)

    # Verify the model is manifold.
    for value in edge_hash.values():
        assert len(value) == 2, "Model is not manifold: {}".format(value)

    return edge_hash

def analyze_edges(mesh):
    edge_hash = build_edge_hash(mesh)

    too_sharp = False
    for values in edge_hash.values():
        n1 = values[0][1]
        n2 = values[1][1]
        angle_between_normals = radians_to_degrees(angle_between(n1, n2))
        angle_of_edge = 180.0 - angle_between_normals
        if angle_of_edge < ANGLE_THRESHOLD:
            print ("Angle greater than threshold({}): {} - Triangles: {}".format(ANGLE_THRESHOLD, angle_of_edge, values))
            too_sharp = True

    if too_sharp:
        print("Shape failed! Edges are too sharp. (Some are less than {} degrees)".format(ANGLE_THRESHOLD))
    else:
        print("Shape passed! Edges aren't too sharp. (All are greater than {} degrees)".format(ANGLE_THRESHOLD))


def plot_mesh(mesh):
    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)

    mesh_collection = mplot3d.art3d.Poly3DCollection(mesh.vectors)
    mesh_collection.set_facecolor((0,1,1))
    mesh_collection.set_edgecolor((0,0,1))
    axes.add_collection3d(mesh_collection)

    # Auto scale to the mesh size
    scale = mesh.points.flatten(-1)
    axes.auto_scale_xyz(scale, scale, scale)

    # Show the plot to the screen
    pyplot.show()


if __name__ == "__main__":
    # Load the STL files and add the vectors to the plot
    # your_mesh = mesh.Mesh.from_file('meshes/z.stl')
    mesh = mesh.Mesh.from_file(STL_FILE)
    if VIEW_PLOT:
        plot_mesh(mesh)
    else:
        analyze_edges(mesh)
