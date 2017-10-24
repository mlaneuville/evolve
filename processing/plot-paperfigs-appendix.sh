FOLDER=../output/appendix-subrate/
## FIG3. Complete evolution -- reservoirs
python generate_single_plot.py $FOLDER*.txt -c Atmosphere0 -n '(a)'\
                                            -l '100 Ma' -l '150 Ma' -l '50 Ma' -e  -o FIGA2A.eps
python generate_single_plot.py $FOLDER*.txt -c LMantle2 -n '(b)'\
                                            -l '100 Ma' -l '150 Ma' -l '50 Ma' -e  -o FIGA2B.eps
python generate_single_plot.py $FOLDER*.txt -c Oceans1 -n '(c)'\
                                            -l '100 Ma' -l '150 Ma' -l '50 Ma' -e  -o FIGA2C.eps
python generate_single_plot.py $FOLDER*.txt -c Oceans2 -n '(d)'\
                                            -l '100 Ma' -l '150 Ma' -l '50 Ma' -o FIGA2D.eps

FOLDER=../output/appendix-ocvol/
## FIG3. Complete evolution -- reservoirs
python generate_single_plot.py $FOLDER*.txt -c Atmosphere0 -n '(a)'\
                                            -l '-40 pc.' -l constant -l '+40 pc.' -e  -o FIGA3A.eps
python generate_single_plot.py $FOLDER*.txt -c LMantle2 -n '(b)'\
                                            -l '-40 pc.' -l constant -l '+40 pc.' -e  -o FIGA3B.eps
python generate_single_plot.py $FOLDER*.txt -c Oceans1 -n '(c)'\
                                            -l '-40 pc.' -l constant -l '+40 pc.' -e  -o FIGA3C.eps
python generate_single_plot.py $FOLDER*.txt -c Oceans2 -n '(d)'\
                                            -l '-40 pc.' -l constant -l '+40 pc.'     -o FIGA3D.eps
