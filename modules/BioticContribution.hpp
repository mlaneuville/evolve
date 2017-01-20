class BioticContribution: public Module {
public:
    BioticContribution(string name): Module(name) { init(); }

    double denitrification, sedimentation;
    double flux_up, flux_down;

    void init(void) {
        this->links.push_back("Oceans1 -> Atmosphere0");
        this->links.push_back("Oceans2 -> Atmpsphere0");
        this->links.push_back("Oceans1 -> OCrust2");
        this->links.push_back("Oceans2 -> OCrust2");
        this->numOutputs = 2;
        this->init_fluxes(2);

        denitrification = config->data["BioticContribution"]["denitrification"].as<double>();
        sedimentation = config->data["BioticContribution"]["sedimentation"].as<double>();
    }

    void evolve(void) {
        int atm = s->idx_map["Atmosphere"];
        int sed = s->idx_map["OCrust"];
        int oc = s->idx_map["Oceans"];

        double flux_up = denitrification;
        double flux_dow = sedimentation;

        s->fluxes[oc+1] -= (flux_up + flux_down);
        s->fluxes[atm] += flux_up;
        s->fluxes[sed+2] += flux_down;

        if(DEBUG) {
            cout << "BioticContribution: up=" << flux_up << endl;
            cout << "BioticContribution: down=" << flux_down << endl;
        }

        vector<double> output = {flux_up, flux_down};
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
REGISTER_MODULE(BioticContribution)
