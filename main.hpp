// standard modules
#include <iostream>
#include <fstream>
#include <valarray>
#include <cstdio>
#include <cassert>

// personal modules
#include "config.hpp"

using namespace std;

// forward declaration
class Module;
class Reservoir;

class Simulation {
public:

    string output_file;
    int current_iter;
    double timestep, time;
    double output, tmax;
    int num_reservoirs;

    map<string,int> idx_map;

    vector<Reservoir*> world;
//    vector<Module*> mchain;

    vector<double> fluxes;
    vector<double> masses;

    Simulation() {};
    void init(string);
    void run(void);
    void to_screen(void);
    void to_file(void);
    void file_header(void);
};

Simulation *s = new Simulation();
Config *config = new Config();
bool DEBUG = true;

#include "impl_modules.hpp"
#include "impl_reservoirs.hpp"
#include "impl_simulation.hpp"
#include "modules/modules.hpp"
