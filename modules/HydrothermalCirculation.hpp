class HydrothermalCirculation: public Module {
public:
    HydrothermalCirculation(string name): Module(name) { init(); }

    double tau, F_NOx, F_N2, F0, F1;

    void init(void) {
        this->links.push_back("Oceans0 -> Oceans2");
        this->links.push_back("Oceans1 -> Oceans2");

        F0 = config->data["HydrothermalCirculation"]["F0"].as<double>();
        F1 = config->data["HydrothermalCirculation"]["F1"].as<double>();
        F_NOx = config->data["HydrothermalCirculation"]["F_NOx"].as<double>();
        F_N2 = config->data["HydrothermalCirculation"]["F_N2"].as<double>();
        tau = config->data["HydrothermalCirculation"]["tau"].as<double>();
    }

    void evolve(void) {
        int oc = s->idx_map["Oceans"];
        int cr = s->idx_map["OCrust"];

        double vol_fraction = F0 + (F1-F0)*exp(-s->time/tau);
        double f_NOx = s->masses[oc+1]*vol_fraction*F_NOx;
        double f_N2 = s->masses[oc]*vol_fraction*F_N2;

        s->fluxes[oc] += -f_N2;
        s->fluxes[oc+1] += -f_NOx;
        s->fluxes[oc+2] += (f_N2+f_NOx);

        if(DEBUG) {
            cout << "HydrothermalCirculation: NOx=" << f_NOx << endl;
            cout << "HydrothermalCirculation: N2=" << f_N2 << endl;
        }
        this->fluxes.push_back(f_N2+f_NOx);
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
REGISTER_MODULE(HydrothermalCirculation)
