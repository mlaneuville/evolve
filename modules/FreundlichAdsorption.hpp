class FreundlichAdsorption: public Module {
public:
    FreundlichAdsorption(string name): Module(name) { init(); }

    double Kf;

    void init(void) {
        Kf = config->data["FreundlichAdsorption"]["Kf"].as<double>();
    }

    void evolve(void) {
        int oc = s->idx_map["Oceans"];
        int cr = s->idx_map["Crust"];

        double flux = Kf;

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
