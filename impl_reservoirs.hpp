class Reservoir {
public:
    int num_modules;
    vector<Module*> mchain;
    vector<double> mass;

    void init(void);

    string name;

    Reservoir(string name, int num_modules) {
        this->name = name;
        this->num_modules = num_modules;
        this->init();
    }
    void run_processes(void);
};

void Reservoir::run_processes(void) {
    for (int i=0; i<this->num_modules; i++) {
        if(DEBUG) cout << "Running " << this->mchain[i]->name << " on " << this->name << endl;
        this->mchain[i]->exec("Evolve");
    }
}

void Reservoir::init(void) {
    YAML::Node modules = config->data["Reservoirs"][this->name]["Processes"];
    this->mchain.resize(this->num_modules);

    for (int i=0; i<this->num_modules; i++) {
        string module = modules[i].as<string>();
        this->mchain[i] = factory.forge(module);
    }

    YAML::Node values = config->data["Reservoirs"][this->name]["InitMasses"];
    s->idx_map.insert( pair<string,int>(this->name, s->masses.size()) );

    if (values.size() != 3) {
        cout << "Error: you should initialize all 3 fields!" << endl;
        exit(1);
    }

    for (int i=0; i<3; i++) {
        s->masses.push_back(values[i].as<double>());
    }

    return;
}
