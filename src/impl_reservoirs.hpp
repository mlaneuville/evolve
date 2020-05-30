class Reservoir {
public:
    vector<double> mass;

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
    s->idx_map.insert( pair<string,int>(this->name, s->masses.size()) );

    if (values.size() != 3) {
        cout << "Error: you should initialize all 3 fields!" << endl;
        exit(1);
    }

    for (int i=0; i<3; i++) {
        s->masses.push_back(values[i].as<double>());
        s->m0 += values[i].as<double>();
    }

    return;
}
