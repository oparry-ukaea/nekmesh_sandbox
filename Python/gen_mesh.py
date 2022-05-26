"""Adapted from Nektar demo at
   https://gitlab.nektar.info/nektar/nektar/-/tree/master/library/Demos/Python/NekMesh/StructuredGrid.py
"""
import sys
from NekPy.LibUtilities import ShapeType
import NekPy.NekMesh as NekMesh
import numpy as np
import os.path

#==================================================================================================
class StructuredGrid(NekMesh.InputModule):
    """ Creates a 2D structured grid of triangles or quads."""
    def __init__(self, mesh):
        super(StructuredGrid, self).__init__(mesh)

        # Only supports 2D for now
        self.mesh.spaceDim = 2
        self.mesh.expDim = 2

        # Define configuration options for this module.
        # AddConfigOption args are:
        # - name (required)
        # - default value (required)
        # - description (optional)
        # - isBoolean (optional; specify 'True' for boolean options)
        self.AddConfigOption("nx", "2", "Number of points in x direction")
        self.AddConfigOption("ny", "2", "Number of points in y direction")
        self.AddConfigOption("lx", "0", "Lower bound for the x coordinate")
        self.AddConfigOption("ux", "0", "Upper bound for the x coordinate")
        self.AddConfigOption("ly", "0", "Lower bound for the y coordinate")
        self.AddConfigOption("uy", "0", "Upper bound for the y coordinate")
        self.AddConfigOption("compid", "0", "Composite ID")
        self.AddConfigOption("shape", "Quadrilateral", "Triangular/Quadrilateral Mesh")

    def Process(self):
        # Retrieve option values using Get<Type>Config(option_name)
        coord_1x   = self.GetFloatConfig("lx")
        coord_1y   = self.GetFloatConfig("ly")
        coord_2x   = self.GetFloatConfig("ux")
        coord_2y   = self.GetFloatConfig("uy")
        nx         = self.GetIntConfig("nx")
        ny         = self.GetIntConfig("ny")
        compID     = self.GetIntConfig("compid")
        shape_type = self.GetStringConfig("shape")

        x_points   = np.linspace(coord_1x, coord_2x, nx)
        y_points   = np.linspace(coord_1y, coord_2y, ny)

        nodes = []
        id_cnt = 0

        for iy in range(ny):
            new_node = []
            for ix in range(nx):
                new_node.append(NekMesh.Node(id_cnt, x_points[ix], y_points[iy], 0.0))
                id_cnt += 1
            nodes.append(new_node)

        if shape_type[0].lower() == "q":
            self._create_quadrilaterals(nodes, nx, ny, compID)
        elif shape_type[0].lower() == "t":
            self._create_triangles(nodes, nx, ny, compID)
        else:
            raise ValueError("Unknown shape type: should be quad or tri.")

        # Call the Module functions to create all of the edges, faces and composites
        self.ProcessVertices()
        self.ProcessEdges()
        self.ProcessFaces()
        self.ProcessElements()
        self.ProcessComposites()

    def _create_quadrilaterals(self, nodes, nx, ny, compID):
        """ Helper function to generate quadrilateral elements"""
        config = NekMesh.ElmtConfig(ShapeType.Quadrilateral, 1, False, False)
        for iy in range(ny-1):
            for ix in range(nx-1):
                self.mesh.element[2].append(
                    NekMesh.Element.Create(
                        config, [
                            nodes[iy][ix], nodes[iy][ix+1],
                            nodes[iy+1][ix+1], nodes[iy+1][ix]
                        ], [compID]
                    )
                )

    def _create_triangles(self, nodes, nx, ny, compID):
        """ Helper function to generate triangular elements"""
        config = NekMesh.ElmtConfig(ShapeType.Triangle, 1, False, False)
        for iy in range(ny-1):
            for ix in range(nx-1):
                self.mesh.element[2].append(
                    NekMesh.Element.Create(
                        config,
                        [nodes[iy][ix], nodes[iy+1][ix+1], nodes[iy+1][ix]],
                        [compID]
                    )
                )

                self.mesh.element[2].append(
                    NekMesh.Element.Create(
                        config,
                        [nodes[iy][ix], nodes[iy][ix+1], nodes[iy+1][ix+1]],
                        [compID]
                    )
                )
#==================================================================================================

# Register our module with the NekMesh factory
NekMesh.Module.Register(NekMesh.ModuleType.Input, "StructuredGrid", StructuredGrid)

#==================================================================================================
# Convenience functions for handling options
    
def outfile_name_from_opts(opts):
    return "output/%sx%s_grid.xml" % (opts["nx"],opts["ny"])
    
def validate_opts(opts):
    assert opts["ux"] > opts["lx"], "ux [%s] must be > lx [%s]" % (opts["ux"],opts["lx"])
    assert opts["uy"] > opts["ly"], "uy [%s] must be > ly [%s]" % (opts["uy"],opts["ly"])

#==================================================================================================
if __name__ == '__main__':
    # Fixed composite ID and compression mode for now
    fixed_comp_id="2"
    uncompress=True

    # Process CL args
    if len(sys.argv) == 8:
        opts=dict(nx=sys.argv[1], ny=sys.argv[2],
                    lx=sys.argv[3], ly=sys.argv[4],
                    ux=sys.argv[5], uy=sys.argv[6],
                    compid = fixed_comp_id, shape = sys.argv[7])
    else:
        print("Usage:")
        print(" gen_mesh.py nx ny lx ly ux uy shape")
        print("  - Where nx,ny set the size of the grid, lx,ly,ux,uy set the coordinate bounds and shape is either 'Quad' or 'Tri'")
        print("  - e.g. gen_mesh.py 5 6 0.0 1.0  2.0 3.0  Quad")
        print("    (generates a 5x6 quadrilateral grid from (0,1) -> (2,3)")
        exit(1)

    validate_opts(opts)

    print("Options are:")
    print(opts)

    outfile = outfile_name_from_opts(opts)

    # Instantiate mesh object
    mesh = NekMesh.Mesh()

    # Call our custom input module via the NekMesh factory
    NekMesh.InputModule.Create("StructuredGrid", mesh, "", **opts).Process()
    
    # Ensure there are no negative Jacobians
    NekMesh.ProcessModule.Create("jac", mesh, list=True).Process()
    
    # Finally, output the mesh file (includes testing it inside Nektar++ first)
    print("Mesh written to %s" % outfile)