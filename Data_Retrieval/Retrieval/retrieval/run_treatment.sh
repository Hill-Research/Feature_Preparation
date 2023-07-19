rm -rf treatment_out
mkdir treatment_out

for i in {0..1}
do
  echo $i"-th iteration"
  python3 feature_extraction_treatment_a.py $((1+500*${i})) 500 $I
done
python3 feature_extraction_treatment_a.py 500001 2394 1112

