#FOLDER=../output/paperfigs/appendix/atmosphere/
#
#python generate_single_plot.py $FOLDER*.txt -c Oceans1 \
#                                             -l '50 Ma' -l '100 Ma' -l '150 Ma' -e  -o FIGA1A.eps
#python generate_single_plot.py $FOLDER*.txt -c Oceans2 \
#                                             -l '50 Ma' -l '100 Ma' -l '150 Ma' -e  -o FIGA1B.eps
#python generate_single_plot.py $FOLDER*.txt -c HydrothermalCirculation0 \
#                                             -l '50 Ma' -l '100 Ma' -l '150 Ma' -e  -o FIGA1C.eps
#python generate_single_plot.py $FOLDER*.txt -c CometDelivery0 \
#                                             -l '50 Ma' -l '100 Ma' -l '150 Ma' -o FIGA1D.eps

FOLDER=../output/paperfigs/appendix/subrate/

# FIG3. Complete evolution -- reservoirs
python generate_single_plot.py $FOLDER*.txt -c Atmosphere0 -n '(a)'\
                                             -l '50 Ma' -l '100 Ma' -l '150 Ma' -e  -o FIGA2A.eps
python generate_single_plot.py $FOLDER*.txt -c LMantle2 -n '(b)'\
                                             -l '50 Ma' -l '100 Ma' -l '150 Ma' -e  -o FIGA2B.eps
python generate_single_plot.py $FOLDER*.txt -c Oceans1 -n '(c)'\
                                             -l '50 Ma' -l '100 Ma' -l '150 Ma' -e  -o FIGA2C.eps
python generate_single_plot.py $FOLDER*.txt -c Oceans2 -n '(d)'\
                                             -l '50 Ma' -l '100 Ma' -l '150 Ma' -o FIGA2D.eps
#
FOLDER=../output/paperfigs/appendix/ocvol/

# FIG3. Complete evolution -- reservoirs
python generate_single_plot.py $FOLDER*.txt -c Atmosphere0 -n '(a)'\
                                             -l -40 -l constant -l +40 -e  -o FIGA3A.eps
python generate_single_plot.py $FOLDER*.txt -c LMantle2 -n '(b)'\
                                             -l -40 -l constant -l +40 -e  -o FIGA3B.eps
python generate_single_plot.py $FOLDER*.txt -c Oceans1 -n '(c)'\
                                             -l -40 -l constant -l +40 -e  -o FIGA3C.eps
python generate_single_plot.py $FOLDER*.txt -c Oceans2 -n '(d)'\
                                             -l -40 -l constant -l +40     -o FIGA3D.eps
#
### FIG4. Complete evolution -- fluxes
##python generate_single_plot.py $FOLDER*.txt -c AbioticFixation0          -o FIG4A.eps
##python generate_single_plot.py $FOLDER*.txt -c FreundlichAdsorption0     -o FIG4B.eps
##python generate_single_plot.py $FOLDER*.txt -c HydrothermalCirculation0  -o FIG4C.eps
##python generate_single_plot.py $FOLDER*.txt -c HydrothermalCirculation1  -o FIG4D.eps
##python generate_single_plot.py $FOLDER*.txt -c Subduction0  -o FIG4Z.eps
##python generate_single_plot.py $FOLDER*.txt -c Volcanism0 -l arc-like    -o FIG4E.eps
##python generate_single_plot.py $FOLDER*.txt -c Volcanism1 -c Volcanism2 \
##                                            -l MORB-like -l hotspot-like \
##                                            -o FIG4F.eps
##
### FIG5. Fixes point approach
##python generate_single_plot.py $FOLDER/*.txt -c Atmosphere0 -c UMantle2 -p -o FIG5A.eps
#
### FIG6. Main parameters influence
##
##python generate_pdependence.py -f $FOLDER/20/oce-mix/ \
##                               -f $FOLDER/40/oce-mix/ \
##                               -f $FOLDER/60/oce-mix/ \
##                               -l 20 -l 40 -l 60 -c Atmosphere0 -o FIG6B.eps
#
##FOLDER=../output/paperfigs/sensitivity/man-ox/
##
### FIG7. Main parameters influence
##python generate_pdependence.py -f $FOLDER  -c Atmosphere0 -o FIG7A.eps
##python generate_pdependence.py -f $FOLDER  \
##                               -c Volcanism0 -c Volcanism1 -c Volcanism2 \
##                               -l arc-like -l MORB-like -l hotspot-like -o FIG7B.eps
#
##python generate_single_plot.py ../output/sensitivity/E6/*.txt -c Atmosphere0 \
##    -l 1e-4 -l 1e-5 -l 3e-5 -l 7e-5 -e -o FIG5E.eps
##python generate_single_plot.py ../output/sensitivity/E6/*.txt -c Oceans1 \
##    -l 1e-4 -l 1e-5 -l 3e-5 -l 7e-5 -e -o FIG5F.eps
##python generate_single_plot.py ../output/sensitivity/E6/*.txt -c Oceans2 \
##    -l 1e-4 -l 1e-5 -l 3e-5 -l 7e-5 -e -o FIG5G.eps
##python generate_single_plot.py ../output/sensitivity/E6/*.txt -c UMantle2 \
##    -l 1e-4 -l 1e-5 -l 3e-5 -l 7e-5 -e -o FIG5H.eps
#
#
