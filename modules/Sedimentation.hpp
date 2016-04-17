class Sedimentation: public Module {
public:
    Sedimentation(string name): Module(name) { init(); }

    double tau, F0;

    void init(void) {
        F0 = config->data["Sedimentation"]["F0"].as<double>();
        tau = config->data["Sedimentation"]["tau"].as<double>();
    }

    void evolve(void) {
        double flux = F0*exp(-s->time/tau);
        int oc = s->idx_map["Oceans"];
        int cr = s->idx_map["OCrust"];
        s->fluxes[oc+1] += -flux;
        s->fluxes[cr+2] += flux;
        if(DEBUG) cout << "Sedimentation: " << flux << endl;
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
REGISTER_MODULE(Sedimentation)
