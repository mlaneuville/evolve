void Simulation::run(void) {

    double lastout = 0;
    while(this->time < this->tmax) {
        this->fluxes.assign(3*this->num_reservoirs, 0);

        // fetch deltas
        for (int j=0; j<this->mchain.size(); j++) {
            this->mchain[j]->exec("Evolve");
        }

        // apply deltas
        double curr_mass = 0;
        for (int j=0; j<this->fluxes.size(); j++) {
            this->masses[j] += this->timestep*this->fluxes[j];
            assert(this->masses[j] >= 0);
            curr_mass += this->masses[j];
        }
        assert(abs(curr_mass-this->m0)/this->m0 < 1e-4);

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


bool Simulation::init(string suffix) {

    fstream file;
    this->output_file = config->data["OutFolder"].as<string>() + "/out_" + suffix + ".txt";
    this->output_file_graph = config->data["OutFolder"].as<string>() + "/out_" + suffix + ".dot";
    file.open(this->output_file.c_str(), fstream::out);
    if (file.fail()) {
        cout << "Couldn't create output file. Your output folder likely doesn't exist." << endl;
        cout << "Check 'OutFolder' value in your config file." << endl;
        return false;
    }
    file.close();

    DEBUG = config->data["Debug"].as<bool>();

    this->current_iter = 0;
    this->timestep = config->data["Timestep"].as<double>();
    this->output = config->data["Output"].as<double>();
    this->tmax = config->data["Tmax"].as<double>();
    this->time = 0;
    this->m0 = 0;

    // reservoirs
    YAML::Node reservoirs = config->data["Reservoirs"];
    this->num_reservoirs = reservoirs.size();
    this->fluxes.resize(3*this->num_reservoirs);

    if(DEBUG) cout << "Number of reservoirs considered: " << this->num_reservoirs << endl;

    for(YAML::const_iterator it=reservoirs.begin(); it != reservoirs.end(); ++it) {
        string name = it->first.as<string>();
        int num_modules = reservoirs[name]["Processes"].size();
        this->world.push_back( new Reservoir(name, num_modules) );
    }

    // processes
    YAML::Node processes = config->data["Processes"];

    if(DEBUG) cout << "Number of processes considered: " << processes.size() << endl;

    for(int i=0;i<processes.size();i++) {
        this->mchain.push_back( factory.forge(processes[i].as<string>()) );
    }

    cout << "=========================" << endl;
    //this->generate_graph(); TODO: this needs to be fixed
    this->to_screen();
    this->file_header();
    this->to_file();

    return true;
}


void Simulation::to_screen(void) {
    printf("TS : %8d, Time: %4g, ", current_iter, time/1e6);

    double m, tot_m;
    for (int i=0; i<world.size(); i++) {
        m = 0;
        cout << world[i]->name.substr(0,2) << ": ";
        int idx = idx_map[world[i]->name];
        m += masses[idx];
        m += masses[idx+1];
        m += masses[idx+2];
        cout << m << ", ";
        tot_m += m;
    }
    cout << "TOT: " << tot_m << endl;
}


void Simulation::to_file(void) {
    fstream file;
    file.open(this->output_file.c_str(), fstream::app);
    file << current_iter << ",";
    file << time/1e6;
    for (int i=0; i<masses.size(); i++) file << "," << setprecision(8) << masses[i];

    for (int j=0; j<this->mchain.size(); j++) {
        for (int k=0; k<this->mchain[j]->numOutputs; k++) {
            file << "," << this->mchain[j]->fluxes.back()[k];
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

    for (int j=0; j<this->mchain.size(); j++) {
        for (int k=0; k<this->mchain[j]->numOutputs; k++) {
            file << "," << this->mchain[j]->name << k;
        }
    }

    file << endl;
    file.close();
}


void Simulation::generate_graph(void) {
    fstream file;
    vector<string> colors;
    colors.push_back("/accent4/1");
    colors.push_back("/accent4/2");
    colors.push_back("/accent4/3");

    file.open(this->output_file_graph.c_str(), fstream::out);
    file << "digraph { rankdir=\"LR\"" << endl;

    for (int i=0; i<this->num_reservoirs; i++) { // loop over reservoirs
        if (world[i]->num_modules == 0) continue;

        // draw boxes around reservoirs
        file << "\tsubgraph cluster_" << i << " { label = \"" << this->world[i]->name << "\"; ";
        for (int tmp=0; tmp<3; tmp++) {
            file << this->world[i]->name << tmp << "[style=\"filled\", color=\"black\", ";
            file << "fillcolor=\"" << colors[tmp] << "\"];";
        }
        file << "}" << endl;

        for (int j=0; j<this->mchain.size(); j++) {
            for (int k=0; k<this->mchain[j]->links.size(); k++) { // over links
                file << "\t" << this->mchain[j]->links[k];
                file << "[label=" << this->mchain[j]->name;
                if (this->mchain[j]->isBidirectional) file << ", dir=\"both\"";
                file << "]" << endl;
            }
        }
    }

    file << "}" << endl;
}
