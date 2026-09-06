//
// Created by defalco on 19/11/23.
//

#include <gtest/gtest.h>
#include "sim/progargs.hpp"
#include "sim/simParticle.hpp"
#include "sim/grid.hpp"
#include <filesystem>

using std::filesystem::current_path;
std::string ROUTE_SMALL = current_path().parent_path().parent_path().string() + "/utest/small.fld";


TEST(ProgargsTest, TestReadArgs) {
  // Observamos que lee correctamente los argumentos
  std::vector<std::string> const args = {"1", ROUTE_SMALL, "output.fld"};
  progargs const myProgargs(args);

  // Verificamos que la función read_args haya leído correctamente los valores
  EXPECT_EQ(myProgargs.getNTS(), 1);
  EXPECT_EQ(myProgargs.getInputfilename(), ROUTE_SMALL);
  EXPECT_EQ(myProgargs.getOutputfilename(), "output.fld");
}

TEST(ProgargsTest, TestReadHeader) {
  // Archivo válido con datos correctos
  std::vector<std::string> const args = {"1", ROUTE_SMALL, "output.fld"};
  progargs const myProgargs(args);

  // Verificamos que la función read_header haya asignado correctamente ppm y np
  EXPECT_FLOAT_EQ(myProgargs.getPPM(), 204);
  EXPECT_EQ(myProgargs.getNP(), 4800);
}


TEST(ProgargsTest, TestInitSimParams) {
  // Parámetros de simulación inicializados y calculados correctamente
  std::vector<std::string> const args = {"1", ROUTE_SMALL, "output.fld"};
  progargs const myProgargs(args);

  // Verificamos que los parámetros de simulación se hayan inicializado correctamente
  EXPECT_FLOAT_EQ(myProgargs.getMass(), 0.00011779029181838056);
  EXPECT_FLOAT_EQ(myProgargs.getH(), 0.0083088235294117643);
}