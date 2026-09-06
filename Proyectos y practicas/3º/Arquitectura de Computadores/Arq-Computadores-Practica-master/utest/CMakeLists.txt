# Executable for all unit tests with list of sources
# For example, you may have one ∗_test.cpp for each ∗.cpp in sim
add_executable(utest
        block_test.cpp
        grid_test.cpp
        grid_test.cpp
        vector_test.cpp
        fileParticle_test.cpp
        simParticle_test.cpp
        progargs_test.cpp
)
# Library dependencies
target_link_libraries (utest
        PRIVATE
        sim
        GTest::gtest_main
        Microsoft.GSL::GSL)
# Discover all tests and add them to the test driver
include(GoogleTest)
gtest_discover_tests(utest)