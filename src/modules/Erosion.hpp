class Erosion: public Module {
public:
    Erosion(string name): Module(name) { init(); }

    double alpha, A0, M0, rho;
    bool uniform_growth;

    void init(void) {
        this->links.push_back("CCrust2 -> Oceans2");
        this->isBidirectional = false;
        this->numOutputs = 2;
        this->init_fluxes(2);

        alpha = config->data["Erosion"]["alpha"].as<double>();
        uniform_growth = config->data["Erosion"]["uniform_growth"].as<bool>();
        A0 = 1.48e14; // m2, today
        M0 = 2.28e22; // kg, today
        rho = 2700; // kg/m3
    }

    void evolve(void) {
        int co = s->idx_map["CCrust"];
        int oc = s->idx_map["Oceans"];
        
        double relative_area;
        if (s->time < 1.5e9) { 
            relative_area = 0.02 + 0.64*s->time/1.5e9;
        } else {
            relative_area = 0.66 + 0.34*(s->time-1.5e9)/3e9;
        }
        if (uniform_growth) { relative_area = 0.02 + 0.98*s->time/4.5e9; }

        double concentration = s->masses[co+2]/(relative_area*M0);
        double flux = alpha*A0*rho*relative_area*concentration;

        s->fluxes[co+2] += -flux;
        s->fluxes[oc+2] += flux;

        if(DEBUG) cout << "Erosion: " << flux << endl;

        vector<double> output = {flux, relative_area};
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
REGISTER_MODULE(Erosion)
