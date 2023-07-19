for i in {0..99}
do
  echo $i"-th iteration"
  python3 feature_extraction_diagnosis_a.py $((1+5000*${i})) 5000
done
python3 feature_extraction_diagnosis_a.py 500001 2394

