class Subduction: public Module {
public:
    Subduction(string name): Module(name) { init(); }

    double tau, F0;

    void init(void) {
        F0 = config->data["Subduction"]["F0"].as<double>();
        tau = config->data["Subduction"]["tau"].as<double>();
    }

    void evolve(void) {
        int cr = s->idx_map["OCrust"];
        int um = s->idx_map["UMantle"];
        double flux = s->masses[cr+2]*F0*exp(-s->time/tau)/1e18;
        s->fluxes[cr+2] += -flux;
        s->fluxes[um+2] += flux;
        if(DEBUG) cout << "Subduction: " << flux << endl;
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
REGISTER_MODULE(Subduction)
