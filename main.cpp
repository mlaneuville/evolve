#include "main.hpp"

using namespace std;

int main(int argc, char** argv) {

    string fname = "config.yaml";
    string suffix = "";

    if (argc == 2) {
        fname = string("config_") + argv[1] + ".yaml";
        suffix = argv[1];
    }

    config->Load(fname);

    s->init(suffix);
    s->run();
    
}
