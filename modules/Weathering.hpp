class Weathering: public Module {
public:
    Weathering(string name): Module(name) { init(); }

    double alpha, tau;

    void init(void) {
        this->links.push_back("CCrust2 -> Oceans2");
        this->isBidirectional = false;
        this->numOutputs = 1;
        this->init_fluxes(1);

        alpha = config->data["Weathering"]["alpha"].as<double>();
        tau = config->data["Weathering"]["tau"].as<double>();
    }

    void evolve(void) {
        int co = s->idx_map["CCrust"];
        int oc = s->idx_map["Oceans"];

        double flux = alpha*s->masses[co+2]/tau;

        s->fluxes[co+2] += -flux;
        s->fluxes[oc+2] += flux;

        if(DEBUG) cout << "Weathering: " << flux << endl;

        vector<double> output = {flux};
        this->fluxes.push_back(output);
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
REGISTER_MODULE(Weathering)
