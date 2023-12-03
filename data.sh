stringSizes=(10 100 250 500 750 1000)
mkdir -vp data

for i in ${!stringSizes[@]}; do
    python ./interweaving_data.py 10 ${stringSizes[$i]} > "./data/dataset${i}.txt"
done
