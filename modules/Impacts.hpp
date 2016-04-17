class Impacts: public Module {
public:
    Impacts(string name): Module(name) { init(); }

    double tau, F0;

    void init(void) {
        F0 = config->data["Impacts"]["F0"].as<double>();
        tau = config->data["Impacts"]["tau"].as<double>();
    }

    void evolve(void) {
        double flux = F0*exp(-s->time/tau);
        int atm = s->idx_map["Atmosphere"];
        int oc = s->idx_map["Oceans"];
        int cr = s->idx_map["Ocrust"];
        s->fluxes[atm] += -flux;
        s->fluxes[oc+1] += 0.5*flux;
        s->fluxes[cr+2] += 0.5*flux;
        if(DEBUG) cout << "Impacts: " << flux << endl;
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
REGISTER_MODULE(Impacts)
