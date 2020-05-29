class Subduction: public Module {
public:
    Subduction(string name): Module(name) { init(); }

    double tau, VCrust, accretion;

    void init(void) {
        this->links.push_back("OCrust2 -> UMantle2");
        this->links.push_back("OCrust2 -> CCrust2");
        this->numOutputs = 2;
        this->init_fluxes(2);

        VCrust = config->data["Subduction"]["VCrust"].as<double>();
        tau = config->data["Subduction"]["tau"].as<double>();
        accretion = config->data["Subduction"]["accretion"].as<double>();
    }

    void evolve(void) {
        int cr = s->idx_map["OCrust"];
        int um = s->idx_map["UMantle"];
        int co = s->idx_map["CCrust"];

        //double flux = s->masses[cr+2]*s->timestep/tau;
        double flux = s->masses[cr+2]/tau;
        s->fluxes[cr+2] += -flux;
        s->fluxes[um+2] += (1-accretion)*flux;
        s->fluxes[co+2] += accretion*flux;

        if(DEBUG) cout << "Subduction::flux::" << flux << endl;

        vector<double> output = {(1-accretion)*flux, accretion*flux};
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
REGISTER_MODULE(Subduction)
