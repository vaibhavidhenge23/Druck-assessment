import struct

def parse_stl(filepath):
    triangles = []
    with open(filepath, "rb") as f:
        f.read(80)
        num_triangles = struct.unpack("<I", f.read(4))[0]
        print(f"Total triangles: {num_triangles}")
        for _ in range(num_triangles):
            f.read(12)
            v1 = struct.unpack("<fff", f.read(12))
            v2 = struct.unpack("<fff", f.read(12))
            v3 = struct.unpack("<fff", f.read(12))
            f.read(2)
            triangles.append((v1, v2, v3))
    return triangles

def compute_volume(triangles):
    total = 0.0
    for (v1, v2, v3) in triangles:
        cx = v2[1]*v3[2] - v2[2]*v3[1]
        cy = v2[2]*v3[0] - v2[0]*v3[2]
        cz = v2[0]*v3[1] - v2[1]*v3[0]
        dot = v1[0]*cx + v1[1]*cy + v1[2]*cz
        total += dot / 6.0
    return abs(total)

def compute_bounding_box(triangles):
    min_x = min_y = min_z = float('inf')
    max_x = max_y = max_z = float('-inf')
    for (v1, v2, v3) in triangles:
        for (x, y, z) in [v1, v2, v3]:
            if x < min_x: min_x = x
            if x > max_x: max_x = x
            if y < min_y: min_y = y
            if y > max_y: max_y = y
            if z < min_z: min_z = z
            if z > max_z: max_z = z
    return (min_x, max_x, min_y, max_y, min_z, max_z)

def slice_at_z(triangles, z_height):
    segments = []
    for (v1, v2, v3) in triangles:
        verts = [v1, v2, v3]
        above = [v for v in verts if v[2] >= z_height]
        below = [v for v in verts if v[2] < z_height]
        if len(above) == 0 or len(below) == 0:
            continue
        intersections = []
        for a in above:
            for b in below:
                t = (z_height - b[2]) / (a[2] - b[2])
                x = b[0] + t * (a[0] - b[0])
                y = b[1] + t * (a[1] - b[1])
                intersections.append((x, y))
        if len(intersections) == 2:
            segments.append((intersections[0], intersections[1]))
    return segments

def perimeter_from_segments(segments):
    total = 0.0
    for (p1, p2) in segments:
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        total += (dx*dx + dy*dy) ** 0.5
    return total

# --- Run ---
triangles = parse_stl("DrucksShoe.stl")

# Task 1
volume = compute_volume(triangles)
print(f"\nVolume: {volume:.2f} mm3")
print(f"Volume in cm3: {volume/1000:.2f} cm3")

# Task 2
(min_x, max_x, min_y, max_y, min_z, max_z) = compute_bounding_box(triangles)
height = max_z - min_z
layers = int(height / 0.2)
print(f"\nBounding Box:")
print(f"  X: {min_x:.2f} to {max_x:.2f} mm")
print(f"  Y: {min_y:.2f} to {max_y:.2f} mm")
print(f"  Z: {min_z:.2f} to {max_z:.2f} mm")
print(f"\nHeight: {height:.2f} mm")
print(f"Layer count at 0.2mm: {layers}")

# Task 3
print("\n--- PRINT TIME ESTIMATION ---")
layer_height = 0.2
print_speed = 60
total_path = 0.0
z = min_z + layer_height
layer_num = 0

while z <= max_z:
    segs = slice_at_z(triangles, z)
    total_path += perimeter_from_segments(segs)
    z += layer_height
    layer_num += 1
    if layer_num % 50 == 0:
        print(f"  Processing layer {layer_num}/{layers}...")

print(f"Total path length: {total_path:.2f} mm")
print(f"Total path length: {total_path/1000:.2f} m")
print(f"Estimated print time: {total_path/print_speed:.2f} seconds")
print(f"Estimated print time: {total_path/print_speed/60:.2f} minutes")