class Subduction: public Module {
public:
    Subduction(string name): Module(name) { init(); }

    double tau, VCrust;

    void init(void) {
        this->links.push_back("OCrust2 -> UMantle2");
        this->numOutputs = 1;
        this->init_fluxes(1);

        VCrust = config->data["Subduction"]["VCrust"].as<double>();
        tau = config->data["Subduction"]["tau"].as<double>();
    }

    void evolve(void) {
        int cr = s->idx_map["OCrust"];
        int um = s->idx_map["UMantle"];

        //double flux = s->masses[cr+2]*s->timestep/tau;
        double flux = s->masses[cr+2]/tau;
        s->fluxes[cr+2] += -flux;
        s->fluxes[um+2] += flux;

        if(DEBUG) cout << "Subduction: " << flux << endl;

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
REGISTER_MODULE(Subduction)
