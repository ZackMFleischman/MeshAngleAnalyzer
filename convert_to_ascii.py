from stl import mesh
from stl.stl import ASCII
your_mesh = mesh.Mesh.from_file('stl/heart.stl')
your_mesh.save('stl/heart_ascii.stl', mode=ASCII)
