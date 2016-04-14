from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

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
    x = 1
    for (key, value) in edge_hash.items():
        print("{}: num triangles on edge: {}".format(x, len(value)))
        x += 1

# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

# Load the STL files and add the vectors to the plot
# your_mesh = mesh.Mesh.from_file('meshes/z.stl')
mesh = mesh.Mesh.from_file('meshes/heart.stl')

analyze_edges(mesh)

plot_mesh = mplot3d.art3d.Poly3DCollection(mesh.vectors)
plot_mesh.set_facecolor((0,1,1))
plot_mesh.set_edgecolor((0,0,1))
axes.add_collection3d(plot_mesh)

# Auto scale to the mesh size
scale = mesh.points.flatten(-1)
axes.auto_scale_xyz(scale, scale, scale)

# Show the plot to the screen
pyplot.show()
