## 3D OpenFOAM FSI Overset Example Cases

### Cases
- 3D Ducky Drop 
- 3D Reference Model 6 (RM6) with Mooring (No PTO) 
- 3D Reference Model 6 (RM6) with Mooring and PTO

### Setup
- **Single Processor**: Use the `Allrun.ser` script in each case to run on a single processing unit. 
- **Multiple Processors**: Use the `Allrun` script in each case to run on multiple processing units.
    - For parallel runs, the number and type of domain decompositions can be adjusted in `<system>/decomposeDict`. 
- **Grid Generation**: The grid files (`<constant>/polyMesh`) are not included in these cases.
    - Use `template_mesh_generation` with the provided `flowParams` and CAD file (place inside 
    `<constant>/polyMesh.orig_gen_grid_files`) to generate the grid for each case. 
    - Alternatively, grids can be generated using the examples provided in `examples_mesh_generation` for each case.
- **Wave conditions and time control**: All settings can be configured through the `flowParams` file located in the top folder of each case.
