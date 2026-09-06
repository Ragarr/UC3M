//
// Created by defalco on 2/10/23.
//
//
// Created by defalco on 25/09/23.
//

#include <iostream>
#include <fstream>
#include <vector>
#include <span>

// include local
#include "sim/constants.h"
#include "sim/fileParticle.hpp"
#include "sim/progargs.hpp"
#include "sim/simParticle.hpp"
#include "sim/grid.hpp"

void storeResults(std::vector<simParticle> particles, const progargs& args){
    std::ofstream outputfile;
    outputfile.open(args.getOutputfilename(), std::ios::binary);
    if (!outputfile.is_open()) {
          std::cerr << "Error: Cannot open " << args.getOutputfilename() << " for writing.\n";
          exit(-4);
    }
    // write header
    float ppm = args.getPPM();
    int numParticles = args.getNP();

    // set file pointer at the beginning of the file
    outputfile.seekp(0, std::ios::beg);

    outputfile.write(reinterpret_cast<char*>(&ppm), sizeof(float)); // NOLINT (cppcoreguidelines-pro-type-reinterpret-cast)
    outputfile.write(reinterpret_cast<char*>(&numParticles), sizeof(int)); // NOLINT (cppcoreguidelines-pro-type-reinterpret-cast)

    // write particles
      for (int i = 0; i < args.getNP(); i++) {
        FileParticle file_particle = particles[i].toFileParticle();
        outputfile.write(reinterpret_cast<char*>(&file_particle), sizeof(FileParticle)); // NOLINT (cppcoreguidelines-pro-type-reinterpret-cast)
      }
    outputfile.close();

}

void printParams(progargs* args, grid* sim_grid){
  std::cout <<
      "Number of particles: " << args->getNP() << "\n" <<
      "Particles per meter: " << args->getPPM() << "\n"<<
      "Smoothing length: " << args->getH()<< "\n"<<
      "Particle mass: " << args->getMass() << "\n"<<
      "Grid size: " << sim_grid->getNBlocks().x() << " x " << sim_grid->getNBlocks().y() << " x "  <<
      sim_grid->getNBlocks().z() << "\n" <<
      "Number of blocks: " << sim_grid->getTotalBlocks() << "\n"<<
      "Block size: " << sim_grid->getBlockSize().x() << " x "<<  sim_grid->getBlockSize().y() << " x " <<
      sim_grid->getBlockSize().z() << "\n";
}

int main(int argc, char* argv[]){
    std::span const args_view{argv, static_cast<size_t>(argc)};
    const std::vector<std::string> v_args{args_view.begin() + 1, args_view.end()};
    progargs args(v_args);
    std::vector<simParticle> particles = readParticlesFromFile(args.getInputfilename(), args.getNP());
    grid sim_grid = grid(args.getH(), args.getMass(), particles);
    printParams(&args, &sim_grid);

    for (int i =0; i<args.getNTS(); i++){
        std::cout << "Time step: " << i << "/" << args.getNTS() <<"\r" << std::flush;
        sim_grid.updateGrid();
    }
    storeResults(particles, args);
}