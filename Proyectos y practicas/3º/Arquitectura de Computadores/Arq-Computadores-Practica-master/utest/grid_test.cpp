//
// Created by defalco on 8/11/23.
//
#include <iostream>
#include <gtest/gtest.h>
#include "sim/grid.hpp"
#include <vector>
#include "sim/constants.h"

using namespace std;
// NOLINTBEGIN

TEST(gridTests, gridConstructor){
    // Comprobamos que la malla se construye correctamente
    double h = 0.1;
    double mass = 1;
    vector<simParticle> particles;
    grid grid1(h, mass, particles);
    EXPECT_EQ(grid1.getNBlocks(), Vector3D<int>(1, 1, 1));
    EXPECT_EQ(grid1.getTotalBlocks(), 1);
    EXPECT_EQ(grid1.getBlockSize(), Vector3D<double>(0.13, 0.18, 0.13));
}

TEST(gridTests, GridFillBlocksTest) {

    double h = 0.025;
    double mass = 1.0;
    std::vector<simParticle> particles = {};
    simParticle particle1 = simParticle();
    particle1.position = {0.1, 0.15, 0.1}; // index = {6, 8, 6} -> {4, 6, 4}
    particle1.id = 150;                           // (fuera de recinto)
    particle1.density = 2;
    simParticle particle2 = simParticle();
    particle2.position = {0.1, 0.1, 0.1}; // index = {6, 6, 6} -> {4, 6, 4}
    particle2.id = 20;
    particle2.density = 1;
    particles.push_back(particle1);
    particles.push_back(particle2);

    grid testGrid(h, mass, particles);
    //testGrid.fillBlocks(particles); -> YA SE LLAMA EN EL CONSTRUCTOR DE GRID

    EXPECT_EQ(testGrid.getBlock({4, 6, 4}).getNParticles(), 2);
    EXPECT_EQ(testGrid.getBlock({4, 6, 4}).getParticles()[0], &particles[0]);
    EXPECT_EQ(testGrid.getBlock({4, 6, 4}).getParticles()[1], &particles[1]);
}


TEST(gridTests, getNBlocks){
    double h = 0.1;
    double mass = 1;
    vector<simParticle> particles;
    grid grid1(h, mass, particles);
    EXPECT_EQ(grid1.getNBlocks(), Vector3D<int>(1, 1, 1));
}

TEST(gridTests, getBlock){
    vector<simParticle> particles;
    simParticle bufferParticle;
    for (int i = 0; i < 100; ++i) {
      bufferParticle = simParticle();
      bufferParticle.id = i;
      bufferParticle.position = {0.1*i, 0.1*i, 0.1*i};
      particles.push_back(bufferParticle);
    }


    double h    = 0.1;
    double mass = 1;
    grid grid1(h, mass, particles);
    EXPECT_EQ(grid1.getBlock(Vector3D<int>(0,0,0)).getBlockIndex(), Vector3D<int>(0,0,0));
}

TEST(gridTests, getTotalBlocks){
    vector<simParticle> particles;
    simParticle bufferParticle;
    for (int i = 0; i < 100; ++i) {
      bufferParticle = simParticle();
      bufferParticle.id = i;
      bufferParticle.position = {0.1*i, 0.1*i, 0.1*i};
      particles.push_back(bufferParticle);
    }

    double h    = 0.1;
    double mass = 1;
    grid grid1(h, mass, particles);
    EXPECT_EQ(grid1.getTotalBlocks(), 1);
}

TEST(gridTests, getBlockSize){
    vector<simParticle> particles;
    simParticle bufferParticle;
    for (int i = 0; i < 100; ++i) {
      bufferParticle = simParticle();
      bufferParticle.id = i;
      bufferParticle.position = {0.1*i, 0.1*i, 0.1*i};
      particles.push_back(bufferParticle);
    }

    double h    = 0.1;
    double mass = 1;
    grid grid1(h, mass, particles);

    EXPECT_EQ(grid1.getBlockSize(), Vector3D<double>(0.13, 0.18, 0.13));
}

TEST(gridTests, blockIsAdjacent){
    double h    = 0.1;
    double mass = 1;
    vector<simParticle> particles;
    grid grid(h, mass, particles);
    block block1({1, 1, 1}, {1,2,4});
    block block2({1, 1, 1}, {1,3,3});
    block block3({1, 1, 1}, {3, 4, 6});
    EXPECT_TRUE(grid.isAdjacent(block1.getBlockIndex(), block2.getBlockIndex()));
    EXPECT_FALSE(grid.isAdjacent(block1.getBlockIndex(), block3.getBlockIndex()));
}



TEST(gridTests, blockIsAdjacent2){
    double h    = 0.1;
    double mass = 1;
    vector<simParticle> particles;
    grid grid(h, mass, particles);
    vector<block> blocks;
    int n_bloques_x = 15;
    int n_bloques_y = 20;
    int n_bloques_z = 15;
    for(int i=0; i < n_bloques_x; ++i){
      for(int j=0; j < n_bloques_y; ++j){
        for(int k=0; k < n_bloques_z; ++k){
          blocks.emplace_back(block({1, 1, 1}, {i, j, k}));
        }
      }
    }
    // Comprobamos que los bloques del medio tienen 26 adyacentes,
    // en una pared tienen 17 adyacentes y en esquina tienen 7 adyacentes
    int adjacentes_medio = 0;
    int adjacentes_pared_medio = 0;
    int adjacentes_pared_borde = 0;
    int adjacentes_esquina = 0;
    for(u_long s = 0; s < blocks.size(); ++s){
      if(grid.isAdjacent(blocks[2000].getBlockIndex(), blocks[s].getBlockIndex())){
        adjacentes_medio += 1;
      }
      if(grid.isAdjacent(blocks[52].getBlockIndex(), blocks[s].getBlockIndex())){
        adjacentes_pared_medio += 1;
      }
      if(grid.isAdjacent(blocks[15].getBlockIndex(), blocks[s].getBlockIndex())){
        adjacentes_pared_borde += 1;
      }
      if(grid.isAdjacent(blocks[0].getBlockIndex(), blocks[s].getBlockIndex())){
        adjacentes_esquina += 1;
      }
    }
    EXPECT_EQ(adjacentes_esquina, 7);
    EXPECT_EQ(adjacentes_pared_borde, 11);
    EXPECT_EQ(adjacentes_pared_medio, 17);
    EXPECT_EQ(adjacentes_medio, 26);
}


TEST(gridTests, reposParticles){
    simParticle particle_fuera_recinto;
    simParticle particle_en_bloque_incorrecto;
    simParticle particle_en_bloque_correcto;
    particle_fuera_recinto.position = {1, 1, 1};
    particle_en_bloque_incorrecto.position = {2, 2, 2};
    particle_en_bloque_correcto.position = {0.003, 0.01, 0.002};
    vector<simParticle> particles;
    particles.push_back(particle_fuera_recinto);
    particles.push_back(particle_en_bloque_incorrecto);
    particles.push_back(particle_en_bloque_correcto);
    double h = 0.025;
    double mass = 1.0;
    grid grid(h, mass, particles);
    particles[0].position = {-1, -4, -1}; // index = (-35, -153, -35) -> (0, 0, 0)
    particles[1].position = {0.006, 0.009, 0.006}; // index = (2, 3, 2)
    particles[2].position = {0.003, 0.01, 0.002}; // index = (2, 3, 2) (no cambia)

    // blockSize = (0.026, 0.0257143, 0.026); nBlocks = (5, 7, 5)
    // Obtego los bloques de grid y añado una particula fuera
    // del recinto, una correctamente y otra donde no corresponde
    grid.reposParticles();
    block block1 = grid.getBlock({0, 0, 0});
    block block2 = grid.getBlock({2, 3, 2});

    EXPECT_EQ(block1.getNParticles(), 1);
    EXPECT_EQ(block1.getParticles()[0], &particles[0]);
    EXPECT_EQ(block2.getNParticles(), 2);
    EXPECT_EQ(block2.getParticles()[0], &particles[2]);
    EXPECT_EQ(block2.getParticles()[1], &particles[1]);
}

TEST(gridTests, initParticles) {
    // Comprobar que las particulas de todos los bloques se inicializan con
    // la aceleración de la gravedad y densidad a 0
    vector<simParticle> particles;
    simParticle particle1;
    simParticle particle2;
    particle1.position = {0.1, 0.1, 0.1};
    particle2.position = {0.1, 0.15, 0.1};
    particles.push_back(particle1);
    particles.push_back(particle2);
    double h    = 0.1;
    double mass = 1;
    grid testGrid(h, mass, particles);
    testGrid.initParticles();
    for (int i = 0; i < testGrid.getNBlocks().x(); ++i) {
      for (int j = 0; j < testGrid.getNBlocks().y(); ++j) {
        for (int k = 0; k < testGrid.getNBlocks().z(); ++k) {
          if (testGrid.getBlock({i, j, k}).getParticles().size() > 0) {
            block block1 = testGrid.getBlock({i, j, k});
            for (auto & particle :  block1.getParticles()) {
              EXPECT_EQ(particle->aceleration, Vector3D<double>(0, -9.8, 0));
              EXPECT_EQ(particle->density, 0);
            }
          }
        }
      }
    }
}

TEST(gridTests, updateDensities) {
    // Comprobar que las densidades de las particulas se actualizan correctamente
    vector<simParticle> particles;
    // Particulas lejanas, no se actualiza la densidad
    simParticle particle1;
    simParticle particle2;
    // Particulas cercanas, se actualiza la densidad SOLO entre ellas
    simParticle particle3;
    simParticle particle4;
    particle1.position = {25, 18, 24};
    particle1.id       = 1;
    particle2.position = {20, 15, 20};
    particle2.id       = 2;
    particle3.position = {0.0005, 0.0005, 0.0005};
    particle3.id       = 3;
    particle4.position = {0.0006, 0.0005, 0.0004};
    particle4.id       = 4;
    particles.push_back(particle1);
    particles.push_back(particle2);
    particles.push_back(particle3);
    particles.push_back(particle4);
    double h    = 0.1;
    double mass = 1;
    grid testGrid(h, mass, particles);
    testGrid.initParticles();
    testGrid.updateDensities();



    for (int i = 0; i < testGrid.getNBlocks().x(); ++i) {
      for (int j = 0; j < testGrid.getNBlocks().y(); ++j) {
        for (int k = 0; k < testGrid.getNBlocks().z(); ++k) {
          if (testGrid.getBlock({i, j, k}).getParticles().size() > 0) {
            block block1 = testGrid.getBlock({i, j, k});
            for (auto & particle : block1.getParticles()) {
              if (particle->id == 1 || particle->id == 2) {
                EXPECT_EQ(particle->density, 0);
              }

              // ¡¡¡¡¡¡¡¡¡¡¡ FALLA SOLO ESTO !!!!!!!!!!!!!!!
              if (particle->id == 3 || particle->id == 4) {
                // Densidad que debería dar calculada con Wolffram Alpha: 9.99994000011999992e-07
                EXPECT_EQ(particle->density, 9.99994000011999992e-07); // El programa da
                                                                      // 9.9999400001200076e-07
                                                                      // Es decir, redondea y no
                                                                      // identificamos porqué
              }
            }
          }

        }
      }
    }
}

TEST(gridTests, densitiesNormalize){
    vector<simParticle> particles;
    simParticle particle1;
    simParticle particle2;
    simParticle particle3;
    simParticle particle4;
    particle1.position = {25, 18, 24};
    particle1.id = 1;
    particle2.position = {20, 15, 20};
    particle2.id = 2;
    particle3.position = {0.0005, 0.0005, 0.0005};
    particle3.id = 3;
    particle4.position = {0.0006, 0.0005, 0.0004};
    particle4.id = 4;
    particles.push_back(particle1);
    particles.push_back(particle2);
    particles.push_back(particle3);
    particles.push_back(particle4);
    double h    = 0.1;
    double mass = 1;
    grid testGrid(h, mass, particles);
    testGrid.updateDensities();
    testGrid.densitiesNormalize();

    for (int i = 0; i < testGrid.getNBlocks().x(); ++i) {
      for (int j = 0; j < testGrid.getNBlocks().y(); ++j) {
        for (int k = 0; k < testGrid.getNBlocks().z(); ++k) {
          if (testGrid.getBlock({i, j, k}).getNParticles() > 0) {
            block block1 = testGrid.getBlock({i, j, k});
            for (auto & particle : block1.getParticles()) {
              if (particle->id == 1 || particle->id == 2) {
                EXPECT_EQ(particle->density, 1566.6814710608448);
              }

              if (particle->id == 3 || particle->id == 4) {
                // Densidad que debería dar calculada con Wolfram Alpha: 3133.3535420516641...
                EXPECT_EQ(particle->density, 3133.3535420516641);
              }
            }
          }
        }
      }
    }
}


TEST(gridTests, acelerationTransfer){
    vector<simParticle> particles;
    simParticle particle1;
    simParticle particle2;
    simParticle particle3;
    simParticle particle4;
    particle1.position = {25, 18, 24};
    particle1.id = 1;
    particle2.position = {20, 15, 20};
    particle2.id = 2;
    particle3.position = {0.0005, 0.0005, 0.0005}; //index = (0, 0, 0)
    particle3.id = 3;
    particle3.velocity = {1, 2, 3};
    particle4.position = {0.0006, 0.0005, 0.0004}; //index = (0, 0, 0)
    particle4.velocity = {4, 5, 6};
    particle4.id = 4;
    particles.push_back(particle1);
    particles.push_back(particle2);
    particles.push_back(particle3);
    particles.push_back(particle4);
    double h    = 0.1;
    double mass = 1;
    grid testGrid(h, mass, particles);
    testGrid.reposParticles();
    testGrid.initParticles();
    testGrid.updateDensities();
    testGrid.densitiesNormalize();
    testGrid.acelerationTransfer();
    cout << "Posicion de la 3: " << particle3.position << endl;
    cout << "Posicion de la 4: " << particle4.position << endl;
    cout << "Velocidad de la 3: " << particle3.velocity << endl;
    cout << "Velocidad de la 4: " << particle4.velocity << endl;

    block block = testGrid.getBlock({0, 0, 0});

    const array<double, 3> magicNums = {10e-13, 15, 45};
    double squaredDistance = pow((particle4.position - particle3.position).norm(), 2);
    double dist_ij = sqrt(max(squaredDistance, magicNums[0]));
    
    Vector3D<double> initialAcc = {0.0, -9.8, 0.0};
    Vector3D<double> expectedAceleration3 = ((particle4.position - particle3.position)*(magicNums[1]/(M_PI*(h*h*h*h*h*h)))*((3*1*cte::PRESION_RIGIDEZ)/2))
                       * (((h-dist_ij)*(h-dist_ij))/dist_ij) * (((block.getParticles()[1]->density + block.getParticles()[0]->density - (2*cte::DENS_FLUIDO))));
    expectedAceleration3 = expectedAceleration3 + ((particle3.velocity-particle4.velocity)*(magicNums[2]/(M_PI*(h*h*h*h*h*h)))*0.4);
    expectedAceleration3 = expectedAceleration3/(block.getParticles()[1]->density*block.getParticles()[0]->density);
    Vector3D<double> expectedAceleration4 = expectedAceleration3;
    expectedAceleration3 = initialAcc - expectedAceleration3;
    expectedAceleration4 = initialAcc + expectedAceleration4;


    cout << block.getParticles()[0]->id << endl;
    cout << block.getParticles()[1]->id << endl;
    EXPECT_EQ(block.getParticles()[0]->aceleration, expectedAceleration3);
    EXPECT_EQ(block.getParticles()[1]->aceleration, expectedAceleration4);
}



TEST(gridTests, collisionX_AXIS){
    simParticle particle = simParticle();
    particle.position = {-8, 2, 3};
    particle.initialVelocity = {2, 2, 4};
    particle.velocity = {4, 2, 1};
    particle.aceleration = {3, -9.8, 0};
    std::vector<simParticle> particles = {particle};
    double h    = 0.1;
    double mass = 1;

    grid testGrid(h, mass, particles);
    testGrid.collisionX_AXIS();

    double const expectedPositionX = -8 + (2*0.001);
    double const deltaX = 0.0002 - (expectedPositionX-(-0.065));
    double const expectedAcelerationX = 3 + ((30000*deltaX)-(128*4));

    EXPECT_EQ(testGrid.getBlock({0, 0, 0}).getParticles()[0]->position.x(), expectedPositionX);
    EXPECT_EQ(testGrid.getBlock({0, 0, 0}).getParticles()[0]->aceleration.x(), expectedAcelerationX);
}


TEST(gridTests, collisionY_AXIS){
    simParticle particle = simParticle();
    particle.position = {-8, 2, 3};
    particle.initialVelocity = {2, 2, 4};
    particle.velocity = {4, 2, 1};
    particle.aceleration = {3, -9.8, 0};
    std::vector<simParticle> particles = {particle};
    double h    = 0.1;
    double mass = 1;

    grid testGrid(h, mass, particles);
    testGrid.collisionY_AXIS();

    double const expectedPositionY = 2 + (2*0.001);
    // double const deltaY = 0.0002 - (expectedPositionY-(-0.08));
    // deltaY = -2.0818 menor que epsilon = 10e-11 -> NO CAMBIA LA ACELERACIÓN
    double const expectedAcelerationY = -9.8;

    EXPECT_EQ(testGrid.getBlock({0, 0, 0}).getParticles()[0]->position.y(), expectedPositionY);
    EXPECT_EQ(testGrid.getBlock({0, 0, 0}).getParticles()[0]->aceleration.y(), expectedAcelerationY);
}



TEST(gridTests, collisionZ_AXIS){
    simParticle particle = simParticle();
    particle.position = {-8, 2, 3};
    particle.initialVelocity = {2, 2, 4};
    particle.velocity = {4, 2, 1};
    particle.aceleration = {3, -9.8, 0};
    std::vector<simParticle> particles = {particle};
    double h    = 0.1;
    double mass = 1;

    grid testGrid(h, mass, particles);
    testGrid.collisionZ_AXIS();

    double const expectedPositionZ = 3 + (4*0.001);
    // double const deltaZ = 0.0002 - (expectedPositionZ-(-0.065));
    // deltaZ = -2.93 es menor que epsilon = 10e-11 -> NO CAMBIA LA ACELERACIÓN
    double const expectedAcelerationZ = 0;

    EXPECT_EQ(testGrid.getBlock({0, 0, 0}).getParticles()[0]->position.z(), expectedPositionZ);
    EXPECT_EQ(testGrid.getBlock({0, 0, 0}).getParticles()[0]->aceleration.z(), expectedAcelerationZ);
}


TEST(gridTests, particlesMovement){

    vector<simParticle> particles;
    simParticle particle1;
    simParticle particle2;
    particle1.position = {-8, -4, -5};
    particle1.id = 1;
    particle1.velocity = {4, 2, 1};
    particle2.position = {-14, -9, -10};
    particle2.id = 2;
    particle2.velocity = {2, 2, 1};
    particles.push_back(particle1);
    particles.push_back(particle2);
    double h    = 0.1;
    double mass = 1;
    Vector3D<double> initialPosition1 = particle1.position;
    Vector3D<double> initialVelocity1 = particle1.velocity;
    Vector3D<double> initialPosition2 = particle2.position;
    Vector3D<double> initialVelocity2 = particle2.velocity;

    grid testGrid(h, mass, particles);
    testGrid.initParticles();
    testGrid.particlesMovement();

    for (int i = 0; i < testGrid.getNBlocks().x(); ++i) {
      for (int j = 0; j < testGrid.getNBlocks().y(); ++j) {
        for (int k = 0; k < testGrid.getNBlocks().z(); ++k) {
          if (testGrid.getBlock({i, j, k}).getParticles().size() > 0) {
            block block1 = testGrid.getBlock({i, j, k});
            for (u_long l = 0; l < block1.getParticles().size(); ++l) {
              if (block1.getParticles()[l]->id == 1) {
                EXPECT_NE(block1.getParticles()[l]->position, initialPosition1);
                EXPECT_NE(block1.getParticles()[l]->velocity, initialVelocity1);
              }
              if (block1.getParticles()[l]->id == 2) {
                EXPECT_NE(block1.getParticles()[l]->position, initialPosition2);
                EXPECT_NE(block1.getParticles()[l]->velocity, initialVelocity2);
              }
            }
          }
        }
      }
    }
}




TEST(gridTests, collisionsX_AXIS2){

    vector<simParticle> particles;
    simParticle particle1;
    simParticle particle2;
    particle1.position = {-8, -4, -5};
    particle1.id = 1;
    particle1.initialVelocity = {2, 2, 4};
    particle1.velocity = {4, 2, 1};
    particle2.position = {-14, -9, -10};
    particle2.id = 2;
    particle2.initialVelocity = {1, 1, 2};
    particle2.velocity = {2, 2, 1};
    particles.push_back(particle1);
    particles.push_back(particle2);
    double h    = 0.1;
    double mass = 1;
    grid testGrid(h, mass, particles);
    testGrid.collisionX_AXIS2();
    double expectedPositionX1 = -0.065 - (-8+0.065);
    double expectedVelocityX1 = -4;
    double expectedInitVelocityX1 = -2;
    double expectedPositionX2 = -0.065 - (-14+0.065);
    double expectedVelocityX2 = -2;
    double expectedInitVelocityX2 = -1;


    for (int i = 0; i < testGrid.getNBlocks().x(); ++i) {
      for (int j = 0; j < testGrid.getNBlocks().y(); ++j) {
        for (int k = 0; k < testGrid.getNBlocks().z(); ++k) {
          if (testGrid.getBlock({i, j, k}).getParticles().size() > 0) {
            block block1 = testGrid.getBlock({i, j, k});
            for (u_long l = 0; l < block1.getParticles().size(); ++l) {
              if (block1.getParticles()[l]->id == 1) {
                EXPECT_EQ(block1.getParticles()[l]->position.x(), expectedPositionX1);
                EXPECT_EQ(block1.getParticles()[l]->velocity.x(), expectedVelocityX1);
                EXPECT_EQ(block1.getParticles()[l]->initialVelocity.x(), expectedInitVelocityX1);
              }
              if (block1.getParticles()[l]->id == 2) {
                EXPECT_EQ(block1.getParticles()[l]->position.x(), expectedPositionX2);
                EXPECT_EQ(block1.getParticles()[l]->velocity.x(), expectedVelocityX2);
                EXPECT_EQ(block1.getParticles()[l]->initialVelocity.x(), expectedInitVelocityX2);
              }
            }
          }
        }
      }
    }
}

TEST(gridTests, collisionsY_AXIS2){

    vector<simParticle> particles;
    simParticle particle1;
    simParticle particle2;
    particle1.position = {-8, -4, -5};
    particle1.id = 1;
    particle1.initialVelocity = {2, 2, 4};
    particle1.velocity = {4, 2, 1};
    particle2.position = {-14, -9, -10};
    particle2.id = 2;
    particle2.initialVelocity = {1, 1, 2};
    particle2.velocity = {2, 2, 1};
    particles.push_back(particle1);
    particles.push_back(particle2);
    double h    = 0.1;
    double mass = 1;
    grid testGrid(h, mass, particles);
    testGrid.collisionY_AXIS2();
    double expectedPositionY1 = -0.08 - (-4+0.08);
    double expectedVelocityY1 = -2;
    double expectedInitVelocityY1 = -2;
    double expectedPositionY2 = -0.08 - (-9+0.08);
    double expectedVelocityY2 = -2;
    double expectedInitVelocityY2 = -1;


    for (int i = 0; i < testGrid.getNBlocks().x(); ++i) {
      for (int j = 0; j < testGrid.getNBlocks().y(); ++j) {
        for (int k = 0; k < testGrid.getNBlocks().z(); ++k) {
          if (testGrid.getBlock({i, j, k}).getParticles().size() > 0) {
            block block1 = testGrid.getBlock({i, j, k});
            for (u_long l = 0; l < block1.getParticles().size(); ++l) {
              if (block1.getParticles()[l]->id == 1) {
                EXPECT_EQ(block1.getParticles()[l]->position.y(), expectedPositionY1);
                EXPECT_EQ(block1.getParticles()[l]->velocity.y(), expectedVelocityY1);
                EXPECT_EQ(block1.getParticles()[l]->initialVelocity.y(), expectedInitVelocityY1);
              }
              if (block1.getParticles()[l]->id == 2) {
                EXPECT_EQ(block1.getParticles()[l]->position.y(), expectedPositionY2);
                EXPECT_EQ(block1.getParticles()[l]->velocity.y(), expectedVelocityY2);
                EXPECT_EQ(block1.getParticles()[l]->initialVelocity.y(), expectedInitVelocityY2);
              }
            }
          }
        }
      }
    }
}

TEST(gridTests, collisionsZ_AXIS2){

    vector<simParticle> particles;
    simParticle particle1;
    simParticle particle2;
    particle1.position = {-8, -4, -5};
    particle1.id = 1;
    particle1.initialVelocity = {2, 2, 4};
    particle1.velocity = {4, 2, 1};
    particle2.position = {-14, -9, -10};
    particle2.id = 2;
    particle2.initialVelocity = {1, 1, 2};
    particle2.velocity = {2, 2, 1};
    particles.push_back(particle1);
    particles.push_back(particle2);
    double h    = 0.1;
    double mass = 1;
    grid testGrid(h, mass, particles);
    testGrid.initParticles();
    testGrid.collisionZ_AXIS2();
    double expectedPositionZ1 = -0.065 - (-5+0.065);
    double expectedVelocityZ1 = -1;
    double expectedInitVelocityZ1 = -4;
    double expectedPositionZ2 = -0.065 - (-10+0.065);
    double expectedVelocityZ2 = -1;
    double expectedInitVelocityZ2 = -2;

    for (int i = 0; i < testGrid.getNBlocks().x(); ++i) {
      for (int j = 0; j < testGrid.getNBlocks().y(); ++j) {
        for (int k = 0; k < testGrid.getNBlocks().z(); ++k) {
          if (testGrid.getBlock({i, j, k}).getParticles().size() > 0) {
            block block1 = testGrid.getBlock({i, j, k});
            for (u_long l = 0; l < block1.getParticles().size(); ++l) {
              if (block1.getParticles()[l]->id == 1) {
                EXPECT_EQ(block1.getParticles()[l]->position.z(), expectedPositionZ1);
                EXPECT_EQ(block1.getParticles()[l]->velocity.z(), expectedVelocityZ1);
                EXPECT_EQ(block1.getParticles()[l]->initialVelocity.z(), expectedInitVelocityZ1);
              }
              if (block1.getParticles()[l]->id == 2) {
                EXPECT_EQ(block1.getParticles()[l]->position.z(), expectedPositionZ2);
                EXPECT_EQ(block1.getParticles()[l]->velocity.z(), expectedVelocityZ2);
                EXPECT_EQ(block1.getParticles()[l]->initialVelocity.z(), expectedInitVelocityZ2);
              }
            }
          }
        }
      }
    }
}


//NOLINTEND