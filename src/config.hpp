// external modules
#include "yaml-cpp/yaml.h"

using namespace std;

class Config {
public:
    string filename;
    YAML::Node data; 

    Config() { this->filename = "config.yaml"; }

    void Load(string fname);
};
