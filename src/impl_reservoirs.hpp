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

    double v;
    for(YAML::const_iterator it=values.begin();it!=values.end();++it) {
        v = it->second.as<double>();
        s->masses.push_back(v);
        s->m0 += v;
    }

    return;
}
