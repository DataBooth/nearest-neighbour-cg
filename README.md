# `nearest-neighbour-cg`

Implementation of nearest neighbour calculations for Computational Geometry demo

---

# What is Computational Geometry and why does it matter?

Computational geometry is a branch of computer science focused on designing and analyzing algorithms to solve geometric problems involving points, lines, polygons, and other shapes, usually in two or three dimensions. It matters because many real-world applications-from computer graphics and robotics to geographic information systems (GIS) and computer-aided design (CAD)-rely on efficiently processing and querying geometric data.

Typical industry use cases include:

- **Computer Graphics:** Rendering scenes, hidden surface removal, and illumination calculations.
- **Robotics:** Motion planning and obstacle avoidance.
- **GIS:** Spatial queries like location search, route planning, and map overlays.
- **CAD/CAM:** Designing and manufacturing parts with precise geometric constraints.
- **Computer Vision:** 3D reconstruction and object recognition.
- **Integrated Circuit Design:** Layout verification and mesh generation.

More specifically, some potential applications of computational geometry in automated embroidery:

1. **CAD/CAM**  
   - **Stitch Path Optimisation**: Planning optimal needle paths to minimise thread breaks, jumps, and runtime (similar to TSP solvers in CG).  
   - **Shape Decomposition**: Splitting complex embroidery designs into stitchable regions using polygon clipping, triangulation, or Voronoi diagrams.  
   - **Collision Detection**: Preventing needle collisions with existing stitches or fabric folds using spatial indexing (e.g., KD-trees, AABB trees).  

2. **Computer Graphics**  
   - **Stitch Rendering**: Simulating thread density, shading, and texture for realistic previews using rasterisation or procedural geometry.  
   - **Pattern Generation**: Creating geometric motifs (e.g., floral, lace) via fractal algorithms or symmetry transformations.  

3. **Numerical Analysis**  
   - **Fabric Deformation Modelling**: Adjusting stitch positions dynamically to account for material stretch using finite element analysis (FEA) or spring-mass models.  

4. **Robotics**  
   - **Multi-Arm Coordination**: Synchronising embroidery machine arms to avoid mechanical interference during high-speed stitching.  

5. **Computer Vision**  
   - **Design Digitisation**: Converting raster images to vectorised embroidery paths using contour tracing or skeletonisation.  

---

### Why This Matters 

Embroidery requires millimeter precision to avoid costly material waste. Computational geometry enables:  

- **Efficiency**: Reducing stitch count while maintaining design integrity.  
- **Adaptability**: Auto-correcting designs for stretchy/fragile fabrics.  
- **Innovation**: Supporting 3D embroidery or hybrid textile-electronics designs.  

Tools like the [Computational Geometry Algorithms Library (**CGAL**)](https://www.cgal.org) (for robust geometric operations) and [**OpenGL**](https://www.opengl.org) (for real-time visualisation) are typically used in the industry.


## DEMO: Nearest Neighbor Problem

The **nearest neighbor problem**, finding the closest point(s) in a dataset to a given query point, is a fundamental example of computational geometry. It illustrates key concepts such as spatial data structures (like kd-trees), distance metrics, and efficient search algorithms. Nearest neighbor search is widely used in recommendation systems, clustering, pattern recognition, and many other fields where understanding proximity in geometric or feature space is essential.

By studying nearest neighbor algorithms, one gains insight into how computational geometry tackles the challenge of organising and querying spatial data efficiently, which is critical for performance in many applications.


## References

[1]: https://en.wikipedia.org/wiki/Computational_geometry

[2]: https://www.cs.cmu.edu/~15451-f22/lectures/lec21-geometry.pdf

[3]: https://cimec.org.ar/twiki/pub/Cimec/GeometriaComputacional/cg.basics.pdf

[4]: https://www.youtube.com/watch?v=qMgF8Fcrk_c

[5]: https://www.cs.umd.edu/class/spring2020/cmsc754/Lects/lect01-intro.pdf

[6]: https://www.longdom.org/open-access/importance-of-algorithms-in-computational-geometry-for-analyzing-geometrical-analysis-101640.html

[7]: https://www.cs.cmu.edu/~15451-s19/lectures/lec22-nearest-neighbor.pdf

[8]: https://www.studysmarter.co.uk/explanations/math/geometry/computational-geometry/

[9]: https://cs.utdallas.edu/6717/dr-benjamin-raichel-and-researcher-two-important-discoveries-computational-geometry/

[10]: https://www.cs.cmu.edu/afs/cs/academic/class/15456-s10/ClassNotes/nn.pdf

[11]: https://en.wikipedia.org/wiki/Nearest_neighbor_search
