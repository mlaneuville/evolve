
for i in $(seq -f "%03g" 75 100); do
    echo $i
    python generate_initial_conditions.py -n 20 -f output/oxi_$i -v $i
    python run_multi_config.py -f output/oxi_$i
done
