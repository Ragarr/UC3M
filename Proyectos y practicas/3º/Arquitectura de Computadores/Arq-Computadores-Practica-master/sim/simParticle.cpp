//
// Created by defalco on 16/10/23.
//

#include "simParticle.hpp"

#include "fileParticle.hpp"
#include "Vector3D.hpp"  // Asegúrate de incluir el archivo de encabezado de Vector3D
#include "errors.h"

#include <fstream>
#include <iostream>
#include <vector>
#include <string>

// read particles from file
std::vector<simParticle> readParticlesFromFile(const std::string& fileName, int np) {
  std::ifstream file(fileName, std::ios::binary);
  std::vector<simParticle> particles = {};
  if (!file.is_open()) {exit(-3); } // en caso de no poder abrir el archivo

  // Check number of particles in file
  int const n_file_particles = (np * (int) sizeof(FileParticle));
  int const file_expected_size = (int)(sizeof(int)+sizeof(float)) + n_file_particles;
  file.seekg(0, std::ios::end);
  if (file_expected_size!=file.tellg()){
    std::cerr<< "Error: Number of particles mismatch. Header: " << np << ", Found: " << n_file_particles;
    exit(errors::NP_ERROR);
  }
  // Set pointer just after the header
  file.seekg(sizeof(int) + sizeof(float), std::ios::beg);
  // start reading
  FileParticle buffer_file_particle;
  for (int i = 0; i < np; i++) {
    file.read(reinterpret_cast<char *>(&buffer_file_particle),  // NOLINT(cppcoreguidelines-pro-type-reinterpret-cast)
              sizeof(FileParticle));
    particles.emplace_back(buffer_file_particle, i);
  }
  file.close();
  return particles;
}

// << operator for simParticle
std::ostream& operator<<(std::ostream& os, simParticle const & particle) {
    os << "Particle " << particle.id << ":\n";
    os << "  Position: " << particle.position << '\n';
    os << "  initVelo: " << particle.initialVelocity << '\n';
    os << "  Velocity: " << particle.velocity << '\n';
    os << "  Acelerat: " << particle.aceleration << '\n';
    os << "  Density : " << particle.density << '\n';
    return os;
}

simParticle::simParticle(){
  position = {0,0,0};
  initialVelocity = {0,0,0};
  velocity = {0,0,0};
  aceleration = {0,0,0};
}

FileParticle simParticle::toFileParticle() const {
  return {(float)position.x(), (float)position.y(), (float)position.z(),
          (float)initialVelocity.x(), (float)initialVelocity.y(), (float)initialVelocity.z(),
          (float)velocity.x(), (float)velocity.y(), (float)velocity.z()};
}
