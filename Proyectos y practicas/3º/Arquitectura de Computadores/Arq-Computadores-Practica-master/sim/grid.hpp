//
// Created by defalco on 2/10/23.
//

#ifndef ARQUITECTURA_DE_COMPUTADORES_GRID_HPP
#define ARQUITECTURA_DE_COMPUTADORES_GRID_HPP

#include "Vector3D.hpp"
#include "block.hpp"
#include <array>
#include "simParticle.hpp"


class grid {
  public:
    grid(double h, double mass, std::vector<simParticle> & particles);
    Vector3D<int> getNBlocks();
    block& getBlock(Vector3D<int> index);
    [[nodiscard]] int getTotalBlocks() const;
    Vector3D <double> getBlockSize();
    void printBlocks();
    // void printBlocks(int index);

    void fillBlocks(std::vector<simParticle> & particles);
    static bool isAdjacent(Vector3D<int> index1, Vector3D<int> index2);

    void reposParticles();
    void initParticles();
    void updateDensities();
    void densitiesNormalize();
    void acelerationTransfer();
    void collisions();
    void particlesMovement();
    void collisions2();
    void updateGrid();
    void collisionX_AXIS();
    void collisionY_AXIS();
    void collisionZ_AXIS();
    void collisionX_AXIS2();
    void collisionY_AXIS2();
    void collisionZ_AXIS2();

  private:
    Vector3D<int> nBlocks{};
    std::vector<block> blocks;
    int totalBlocks = 0;
    Vector3D <double> blockSize{};
    double h;
    double mass;
};


#endif //ARQUITECTURA_DE_COMPUTADORES_GRID_HPP

