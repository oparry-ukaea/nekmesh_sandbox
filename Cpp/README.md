## Cpp Examples

To build examples in this directory, configure with CMake and point `Nektar++_DIR` to the location of Nektar++Config.cmake.

e.g.
```
app=ReadXmlMesh
mkdir "$app/build"
cd "$app/build"
cmake -DNektar++_DIR=[NEKTAR_ROOT]/build/dist/lib64/nektar++/cmake ..
make
```

Executables are generated in the build directory.
Run the executable without arguments for a list of options.
