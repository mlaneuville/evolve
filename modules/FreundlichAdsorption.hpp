class FreundlichAdsorption: public Module {
public:
    FreundlichAdsorption(string name): Module(name) { init(); }

    double Kf, VSed, VOceans, rhoSed;

    void init(void) {
        this->links.push_back("Oceans2 -> OCrust2");
        this->isBidirectional = true;
        this->numOutputs = 1;
        this->init_fluxes(1);

        Kf = config->data["FreundlichAdsorption"]["Kf"].as<double>();
        VSed = config->data["FreundlichAdsorption"]["VSed"].as<double>();
        rhoSed = config->data["FreundlichAdsorption"]["rhoSed"].as<double>();
        VOceans = config->data["Henry"]["V0"].as<double>();
    }

    void evolve(void) {
        int oc = s->idx_map["Oceans"];
        int cr = s->idx_map["OCrust"];

        double mtot = s->masses[oc+2] + s->masses[cr+2];
        double cst = VSed/VOceans*rhoSed*Kf;
        double m_oc_eq = mtot/(1+cst);
        double flux = -(m_oc_eq-s->masses[oc+2])/s->timestep;

        s->fluxes[cr+2] += flux;
        s->fluxes[oc+2] += -flux;

        if(DEBUG) cout << "FreundlichAdsorption: " << flux << endl;

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
REGISTER_MODULE(FreundlichAdsorption)
