#include <omp.h>
#include <math.h>
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
    double cost_time;

    int i; 	  
    int NUM_THREADS = atoi(argv[1]);
    int n = atoi(argv[2]);
    int res, count[NUM_THREADS];  

    // start = clock();
    double wtime = omp_get_wtime();
    omp_set_num_threads(NUM_THREADS); 
    #pragma omp parallel 
    {	  
	int flag, i, j;     
	int id; 
	id = omp_get_thread_num();       
	count[id] = 0; 
	#pragma omp for
    	for(i = 2;i <= n;i++)
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
                count[id] += 1;
       }


    }
    
    for(i = 0, res = 0;i < NUM_THREADS;i++)
	res += count[i];

    wtime = omp_get_wtime() - wtime;
    // printf("%lfs\n", wtime);
    
    // end = clock();
    // cost_time = (double)(end - start) / CLOCKS_PER_SEC;
    printf("[INFO]Use OMP.res = %d, time is %lfs.\n", res, wtime);
    return 0;
} 

