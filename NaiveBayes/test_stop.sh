for i in $(seq 1 100)
do
    echo ${i}
    python nbStopWords.py split.train split.test ${i}
done
