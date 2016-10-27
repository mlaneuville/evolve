class AbioticFixation: public Module {
public:
    AbioticFixation(string name): Module(name) { init(); }

    double F_NOx, F_NH3, M_REF;

    void init(void) {
        this->links.push_back("Atmosphere0 -> Oceans1");
        this->links.push_back("Atmosphere0 -> Oceans2");
        this->numOutputs = 2;
        this->init_fluxes(2);

        F_NOx = config->data["AbioticFixation"]["F_NOx"].as<double>();
        F_NH3 = config->data["AbioticFixation"]["F_NH3"].as<double>();
        M_REF = config->data["AbioticFixation"]["M_REF"].as<double>();
    }

    void evolve(void) {
        int atm = s->idx_map["Atmosphere"];
        int oc = s->idx_map["Oceans"];

        double flux_NOx = F_NOx*s->masses[atm]/M_REF;
        double flux_NH3 = F_NH3*s->masses[atm]/M_REF;

        s->fluxes[atm] += -(flux_NOx + flux_NH3);
        s->fluxes[oc+1] += flux_NOx;
        s->fluxes[oc+2] += flux_NH3;

        if(DEBUG) {
            cout << "AbioticFixation: NOx=" << flux_NOx << endl;
            cout << "AbioticFixation: NH3=" << flux_NH3 << endl;
        }

        vector<double> output = {flux_NOx, flux_NH3};
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
REGISTER_MODULE(AbioticFixation)
