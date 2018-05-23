#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char *argv[]) 
{	  
    if(argc != 3)
    {
	printf("[ERROR]para wrong!\n");
	return -1;
    }

    // clock_t start, end;
    double wtime;

    int i; 	  
    int NUM_THREADS = atoi(argv[1]);
    long num_steps = atoi(argv[2]);
    double pi, sum[NUM_THREADS];  

    // start = clock();
    wtime = omp_get_wtime();
    omp_set_num_threads(NUM_THREADS); 
    #pragma omp parallel 
    {	  
	double x;     
	int id; 
	id = omp_get_thread_num();       
	sum[id] = 0; 
	#pragma omp for
	for (i = 0;i < num_steps; i++)
	{  
	    x = (i + 0.5) / (double)num_steps;
	    sum[id] += 4.0 / (1.0 + x*x); 
        } 
    }
    
    for(i = 0, pi = 0.0;i < NUM_THREADS;i++)
	pi += sum[i];

    pi /= (double)num_steps;
    wtime = omp_get_wtime() - wtime;
    // end = clock();
    // cost_time = (double)(end - start) / CLOCKS_PER_SEC;
    printf("[INFO]Use OMP.PI is %lf, time is %lfs.\n", pi, wtime);
    return 0;
} 

