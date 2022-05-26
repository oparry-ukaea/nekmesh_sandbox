
#include <NekMesh/Module/Module.h>
#include <NekMesh/MeshElements/Mesh.h>

#include <iostream>

namespace nm = Nektar::NekMesh;

nm::MeshSharedPtr ReadMesh(std::string mesh_fpath)
{
    // Instantiate empty mesh object
    nm::MeshSharedPtr mesh = std::make_shared<nm::Mesh>();

    // Create an instance of NekMesh's XML input module
    nm::ModuleSharedPtr mod = nm::GetModuleFactory().CreateInstance(nm::ModuleKey(nm::eInputModule, "xml"),mesh);

    // Set the input file and call Process() to read it
    mod->RegisterConfig("infile", mesh_fpath);
    mod->Process();
    
    return mesh;
}

int main(int argc, char *argv[])
{
    // Read mesh filepath from CL 
    if (argc != 2){
        std::cout << "Usage: " << argv[0] << ": [path_to_mesh_xml]" << std::endl;
        exit(1);
    }
    std::string mesh_fpath(argv[1]);

    // Read mesh from file
    nm::MeshSharedPtr mesh = ReadMesh(mesh_fpath);

    // Log mesh properties to stdout
    auto logStrm = std::make_shared<nm::StreamOutput>(std::cout);
    nm::Logger stdout_logger(logStrm,nm::LogLevel::INFO);
    mesh->PrintStats(stdout_logger);
}