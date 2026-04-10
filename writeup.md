\# Drucks Technical Assessment

\*\*Vaibhavi Dhenge\*\*

\*\*Role: Software Developer — Computational Geometry\*\*



\---



\## Overview



This assessment required me to parse a 3D shoe model from an STL file 

and extract geometric properties from first principles — without using 

any geometry libraries. Below is my approach, implementation, results, 

and honest reflection on each task.



\---



\## Task 1: Volume Computation



\### Approach



An STL file contains no volume information directly — it is just a list 

of triangles forming the surface of a 3D object. To compute volume, I 

used the signed tetrahedra method.



The idea is simple: for each triangle on the surface, I connect its 

three vertices to the origin (0,0,0), forming a tetrahedron. I compute 

the signed volume of that tetrahedron using the scalar triple product:



&#x20;   volume = v1 · (v2 × v3) / 6



The "signed" part is what makes this work — triangles facing outward 

give positive volume, inward-facing give negative. When summed, they 

cancel out and leave the exact enclosed volume.



\### Result



| Metric | Value |

|---|---|

| Computed Volume | 406,550.65 mm³ |

| OrcaSlicer Volume | 406,547 mm³ |

| Difference | 3.65 mm³ (0.0007%) |



The tiny difference is due to floating point precision in reading 

binary STL data — negligible for any practical purpose.



\---



\## Task 2: Bounding Box and Layer Count



\### Approach



I looped through every vertex of every triangle and tracked min/max 

values for X, Y, Z. This gives the axis-aligned bounding box.



Layer count:

&#x20;   layers = floor(116.25 / 0.2) = 581



\### Result



| Axis | Min | Max | Extent |

|---|---|---|---|

| X | -6.95 mm | 282.61 mm | 289.56 mm |

| Y | -62.76 mm | 46.27 mm | 109.03 mm |

| Z | -6.38 mm | 109.87 mm | 116.25 mm |



\*\*Model height:\*\* 116.25 mm  

\*\*Layer count at 0.2mm:\*\* 581 layers



\### On Print Orientation



The shoe as loaded is not flat on the print bed. Current Z height is 

116.25mm giving 581 layers. If rotated to lie flat on its sole, height 

reduces to \~109mm giving \~545 layers. Orientation affects both layer 

count and surface quality — a production slicer would auto-orient to 

minimize supports and maximize quality.



\---



\## Task 3: Print Time Estimation



\### Approach



For a hollow shell, the nozzle traces the perimeter of each layer 

cross-section. So:



&#x20;   Time = Total path length / print speed



&#x20;   For each layer at height z:

&#x20;     segments = intersect all triangles with plane z

&#x20;     perimeter = sum of segment lengths



&#x20;   Total path = sum of all 581 layer perimeters

&#x20;   Time = Total path / 60 mm/s



I implemented triangle-plane intersection using linear interpolation 

to find where each triangle crosses the cutting plane.



\### Result



| Metric | Value |

|---|---|

| Total path length | 408,752 mm (408.75 m) |

| Estimated print time | 6,812 seconds |

| \*\*My estimate\*\* | \*\*113 minutes\*\* |



\### Verification with OrcaSlicer



Getting OrcaSlicer's time was not straightforward. The shoe is 289mm 

long — it exceeded the default printer bed size in Generic RRF Printer 

profile. I solved this by switching to Elegoo Neptune 4 Max (420x420mm 

bed).



Second issue: even with infill 0%, OrcaSlicer was still printing 

top/bottom shell layers. I had to set Top shell layers: 0 and Bottom 

shell layers: 0 to get a true hollow shell.



After these fixes:



| | Time |

|---|---|

| My estimate | 113 min |

| OrcaSlicer | 148 min |

| Difference | 35 min (24%) |



\### Why is my estimate lower?



1\. \*\*Travel moves not counted\*\* — my formula only counts extrusion 

path. OrcaSlicer shows 7m of travel moves separately.



2\. \*\*Acceleration/deceleration\*\* — real printers slow down at corners. 

OrcaSlicer models this; I assumed constant 60mm/s throughout.



3\. \*\*Overhang walls\*\* — OrcaSlicer printed 40min of overhang walls at 

reduced speed. My formula treats all perimeters equally.



4\. \*\*Printer profile speeds\*\* — Elegoo Neptune 4 Max uses 120mm/s 

outer wall speed vs the 60mm/s in the assessment spec. This partially 

explains the gap.



5\. \*\*Start/end routines\*\* — homing, purge lines add \~22s that my 

formula ignores.



The 24% difference is expected for a geometric approximation with no 

motion planning model.



\---



\## Task 4: OrcaSlicer Codebase Navigation



\### Question: Where is layer height applied during slicing?



\### Search Strategy



I searched for `layer\_height` in the OrcaSlicer GitHub repository 

and found 3,100+ matches. I focused on files in `src/libslic3r/` 

which is the core slicing library.



\### Call Chain



\*\*Step 1 — User setting:\*\*  

`src/libslic3r/PrintConfig.hpp`  

The `layer\_height` config option is defined here. This is what the 

user sets in the UI (e.g. 0.2mm). It is stored as a float config 

parameter.



\*\*Step 2 — Layer height profile computed:\*\*  

`src/libslic3r/Slicing.hpp` and `Slicing.cpp`  

The function `layer\_height\_profile\_from\_ranges()` builds a profile 

mapping Z positions to layer heights across the full model height. 

This handles variable layer height if the user has set it.



\*\*Step 3 — Per-layer Z position:\*\*  

`src/libslic3r/SLAPrint.hpp` line 144:  

Each layer object stores its own height via `layer\_height()`. Z 

positions are computed from the cumulative sum of these heights.



\*\*Step 4 — Toolpath generated:\*\*  

The Z position from Step 3 is used to generate the actual toolpath 

for each layer.



\### Summary



&#x20;   UI (layer\_height = 0.2mm)

&#x20;     → PrintConfig.hpp (stored as config)

&#x20;       → Slicing.cpp (profile across Z computed)

&#x20;         → Layer object (Z position assigned)

&#x20;           → Toolpath generated at that Z



\---



\## What I Would Improve



1\. \*\*Performance\*\* — Task 3 took a few minutes. A Z-sorted spatial 

index would make slicing much faster — only check triangles near 

current Z height instead of all 373k triangles per layer.



2\. \*\*Print time accuracy\*\* — Modelling acceleration curves and travel 

moves would give a closer estimate to real slicer output.



3\. \*\*Auto-orientation\*\* — Detect the flattest face and orient to bed 

automatically before computing layer count.



4\. \*\*ASCII STL support\*\* — My parser handles binary STL only. Would 

add ASCII support for completeness.



\---



\## AI Tool Declaration



I used \*\*Claude (Anthropic)\*\* throughout this assessment for 

guidance, explanation, and code review. The complete conversation 

is submitted separately as required.

