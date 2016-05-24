class FreundlichAdsorption: public Module {
public:
    FreundlichAdsorption(string name): Module(name) { init(); }

    double Kf, VCrust, VOceans, rho_cr;

    void init(void) {
        this->links.push_back("Oceans2 -> OCrust2");
        this->isBidirectional = true;

        Kf = config->data["FreundlichAdsorption"]["Kf"].as<double>();

        // read that from somewhere later
        VCrust = config->data["Subduction"]["VCrust"].as<double>();
        VOceans = config->data["Henry"]["V0"].as<double>();
        rho_cr = 2800.;
    }

    void evolve(void) {
        int oc = s->idx_map["Oceans"];
        int cr = s->idx_map["OCrust"];

        double mtot = s->masses[oc+2] + s->masses[cr+2];
        double cst = VCrust/VOceans*rho_cr*Kf;
        double m_oc_eq = mtot/(1+cst);
        double flux = -(m_oc_eq-s->masses[oc+2])/s->timestep;

        s->fluxes[cr+2] += flux;
        s->fluxes[oc+2] += -flux;

        if(DEBUG) cout << "FreundlichAdsorption: " << flux << endl;
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
REGISTER_MODULE(FreundlichAdsorption)
