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
        int nhx = s->element_map["nhx"];

        int cr = s->reservoir_map["OCrust"];
        int co = s->reservoir_map["CCrust"];
        int um = s->reservoir_map["UMantle"];

        //double flux = s->masses[cr+2]*s->timestep/tau;
        double flux = s->world[cr]->masses[nhx]/tau;
        s->world[cr]->fluxes[nhx] += -flux;
        s->world[um]->fluxes[nhx] += (1-accretion)*flux;
        s->world[co]->fluxes[nhx] += accretion*flux;

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
