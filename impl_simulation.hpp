void Simulation::run(void) {

    double lastout = 0;
    while(this->time < this->tmax) {
        this->fluxes.assign(3*this->num_reservoirs, 0);

        // fetch deltas
        for (int j=0; j<this->num_reservoirs; j++) {
            world[j]->run_processes();
        }

        // apply deltas
        for (int j=0; j<this->fluxes.size(); j++) {
            this->masses[j] += this->timestep*this->fluxes[j];
            assert(this->masses[j] >= 0);
        }

        this->current_iter++;
        this->time += this->timestep;

        if (this->time - lastout >= this->output) {
            this->to_screen();
            this->to_file();
            lastout = this->time;
        }
    }

    return; 
}


void Simulation::init(string suffix) { 

    fstream file;
    this->output_file = config->data["OutFolder"].as<string>() + "/out_" + suffix + ".txt";
    this->output_file_graph = config->data["OutFolder"].as<string>() + "/out_" + suffix + ".dot";
    file.open(this->output_file.c_str(), fstream::out);
    file.close();

    DEBUG = config->data["Debug"].as<bool>();

    this->current_iter = 0;
    this->timestep = config->data["Timestep"].as<double>();
    this->output = config->data["Output"].as<double>();
    this->tmax = config->data["Tmax"].as<double>();
    this->time = 0;

    YAML::Node reservoirs = config->data["Reservoirs"];
    this->num_reservoirs = reservoirs.size();
    this->fluxes.resize(3*this->num_reservoirs);

    if(DEBUG) cout << "Number of reservoirs considered: " << this->num_reservoirs << endl;

    for(YAML::const_iterator it=reservoirs.begin(); it != reservoirs.end(); ++it) {
        string name = it->first.as<string>();
        int num_modules = reservoirs[name]["Processes"].size();
        cout << "Loading reservoir " << name << " with " << num_modules << " modules" << endl;
        this->world.push_back( new Reservoir(name, num_modules) );
    }
    
    cout << "=========================" << endl;
    this->generate_graph();
    this->to_screen();
    this->file_header();
    this->to_file();

    return; 
}


void Simulation::to_screen(void) {
    printf("TS : %8d, Time: %4g, ", current_iter, time/1e6);

    double m;
    for (int i=0; i<world.size(); i++) {
        m = 0;
        cout << world[i]->name.substr(0,2) << ": ";
        int idx = idx_map[world[i]->name];
        m += masses[idx];
        m += masses[idx+1];
        m += masses[idx+2];
        cout << m << ", ";
    }
    cout << endl;
}


void Simulation::to_file(void) {
    fstream file;
    file.open(this->output_file.c_str(), fstream::app);
    file << current_iter << ",";
    file << time/1e6;
    for (int i=0; i<masses.size(); i++) file << "," << masses[i];

    for (int i=0; i<this->num_reservoirs; i++) {
        for (int j=0; j<world[i]->num_modules; j++) {
            file << "," << world[i]->mchain[j]->fluxes.back();
        }
    }

    file << endl;
    file.close();
}


void Simulation::file_header(void) {
    fstream file;
    file.open(this->output_file.c_str(), fstream::app);
    file << "iter,time";

    for (int i=0; i<world.size(); i++)
        for (int j=0; j<3; j++)
            file << "," << world[i]->name << j;

    for (int i=0; i<this->num_reservoirs; i++) {
        for (int j=0; j<world[i]->num_modules; j++) {
            file << "," << world[i]->mchain[j]->name;
        }
    }

    file << endl;
    file.close();
}

void Simulation::generate_graph(void) {
    fstream file;
    file.open(this->output_file_graph.c_str(), fstream::out);
    file << "digraph {" << endl;
    for (int i=0; i<this->num_reservoirs; i++) { // loop over reservoirs
        file << "\tsubgraph cluster_" << i << " { label = \"" << this->world[i]->name << "\"; ";
        for (int tmp=0; tmp<3; tmp++) file << this->world[i]->name << tmp << "; ";
        file << "}" << endl;
        for (int j=0; j<world[i]->num_modules; j++) {
            for (int k=0; k<world[i]->mchain[j]->links.size(); k++) {
                file << "\t" << world[i]->mchain[j]->links[k];
                file << "[label=" << world[i]->mchain[j]->name;
                if (world[i]->mchain[j]->isBidirectional) file << ", dir=\"both\"";
                file << "]" << endl;
            }
        }
    }
    file << "}" << endl;
}
