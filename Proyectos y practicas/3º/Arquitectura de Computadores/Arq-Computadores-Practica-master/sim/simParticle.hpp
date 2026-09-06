//
// Created by defalco on 16/10/23.
//

#ifndef FLUID_SIMPARTICLE_HPP
#define FLUID_SIMPARTICLE_HPP
#include "fileParticle.hpp"
#include "Vector3D.hpp"  // Asegúrate de incluir el archivo de encabezado de Vector3D
#include "constants.h"

class simParticle {
  public:
    simParticle();
    int64_t id{};
    Vector3D<double> position{};
    Vector3D<double> initialVelocity{}; // Velocidad inicial = hv
    Vector3D<double> velocity{};
    double density = 0;
    Vector3D<double> aceleration = cte::GRAVEDAD;
    [[nodiscard]] FileParticle toFileParticle() const;


    // Constructor from FileParticle
    simParticle(FileParticle const &particle, int id)
      : id(id),
        position(particle.px, particle.py, particle.pz),
        initialVelocity(particle.hvx, particle.hvy, particle.hvz),
        velocity(particle.vx, particle.vy, particle.vz){}


    // << operator
    friend std::ostream& operator<<(std::ostream& os, simParticle const &particle);
};

std::vector<simParticle> readParticlesFromFile(const std::string& fileName, int np);


#endif  // FLUID_SIMPARTICLE_HPP
