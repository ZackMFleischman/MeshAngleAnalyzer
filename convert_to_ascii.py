from stl import mesh
from stl.stl import ASCII
your_mesh = mesh.Mesh.from_file('meshes/heart.stl')
your_mesh.save('meshes/heart_ascii.stl', mode=ASCII)
