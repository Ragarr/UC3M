//
// Created by defalco on 19/11/23.
//
#include <gtest/gtest.h>
#include <iostream>
#include "sim/simParticle.hpp"
#include <fstream>
#include <filesystem>
#include <string>

using std::filesystem::current_path;

//NOLINTBEGIN
std::string ROUTE = current_path().parent_path().parent_path().string() + "/utest/small.fld";

TEST(simParticle, readParticlesFromFile){
  int np = 4800;
  std::vector<simParticle> particles = readParticlesFromFile(ROUTE, np);
  std::ifstream file(ROUTE, std::ios::binary);

  FileParticle buffer_file_particle;
  file.seekg(sizeof(int) + sizeof(float), std::ios::beg);
  for (int i = 0; i < np; i++) {
    file.read(reinterpret_cast<char *>(&buffer_file_particle),
              sizeof(FileParticle));  // NOLINT(cppcoreguidelines-pro-type-reinterpret-cast)
    // Transform the particle to simParticle and add to the vector
    EXPECT_EQ(particles[i].toFileParticle().hvx, buffer_file_particle.hvx);
    EXPECT_EQ(particles[i].toFileParticle().hvy, buffer_file_particle.hvy);
    EXPECT_EQ(particles[i].toFileParticle().hvz, buffer_file_particle.hvz);
    EXPECT_EQ(particles[i].toFileParticle().px, buffer_file_particle.px);
    EXPECT_EQ(particles[i].toFileParticle().py, buffer_file_particle.py);
    EXPECT_EQ(particles[i].toFileParticle().pz, buffer_file_particle.pz);
    EXPECT_EQ(particles[i].toFileParticle().vx, buffer_file_particle.vx);
    EXPECT_EQ(particles[i].toFileParticle().vy, buffer_file_particle.vy);
    EXPECT_EQ(particles[i].toFileParticle().vz, buffer_file_particle.vz);
  }
  file.close();
}


TEST(simParticle, simParticleConstructor){
  FileParticle fileParticle(1, 2, 3, 4, 5, 6, 7, 8, 9);
  simParticle particle1(fileParticle, 1);
  EXPECT_EQ(particle1.id, 1);
  EXPECT_EQ(particle1.position, Vector3D<double>(1, 2, 3));
  EXPECT_EQ(particle1.initialVelocity, Vector3D<double>(4, 5, 6));
  EXPECT_EQ(particle1.velocity, Vector3D<double>(7, 8, 9));
}

//NOLINTEND