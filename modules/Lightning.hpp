class Lightning: public Module {
public:
    Lightning(string name): Module(name) { init(); }

    double F0, tau;

    void init(void) {
        F0 = config->data["Lightning"]["F0"].as<double>();
        tau = config->data["Lightning"]["tau"].as<double>();
    }

    void evolve(void) {
        int atm = s->idx_map["Atmosphere"];
        int oc = s->idx_map["Oceans"];
        s->fluxes[atm] += -F0*exp(-s->time/tau);
        s->fluxes[oc+1] += F0*exp(-s->time/tau);
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
REGISTER_MODULE(Lightning)
