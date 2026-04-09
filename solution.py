import struct

def parse_stl(filepath):
    """
    Reads a binary STL file.
    Returns a list of triangles, each with 3 vertices.
    """
    triangles = []
    with open(filepath, "rb") as f:
        f.read(80)  # skip header (not useful)
        num_triangles = struct.unpack("<I", f.read(4))[0]  # number of triangles
        print(f"Total triangles: {num_triangles}")

        for _ in range(num_triangles):
            f.read(12)  # skip normal vector (not needed)
            v1 = struct.unpack("<fff", f.read(12))  # vertex 1 (x, y, z)
            v2 = struct.unpack("<fff", f.read(12))  # vertex 2 (x, y, z)
            v3 = struct.unpack("<fff", f.read(12))  # vertex 3 (x, y, z)
            f.read(2)   # skip attribute bytes
            triangles.append((v1, v2, v3))

    return triangles


def compute_volume(triangles):
    """
    Signed Tetrahedra Method:
    - Connect each triangle to the origin -> forms a tetrahedron (pyramid)
    - Compute the signed volume of each tetrahedron
    - Sum all signed volumes -> gives the exact volume of the mesh

    Why signed?
    Outward-facing triangles give positive volume,
    inward-facing give negative -> they cancel out automatically.
    Final result = actual enclosed volume of the shoe.
    """
    total_volume = 0.0

    for (v1, v2, v3) in triangles:
        # Formula: volume = v1 . (v2 x v3) / 6
        # where x = cross product, . = dot product

        # Step 1: Cross product of v2 and v3
        cross_x = v2[1]*v3[2] - v2[2]*v3[1]
        cross_y = v2[2]*v3[0] - v2[0]*v3[2]
        cross_z = v2[0]*v3[1] - v2[1]*v3[0]

        # Step 2: Dot product of v1 with the cross product
        dot = v1[0]*cross_x + v1[1]*cross_y + v1[2]*cross_z

        total_volume += dot / 6.0

    return abs(total_volume)  # abs because sign only indicates orientation


def compute_bounding_box(triangles):
    """
    Finds the axis-aligned bounding box of the mesh.
    Loops through all vertices and tracks min/max for X, Y, Z.
    """
    min_x = min_y = min_z = float('inf')
    max_x = max_y = max_z = float('-inf')

    for (v1, v2, v3) in triangles:
        for v in [v1, v2, v3]:
            if v[0] < min_x: min_x = v[0]
            if v[0] > max_x: max_x = v[0]
            if v[1] < min_y: min_y = v[1]
            if v[1] > max_y: max_y = v[1]
            if v[2] < min_z: min_z = v[2]
            if v[2] > max_z: max_z = v[2]

    return (min_x, max_x, min_y, max_y, min_z, max_z)


# ── Run ──────────────────────────────────────────────────────────────────────

triangles = parse_stl("DrucksShoe.stl")

# Task 1: Volume
volume = compute_volume(triangles)
print(f"\nVolume: {volume:.2f} mm³")
print(f"Volume in cm³: {volume/1000:.2f} cm³")

# Task 2: Bounding Box + Layer Count
(min_x, max_x, min_y, max_y, min_z, max_z) = compute_bounding_box(triangles)
height = max_z - min_z
layers = int(height / 0.2)  # round down -partial layers do not print

print(f"\nBounding Box:")
print(f"  X: {min_x:.2f} to {max_x:.2f} mm")
print(f"  Y: {min_y:.2f} to {max_y:.2f} mm")
print(f"  Z: {min_z:.2f} to {max_z:.2f} mm")
print(f"\nHeight: {height:.2f} mm")
print(f"Layer count at 0.2mm: {layers}")