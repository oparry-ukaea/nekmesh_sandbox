## NekPy demos
This directory contains Python scripts intended to demonstrate `NekPy` functionality.

## Installing dependencies
### Nektar
To use NekPy, Nektar needs to have been built and installed with the `NEKTAR_BUILD_PYTHON` CMake flag turned on.
There are [full instructions](https://doc.nektar.info/userguide/latest/user-guidese3.html#x7-60001.3) on the Nektar website, but the below can be used as starting point in linux or WSL:

```bash
git clone https://gitlab.nektar.info/nektar/nektar
cd nektar
mkdir build && cd build
cmake -DNEKTAR_BUILD_PYTHON=ON -DNEKTAR_BUILD_SOLVERS=OFF ..
cmake --build .
make install
```
### Python environment
To generate a Python environment and install NekPy and numpy (a NekPy dependency), run
```bash
./make_env.sh
```
N.B. You could also install NekPy at a user or system level; see the [Nektar user guide](https://doc.nektar.info/userguide/latest/user-guidese3.html#x7-80001.3.2) for instructions.


## Scripts

### Mesh generation (gen_mesh.py)
gen_mesh.py uses NekPy to generate simple 2D triangular or quadrilateral meshes.
It was adapted from [this](https://gitlab.nektar.info/nektar/nektar/-/tree/master/library/Demos/Python/NekMesh/StructuredGrid.py) Nektar example.

To use it, run
```
. env/bin/activate
python gen_mesh.py [nx] [ny] [lx] [ly] [ux] [uy] [shape]
```
where `nx`,`ny` are the number of vertices in each direction; `lx`,`ly`,`ux`,`uy` are the lower and upper bounds in x and y respectively; and `shape` is one of 'Tri' or 'Quad'.

Mesh files are generated in ./output.
