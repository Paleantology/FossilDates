for i in {1..10}
do
python code/IntervalSampler.py
mkdir Data/$i
cp Data/accessory/* Data/$i
done