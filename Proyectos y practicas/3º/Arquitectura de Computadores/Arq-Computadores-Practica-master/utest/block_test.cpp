//
// Created by defalco on 2/10/23.
//
#include <iostream>
#include <gtest/gtest.h>
#include "sim/simParticle.hpp"
#include "sim/block.hpp"
#include <cmath>

using namespace std;
//NOLINTBEGIN
TEST(blockTests, blockConstructor1){
    Vector3D<double> const sizeBlock = {1, 1, 1};
    Vector3D<int> const blockIndex = {1, 1, 1};
    block block1(sizeBlock, blockIndex);
    EXPECT_EQ(block1.getSizeBlock(), sizeBlock);
    EXPECT_EQ(block1.getBlockIndex(), blockIndex);
}

TEST(blockTests, getSizeBlock){
      Vector3D<double> const sizeBlock = {1, 1, 1};
      block block1(sizeBlock, {1, 1, 1});
      EXPECT_EQ(block1.getSizeBlock(), sizeBlock);
}

TEST(blockTests, getBlockIndex){
      Vector3D<double> const sizeBlock = {1, 1, 1};
      block const block1(sizeBlock, {1, 1, 1});
      Vector3D<int> const index = {1,1,1};
      EXPECT_EQ(block1.getBlockIndex(), index);
}

TEST(blockTests, getI ){
      Vector3D<double> const sizeBlock = {1, 1, 1};
      block const block1(sizeBlock, {1, 2, 3});
      int const cordi = 1;
      EXPECT_EQ(block1.getI(), cordi);
}

TEST(blockTests, getJ){
      Vector3D<double> const sizeBlock = {1, 1, 1};
      block const block1(sizeBlock, {1, 2, 3});
      int const cordj = 2;
      EXPECT_EQ(block1.getJ(), cordj);
}

TEST(blockTests, getK){
      Vector3D<double> const sizeBlock = {1, 1, 1};
      block const block1(sizeBlock, {1, 2, 3});
      int const cordk = 3;
      EXPECT_EQ(block1.getK(), cordk);
}

TEST(blockTests, storeParticle){
      Vector3D<double> const sizeBlock = {1, 1, 1};
      block block1(sizeBlock, {1, 2, 3});

      simParticle particle1;
      block1.storeParticle(&particle1);

      EXPECT_EQ(block1.getNParticles(),1);

}

TEST(blockTests, getParticles){
      Vector3D<double> const sizeBlock = {1, 1, 1};
      block block1(sizeBlock, {1, 2, 3});
      simParticle particle1;
      block1.storeParticle(&particle1);

      std::vector<simParticle*> particles = block1.getParticles();
      EXPECT_EQ(particles[0], &particle1);
}

TEST(blockTests, popParticle){
      Vector3D<double> const sizeBlock = {1, 1, 1};
      block block1(sizeBlock, {1, 2, 3});
      simParticle particle1;
      block1.storeParticle(&particle1);

      simParticle* particle2 = block1.popParticle(&particle1);
      EXPECT_EQ(particle2, &particle1);
      EXPECT_EQ(block1.getNParticles(), 0);
}

TEST(blockTests, getNParticles0){
      Vector3D<double> const sizeBlock = {1, 1, 1};
      block block1(sizeBlock, {1, 2, 3});
      EXPECT_EQ(block1.getNParticles(), 0);
}

TEST(blockTests, getNParticles1){
      Vector3D<double> const sizeBlock = {1, 1, 1};
      block block1(sizeBlock, {1, 2, 3});
      simParticle particle1;
      block1.storeParticle(&particle1);
      EXPECT_EQ(block1.getNParticles(), 1);
}

TEST(blockTests, getNParticles2){
      Vector3D<double> const sizeBlock = {1, 1, 1};
      block block1(sizeBlock, {1, 2, 3});
      vector<simParticle*> particles;
      const int iters = 15;
      for (int i = 0; i < iters; ++i) {
            simParticle particle1;
            particles.push_back(&particle1);
            block1.storeParticle(&particle1);
      }
      EXPECT_EQ(block1.getNParticles(), 15);
}

TEST(blockTests, initParticles){
      Vector3D<double> const sizeBlock = {1, 1, 1};
      block block(sizeBlock, {0, 0, 0});
      simParticle particle = simParticle();
      particle.position = {-8, 2, 3};
      particle.initialVelocity = {2, 2, 4};
      particle.velocity = {4, 2, 1};
      particle.aceleration = {3, -9.8, 0};
      block.storeParticle(&particle);

      block.initParticles({1,2,3});

      EXPECT_EQ(particle.density, 0);
      EXPECT_EQ(particle.aceleration, Vector3D<double>(1,2,3));
}

TEST(blockTests, updateDensities){
      Vector3D<double> const sizeBlock = {1, 1, 1};
      block block1(sizeBlock, {1, 2, 3});
      block block2(sizeBlock, {2, 2, 3});
      simParticle particle1 = simParticle();
      particle1.position = {2, 3, 2};
      particle1.id = 150;
      particle1.density = 2;
      simParticle particle2 = simParticle();
      particle2.position = {3, 3, 3};
      particle2.id = 20;
      particle2.density = 1;
      block1.storeParticle(&particle1);
      block2.storeParticle(&particle2);

      double const h = 3;
      double deltaDensity = (h*h)-(particle1.position-particle2.position).norm()*(particle1.position-particle2.position).norm();
      deltaDensity = deltaDensity * deltaDensity * deltaDensity;
      double const expectedDensityPticle1 = 2 + deltaDensity;
      double const expectedDensityPticle2 = 1 + deltaDensity;

      block1.updateDensities(h, &block2);

      EXPECT_EQ(particle1.density, expectedDensityPticle1);
      EXPECT_EQ(particle2.density, expectedDensityPticle2);

      // No deben actualizarse las densidades
      block2.updateDensities(h,&block1);
      EXPECT_EQ(particle1.density, expectedDensityPticle1);
      EXPECT_EQ(particle2.density, expectedDensityPticle2);
}



TEST(blockTests, densitiesNormalize){
      block block1({1,1,1}, {0,0,0});
      simParticle particle = simParticle();
      particle.density = 1;
      double const h = 1;
      double const mass = 1;
      block1.storeParticle(&particle);
      double const expectedDensity = (particle.density+h)*(315/(64*M_PI*h))*mass;
      block1.densitiesNormalize(h, mass);
      EXPECT_EQ(particle.density, expectedDensity);
}


TEST(blockTests, acelerationTransfer){
      Vector3D<double> const sizeBlock = {1, 1, 1};
      block block1(sizeBlock, {1, 2, 3});
      block block2(sizeBlock, {2, 2, 3});
      simParticle particle1 = simParticle();
      particle1.id = 800;
      particle1.density = 2;
      particle1.position = {1, 1, 1};
      particle1.aceleration = {1, 1, 1};
      Vector3D<double> const Acc1 = {1, 1, 1};
      simParticle particle2 = simParticle();
      particle2.id = 24;
      particle2.density = 1;
      particle2.position = {2, 2, 2};
      particle2.aceleration = {2, 2, 2};
      Vector3D<double> const Acc2 = {2, 2, 2};
      double const h = 3;
      double const mass = 1;
      block1.storeParticle(&particle1);
      block2.storeParticle(&particle2);
      Vector3D<double> deltaAceleration = {};
      double const squaredDistance = pow((particle1.position - particle2.position).norm(), 2);
      const array<double, 3> magicNums = {10e-13, 15, 45};
      double const dist_ij = sqrt(max(squaredDistance, magicNums[0]));

      deltaAceleration = ((particle1.position - particle2.position)*(magicNums[1]/(M_PI*(h*h*h*h*h*h)))*((3*mass*cte::PRESION_RIGIDEZ)/2))
                         * (((h-dist_ij)*(h-dist_ij))/dist_ij) * ((particle1.density + particle2.density - (2*cte::DENS_FLUIDO)));
      deltaAceleration = deltaAceleration + (particle2.velocity - particle1.velocity)* (magicNums[2]/(M_PI*(h*h*h*h*h*h)))*cte::VISCOSIDAD*mass;
      deltaAceleration = deltaAceleration/(particle1.density*particle2.density);
      Vector3D<double> const expectedAccPticle1 = Acc1 + deltaAceleration;
      Vector3D<double> const expectedAccPticle2 = Acc2 - deltaAceleration;

      block1.acelerationTransfer(h, mass, &block2);
      EXPECT_EQ(particle1.aceleration, expectedAccPticle1);
      EXPECT_EQ(particle2.aceleration, expectedAccPticle2);

      // No deben actualizarse las aceleraciones
      block2.acelerationTransfer(h, mass, &block1);
      EXPECT_EQ(particle1.aceleration, expectedAccPticle1);
      EXPECT_EQ(particle2.aceleration, expectedAccPticle2);
}

TEST(blockTests, collisionX_AXIS){
      Vector3D<double> const sizeBlock = {1, 1, 1};
      block block(sizeBlock, {0, 0, 0});
      simParticle particle = simParticle();
      particle.position = {-8, 2, 3};
      particle.initialVelocity = {2, 2, 4};
      particle.velocity = {4, 2, 1};
      particle.aceleration = {3, -9.8, 0};
      block.storeParticle(&particle);

      double const expectedPositionX = -8 + (2*0.001);
      double const deltaX = 0.0002 - (expectedPositionX-(-0.065));
      double const expectedAcelerationX = 3 + ((30000*deltaX)-(128*4));

      block.collisionX_AXIS();

      EXPECT_EQ(particle.position.x(), expectedPositionX);
      EXPECT_EQ(particle.aceleration.x(), expectedAcelerationX);
}

TEST(blockTests, collisionY_AXIS){
      Vector3D<double> const sizeBlock = {1, 1, 1};
      block block(sizeBlock, {0, 0, 0});
      simParticle particle = simParticle();
      particle.position = {-8, -2, 3};
      particle.initialVelocity = {2, 2, 4};
      particle.velocity = {4, 2, 1};
      particle.aceleration = {3, -9.8, 0};
      block.storeParticle(&particle);

      double const expectedPositionY = -2 + (2*0.001);
      double const deltaY = 0.0002 - (expectedPositionY-(-0.08));
      double const expectedAcelerationY = -9.8 + ((30000*deltaY)-(128*2));

      block.collisionY_AXIS();

      EXPECT_EQ(particle.position.y(), expectedPositionY);
      EXPECT_EQ(particle.aceleration.y(), expectedAcelerationY);
}

TEST(blockTests, collisionZ_AXIS){
      Vector3D<double> const sizeBlock = {1, 1, 1};
      block block(sizeBlock, {0, 0, 0});
      simParticle particle = simParticle();
      particle.position = {-8, 2, -3};
      particle.initialVelocity = {2, 2, 4};
      particle.velocity = {4, 2, 1};
      particle.aceleration = {3, -9.8, 0};
      block.storeParticle(&particle);

      double const expectedPositionZ = -3 + (4*0.001);
      double const deltaZ = 0.0002 - (expectedPositionZ-(-0.065));
      double const expectedAcelerationZ = 0 + ((30000*deltaZ)-(128*1));

      block.collisionZ_AXIS();

      EXPECT_EQ(particle.position.z(), expectedPositionZ);
      EXPECT_EQ(particle.aceleration.z(), expectedAcelerationZ);
}


TEST(blockTests, particlesMovement){
      block testBlock({1, 1, 1}, {0, 0, 0});
      // Agrega partículas a testBlock para la prueba
        for (double i = 0; i < 10; ++i) {
                simParticle* particle = new simParticle();
                particle->position = {i, i, i};
                particle->velocity = {i, i, i};
                particle->aceleration = {i, i, i};
                testBlock.storeParticle(particle);
        }

      // Guarda el estado inicial de las partículas para comparar después de llamar a particlesMovement()
      Vector3D<double> initialPositions{};
      Vector3D<double> initialVelocities{};

      for (const auto &particle : testBlock.getParticles()) {
            initialPositions = particle->position;
            initialVelocities = particle->velocity;

      }

      // Llama a la función que se va a probar
      testBlock.particlesMovement();

      // Verifica que las posiciones, velocidades e inicializaciones hayan cambiado según lo esperado

      for (const auto &particle : testBlock.getParticles()) {
            // Verifica que la posición se haya actualizado correctamente
            EXPECT_NE(initialPositions, particle->position);

            // Verifica que la velocidad se haya actualizado correctamente
            EXPECT_NE(initialVelocities, particle->velocity);

      }
}

TEST(blockTests, collisionX_AXIS2){
      Vector3D<double> const sizeBlock = {1, 1, 1};
      block block(sizeBlock, {0, 0, 0});
      simParticle particle = simParticle();
      particle.position = {-8, -2, -3};
      particle.initialVelocity = {2, 2, 4};
      particle.velocity = {4, 2, 1};
      block.storeParticle(&particle);

      double const expectedPositionX = -0.065 - (-8+0.065);
      double const expectedVelocityX = -4;
      double const expectedInitVelocityX = -2;

      block.collisionX_AXIS2();

      EXPECT_EQ(particle.position.x(), expectedPositionX);
      EXPECT_EQ(particle.velocity.x(), expectedVelocityX);
      EXPECT_EQ(particle.initialVelocity.x(), expectedInitVelocityX);
}

TEST(blockTests, collisionY_AXIS2){
      Vector3D<double> const sizeBlock = {1, 1, 1};
      block block(sizeBlock, {0, 0, 0});
      simParticle particle = simParticle();
      particle.position = {-8, -2, -3};
      particle.initialVelocity = {2, 2, 4};
      particle.velocity = {4, 2, 1};
      block.storeParticle(&particle);

      double const expectedPositionY = -0.08 - (-2+0.08);
      double const expectedVelocityY = -2;
      double const expectedInitVelocityY = -2;

      block.collisionY_AXIS2();

      EXPECT_EQ(particle.position.y(), expectedPositionY);
      EXPECT_EQ(particle.velocity.y(), expectedVelocityY);
      EXPECT_EQ(particle.initialVelocity.y(), expectedInitVelocityY);
}

TEST(blockTests, collisionZ_AXIS2){
      Vector3D<double> const sizeBlock = {1, 1, 1};
      block block(sizeBlock, {0, 0, 0});
      simParticle particle = simParticle();
      particle.position = {-8, -2, -3};
      particle.initialVelocity = {2, 2, 4};
      particle.velocity = {4, 2, 1};
      block.storeParticle(&particle);

      double const expectedPositionZ = -0.065 - (-3+0.065);
      double const expectedVelocityZ = -1;
      double const expectedInitVelocityZ = -4;

      block.collisionZ_AXIS2();

      EXPECT_EQ(particle.position.z(), expectedPositionZ);
      EXPECT_EQ(particle.velocity.z(), expectedVelocityZ);
      EXPECT_EQ(particle.initialVelocity.z(), expectedInitVelocityZ);
}

//NOLINTEND