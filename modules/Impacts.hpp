class Impacts: public Module {
public:
    Impacts(string name): Module(name) { init(); }

    double tau, F0, F1;

    void init(void) {
        this->links.push_back("Atmosphere0 -> Oceans1");

        F0 = config->data["Impacts"]["F0"].as<double>();
        F1 = config->data["Impacts"]["F1"].as<double>();
        tau = config->data["Impacts"]["tau"].as<double>();
    }

    void evolve(void) {
        int atm = s->idx_map["Atmosphere"];
        int oc = s->idx_map["Oceans"];

        double scaling = s->masses[atm]/1e19;
        double flux = scaling*(F0 + (F1-F0)*exp(-s->time/tau));

        s->fluxes[atm] += -flux;
        s->fluxes[oc+1] += flux;
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
