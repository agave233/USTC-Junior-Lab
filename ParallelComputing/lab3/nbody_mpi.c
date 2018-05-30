#include <stdio.h>
#include <time.h>
#include <sys/timeb.h>
#include <stdlib.h>
#include <math.h>
#include <mpi.h>
#include <string.h>

#define N 64
#define G 6.67e-11
#define R 0.01
#define M 10000
#define TIME 10
#define TIME_STEP 1000

MPI_Status status;
int rank, size;

double all_balls_x[N];
double all_balls_y[N];
double *curr_balls_x;
double *curr_balls_y;
double *curr_balls_vx;
double *curr_balls_vy;

double a_x, a_y;


void compute_force(int k)
{
	double dis_x, dis_y, a;
	k = N / size * rank + k;
	a_x = 0.0;
	a_y = 0.0;

	for(int i = 0; i < N; i++)
	{
		if(i == k)
			continue;
		dis_x = fabs(all_balls_x[i] - all_balls_x[k]);
		dis_y = fabs(all_balls_y[i] - all_balls_y[k]);
		dis_x = dis_x > 0.02 ? dis_x : 0.02;
		dis_y = dis_y > 0.02 ? dis_y : 0.02;		
		a = G * M / pow(dis_x * dis_x + dis_y * dis_y, 1.5);
		a_x += a * (all_balls_x[i] - all_balls_x[k]);
		a_y += a * (all_balls_y[i] - all_balls_y[k]);
	}
	printf("%f, %f\n", a_x, a_y);
}

void compute_velocities(int k)
{
	curr_balls_vx[k] += a_x / TIME_STEP;
	curr_balls_vy[k] += a_y / TIME_STEP;
}

void compute_positions(int k)
{
	curr_balls_x[k] += curr_balls_vx[k] / TIME_STEP;
	curr_balls_y[k] += curr_balls_vy[k] / TIME_STEP;
}

int main(int argc, char *argv[])
{
    MPI_Init (&argc, &argv);        	    
    MPI_Comm_rank (MPI_COMM_WORLD, &rank);  
    MPI_Comm_size (MPI_COMM_WORLD, &size); 
    double wtime;

    curr_balls_x = (double*)malloc(N / size * sizeof(double));
    curr_balls_y = (double*)malloc(N / size * sizeof(double));
    curr_balls_vx = (double*)malloc(N / size * sizeof(double));
    curr_balls_vy = (double*)malloc(N / size * sizeof(double));

    memset(curr_balls_vx, 0.0, N / size * sizeof(double));
    memset(curr_balls_vy, 0.0, N / size * sizeof(double));

    int k = 0;
    for(int i = N / size * rank; i < N / size * (rank + 1); i++)
    {
    	curr_balls_x[k] = i % (N / size);
    	curr_balls_y[k++] = i / (N / size);
    }
    // printf("...%d..", rank);
    wtime = MPI_Wtime();
    for(int i = 0; i < TIME * TIME_STEP; i++)
    {
       	// printf("%d\n", i);
    	MPI_Allgather(curr_balls_x, N / size, MPI_DOUBLE, all_balls_x, N / size, MPI_DOUBLE, MPI_COMM_WORLD);
    	MPI_Allgather(curr_balls_y, N / size, MPI_DOUBLE, all_balls_y, N / size, MPI_DOUBLE, MPI_COMM_WORLD);    	
    
		for(int j = 0; j < N / size; j++)
	    	{
	    		compute_force(j);
	    		compute_velocities(j);
	    		compute_positions(j);
	    	}
    }

	// for(int i = 0; i < N / size; i++)
	//	printf("(%d, %f, %f)  ", rank, curr_balls_x[i], curr_balls_y[i]);
	// printf("\n");

    if(rank == 0)
    {
    	wtime = MPI_Wtime() - wtime;
    	printf("[INFO]time is %lfs.\n", wtime);
    	for(int i = 0; i < N; i++)
    		printf("(%f, %f) ", all_balls_x[i], all_balls_y[i]);
    }

	return 0;
}
