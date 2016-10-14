class Impacts: public Module {
public:
    Impacts(string name): Module(name) { init(); }

    double oxidizing, tau, F0, F1, M_REF;

    void init(void) {
        this->links.push_back("Atmosphere0 -> Oceans1");
        this->links.push_back("Atmosphere0 -> Oceans2");

        M_REF = config->data["Impacts"]["M_REF"].as<double>();
        F0 = config->data["Impacts"]["F0"].as<double>();
        F1 = config->data["Impacts"]["F1"].as<double>();
        tau = config->data["Impacts"]["tau"].as<double>();
        oxidizing = config->data["atm_ox"].as<double>();
    }

    void evolve(void) {
        int atm = s->idx_map["Atmosphere"];
        int oc = s->idx_map["Oceans"];

        double scaling = s->masses[atm]/M_REF;
        double flux = scaling*(F0 + (F1-F0)*exp(-s->time/tau));

        s->fluxes[atm] += -flux;
        s->fluxes[oc+1] += oxidizing*flux;
        s->fluxes[oc+2] += (1-oxidizing)*flux;

        if(DEBUG) cout << "Impacts: " << flux << endl;
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
REGISTER_MODULE(Impacts)
