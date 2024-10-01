//
// Created by defalco on 2/10/23.
//

#ifndef ARQUITECTURA_DE_COMPUTADORES_PROGARGS_HPP
#define ARQUITECTURA_DE_COMPUTADORES_PROGARGS_HPP

#include <string>
#include <vector>
#include <array>
#include <fstream>
#include "Vector3D.hpp"




class progargs {
public:
    progargs(std::vector<std::string>);
    [[nodiscard]] int getNTS() const {
      return nts;
    }

    [[nodiscard]] float getPPM() const {
      return ppm;
    }

    [[nodiscard]] int getNP() const {
      return np;
    }
    [[nodiscard]] double getMass() const {
      return mass;
    }

    [[nodiscard]] double getH() const {
      return h;
    }

    [[nodiscard]] std::string getInputfilename() const {
      return inputfilename;
    }
    [[nodiscard]] std::string getOutputfilename() const {
      return outputfilename;
    }


  private:
    int nts{};
    float ppm{};
    int np{};
    double mass{};
    double h{};
    std::string inputfilename;
    std::string outputfilename;

    void read_header();
    void read_args(std::vector<std::string> args);
    void init_sim_params();

};


#endif //ARQUITECTURA_DE_COMPUTADORES_PROGARGS_HPP
