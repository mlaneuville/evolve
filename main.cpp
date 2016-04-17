#include "main.hpp"

using namespace std;

int main(int argc, char** argv) {

    string fname = "config.yaml";
    if (argc == 2) fname = argv[1];
    config->Load(fname);

    s->init();
    s->run();
    
}

