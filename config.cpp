#include <iostream>
#include "config.hpp"

void Config::Load(string fname) {
    this->filename = fname;
    this->data = YAML::LoadFile(fname);
    cout << "Loading config file " << this->filename << endl;
}
