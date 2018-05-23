#include <stdio.h>
#include <time.h>
#include <sys/timeb.h>
#include <stdlib.h>
#include <string.h>
#include <mpi.h>
#define SPEED_MAX 20
#define SLOW_P 0.15


MPI_Status status;
int rank, size;
int *all_on_road_pos;
int *car_on_road_pos;
int *car_on_road_speed;
int *search_buff;
int *search_array;
int car_num, run_time, k=1;

int cmpfunc(const void * a, const void * b)
{
   return ( *(int*)a - *(int*)b );
}

void simulate()
{

	int dis, p;
	int *item;
	for(int i = 0;i < car_num;i++)
	{

		item = (int*)bsearch(&car_on_road_pos[i], search_array, k, sizeof(int), cmpfunc);
		dis = *(item + 1);

		if(dis == 0 && car_on_road_speed[i] < SPEED_MAX)
			car_on_road_speed[i] ++;
		else if(dis > 0 && dis <= car_on_road_speed[i])
			car_on_road_speed[i] = dis - 1;

		p = rand() % 100;
		if(p < SLOW_P * 100 && car_on_road_speed[i] > 0)
			car_on_road_speed[i] --;

		car_on_road_pos[i] += car_on_road_speed[i];
	}
}


int main(int argc, char *argv[])
{
    MPI_Init (&argc, &argv);        	    
    MPI_Comm_rank (MPI_COMM_WORLD, &rank);  
    MPI_Comm_size (MPI_COMM_WORLD, &size); 
    double wtime;
    if(rank == 0)
    {
    	// Get arguments from command line.
    	if(argc != 3)
    	{
    		printf("Error arguments!\n");
    		return -1;
    	}
    	car_num = atoi(argv[1]) / size;
    	run_time = atoi(argv[2]);
    	// Send car number.
    	wtime = MPI_Wtime();
        for(int j = 1; j < size; j++)
        {
            MPI_Send(&car_num, 1, MPI_INT, j, 1, MPI_COMM_WORLD);
            MPI_Send(&run_time, 1, MPI_INT, j, 1, MPI_COMM_WORLD);
        }	
    }
    else
    {
    	MPI_Recv(&car_num, 1, MPI_INT, 0, 1, MPI_COMM_WORLD, &status);
    	MPI_Recv(&run_time, 1, MPI_INT, 0, 1, MPI_COMM_WORLD, &status);
    }

    // initial.
    car_on_road_pos = (int*)malloc(car_num *  sizeof(int));
    all_on_road_pos = (int*)malloc(car_num * size * sizeof(int));
    car_on_road_speed = (int*)malloc(car_num * sizeof(int));
    search_buff = (int*)malloc(run_time * SPEED_MAX * sizeof(int));
    search_array = (int*)malloc(run_time * SPEED_MAX * sizeof(int));
    memset(car_on_road_pos, 0, car_num * sizeof(int));
    memset(search_array, 0, run_time * SPEED_MAX * sizeof(int));
    memset(all_on_road_pos, 0, car_num * size * sizeof(int));
    memset(car_on_road_speed, 0, car_num * sizeof(int));

    srand(time(NULL) * (rank + 1) * 10);
    // simulate running.
    for(int i = 0;i < run_time;i++)
    {
    	simulate();

    	memset(search_buff, 0, run_time * SPEED_MAX *  sizeof(int));
    	MPI_Allgather(car_on_road_pos, car_num, MPI_INT, all_on_road_pos, car_num, MPI_INT, MPI_COMM_WORLD);
        k = 0;
    	for(int j = 0;j < car_num * size;j++)
    	    search_buff[all_on_road_pos[j]] ++;
    	for(int j = 0;j < run_time * SPEED_MAX;j++)
    	    if(search_buff[j] > 0)
    	        search_array[k++] = j;
    	search_array[k] = 0;
    }


    if(rank == 0)
    {
        wtime = MPI_Wtime() - wtime;
        printf("[INFO]time is %lfs.\n", wtime);

        for(int i = 0;i < run_time * SPEED_MAX;i++)
            if(search_buff[i] > 0)
                printf("%d,%d\n", i, search_buff[i]);
    }

    free(car_on_road_pos);
    free(all_on_road_pos);
    free(car_on_road_speed);
    free(search_buff);
    free(search_array);
    MPI_Finalize();
    return 0;
}
