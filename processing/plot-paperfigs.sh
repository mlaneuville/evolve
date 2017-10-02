FOLDER=../output/paperfigs/fixed-point/
#
# FIG3. Complete evolution -- reservoirs
#python generate_single_plot.py $FOLDER*.txt -c Atmosphere0 -e  -o FIG3A.eps -n '(a)'
#python generate_single_plot.py $FOLDER*.txt -c LMantle2 -c UMantle2 \
#                                            -l 'Lower mantle'  -l 'Upper mantle'  \
#                                            -e  -o FIG3B.eps -n '(b)'
#python generate_single_plot.py $FOLDER*.txt -c Oceans1     -e  -o FIG3C.eps -n '(c)'
#python generate_single_plot.py $FOLDER*.txt -c Oceans2         -o FIG3D.eps -n '(d)'

# FIG4. Complete evolution -- fluxes
python generate_single_plot.py $FOLDER*.txt -c AbioticFixation0          -o FIG4A.eps -n '(a)'
python generate_single_plot.py $FOLDER*.txt -c FreundlichAdsorption0     -o FIG4B.eps -n '(b)'
python generate_single_plot.py $FOLDER*.txt -c HydrothermalCirculation0  -o FIG4C.eps -n '(c)'
python generate_single_plot.py $FOLDER*.txt -c HydrothermalCirculation1  -o FIG4D.eps -n '(d)'
python generate_single_plot.py $FOLDER*.txt -c Volcanism0 -l arc-like    -o FIG4E.eps -n '(e)'
python generate_single_plot.py $FOLDER*.txt -c Volcanism1 -c Volcanism2 \
                                            -l MORB-like -l hotspot-like \
                                            -o FIG4F.eps -n '(f)'

## FIG5. Fixes point approach
#python generate_single_plot.py $FOLDER/*.txt -c Atmosphere0 -c UMantle2 -p -o FIG5A.eps

#FOLDER=../output/paperfigs/sensitivity/alpha/
#
# FIG6. Main parameters influence
#python generate_pdependence.py -f $FOLDER/20/man-mix/ \
#                               -f $FOLDER/40/man-mix/ \
#                               -f $FOLDER/60/man-mix/ \
#                               -l 20 -l 40 -l 60 -c Atmosphere0 -o FIG6A.eps -n '(a)'
#
#python generate_pdependence.py -f $FOLDER/20/oce-mix/ \
#                               -f $FOLDER/40/oce-mix/ \
#                               -f $FOLDER/60/oce-mix/ \
#                               -l 20 -l 40 -l 60 -c Atmosphere0 -o FIG6B.eps -n '(b)'

FOLDER=../output/paperfigs/sensitivity/man-ox/

# FIG7. Main parameters influence
#python generate_pdependence.py -f $FOLDER  -c Atmosphere0 -o FIG7A.eps -n '(a)'
#python generate_pdependence.py -f $FOLDER  \
#                               -c Volcanism0 -c Volcanism1 -c Volcanism2 \
#                               -l arc-like -l MORB-like -l hotspot-like \
#                               -o FIG7B.eps -n '(b)'

#python generate_single_plot.py ../output/sensitivity/E6/*.txt -c Atmosphere0 \
#    -l 1e-4 -l 1e-5 -l 3e-5 -l 7e-5 -e -o FIG5E.eps
#python generate_single_plot.py ../output/sensitivity/E6/*.txt -c Oceans1 \
#    -l 1e-4 -l 1e-5 -l 3e-5 -l 7e-5 -e -o FIG5F.eps
#python generate_single_plot.py ../output/sensitivity/E6/*.txt -c Oceans2 \
#    -l 1e-4 -l 1e-5 -l 3e-5 -l 7e-5 -e -o FIG5G.eps
#python generate_single_plot.py ../output/sensitivity/E6/*.txt -c UMantle2 \
#    -l 1e-4 -l 1e-5 -l 3e-5 -l 7e-5 -e -o FIG5H.eps


