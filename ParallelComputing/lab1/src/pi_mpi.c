#include <stdio.h>
#include <mpi.h>
#include <stdlib.h>
#include <time.h>

double sum = 0.0;
MPI_Status status;
int rank, size;

void simulate_pi(int start, int end, long num_steps)
{
    double x;
    for (int i = start;i <= end; i++)
    {
         x = (i + 0.5) / (double)num_steps;
         sum += 4.0 / (1.0 + x*x);
    }

}

int main (int argc, char *argv[])
{

    MPI_Init (&argc, &argv);        	    /* starts MPI */
    MPI_Comm_rank (MPI_COMM_WORLD, &rank);  /* get current process id */
    MPI_Comm_size (MPI_COMM_WORLD, &size);  /* get number of processes */

    if (rank == 0)
    {
        long num_steps = atoi(argv[1]);

	// clock_t start_time = clock();
	double wtime = MPI_Wtime();
        for(int j = 1; j < size; j++)
        {
            MPI_Send(&num_steps, 1, MPI_LONG, j, 1, MPI_COMM_WORLD);
        }

        int start = num_steps / size;
        start = start * rank;
        int end = start + (num_steps / size) - 1;

	simulate_pi(start, end, num_steps);
	double k, pi;
	for(int j = 1;j < size;j++)
	{
	    MPI_Recv(&k, 1, MPI_DOUBLE, j, 1, MPI_COMM_WORLD, &status);
	    sum += k;
	}

	pi = sum / (double)num_steps;
	// clock_t end_time = clock();
	// double cost_time = (double)(end_time - start_time) / CLOCKS_PER_SEC;
	wtime = MPI_Wtime() - wtime;
	printf("[INFO]Use MPI.PI is %lf, time is %lfs.\n", pi, wtime);
    }

    else
    {
	long num_steps;
        MPI_Recv(&num_steps, 1, MPI_LONG, 0, 1, MPI_COMM_WORLD, &status);
        
	// printf("[INFO]Rank = %d where range from %d to %d \n", rank, start, end);
        int end, start = num_steps / size;
        start = start * rank;
        if(rank == size - 1)
            end = num_steps;
        else
            end = start + (num_steps / size)-1;

	simulate_pi(start, end, num_steps);
        MPI_Send(&sum, 1, MPI_DOUBLE, 0, 1, MPI_COMM_WORLD);
    }

    MPI_Finalize();
    return 0;
}

