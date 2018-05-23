threads=(1 2 4 8)
n_all=(1000 10000 50000 100000 500000)
echo count pi_omp > pi_omp.txt
echo count pi_mpi > pi_mpi.txt
echo count prime_omp > prime_omp.txt
echo count prime_mpi > prime_mpi.txt

for n in ${n_all[@]}
do
	echo n = $n >> pi_omp.txt
	echo n = $n >> pi_mpi.txt
	echo n = $n >> prime_omp.txt
	echo n = $n >> prime_mpi.txt

	for thread in ${threads[@]}
	do
		#echo -n Thread = $thread 
		pi_omp=$(exec ./pi_omp $thread $n)
		echo $pi_omp >> pi_omp.txt

		#echo -n Thread = $thread
		pi_mpi=$(exec mpirun -np $thread ./pi_mpi $n)
		echo $pi_mpi >> pi_mpi.txt

		#echo -n Thread = $thread
		prime_omp=$(exec ./primes_omp $thread $n)
		echo $prime_omp >> prime_omp.txt

                #echo -n Thread = $thread
                prime_mpi=$(exec mpirun -np $thread ./primes_mpi $n)
                echo $prime_mpi >> prime_mpi.txt

	done
done

