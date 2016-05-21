class CometDelivery: public Module {
public:
    CometDelivery(string name): Module(name) { init(); }

    double tau, F0, F1;

    void init(void) {
        F0 = config->data["CometDelivery"]["F0"].as<double>();
        F1 = config->data["CometDelivery"]["F1"].as<double>();
        tau = config->data["CometDelivery"]["tau"].as<double>();
    }

    void evolve(void) {
        double flux = F0 + (F1-F0)*exp(-s->time/tau);
        int oc = s->idx_map["Oceans"];
        s->fluxes[oc+1] += flux; // this is a net source, so no need to balance
        if(DEBUG) cout << "CometDelivery: " << flux << endl;
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
REGISTER_MODULE(CometDelivery)
