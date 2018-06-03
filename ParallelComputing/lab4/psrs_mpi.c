#include <stdlib.h>
#include <stdio.h>
#include <limits.h>
#include <assert.h>
#include <sys/time.h>
#include <unistd.h>
#include "mpi.h"

MPI_Status status;

int array_size, sub_array_size;
int rank, size;
int start, end;
int *my_array;
int *sorted_array;
int *sample_array;
int *partition_sizes;
int *new_partition_sizes;
int *new_sub_array;


int cmp(const void * a, const void * b)
{
    if (*(int*)a < *(int*)b) return -1;
    if (*(int*)a > *(int*)b) return 1;
    else return 0;
}

void regular_sample()
{
    // local qsort
    qsort(my_array + start, sub_array_size, sizeof(my_array[0]), cmp);
    // regular sample
    for(int i = 0; i < size; i++) 
        sample_array[i] = my_array[start + (i * (array_size / (size * size)))];    
}

void pivots_partition() 
{
    int *all_sample_array = (int *)malloc(size * size * sizeof(sample_array[0]));
    int *sample_pivots = (int*)malloc((size - 1) * sizeof(sample_array[0]));          
    int index = 0;

    // Gather samples
    MPI_Gather(sample_array, size, MPI_INT, all_sample_array, size, MPI_INT, 0, MPI_COMM_WORLD);       
    if(rank == 0)
    {
        qsort(all_sample_array, size * size, sizeof(sample_array[0]), cmp);
        for(int i = 0; i < (size - 1); i++)
            sample_pivots[i] = all_sample_array[(((i + 1) * size) + (size / 2)) - 1];
    
    }
    // Bcast pivots
    MPI_Bcast(sample_pivots, size - 1, MPI_INT, 0, MPI_COMM_WORLD);
    // Partitions
    for (int i = 0; i < sub_array_size; i++)
    {
        if(my_array[start + i] > sample_pivots[index])
            index += 1;

        if (index == size)
        {
            // the last partition
            partition_sizes[size - 1] = sub_array_size - i + 1;
            break;
        }
        partition_sizes[index]++ ;   
    }
    free(all_sample_array);
    free(sample_pivots);
}

void partitions_exchange()
{
    int new_sub_array_size = 0;
    int *sdispls = (int*)malloc(size * sizeof(int));
    int *rdispls = (int*)malloc(size * sizeof(int));

    MPI_Alltoall(partition_sizes, 1, MPI_INT, new_partition_sizes, 1, MPI_INT, MPI_COMM_WORLD);
     // calculate the size of the new sub_arrray and allocate space.
    for(int i = 0; i < size; i++) 
        new_sub_array_size += new_partition_sizes[i];

    new_sub_array = (int*)malloc(new_sub_array_size * sizeof(int));

    // calculate offsets
    sdispls[0] = 0;
    rdispls[0] = 0;
    for(int i = 1; i < size; i++)
    {
        sdispls[i] = partition_sizes[i - 1] + sdispls[i - 1];
        rdispls[i] = new_partition_sizes[i - 1] + rdispls[i - 1];
    }

    // communicate
    MPI_Alltoallv(&(my_array[start]), partition_sizes, sdispls, MPI_INT, new_sub_array, new_partition_sizes, rdispls, MPI_INT, MPI_COMM_WORLD);
    free(sdispls);
    free(rdispls);
    return;
}

void partition_merge()
{
    int *sorted_sub_array;
    int *rdispls, *partitions_start, *partitions_end, *sub_array_sizes, sub_array_size;

    partitions_start = (int*)malloc(size * sizeof(int));
    partitions_end = (int*)malloc(size * sizeof(int));
    partitions_start[0] = 0;
    sub_array_size = new_partition_sizes[0];

    for(int i = 1; i < size; i++)
    {
        sub_array_size += new_partition_sizes[i];
        partitions_start[i] = partitions_start[i - 1] + new_partition_sizes[i - 1];
        partitions_end[i - 1] = partitions_start[i];
    }
    partitions_end[size - 1] = sub_array_size;

    sorted_sub_array = (int*)malloc(sub_array_size * sizeof(int));
    sub_array_sizes = (int*)malloc(size * sizeof(int));
    rdispls = (int*)malloc(size * sizeof(int));

    // merge sort locally
    for(int i = 0; i < sub_array_size; i++)
    {
        int min_value = INT_MAX;
        int min_index;
        for(int j = 0; j < size; j++)
        {
            if((partitions_start[j] < partitions_end[j]) && (new_sub_array[partitions_start[j]] < min_value))
            {
                min_value = new_sub_array[partitions_start[j]];
                min_index = j;
            }
        }
        sorted_sub_array[i] = min_value;
        partitions_start[min_index] += 1;
    }

    MPI_Gather(&sub_array_size, 1, MPI_INT, sub_array_sizes, 1, MPI_INT, 0, MPI_COMM_WORLD);

    // calculate offsets
    if(rank == 0)
    {
        rdispls[0] = 0;
        for (int i = 1; i < size; i++)
            rdispls[i] = sub_array_sizes[i - 1] + rdispls[i - 1];
    }

    MPI_Gatherv(sorted_sub_array, sub_array_size, MPI_INT, my_array, sub_array_sizes, rdispls, MPI_INT, 0, MPI_COMM_WORLD);

    free(partitions_end);
    free(sorted_sub_array);
    free(partitions_start);
    free(sub_array_sizes);
    free(rdispls);
}

int check_result()
{
    qsort(sorted_array, array_size, sizeof(my_array[0]), cmp);
    for(int i = 0; i < array_size; i++)
    if(sorted_array[i] != my_array[i])
        return 0;
    return 1;
}
int main(int argc, char *argv[])
{
    double wtime;
    MPI_Init(&argc, &argv);  
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    if(rank == 0)
    {
        array_size = atoi(argv[1]);

        wtime = MPI_Wtime();
        for(int j = 1; j < size; j++)
          MPI_Send(&array_size, 1, MPI_INT, j, 1, MPI_COMM_WORLD);
    }
    else
        MPI_Recv(&array_size, 1, MPI_INT, 0, 1, MPI_COMM_WORLD, &status);


    my_array = (int*)malloc(array_size * sizeof(int));
    sorted_array = (int*)malloc(array_size * sizeof(int));
    // initial array
    srand(array_size * 10);
    for(int i = 0; i < array_size; i++) 
    {
        my_array[i] = rand() % (array_size * 10);
        sorted_array[i] = my_array[i];
    }

    sample_array = (int*)malloc(size * sizeof(int));
    partition_sizes = (int*)malloc(size * sizeof(int));
    new_partition_sizes = (int*)malloc(size * sizeof(int));
    for(int i = 0; i < size; i++)
        partition_sizes[i] = 0;

    // calculate the start and size of sub_array
    start = rank * array_size / size;
    if(size == (rank + 1))
        end = array_size;
    else
        end = (rank + 1) * array_size / size;

    sub_array_size = end - start;

    MPI_Barrier(MPI_COMM_WORLD);
    // start executing psrs sort
    regular_sample();
    if(size > 1)
    {
        pivots_partition();
        partitions_exchange();
        partition_merge();
    }

    wtime = MPI_Wtime() - wtime;

    if(rank == 0 && array_size < 100)
    {
        for(int i = 0; i < array_size; i++)
            printf("%d ",my_array[i]);
        printf("\n");
    }
    if(rank == 0)
    {
        printf("[INFO]time is %lfs.\n", wtime);
        if(check_result() == 1)
        printf("[INFO]sorted result is right.\n");
        else
        printf("[ERROR]sorted result is wrong.\n");
    }
    if(size > 1)
        free(new_sub_array);
    free(partition_sizes);
    free(new_partition_sizes);
    free(sample_array);
    free(my_array);

    MPI_Finalize();;       
    return 0;
}
