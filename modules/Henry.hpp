class Henry: public Module {
public:
    Henry(string name): Module(name) { init(); }

    double MN2, H0, V0, Mref, Pref;

    void init(void) {
        this->links.push_back("Atmosphere0 -> Oceans0");
        this->isBidirectional = true;
        this->numOutputs = 1;
        this->init_fluxes(1);

        H0 = config->data["Henry"]["H0"].as<double>();
        V0 = config->data["Henry"]["V0"].as<double>();
        MN2 = 28e-3; // the masses are in kg
        Pref = 0.8e5;
        Mref = 4e18;
    }

    void evolve(void) {
        int atm = s->idx_map["Atmosphere"];
        int oc = s->idx_map["Oceans"];

        double mtot = s->masses[atm] + s->masses[oc];
        double cst = Pref/Mref*H0;
        double m_oc_eq = mtot*cst/(1./V0/MN2-cst);
        double flux = (m_oc_eq-s->masses[oc])/s->timestep;

        s->fluxes[atm] += -flux;
        s->fluxes[oc] += flux;

        if(DEBUG) cout << "Henry: " << flux << endl;

        vector<double> output = {flux};
        this->fluxes.push_back(output);
    }

    bool exec(string param) {
        if (param == "Init") {
            init();
            return true;
        }
        if (param == "Evolve") {
            evolve();
            return true;
        }
        return false;
    }
};
REGISTER_MODULE(Henry)
