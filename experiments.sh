echo "id,input_size,comparisons,match_status" > ./output.csv

for file in ./data/*; do
    python ./interweaving_analysis.py $file >> ./output.csv
done
