#include "main.hpp"

using namespace std;

int main(int argc, char** argv) {

    string fname = "config.yaml";
    string suffix = "";

    if (argc == 2) {
        fname = argv[1];

        int begin = string(argv[1]).find("config_") + 7;
        int end = string(argv[1]).find(".yaml", 4);
        suffix = string(argv[1]).substr(begin, end-begin);
    }

    config->Load(fname);

    s->init(suffix);
    s->run();
    
}
