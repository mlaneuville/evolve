class Volcanism: public Module {
public:
    Volcanism(string name): Module(name) { init(); }

    double F_arc, F_MORB, F_hotspot, density, scaling;

    void init(void) {
        this->links.push_back("UMantle2 -> Atmosphere0");
        this->links.push_back("UMantle2 -> Oceans1");
        this->links.push_back("LMantle2 -> Oceans1");

        // these are given in km3/yr
        F_arc = config->data["Volcanism"]["F_arc"].as<double>();
        F_MORB = config->data["Volcanism"]["F_MORB"].as<double>();
        F_hotspot = config->data["Volcanism"]["F_hotspot"].as<double>();
        density = config->data["Volcanism"]["density"].as<double>();
        scaling = config->data["Volcanism"]["scaling"].as<double>();
    }

    void evolve(void) {
        int um = s->idx_map["UMantle"];
        int lm = s->idx_map["LMantle"];
        int atm = s->idx_map["Atmosphere"];
        int oc = s->idx_map["Oceans"];

        double factor_um = s->masses[um+2]/scaling;
        double factor_lm = s->masses[lm+2]/scaling;
        double flux_arc = F_arc*density*1e9*factor_um;
        double flux_MORB = F_MORB*density*1e9*factor_um;
        double flux_hotspot = F_hotspot*density*1e9*factor_lm;

        s->fluxes[um+2] -= (flux_arc + flux_MORB);
        s->fluxes[lm+2] -= flux_hotspot;
        s->fluxes[atm] += flux_arc;
        // s->fluxes[atm+1] += (flux_MORB + flux_hotspot); this goes directly
        // back to the oceans in practice
        s->fluxes[oc+1] += (flux_MORB + flux_hotspot);

        if(DEBUG) {
            cout << "Volcanism: arc=" << flux_arc << endl;
            cout << "Volcanism: morb=" << flux_MORB << endl;
            cout << "Volcanism: hotspot=" << flux_hotspot << endl;
        }
        this->fluxes.push_back(flux_arc+flux_MORB+flux_hotspot);
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
