# MeshAngleAnalyzer
Determines whether or not a manifold mesh has any sharp edges.

Run `find_sharp_edges.py` with a manifold mesh in a **.stl** file format.
By default it will test for edges of 80 degrees or less.

## Dependencies
- numpy-stl
- matplotlib

## Usage
usage: find_sharp_edges.py [-h] [-t THRESHOLD] [-v] STL_FILE

Analyze a manifold mesh to see if it has acute edges.

positional arguments:
  STL_FILE

optional arguments:
  -h, --help            show this help message and exit
  -t THRESHOLD, --threshold THRESHOLD
                        The degree in angles that all edges must be greater
                        than.
  -v, --view            Show a plot of the model
