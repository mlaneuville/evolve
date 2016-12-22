# FIG1. Typical evolution over a wide range of initial conditions
python generate_single_plot.py ../prod-runs/redox-mantle/020/*.txt -e -c Atmosphere0 -o FIG1A.eps
python generate_single_plot.py ../prod-runs/redox-mantle/020/*.txt -e -c Oceans0 -c Oceans1 -c Oceans2 -l N2 -l NOx -l NHy -o FIG1B.eps
python generate_single_plot.py ../prod-runs/redox-mantle/020/*.txt -e -c OCrust2 -c UMantle2 -l sediments -l umantle -o FIG1C.eps
python generate_single_plot.py ../prod-runs/redox-mantle/020/*.txt -e -c LMantle2 -o FIG1D.eps

# FIG2. Atmosphere N-content as a function of ocean and mantle mixing rate
python generate_pdependence.py -f ../prod-runs/comp-conv/ -c Atmosphere0  -o FIG2A.eps
python generate_pdependence.py -f ../prod-runs/comp-hydro/ -c Atmosphere0 -o FIG2C.eps

#python generate_pdependence.py -f ../prod-runs/comp-hydro/ -c Oceans0 -c Oceans1 -c Oceans2 -l N2 -l NOx -l NHy -o FIG2C.eps
#python generate_pdependence.py -f ../prod-runs/comp-hydro/ -c Oceans0 -c Oceans1 -c Oceans2 -l N2 -l NOx -l NHy -r -o FIG2D.eps

# FIG3. Ocean content as a function of mantle and atmosphere redox
python generate_pdependence.py -f ../prod-runs/redox-mantle/ -c Oceans0 -c Oceans1 -c Oceans2 -l N2 -l NOx -l NHy -o FIG3A.eps
python generate_pdependence.py -f ../prod-runs/redox-mantle/ -c Atmosphere0 -o FIG3B.eps
python generate_pdependence.py -f ../prod-runs/redox-mantle/ -c Oceans0 -c Oceans1 -c Oceans2 -l N2 -l NOx -l NHy -r -o FIG3C.eps
python generate_pdependence.py -f ../prod-runs/redox-mantle/ -c Atmosphere0 -r -o FIG3D.eps

# FIG4. Atmosphere content as a function of mantle and atmosphere redox
#python generate_pdependence.py -f ../prod-runs/redox-mantle/ -c Atmosphere0 -o FIG4A.eps
#python generate_pdependence.py -f ../prod-runs/redox-atmosphere/ -c Atmosphere0 -o FIG4B.eps

# FIG5. Volcanic fluxes as a function of ocean and mantle mixing rate
python generate_pdependence.py -f ../prod-runs/comp-conv/ -c Volcanism0 -c Volcanism1 -c Volcanism2 -l arc -l morb -l hotspot -o FIG5A.eps
python generate_pdependence.py -f ../prod-runs/comp-conv/ -c Volcanism0 -c Volcanism1 -c Volcanism2 -l arc -l morb -l hotspot -r -o FIG5B.eps
python generate_pdependence.py -f ../prod-runs/comp-hydro/ -c Volcanism0 -c Volcanism1 -c Volcanism2 -l arc -l morb -l hotspot -o FIG5C.eps
python generate_pdependence.py -f ../prod-runs/comp-hydro/ -c Volcanism0 -c Volcanism1 -c Volcanism2 -l arc -l morb -l hotspot -r -o FIG5D.eps

# FIG6. Convergence to fixed point
python generate_single_plot.py ../output/phase-space/020/*.txt -c Atmosphere0 -c LMantle2 -p -o FIG6.eps
