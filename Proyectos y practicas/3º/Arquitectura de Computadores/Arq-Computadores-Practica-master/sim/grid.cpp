//
// Created by nekos on 06/11/2023.
//


#include "grid.hpp"
#include "constants.h"

grid::grid(double h, double mass, std::vector<simParticle> & particles): h(h), mass(mass){
  grid::nBlocks = ((cte::Bmax-cte::Bmin)/h).to_int();
  grid::totalBlocks = nBlocks.x()*nBlocks.y()*nBlocks.z(); // NOLINT
  grid::blockSize = (cte::Bmax-cte::Bmin)/nBlocks.to_double();
  Vector3D<int> index = {};
  for (int i = 0; i < totalBlocks; ++i) {
    index = {i % nBlocks.x(),(i / nBlocks.x()) % nBlocks.y(), i / (nBlocks.x() * nBlocks.y())};
    blocks.emplace_back(blockSize, index);
  }
  fillBlocks(particles);
}

void grid::fillBlocks(std::vector<simParticle> & particles) {
  // fill the blocks
  Vector3D<int> index = {};
  for (auto & particle : particles) {
    simParticle* particlePtr = &particle;
    index = ((particlePtr->position.to_double()-cte::Bmin).to_double()/blockSize).to_int();
    if (index.x() < 0){index.set_x(0);}
    if (index.y() < 0){index.set_y(0);}
    if (index.z() < 0){index.set_z(0);}
    if (index.x() > nBlocks.x()-1){index.set_x(nBlocks.x()-1);}
    if (index.y() > nBlocks.y()-1){index.set_y(nBlocks.y()-1);}
    if (index.z() > nBlocks.z()-1){index.set_z(nBlocks.z()-1);}
    getBlock(index).storeParticle(particlePtr);
  }
}

Vector3D<int> grid::getNBlocks() {
  return nBlocks;
}

block & grid::getBlock(Vector3D<int> idx) {
  int const index = idx.x()+idx.y()*nBlocks.x()+idx.z()*(nBlocks.x()*nBlocks.y());
  return grid::blocks[index];
}

Vector3D<double> grid::getBlockSize() {
  return blockSize;
}

int grid::getTotalBlocks() const {
  return totalBlocks;
}

bool grid::isAdjacent(Vector3D<int> index1, Vector3D<int> index2) {
  return index1.isAdjacent(index2);
}

void grid::reposParticles(){
  std::vector<simParticle*> const blockParticles;
  Vector3D<int> index{};
  block* currentBlock; // NOLINT -> si lo inicializo dice que no se usa el valor.
  for (int i = 0; i < totalBlocks; ++i){
    currentBlock = &blocks[i];
    currentBlock->setNParticlesToZero();
    for (auto & particle : currentBlock->getParticles()) {
        index = ((particle->position.to_double()-cte::Bmin).to_double()/blockSize).to_int();
        if (index !=blocks[i].getBlockIndex()){
          if (index.x() < 0){index.set_x(0);}
          if (index.y() < 0){index.set_y(0);}
          if (index.z() < 0){index.set_z(0);}
          if (index.x() > nBlocks.x()-1){index.set_x(nBlocks.x()-1);}
          if (index.y() > nBlocks.y()-1){index.set_y(nBlocks.y()-1);}
          if (index.z() > nBlocks.z()-1){index.set_z(nBlocks.z()-1);}
          getBlock(index).storeParticle(currentBlock->popParticle(particle));
        }
        else{
          getBlock(index).addOneToNParticles();
        }
    }
  }
}

void grid::initParticles() {
  for (int i = 0; i < totalBlocks; ++i){
    blocks[i].initParticles(cte::GRAVEDAD);
  }
}

void grid::updateDensities() {
  for (int n1 = 0; n1 < totalBlocks; ++n1) {
    for (int n2 = 0; n2 < totalBlocks; ++n2) {
      if (isAdjacent(blocks[n1].getBlockIndex(),blocks[n2].getBlockIndex())){
        blocks[n1].updateDensities(h, &blocks[n2]);
      }
    }
    blocks[n1].updateDensities(h, &blocks[n1]);
  }
}

void grid::densitiesNormalize(){
  for (int i = 0; i < totalBlocks; ++i){
    blocks[i].densitiesNormalize(h, mass);
  }
}

void grid::acelerationTransfer(){
  for (int n1 = 0; n1 < totalBlocks; ++n1) {
    for (int n2 = 0; n2 < totalBlocks; ++n2) {
      if (isAdjacent(blocks[n1].getBlockIndex(),blocks[n2].getBlockIndex())){
        blocks[n1].acelerationTransfer(h, mass, &blocks[n2]);
      }
    }
    blocks[n1].acelerationTransfer(h, mass, &blocks[n1]); // bloque con si mismo
  }
}

void grid::collisions(){
    collisionX_AXIS();
    collisionY_AXIS();
    collisionZ_AXIS();
}

void grid::collisionX_AXIS(){
  for (int i = 0; i < totalBlocks; ++i){
    if (blocks[i].getBlockIndex().x() == 0 || blocks[i].getBlockIndex().x() == grid::nBlocks.x() - 1){
      blocks[i].collisionX_AXIS();
    }
  }
}

void grid::collisionY_AXIS(){
  for (int i = 0; i < totalBlocks; ++i){
    if (blocks[i].getBlockIndex().y() == 0 || blocks[i].getBlockIndex().y() == grid::nBlocks.y() - 1){
      blocks[i].collisionY_AXIS();
    }
  }
}

void grid::collisionZ_AXIS(){
  for (int i = 0; i < totalBlocks; ++i){
    if (blocks[i].getBlockIndex().z() == 0 || blocks[i].getBlockIndex().z() == grid::nBlocks.z() - 1){
      blocks[i].collisionZ_AXIS();
    }
  }
}

void grid::particlesMovement() {
    for (int i = 0; i < totalBlocks; ++i){
        blocks[i].particlesMovement();
    }
}

void grid::collisions2() {
    collisionX_AXIS2();
    collisionY_AXIS2();
    collisionZ_AXIS2();
}

void grid::collisionX_AXIS2() {
    for (int i = 0; i < totalBlocks; ++i){
            if (blocks[i].getBlockIndex().x() == 0 || blocks[i].getBlockIndex().x() == grid::nBlocks.x() - 1){
            blocks[i].collisionX_AXIS2();
            }
    }
}

void grid::collisionY_AXIS2() {
    for (int i = 0; i < totalBlocks; ++i){
        if (blocks[i].getBlockIndex().y() == 0 || blocks[i].getBlockIndex().y() == grid::nBlocks.y() - 1){
            blocks[i].collisionY_AXIS2();
        }
    }
}

void grid::collisionZ_AXIS2() {
    for (int i = 0; i < totalBlocks; ++i){
        if (blocks[i].getBlockIndex().z() == 0 || blocks[i].getBlockIndex().z() == grid::nBlocks.z() - 1){
            blocks[i].collisionZ_AXIS2();
        }
    }
}

void grid::updateGrid() {
    grid::reposParticles();
    grid::initParticles();
    grid::updateDensities();
    grid::densitiesNormalize();
    grid::acelerationTransfer();
    grid::collisions();
    grid::particlesMovement();
    grid::collisions2();
}




void grid::printBlocks() {
for (int n = 0; n < totalBlocks; ++n) {
  std::cout << "Block " << n << " index: " << blocks[n].getBlockIndex() << '\n';
  blocks[n].printParticles();
  std::cout << '\n' << '\n' << '\n';
  }
}
/*
void grid::printBlocks(int index) {
    for (int n = 0; n < totalBlocks; ++n){
        blocks[n].printParticles(index);
    };
}*/

