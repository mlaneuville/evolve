class Reservoir {
public:
    vector<double> masses;
    vector<double> fluxes;

    void init(void);

    string name;

    Reservoir(string name) {
        this->name = name;
        this->init();
    }
};


void Reservoir::init(void) {
    cout << "Loading reservoir '" << name << "' ..." << endl;

    YAML::Node values = config->data["Reservoirs"][this->name]["InitMasses"];
    this->masses.assign(values.size(), 0);
    this->fluxes.assign(values.size(), 0);

    if (values.size() != 3) {
        cout << "Error: you should initialize all 3 fields!" << endl;
        exit(1);
    }

    double v;
    int idx;
    for(YAML::const_iterator it=values.begin();it!=values.end();++it) {
        idx = s->element_map[it->first.as<string>()];
        this->masses[idx] = it->second.as<double>();
        s->m0 += it->second.as<double>();
    }

    return;
}
