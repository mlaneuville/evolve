class AbioticFixation: public Module {
public:
    AbioticFixation(string name): Module(name) { init(); }

    double Fi_NOx, Ff_NOx, Fi_NH3, Ff_NH3, M_REF, tau, goe;

    void init(void) {
        this->links.push_back("Atmosphere0 -> Oceans1");
        this->links.push_back("Atmosphere0 -> Oceans2");
        this->numOutputs = 2;
        this->init_fluxes(2);

        Fi_NOx = config->data["AbioticFixation"]["Fi_NOx"].as<double>();
        Fi_NH3 = config->data["AbioticFixation"]["Fi_NH3"].as<double>();
        Ff_NOx = config->data["AbioticFixation"]["Ff_NOx"].as<double>();
        Ff_NH3 = config->data["AbioticFixation"]["Ff_NH3"].as<double>();
        tau = config->data["AbioticFixation"]["tau"].as<double>();
        goe = config->data["AbioticFixation"]["goe"].as<double>();
        M_REF = config->data["AbioticFixation"]["M_REF"].as<double>();
    }

    void evolve(void) {
        int atm = s->idx_map["Atmosphere"];
        int oc = s->idx_map["Oceans"];

        double F_NOx = Ff_NOx + Fi_NOx*(1-1/(1+exp(-(s->time-goe)/tau)));
        double F_NH3 = Ff_NH3 + Fi_NH3*(1-1/(1+exp(-(s->time-goe)/tau)));

        double flux_NOx = F_NOx*s->masses[atm]/M_REF;
        double flux_NH3 = F_NH3*s->masses[atm]/M_REF;

        s->fluxes[atm] += -(flux_NOx + flux_NH3);
        s->fluxes[oc+1] += flux_NOx;
        s->fluxes[oc+2] += flux_NH3;

        if(DEBUG) {
            cout << "AbioticFixation::flux_NOx::" << flux_NOx << endl;
            cout << "AbioticFixation::flux_NH3::" << flux_NH3 << endl;
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
