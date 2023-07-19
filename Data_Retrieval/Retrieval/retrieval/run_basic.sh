rm -rf basic_out
mkdir basic_out
for i in {0..1}
do
  echo $i"-th iteration"
  python3 feature_extraction_basic_a.py $((1+500*${i})) 500 $i
done
#python3 feature_extraction_basic_a.py 500001 2394 1112

