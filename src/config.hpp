// external modules
#include "yaml-cpp/yaml.h"

using namespace std;

class Config {
public:
    string filename;
    YAML::Node data; 

    Config() { this->filename = "config.yaml"; }

    bool Load(string fname);
};
