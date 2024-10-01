//
// Created by ragarr on 10/7/23.
//

#ifndef FLUID_CONSTANTS_H
#define FLUID_CONSTANTS_H

#include "Vector3D.hpp"
#include <array>
namespace cte{
  // Constantes de simulación
    const double MULT_RADIO= 1.695; // Multiplicador de radio
    const double DENS_FLUIDO = 1000; // Densidad de fluido
    const double PRESION_RIGIDEZ = 3; // Presión de rigidez
    const double COLISIONES_RIGIDEZ = 30000; // Colisiones de rigidez
    const double AMORTIGUAMIENTO = 128; // Amortiguamiento
    const double VISCOSIDAD = 0.4; // Viscosidad
    const double TAMANO_PARTICULA = 0.0002; // Tamaño de partícula
    const double DELTA_T = 0.001; // Paso de tiempo

  // Constantes Vectoriales
    // Gravedad -> los vectores probocan warning al usar una clase personalizada como una statoc variable
    const Vector3D<double> GRAVEDAD = {0.0, -9.8, 0.0}; // NOLINT
    const Vector3D<double> Bmin = {-0.065, -0.08, -0.065}; // NOLINT
    const Vector3D<double> Bmax = {0.065, 0.1, 0.065}; //  NOLINT
}

#endif  // FLUID_CONSTANTS_H
