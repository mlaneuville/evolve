class Module {
public:
    string name;
    vector<double> fluxes;

    Module(string name) {
        this->name = name;
        this->fluxes.push_back(0);
    }
    virtual bool exec(string param) = 0;
};

class basic_factory {
public:
    virtual Module* forge() = 0;
};

class ModuleFactory {
    map<string, basic_factory*> factories;

public:
    void register_module(string name, basic_factory* factory) {
        factories[name] = factory;
    }

    Module* forge(string name) {
        if (factories.find(name) == factories.end()) {
            cout << "Module '" << name << "' was never registered! Exiting..." << endl;
            exit(1);
        }
        cout << "-- Loading '" << name << "' ..." << endl;
        return factories[name]->forge();
    }
};



ModuleFactory factory;


#define REGISTER_MODULE(name) \
class name##_factory : public basic_factory { \
public: \
    name##_factory() { \
        factory.register_module(#name, this);\
    }; \
    Module* forge() { \
        return new name(#name); \
    } \
};\
name##_factory _##name##_factory;
