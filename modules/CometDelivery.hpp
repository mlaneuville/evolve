class CometDelivery: public Module {
public:
    CometDelivery(string name): Module(name) { init(); }

    double tau, F0, F1;

    void init(void) {
        this->links.push_back("Space -> Oceans2");
        this->numOutputs = 1;
        this->init_fluxes(1);

        F0 = config->data["CometDelivery"]["F0"].as<double>();
        F1 = config->data["CometDelivery"]["F1"].as<double>();
        tau = config->data["CometDelivery"]["tau"].as<double>();
    }

    void evolve(void) {
        int oc = s->idx_map["Oceans"];

        double flux = F0 + (F1-F0)*exp(-s->time/tau);

        s->fluxes[oc+2] += flux; // this is a net source, so no need to balance

        if(DEBUG) cout << "CometDelivery: " << flux << endl;

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
REGISTER_MODULE(CometDelivery)
