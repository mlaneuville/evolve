class UVLight: public Module {
public:
    UVLight(string name): Module(name) { init(); }

    double F0;

    void init(void) {
        this->links.push_back("Oceans1 -> Atmosphere0");
        this->numOutputs = 1;
        this->init_fluxes(1);

        F0 = config->data["UVLight"]["F0"].as<double>();
    }

    void evolve(void) {
        int atm = s->idx_map["Atmosphere"];
        int oc = s->idx_map["Oceans"];

        double f_N2 = s->masses[oc+1]*F0;

        s->fluxes[oc+1] += -f_N2;
        s->fluxes[atm] += f_N2;

        if(DEBUG) {
            cout << "UVLight::f_N2::" << f_N2 << endl;
        }

        vector<double> output = {f_N2};
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
REGISTER_MODULE(UVLight)
