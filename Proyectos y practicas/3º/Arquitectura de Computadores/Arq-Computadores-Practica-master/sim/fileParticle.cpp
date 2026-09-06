//
// Created by ragarr on 10/8/23.
//

#include "fileParticle.hpp"

#include <iostream>


std::ostream& operator<<(std::ostream& os, FileParticle const & particle) {
  std::cout << "{";
  std::cout << "\"px\": " << particle.px << ", ";
  std::cout << "\"py\": " << particle.py << ", ";
  std::cout << "\"pz\": " << particle.pz << ", ";
  std::cout << "\"hvx\": " << particle.hvx << ", ";
  std::cout << "\"hvy\": " << particle.hvy << ", ";
  std::cout << "\"hvz\": " << particle.hvz << ", ";
  std::cout << "\"vx\": " << particle.vx << ", ";
  std::cout << "\"vy\": " << particle.vy << ", ";
  std::cout << "\"vz\": " << particle.vz;
  std::cout << "}\n";
  return os;
}


