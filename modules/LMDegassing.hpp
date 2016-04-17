class LMDegassing: public Module {
public:
    LMDegassing(string name): Module(name) { init(); }

    double tau, F0, eps;

    void init(void) {
        F0 = config->data["LMDegassing"]["F0"].as<double>();
        tau = config->data["LMDegassing"]["tau"].as<double>();
        eps = config->data["LMDegassing"]["subaqueous"].as<double>();
    }

    void evolve(void) {
        int lm = s->idx_map["LMantle"];
        int atm = s->idx_map["Atmosphere"];
        int oc = s->idx_map["Oceans"];
        double flux = s->masses[lm+2]*F0*exp(-s->time/tau)/1e18;
        s->fluxes[lm+2] += -flux;
        s->fluxes[atm] += (1-eps)*flux;
        s->fluxes[oc+1] += eps*flux;
        if(DEBUG) cout << "LMDegassing: " << flux << endl;
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
REGISTER_MODULE(LMDegassing)
