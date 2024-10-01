//
// Created by ragarr on 11/18/23.
//

#include <iostream>
#include <gtest/gtest.h>
#include <vector>

#include "sim/Vector3D.hpp"

using namespace std;

//NOLINTBEGIN
vector<Vector3D<int>> bloquesAdyacentes(const Vector3D<int> v) {
    vector<Vector3D<int>> adyacentes;

    for (int dx = -1; dx <= 1; ++dx) {
        for (int dy = -1; dy <= 1; ++dy) {
            for (int dz = -1; dz <= 1; ++dz) {
                // Excluir el bloque actual
                if (dx != 0 || dy != 0 || dz != 0) {
                    adyacentes.emplace_back(v.x() + dx, v.y() + dy, v.z() + dz);
                }
            }
        }
    }
    return adyacentes;
}

TEST(vector3DTest, TestSetters){
    Vector3D<double> vect = {0, 2, 3};
    vect.set_x(24);
    vect.set_y(1);
    vect.set_z(100);

    Vector3D<double> vect_expected = {24, 1, 100};

    EXPECT_EQ(vect, vect_expected);
}

TEST(vector3DTest, TestGetters){
    Vector3D<float> vect = {34, 20, 50};
    float x = vect.x();
    float y = vect.y();
    float z = vect.z();

    EXPECT_EQ(x, 34);
    EXPECT_EQ(y, 20);
    EXPECT_EQ(z, 50);
}

TEST(vector3DTest, SumaDeVectores){
    Vector3D<int> vector1(1,2,3);
    Vector3D<int> vector2(4,5,6);
    Vector3D<int> resultado = vector1 + vector2;
    Vector3D<int> resultadoEsperado(5,7,9);

    EXPECT_EQ(resultado, resultadoEsperado);

}

TEST(vector3DTest, RestaDeVectores){
    Vector3D<int> vector1(1,2,3);
    Vector3D<int> vector2(4,5,6);
    Vector3D<int> resultado = vector1 - vector2;
    Vector3D<int> resultadoEsperado(-3,-3,-3);

    EXPECT_EQ(resultado, resultadoEsperado);
}


TEST(vector3DTest, ProductoPorVector){
    Vector3D<int> vector1(1,2,3);
    Vector3D<int> vector2(4,5,6);
    Vector3D<int> resultado = vector1 * vector2;
    Vector3D<int> resultadoEsperado(4,10,18);

    EXPECT_EQ(resultado, resultadoEsperado);
}

TEST(vector3DTest, ProductoPorEscalar){
    Vector3D<double> vector(1,2,3);
    double escalar = 2;
    Vector3D<double> resultado = vector * escalar;
    Vector3D<double> resultadoEsperado(2,4,6);

    EXPECT_EQ(resultado, resultadoEsperado);
}

TEST(vector3DTest, DivisionDeVectores){
    Vector3D<double> vector1(1,2,3);
    Vector3D<double> vector2(4,5,6);
    Vector3D<double> resultado = vector1 / vector2;
    Vector3D<double> resultadoEsperado(0.25,0.4,0.5);

    EXPECT_EQ(resultado, resultadoEsperado);
}

TEST(vector3DTest, DivisionVectorConstante){
    Vector3D<double> vector1(1,2,3);
    int value = 2;
    Vector3D<double> resultado = vector1 / value;
    Vector3D<double> resultadoEsperado(0.5,1,1.5);

    EXPECT_EQ(resultado, resultadoEsperado);
}

TEST(vector3DTest, IgualdadVectores){
    Vector3D<float> vect1(1, 2, 3);
    Vector3D<float> vect2(1, 2, 3);
    Vector3D<float> vect3(1, 4, 3);

    bool is_equal_1 = (vect1 == vect2);
    bool is_equal_2 = (vect1 == vect3);

    EXPECT_EQ(is_equal_1, true);
    EXPECT_EQ(is_equal_2, false);
}

TEST(vector3DTest, To_int){
    Vector3D<float> vect1(1, 2, 3);
    Vector3D<int> vect2(1,2,3);
    Vector3D<int> vect3 = vect1.to_int();

    EXPECT_EQ(vect2, vect3);
    EXPECT_TRUE(typeid(vect3)==typeid(Vector3D<int>));
}

TEST(vector3DTest, To_double){
    Vector3D<int> vect_int(1, 2, 3);
    Vector3D<double> vect_double = vect_int.to_double();
    Vector3D<double> vect_double_2 = {1, 2, 3};

    EXPECT_EQ(vect_double, vect_double_2);
    EXPECT_TRUE(typeid(vect_double)==typeid(Vector3D<double>));
}

// test is adjacent
TEST(vector3DTest, TestIsAdjacent0){
    Vector3D<int> origin = {0,0,0};
    vector<Vector3D<int>> noAdyacentes {{0,2,3},{2,4,5}, {1,2,3}, {12,3,4}};
    vector<Vector3D<int>> adyacentes = bloquesAdyacentes(origin);

    for (auto &adyacente : adyacentes) {
            EXPECT_TRUE(adyacente.isAdjacent(origin));
    }
    for (auto &noAdyacente : noAdyacentes) {
            EXPECT_FALSE(noAdyacente.isAdjacent(origin));
    }
}

TEST(vector3DTest, TestIsAdjacent1){
    Vector3D<int> origin = {1,5,1};
    vector<Vector3D<int>> noAdyacentes {{0,2,3},{2,4,5}, {1,2,3}, {12,3,4}};

    vector<Vector3D<int>> adyacentes = bloquesAdyacentes(origin);
    for (auto &adyacente : adyacentes) {
            EXPECT_TRUE(adyacente.isAdjacent(origin));
    }
    for (auto &noAdyacente : noAdyacentes) {
            EXPECT_FALSE(noAdyacente.isAdjacent(origin));
    }
}

TEST(vector3DTest, TestIsAdjacent2){
    Vector3D<int> origin = {2,0,0};
    Vector3D<int> adyacente = {3,1,0};
    EXPECT_TRUE(origin.isAdjacent(adyacente));
}


TEST(vector3D, TestPrintVector3D){
    Vector3D<int> origin = {2,0,0};
    std::ostringstream buffer;
    std::streambuf* oldCoutStreamBuf = std::cout.rdbuf(buffer.rdbuf());
    std::cout << origin << std::endl;
    std::cout.rdbuf(oldCoutStreamBuf);
    std::string output = buffer.str();
    EXPECT_EQ(output, "(2, 0, 0)\n");

}

TEST(vector3DTest, NormaVector){
    Vector3D<double> vect = {2, 2, 4};
    double norma = vect.norm();
    double norma_expected = std::sqrt(2*2 + 2*2 +4*4);

    EXPECT_EQ(norma, norma_expected);
}


//NOLINTEND