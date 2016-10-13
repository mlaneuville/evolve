class Convection: public Module {
public:
    Convection(string name): Module(name) { init(); }

    double tau, F0, F1, density;
    double vol_umantle;
    double vol_lmantle;

    void init(void) {
        this->links.push_back("UMantle2 -> LMantle2");
        this->isBidirectional = true;

        F0 = config->data["Convection"]["F0"].as<double>();
        F1 = config->data["Convection"]["F1"].as<double>();
        tau = config->data["Convection"]["tau"].as<double>();
        density = config->data["Volcanism"]["density"].as<double>();

        vol_umantle = 2.4e20; // m3
        vol_lmantle = 6.3e20; // m3
    }

    void evolve(void) {
        int um = s->idx_map["UMantle"];
        int lm = s->idx_map["LMantle"];

        // convection should homogeneize both reservoirs
        double vol_fraction = F0 + (F1-F0)*exp(-s->time/tau);
        double c_umantle = s->masses[um+2]/9.6e17/1e6; // wt.%
        double c_lmantle = s->masses[lm+2]/2.5e18/1e6; // wt.%

        double flux = density*vol_lmantle*vol_fraction*(c_umantle-c_lmantle)*0.5;

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
