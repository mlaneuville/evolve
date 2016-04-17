class UMDegassing: public Module {
public:
    UMDegassing(string name): Module(name) { init(); }

    double tau, F0, eps1, eps2;

    void init(void) {
        F0 = config->data["UMDegassing"]["F0"].as<double>();
        tau = config->data["UMDegassing"]["tau"].as<double>();
        eps1 = config->data["UMDegassing"]["speciation"].as<double>();
        eps2 = config->data["UMDegassing"]["subaqueous"].as<double>();
    }

    void evolve(void) {
        int um = s->idx_map["UMantle"];
        int atm = s->idx_map["Atmosphere"];
        int oc = s->idx_map["Oceans"];
        int lm = s->idx_map["LMantle"];
        double flux = s->masses[um+2]*F0*exp(-s->time/tau)/1e18;
        s->fluxes[um+2] += -flux;
        s->fluxes[atm] += eps1*(1-eps2)*flux;
        s->fluxes[oc+1] += eps1*eps2*flux;
        s->fluxes[lm+2] += (1-eps1)*flux;
        if(DEBUG) cout << "UMDegassing: " << flux << endl;
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
REGISTER_MODULE(UMDegassing)
