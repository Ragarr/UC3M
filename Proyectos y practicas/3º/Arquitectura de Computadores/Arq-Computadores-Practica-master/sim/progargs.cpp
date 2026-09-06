//
// Created by defalco on 2/10/23.
//

#include <string>
#include "progargs.hpp"
#include <iostream>
#include <utility>
#include "constants.h"
#include "grid.hpp"
#include "errors.h"

// comprobar y asignar los valores de los argumentos de programa
progargs::progargs(std::vector<std::string> args){
    read_args(std::move(args));
    read_header();
    init_sim_params();
}

void progargs::read_args(std::vector<std::string> args){
        if (args.size()!=3){
            std::cerr << "Error: Invalid number of arguments: " << args.size() << "\n";
            exit(errors::ARGS_ERROR);
        }
        try {nts = std::stoi(args[0]);}
        catch (const std::invalid_argument& e) {std::cerr << "Error: Time steps must be an integer.\n";exit(errors::ARGS_ERROR);}
        if (nts < 0) {std::cerr << "Error: Time steps must be positive.\n";exit(errors::TIME_STEPS_ERROR);}
        inputfilename = args[1];
        std::ifstream inputfile;
        inputfile.open(args[1], std::ios::binary);
        if (!inputfile.is_open()) {
            std::cerr << "Error: Cannot open " << args[1] << " for reading.\n";
            exit(errors::READ_ERROR);
        }
        outputfilename = args[2];
        std::ofstream outputfile;
        outputfile.open(args[2], std::ios::binary);
        if (!outputfile.is_open()) {
            std::cerr << "Error: Cannot open " << args[2] << " for writing.\n";
            exit(errors::WRITE_ERROR);
        }
}

void progargs::read_header() {
        // Leemos los bytes de un entero y un flotante
        // sacar los size(int)+size(float) primeros bytes del archivo
        // leer el entero y el flotante
        // asignarlos a las variables nts y ppm
        // ignorar warning de reinterpret_cast, es valido en este caso, para read.
        std::ifstream inputfile;
        inputfile.open(inputfilename, std::ios::binary);

        inputfile.read(reinterpret_cast<char *>(&ppm), sizeof(float)); // NOLINT(cppcoreguidelines-pro-type-reinterpret-cast)
        // read the next 4 bytes of the file as int
        inputfile.read(reinterpret_cast<char *>(&np), sizeof(int)); // NOLINT(cppcoreguidelines-pro-type-reinterpret-cast)
        // print the values
        if (np<=0){
            std::cerr << "Error: Invalid number of particles: " << np << '\n';
          exit(errors::NP_ERROR);
        }
}

void progargs::init_sim_params() {
        // calc mass m=p/ppm³
        mass = cte::DENS_FLUIDO/((double)ppm*(double)ppm*(double)ppm);
        // calc h
        h = cte::MULT_RADIO/(double)ppm;
}