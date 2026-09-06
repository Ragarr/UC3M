//
// Created by defalco on 19/11/23.
//

#include <gtest/gtest.h>
#include "sim/fileParticle.hpp"

int main(int argc, char* argv[]){
  // cout<<"v0.12\n";
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}

TEST(fileParticle, fileParticleConstructor){
    FileParticle const particle1(1, 2, 3, 4, 5, 6, 7, 8, 9);
    EXPECT_EQ(particle1.px, 1);
    EXPECT_EQ(particle1.py, 2);
    EXPECT_EQ(particle1.pz, 3);
    EXPECT_EQ(particle1.hvx, 4);
    EXPECT_EQ(particle1.hvy, 5);
    EXPECT_EQ(particle1.hvz, 6);
    EXPECT_EQ(particle1.vx, 7);
    EXPECT_EQ(particle1.vy, 8);
    EXPECT_EQ(particle1.vz, 9);
}
