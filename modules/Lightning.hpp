class Lightning: public Module {
public:
    Lightning(string name): Module(name) { init(); }

    double F0, tau;

    void init(void) {
        F0 = config->data["Lightning"]["F0"].as<double>();
        tau = config->data["Lightning"]["tau"].as<double>();
    }

    void evolve(void) {
        double flux = F0*exp(-s->time/tau);
        int atm = s->idx_map["Atmosphere"];
        int oc = s->idx_map["Oceans"];
        s->fluxes[atm] += -flux;
        s->fluxes[oc+1] += flux;
        if(DEBUG) cout << "Lightning: " << flux << endl;
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
