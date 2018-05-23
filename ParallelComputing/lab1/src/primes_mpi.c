#include <stdio.h>
#include <math.h>
#include <mpi.h>
#include <stdlib.h>
#include <time.h>

int x , n , h = 0;
int start;
int end;
MPI_Status status;
int rank, size;

int is_prime(int n)
{
    int i = 2;
    if (n < 2)
    {
        return 0;
    }
    while (i <= sqrt(n))
    {
        if (n%i == 0)
        {
            return 0;
        }
        i++;
    }
    return 1;
}

void primes_count(int x, int y)
{
    int i, j, flag;
    if(x < 2)
	x = 2;
    for(i = x;i <= y;i++)
    {
	flag = 0;
        for(j = 2;j <= sqrt(i);j++)
        {
            if(i % j == 0)
	    { 
		flag = 1;
	        break;
	    }
        }
	if(flag == 0)
	{
	   h++;
    	   if(is_prime(i) == 0)
	       printf("---%d\n",i);
	}
    }

}

int main (int argc, char *argv[])
{

    MPI_Init (&argc, &argv);        	    /* starts MPI */
    MPI_Comm_rank (MPI_COMM_WORLD, &rank);  /* get current process id */
    MPI_Comm_size (MPI_COMM_WORLD, &size);  /* get number of processes */

    if (rank == 0)
    {
        n = atoi(argv[1]);

	// clock_t start_time = clock();
	double wtime = MPI_Wtime();
        for(int j = 1; j < size; j++)
        {
            MPI_Send(&n, 1, MPI_INT, j, 1, MPI_COMM_WORLD);
        }

        start = n / size;
        start = start * rank;
	end = start + (n / size) - 1;
	
	primes_count(start, end);

	int k;
	for(int j = 1;j < size;j++)
	{
	    MPI_Recv(&k, 1, MPI_INT, j, 1, MPI_COMM_WORLD, &status);
	    h += k;
	}
	// printf("Rank = %d where range from %d to %d \n",rank,start,end);
	// clock_t end_time = clock();
	// double cost_time = (double)(end_time - start_time) / CLOCKS_PER_SEC;
	wtime = MPI_Wtime() - wtime;
	printf("[INFO]Use MPI.res is %d, time is %lfs\n", h, wtime);
    }

    else
    {
        MPI_Recv(&n, 1, MPI_INT, 0, 1, MPI_COMM_WORLD, &status);
        
	start = n / size;
        start = start * rank;
        if(rank == size - 1)
            end = n;
        else
            end = start + (n/size)-1;
        primes_count(start, end);
	// printf("Rank = %d where range from %d to %d....h:%d \n",rank,start,end,h);
        MPI_Send(&h, 1, MPI_INT, 0, 1, MPI_COMM_WORLD);
    }

    MPI_Finalize();
    return 0;
}

