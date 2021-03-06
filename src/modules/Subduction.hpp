class Subduction: public Module {
public:
    Subduction(string name): Module(name) { init(); }

    double tau, VCrust, accretion;
    int nhx, cr, co, um;

    void init(void) {
        this->links.push_back("OCrust2 -> UMantle2");
        this->links.push_back("OCrust2 -> CCrust2");
        this->numOutputs = 1;
        this->init_fluxes(1);

        VCrust = config->data["Subduction"]["VCrust"].as<double>();
        tau = config->data["Subduction"]["tau"].as<double>();
        accretion = config->data["Subduction"]["accretion"].as<double>();

        nhx = s->element_map["nhx"];

        cr = s->reservoir_map["OCrust"];
        co = s->reservoir_map["CCrust"];
        um = s->reservoir_map["UMantle"];
    }

    void evolve(void) {
        //double flux = s->masses[cr+2]*s->timestep/tau;
        double flux = s->world[cr]->masses[nhx]/tau;
        s->world[cr]->fluxes[nhx] += -flux;
        s->world[um]->fluxes[nhx] += (1-accretion)*flux;
        s->world[co]->fluxes[nhx] += accretion*flux;

        if(DEBUG) cout << "Subduction::flux::" << flux << endl;

        vector<double> output = {(1-accretion)*flux};
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
