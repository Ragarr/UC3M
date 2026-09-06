# Add to this list all files related to sim library
add_library(sim
        progargs.hpp
        progargs.cpp
        grid.cpp
        grid.hpp
        constants.h
        fileParticle.cpp
        fileParticle.hpp
        simParticle.cpp
        simParticle.hpp
        Vector3D.hpp
        block.cpp
        block.hpp
        errors.h
)
# Use this line only if you have dependencies from stim to GSL
target_link_libraries(sim PRIVATE Microsoft.GSL::GSL)


