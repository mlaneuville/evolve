class Volcanism: public Module {
public:
    Volcanism(string name): Module(name) { init(); }

    double F_arc, F_MORB, F_hotspot, density, scaling, oxidizing;

    void init(void) {
        this->links.push_back("UMantle2 -> Atmosphere0");
        this->links.push_back("UMantle2 -> Oceans2");
        this->links.push_back("LMantle2 -> Oceans2");

        this->numOutputs = 3;
        this->init_fluxes(3);

        // these are given in km3/yr
        F_arc = config->data["Volcanism"]["F_arc"].as<double>();
        F_MORB = config->data["Volcanism"]["F_MORB"].as<double>();
        F_hotspot = config->data["Volcanism"]["F_hotspot"].as<double>();
        // oxidizing = 0.2 corresponds to partitioning in Jim's notes
        oxidizing = config->data["man_ox"].as<double>();
        density = config->data["Volcanism"]["density"].as<double>();
        scaling = config->data["Volcanism"]["scaling"].as<double>();
    }

    void evolve(void) {
        int n2 = s->element_map["n2"];
        int nhx = s->element_map["nhx"];

        int atm = s->reservoir_map["Atmosphere"];
        int oc = s->reservoir_map["Oceans"];
        int um = s->reservoir_map["UMantle"];
        int lm = s->reservoir_map["LMantle"];

        double factor_um = s->world[um]->masses[nhx]/scaling;
        double factor_lm = s->world[lm]->masses[nhx]/scaling;
        double flux_arc = oxidizing*(F_MORB+F_arc)*density*1e9*factor_um;
        double flux_MORB = (1-oxidizing)*(F_MORB+F_arc)*density*1e9*factor_um;
        double flux_hotspot = F_hotspot*density*1e9*factor_lm;

        s->world[um]->fluxes[nhx] -= (flux_arc + flux_MORB);
        s->world[lm]->fluxes[nhx] -= flux_hotspot;
        s->world[atm]->fluxes[n2] += flux_arc;
        // s->fluxes[atm+1] += (flux_MORB + flux_hotspot); this goes directly
        // back to the oceans in practice
        s->world[oc]->fluxes[nhx] += (flux_MORB + flux_hotspot);

        if(DEBUG) {
            cout << "Volcanism::flux_arc::" << flux_arc << endl;
            cout << "Volcanism::flux_MORB::" << flux_MORB << endl;
            cout << "Volcanism::flux_hotspot::" << flux_hotspot << endl;
        }

        vector<double> output = {flux_arc, flux_MORB, flux_hotspot};
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
REGISTER_MODULE(Volcanism)
