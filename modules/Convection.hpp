class Convection: public Module {
public:
    Convection(string name): Module(name) { init(); }

    double tau, F0, F1;

    void init(void) {
        this->links.push_back("UMantle2 -> LMantle2");

        F0 = config->data["Convection"]["F0"].as<double>();
        F1 = config->data["Convection"]["F1"].as<double>();
        tau = config->data["Convection"]["tau"].as<double>();
    }

    void evolve(void) {
        int um = s->idx_map["UMantle"];
        int lm = s->idx_map["LMantle"];

        double vol_fraction = F0 + (F1-F0)*exp(-s->time/tau);
        double flux = s->masses[um+2]*vol_fraction;

        s->fluxes[um+2] += -flux;
        s->fluxes[lm+2] += flux;

        if(DEBUG) cout << "Convection: " << flux << endl;
        this->fluxes.push_back(flux);
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
REGISTER_MODULE(Convection)
