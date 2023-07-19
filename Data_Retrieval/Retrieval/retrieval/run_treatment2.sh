rm -rf treatment_out2
mkdir treatment_out2

for i in {378..1005}
do
  echo $i"-th iteration"
  python3 feature_extraction_treatment_a.py $((1+500*${i})) 500 $i
done
python3 feature_extraction_treatment_a.py 500001 2394 1006

