//
// Created by nekos on 06/11/2023.
//

#ifndef FLUID_BLOCK_HPP
#define FLUID_BLOCK_HPP

#include "Vector3D.hpp"
#include "simParticle.hpp"

class block {
  public:
    block(Vector3D<double> sizeBlock, Vector3D<int> blockIndex);


    Vector3D<double> getSizeBlock();
    [[nodiscard]] Vector3D<int> getBlockIndex() const;
    [[nodiscard]] int getI() const;
    [[nodiscard]] int getJ() const;
    [[nodiscard]] int getK() const;
    void storeParticle(simParticle* particle);
    simParticle* popParticle(simParticle *particle);
    int getNParticles();
    void setNParticlesToZero();
    void addOneToNParticles();
    void printParticles();
    // void printParticles(int index);
    void updateDensities(double h, block* block2);
    void densitiesNormalize(double h, double mass);
    void acelerationTransfer(double h, double mass, block* block2);
    std::vector<simParticle*> getParticles();
    void collisionX_AXIS();
    void collisionY_AXIS();
    void collisionZ_AXIS();
    void collisionX_AXIS2();
    void collisionY_AXIS2();
    void collisionZ_AXIS2();
    void initParticles(Vector3D<double> externalForce);

    void particlesMovement();

  private:
    std::vector<simParticle*> particles;
    int nParticles = 0;
    Vector3D<double> sizeBlock = {0, 0, 0};
    int i, j, k;
};

#endif  // FLUID_BLOCK_HPP
