//
// Created by ragarr on 10/8/23.
//

#ifndef FLUID_FILEPARTICLE_HPP
#define FLUID_FILEPARTICLE_HPP
#include <vector>
#include <string>



class FileParticle {
  public:
    float px{};
    float py{};
    float pz{};
    float hvx{};
    float hvy{};
    float hvz{};
    float vx{};
    float vy{};
    float vz{};
    // Constructor con parámetros TODO: Borrar si no se utiliza en el futuro
    FileParticle(float _px, float _py, float _pz, float _hvx, float _hvy, float _hvz, float _vx, float _vy, float _vz)
      : px(_px), py(_py), pz(_pz), hvx(_hvx), hvy(_hvy), hvz(_hvz), vx(_vx), vy(_vy), vz(_vz) {
    }
    // Constructor por defecto
    FileParticle()= default;

    friend std::ostream& operator<<(std::ostream& os, FileParticle const & particle);

};

#endif  // FLUID_FILEPARTICLE_HPP
