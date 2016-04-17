class Impacts: public Module {
public:
    Impacts(string name): Module(name) { init(); }

    double tau, F0;

    void init(void) {
        F0 = config->data["Impacts"]["F0"].as<double>();
        tau = config->data["Impacts"]["tau"].as<double>();
    }

    void evolve(void) {
        // dX/dt = ;
        int atm = s->idx_map["Atmosphere"];
        int oc = s->idx_map["Oceans"];
        int cr = s->idx_map["Ocrust"];
        s->fluxes[atm] += -F0*exp(-s->time/tau);
        s->fluxes[oc+1] += 0.5*F0*exp(-s->time/tau);
        s->fluxes[cr+2] += 0.5*F0*exp(-s->time/tau);
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
