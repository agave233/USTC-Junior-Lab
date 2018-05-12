echo "Test for NQueens..."
a=(10 100 1000 10000 30000 50000 80000 100000 300000 500000 800000 1000000)
for n in ${a[@]}
do
	b=(0 `expr $n / 8` `expr $n / 4` `expr $n / 2` $n)
	for m in ${b[@]}
	do 
		# sed '1, $d' input.txt
                echo $n $m > input.txt
		a=$(exec ./sa_test)
		b=$(exec ./hc_test)
		a1=(${a})
		b1=(${b})
		echo n=$n, m=$m, count=${a1[0]},${b1[0]}
                echo ${a1[1]}, >> sa_time.csv
                echo ${b1[1]}, >> hc_time.csv
	done
        echo -e "\n" >> sa_time.csv
	echo -e "\n" >> hc_time.csv
done
