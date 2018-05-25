#include "stdio.h"
#include "stdlib.h"
#include "time.h"
#include "math.h"
#define BLOCK_SIZE 32
int block_size;


void generate_matrix(float *mat, int a, int b)
{
	int i, j, m, n;
	m = a * block_size;
	n = b * block_size;

	for(i = 0; i < m; i++)
		for(j = 0; j < n; j++)
			mat[i * n + j] = (float)(rand() % 100) / 10.0;
}

void serial_compute(float *A, float *B, float *C)
{
	int i, j, k, m, n;
	m = 10 * block_size;
	n = 20 * block_size;

	for(i = 0; i < m; i++)
		for(j = 0;j < n; j++)
		{
			float sum = 0;
			for(k = 0; k < m; k++)
				sum += A[i * m + k] * B[k * n + j];
			C[i * n + j] = sum;
		}
}

bool check_result(float *C1, float *C2)
{
	int m = 10 * block_size, n = 20 * block_size;
	for(int i = 0; i < m; i++)
		for(int j = 0; j < n; j++)
			if(fabs(C1[i * n + j] - C2[i * n + j]) > 1e-2)
			{
				printf("C1:%lf, C2:%lf\n", C1[i * n + j], C2[i * n + j]);
				return false;
			}

	return true;
}

__global__ void tiled_parallel_compute(float *A, float *B, float *C, int block_size)
{
	__shared__ float block_A[BLOCK_SIZE][BLOCK_SIZE];
	__shared__ float block_B[BLOCK_SIZE][BLOCK_SIZE];

	int row = blockIdx.y * BLOCK_SIZE + threadIdx.y;
	int column = blockIdx.x * BLOCK_SIZE + threadIdx.x;
	int m = 10 * block_size, n = 20 * block_size;
	int t_x = threadIdx.x, t_y = threadIdx.y;
	float sum = 0;

	for(int i = 0; i < m / BLOCK_SIZE; i++)
	{
		block_A[t_y][t_x] = A[row * m + i * BLOCK_SIZE + t_x];
		block_B[t_y][t_x] = B[(i * BLOCK_SIZE + t_y) * n + column];
		__syncthreads();

		for(int j = 0; j < BLOCK_SIZE; j++)
			sum += block_A[t_y][j] * block_B[j][t_x];
		__syncthreads();
	}

	C[row * n + column] = sum;

}

__global__ void parallel_compute(float *A, float *B, float *C, int block_size)
{
	int row = blockIdx.y * BLOCK_SIZE + threadIdx.y;
	int column = blockIdx.x * BLOCK_SIZE + threadIdx.x;
	int m = 10 * block_size, n = 20 * block_size;
	float sum = 0;

	if(row < m && column < n)
	{
		for(int i = 0; i < m; i++)
			sum += A[row * m + i] * B[i * n + column];
		C[row * n + column] = sum;
	}

}

int main(int argc, char const *argv[])
{

	float *A, *B, *C1, *C2, *CUDA_A, *CUDA_B, *CUDA_C;
	clock_t start, end;
	double t0, t1, t2;
	int m, n;

	block_size = atoi(argv[1]) / BLOCK_SIZE * BLOCK_SIZE;
	m = 10 * block_size;
	n = 20 * block_size;
	A = (float*)malloc(sizeof(float) * m * m);
	B = (float*)malloc(sizeof(float) * m * n);
	C1 = (float*)malloc(sizeof(float) * m * n);
	C2 = (float*)malloc(sizeof(float) * m * n);
	srand(time(NULL));

	generate_matrix(A, 10, 10);
	generate_matrix(B, 10, 20);

	start = clock();
	serial_compute(A, B, C1);
	end = clock();
	t0 = (((double) (end - start)) / CLOCKS_PER_SEC );
	printf("Serial algorithm costs %lfs.\n", t0);

    dim3 threads(BLOCK_SIZE, BLOCK_SIZE, 1);
    dim3 blocks(n / BLOCK_SIZE, m / BLOCK_SIZE, 1);
	cudaMalloc(&CUDA_A, sizeof(float) * m * m);
	cudaMalloc(&CUDA_B, sizeof(float) * m * n);
	cudaMalloc(&CUDA_C, sizeof(float) * m * n);
	// Copy to GPU memory
	cudaMemcpy(CUDA_A, A, m * m * sizeof(float), cudaMemcpyHostToDevice);
	cudaMemcpy(CUDA_B, B, m * n * sizeof(float), cudaMemcpyHostToDevice);
	// parallel
	start = clock();
	parallel_compute<<<blocks, threads>>>(CUDA_A, CUDA_B, CUDA_C, block_size);
	end = clock();
	cudaMemcpy(C2, CUDA_C, m * n * sizeof(float), cudaMemcpyDeviceToHost);
	t1 = ((double) (clock() - start)) / CLOCKS_PER_SEC;

	bool right = check_result(C1, C2);
	if(right)
		printf("Parallel algorithm costs %lfs, speedup is %lf, result is right.\n", t1, t0 / t1 / 10);
	else
		printf("Result is wrong.\n");

	// tiled
	start = clock();
	tiled_parallel_compute<<<blocks, threads>>>(CUDA_A, CUDA_B, CUDA_C, block_size);
	end = clock();
	cudaMemcpy(C2, CUDA_C, m * n * sizeof(float), cudaMemcpyDeviceToHost);
	t2 = ((double) (clock() - start)) / CLOCKS_PER_SEC;

	right = check_result(C1, C2);
	if(right)
		printf("Parallel tiled algorithm costs %lfs, speedup is %lf, result is right.\n", t2, t0 / t2 / 10);
	else
		printf("Result is wrong.\n");

	return 0;
}