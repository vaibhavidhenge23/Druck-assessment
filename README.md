Drucks Computational Geometry Assessment
A first-principles 3D model parser and slicer metric calculator built purely in Python.

Overview
Modern 3D printing relies on slicers to convert 3D models (STL files) into toolpaths, but understanding the underlying geometry is crucial for optimization. This project solves the problem of extracting core physical metrics from a raw 3D mesh without leaning on heavy abstractions or third-party geometric libraries like Trimesh or NumPy.
It reads binary .stl files at the byte level, reconstructs the 3D surface, and calculates the true enclosed volume, spatial footprint, and extrusion path length required to 3D print the object as a hollow shell
Features
Zero-Dependency STL Parsing: Decodes binary STL structs natively in Python.

Accurate Volume Computation: Utilizes the scalar triple product (signed tetrahedra method) to compute precise millimeter-scale volumes.

Spatial Bounds Extraction: Calculates the Axis-Aligned Bounding Box (AABB) and maximum physical extents.

Z-Plane Slicing: Computes planar intersections across the mesh to generate layer perimeters.

Print Time Estimation: Simulates constant-velocity perimeter extrusion to project real-world 3D printing durations.

Tech Stack

Domain,Technologies
Language,Python 3
Libraries,struct (Standard Library)
Input Format,Binary STL
Concepts,"Computational Geometry, Linear Algebra"

Architecture
The system executes as a single procedural pipeline. It loads the file into memory, processes the triangles mathematically, and outputs the results iteratively.

Code snippet
graph TD
    A[Binary STL File] -->|struct.unpack| B(Parse Triangles)
    B --> C{Geometric Analysis}
    C --> D[Volume Computation]
    C --> E[Bounding Box & Dimensions]
    C --> F[Iterative Z-Slicing]
    F -->|Plane Intersection| G[Calculate Layer Perimeters]
    G --> H[Print Time Estimation]
Project Structure
Plaintext
druck-assessment/
├── solution.py          # Core geometric logic and executable script
├── writeup.md           # Detailed technical reflection and algorithm explanation
└── DrucksShoe.stl       # Sample 3D model used for testing
Installation
This script relies entirely on the Python Standard Library. No package manager or virtual environment is required.

Clone the repository:

Bash
git clone https://github.com/vaibhavidhenge23/druck-assessment.git
cd druck-assessment
Ensure Python 3 is installed:

Bash
python --version
Usage
Place the target binary STL file in the root directory (defaults to DrucksShoe.stl) and execute the script.

Bash
python solution.py
The script will output the triangle count, volume in mm³ and cm³, bounding coordinates, layer counts, and a progressive layer processing readout before delivering the final estimated print time.
Configuration
The script contains hardcoded constants optimized for the technical assessment specifications. These can be adjusted directly in solution.py under the # --- Run --- section:
Variable,Default Value,Description
layer_height,0.2,The vertical resolution of the slicer in mm.
print_speed,60,The assumed constant nozzle travel speed in mm/s.
API or Modules

parse_stl(filepath): Reads an 80-byte header and extracts coordinate floats using little-endian unpacking.

compute_volume(triangles): Calculates total mesh volume via scalar triple products.

compute_bounding_box(triangles): Returns the (min_x, max_x, min_y, max_y, min_z, max_z) tuple.

slice_at_z(triangles, z_height): Returns a list of 2D line segments where the triangles intersect a horizontal plane.

perimeter_from_segments(segments): Computes the Euclidean distance of all segment combinations for a single layer.

Contributing
While this was built as a static technical assessment, forks and improvements are welcome.

Fork the Project

Create your Feature Branch (git checkout -b feature/FastSpatialIndex)

Commit your Changes (git commit -m 'Add Z-sorted spatial index for faster slicing')

Push to the Branch (git push origin feature/FastSpatialIndex)

Open a Pull Request

Roadmap
Spatial Indexing: Implement a Z-sorted spatial index or bounding volume hierarchy (BVH) to prevent checking all triangles for every layer slice.

ASCII STL Support: Extend the parse_stl function to automatically detect and parse ASCII formatted STLs.

Auto-Orientation: Add a matrix rotation module to calculate the optimal resting face, minimizing the Z-height for faster prints.

Acceleration Curves: Factor in real-world printer kinematics (jerk/acceleration) for more accurate time estimates.

License
Distributed under the MIT License. See LICENSE for more information.
