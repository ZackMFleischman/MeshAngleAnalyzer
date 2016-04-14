from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

# Load the STL files and add the vectors to the plot
# your_mesh = mesh.Mesh.from_file('stl/z.stl')
your_mesh = mesh.Mesh.from_file('stl/heart.stl')
plot_mesh = mplot3d.art3d.Poly3DCollection(your_mesh.vectors)
plot_mesh.set_facecolor((0,1,1))
plot_mesh.set_edgecolor((0,0,1))
axes.add_collection3d(plot_mesh)

# Auto scale to the mesh size
scale = your_mesh.points.flatten(-1)
axes.auto_scale_xyz(scale, scale, scale)

# Show the plot to the screen
pyplot.show()
