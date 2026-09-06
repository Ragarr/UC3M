//
// Created by nekos on 06/11/2023.
//

#include "block.hpp"
#include "Vector3D.hpp"

#include <iostream>
#include <cmath>
#include <algorithm>
#include <array>
#include <iomanip>

using namespace std;

Vector3D<double> block::getSizeBlock(){
   return block::sizeBlock;
}

Vector3D<int> block::getBlockIndex() const{
   return {block::i, block::j, block::k};
}

int block::getI() const{
   return block::i;
}

int block::getJ() const{
   return block::j;
}

int block::getK() const{
   return block::k;
}

std::vector<simParticle*> block::getParticles(){
  return  particles;
}

block::block(Vector3D<double> sizeBlock, Vector3D<int> blockIndex) : sizeBlock(sizeBlock), i(blockIndex.x()), j(blockIndex.y()), k(blockIndex.z()) {}

void block::storeParticle(simParticle* particle){
  nParticles += 1;
  particles.push_back(particle);
}

simParticle* block::popParticle(simParticle* particle) {
  for (u_long index = 0; index < particles.size(); ++index) {
    if (particle == particles[index]){
        particles.erase(particles.begin()+ (int)index);
        nParticles -= 1;
        return particle;
    }
  }
  // Si no se encuentra la partícula, lanza una excepción.
  throw runtime_error("La partícula no se encuentra en el bloque.");
}




int block::getNParticles() {
    return nParticles;
}

void block::setNParticlesToZero() {
    nParticles = 0;
}

void block::addOneToNParticles() {
    nParticles = nParticles + 1;
}


void block::initParticles(Vector3D<double> externalForce) {
    for (auto & particle : particles) {
    particle->aceleration = externalForce;
    particle->density = 0;
    }
}

void block::updateDensities(double h, block* block2){
  double deltaDensity = NAN;
  double squaredDistance = NAN;
  double hSquared = NAN;
  vector <simParticle*> const Particles1(particles);
  vector <simParticle*> const Particles2(block2->particles);
  Vector3D<double> deltaPosition = {};

  for (const auto & particle : Particles1) {
      for (const auto & particle2 : Particles2) {
        deltaPosition = particle->position - particle2->position;

        squaredDistance = deltaPosition.x()*deltaPosition.x()+deltaPosition.y()*deltaPosition.y()+
                          deltaPosition.z()*deltaPosition.z();
        hSquared        = h*h;

        if ((particle->id > particle2->id) && (squaredDistance < hSquared))   {
          deltaDensity = (hSquared - squaredDistance);
          deltaDensity = deltaDensity * deltaDensity * deltaDensity;
          particle->density = particle->density + deltaDensity;
          particle2->density = particle2->density + deltaDensity;
        }
      }
  }
}

void block::densitiesNormalize(double h, double mass) {
  for (auto & particle : particles){
      const int normFact1 = 315;
      const int normFact2 = 64;
      particle->density =
          (particle->density + (h*h*h*h*h*h)) * (normFact1 / (normFact2 * M_PI * (h*h*h*h*h*h*h*h*h))) * mass;
  }
}


void block::acelerationTransfer(double h, double mass, block* block2){
      Vector3D<double> deltaAceleration = {};
      double squaredDistance = NAN;
      double const hSquared = h*h;
      double dist_ij = NAN;
      vector <simParticle*> const Particles1(particles);
      vector <simParticle*> const Particles2(block2->particles);
      const array<double, 3> magicNums = {10e-13, 15, 45};

      for (const auto & particle : Particles1) {
        for (const auto & particle2 : Particles2) {
          squaredDistance = pow((particle->position - particle2->position).norm(), 2);
          if ((particle->id > particle2->id) && (squaredDistance < hSquared)){
            dist_ij = sqrt(max(squaredDistance, magicNums[0]));
            deltaAceleration = ((particle->position - particle2->position)*(magicNums[1]/(M_PI*(h*h*h*h*h*h)))*((3*mass*cte::PRESION_RIGIDEZ)/2))
                * (((h-dist_ij)*(h-dist_ij))/dist_ij) * (((particle->density + particle2->density - (2*cte::DENS_FLUIDO))));
            deltaAceleration = deltaAceleration + (particle2->velocity - particle->velocity)* (magicNums[2]/(M_PI*(h*h*h*h*h*h)))*cte::VISCOSIDAD*mass;
            deltaAceleration = deltaAceleration/(particle->density*particle2->density);
            particle->aceleration  = particle->aceleration + deltaAceleration;
            particle2->aceleration = particle2->aceleration - deltaAceleration;
          }
        }
      }
}


void block::collisionX_AXIS(){
  double deltaX = NAN;
  double amortiguamientoX = NAN;
  const double epsilon = 10e-11;
  for(auto & particle : particles){
    particle->position.set_x(particle->position.x() + (particle->initialVelocity.x()* cte::DELTA_T));
    if(block::getI() == 0){
        deltaX = cte::TAMANO_PARTICULA - (particle->position.x() - cte::Bmin.x());
        amortiguamientoX = particle->aceleration.x() + ((cte::COLISIONES_RIGIDEZ*deltaX)-(cte::AMORTIGUAMIENTO*
                           particle->velocity.x()));
    }
    else{
        deltaX = cte::TAMANO_PARTICULA - (cte::Bmax.x() - particle->position.x());
        amortiguamientoX = particle->aceleration.x() - ((cte::COLISIONES_RIGIDEZ*deltaX)+(cte::AMORTIGUAMIENTO*
                           particle->velocity.x()));
    }
    if (deltaX>epsilon){
        particle->aceleration.set_x(amortiguamientoX);
    }

  }
}

void block::collisionY_AXIS(){
  double deltaY = NAN;
  double AmortiguamientoY = NAN;
  const double epsilon = 10e-11;

  for(auto & particle : particles){
    particle->position.set_y(particle->position.y() + (particle->initialVelocity.y()*
                                                           cte::DELTA_T));

    if(block::getJ() == 0){
        deltaY = cte::TAMANO_PARTICULA - (particle->position.y() - cte::Bmin.y());
        AmortiguamientoY = particle->aceleration.y() + ((cte::COLISIONES_RIGIDEZ*deltaY)-(cte::AMORTIGUAMIENTO*particle->velocity.y()));
    }
    else{
        deltaY = cte::TAMANO_PARTICULA - (cte::Bmax.y() - particle->position.y());
        AmortiguamientoY = particle->aceleration.y() - ((cte::COLISIONES_RIGIDEZ*deltaY)+(cte::AMORTIGUAMIENTO*
                                          particle->velocity.y()));
    }
    if (deltaY>epsilon){
        particle->aceleration.set_y(AmortiguamientoY);
    }
  }
}


void block::collisionZ_AXIS(){
  double deltaZ = NAN;
  double amortiguamientoZ = NAN;
  const double epsilon = 10e-11;


  for(auto & particle : particles){
    particle->position.set_z(particle->position.z() + (particle->initialVelocity.z()*cte::DELTA_T));

    if(block::getK() == 0){
        deltaZ = cte::TAMANO_PARTICULA - (particle->position.z() - cte::Bmin.z());
        amortiguamientoZ = particle->aceleration.z() + ((cte::COLISIONES_RIGIDEZ*deltaZ)-(cte::AMORTIGUAMIENTO*particle->velocity.z()));
    }
    else{
        deltaZ = cte::TAMANO_PARTICULA - (cte::Bmax.z() - particle->position.z());
        amortiguamientoZ = particle->aceleration.z() - ((cte::COLISIONES_RIGIDEZ*deltaZ)+(cte::AMORTIGUAMIENTO*
                                         particle->velocity.z()));
    }
    if (deltaZ>epsilon){
        particle->aceleration.set_z(amortiguamientoZ);
    }
  }
}

void block::particlesMovement() {
    for (auto & particle : particles) {
        particle->position = particle->position + (particle->initialVelocity * cte::DELTA_T) +
                             (particle->aceleration * (cte::DELTA_T * cte::DELTA_T));
        particle->velocity = particle->initialVelocity + (particle->aceleration * cte::DELTA_T)/2;
        particle->initialVelocity = particle->initialVelocity + particle->aceleration * cte::DELTA_T;
  }
}

void block::collisionX_AXIS2() {
    double distX = NAN;
    for (auto & particle : particles) {
        if (block::getI() == 0) {
        distX = particle->position.x() - cte::Bmin.x();
            if (distX <0){
                particle->position.set_x(cte::Bmin.x()- distX);
                particle->velocity.set_x(-particle->velocity.x());
                particle->initialVelocity.set_x(-particle->initialVelocity.x());
            }
        } else {
            distX = (cte::Bmax.x() - particle->position.x());
            if (distX <0){
                    particle->position.set_x(cte::Bmax.x()+ distX);
                    particle->velocity.set_x(-particle->velocity.x());
                    particle->initialVelocity.set_x(-particle->initialVelocity.x());
            }
        }
    }
}

void block::collisionY_AXIS2() {
    double distY = NAN;
    for (auto & particle : particles) {
        if (block::getJ() == 0) {
            distY = particle->position.y() - cte::Bmin.y();
            if (distY <0){
                particle->position.set_y(cte::Bmin.y()- distY);
                particle->velocity.set_y(-particle->velocity.y());
                particle->initialVelocity.set_y(-particle->initialVelocity.y());
            }
        } else {
            distY = (cte::Bmax.y() - particle->position.y());
            if (distY <0){
                particle->position.set_y(cte::Bmax.y()+ distY);
                particle->velocity.set_y(-particle->velocity.y());
                particle->initialVelocity.set_y(-particle->initialVelocity.y());
            }
        }
    }
}

void block::collisionZ_AXIS2() {
    double distZ = NAN;
    for (auto & particle : particles) {
            if (block::getK() == 0) {
            distZ = particle->position.z() - cte::Bmin.z();
            if (distZ <0){
                    particle->position.set_z(cte::Bmin.z()- distZ);
                    particle->velocity.set_z(-particle->velocity.z());
                    particle->initialVelocity.set_z(-particle->initialVelocity.z());
            }
            } else {
            distZ = (cte::Bmax.z() - particle->position.z());
            if (distZ <0){
                    particle->position.set_z(cte::Bmax.z()+ distZ);
                    particle->velocity.set_z(-particle->velocity.z());
                    particle->initialVelocity.set_z(-particle->initialVelocity.z());
            }
            }
    }
}


/*
void block::printParticles(int index) {
    for (auto & particle : particles) {
        if (particle->id == index) {
            cout << "Block " <<block::getBlockIndex() << '\n';
            cout << particle<< ": \n"<<*particle;
        }
    }
}*/
void block::printParticles(){
    for (auto & particle : particles) {
        cout << "Block " <<block::getBlockIndex() << '\n';
        cout << particle<< ": \n"<<*particle;
    }
}