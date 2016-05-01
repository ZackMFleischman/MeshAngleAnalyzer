import numpy as np
import trimesh

# load a file by name or from a buffer
mesh = trimesh.load_mesh('./meshes/heart.stl')

# is the current mesh watertight?
print(mesh.is_watertight)

# what's the euler number for the mesh?
print(mesh.euler_number)

# lets get a convex hull of the mesh
hull = mesh.convex_hull

# since the mesh is watertight, it means there is a
# volumetric center of mass which we can set as the origin for our mesh
mesh.vertices -= mesh.center_mass

# what's the moment of inertia for the mesh?
print(mesh.moment_inertia)

# find groups of coplanar adjacent faces
facets, facets_area = mesh.facets(return_area=True)

# set each facet to a random color
for facet in facets:
    mesh.visual.face_colors[facet] = trimesh.visual.random_color()

# preview mesh in an opengl window if you installed pyglet with pip
mesh.show()

# transform method can be passed a (4,4) matrix and will cleanly apply the transform
mesh.transform(trimesh.transformations.random_rotation_matrix())

# a minimum volume oriented bounding box is available
print(mesh.bounding_box_oriented.box_extents)
print(mesh.bounding_box_oriented.box_transform)

# show the mesh overlayed with its oriented bounding box
# the bounding box is a trimesh.primitives.Box object, which subclasses
# Trimesh and lazily evaluates to fill in vertices and faces when requested
# (press w in viewer to see triangles)
(mesh + mesh.bounding_box_oriented).show()
