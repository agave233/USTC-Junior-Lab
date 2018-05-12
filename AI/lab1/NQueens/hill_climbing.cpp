#include <iostream>
#include <fstream>
#include <string>
#include <iomanip>
#include <ctime>
#include <cstdlib>
#include <cmath>
#include <vector>
#include <sys/timeb.h>
#define MAX_TIMES 50000

using namespace std;
int64_t m, n;
int64_t count;
vector<int64_t> queen_state;
vector<int64_t> diag1_nums;
vector<int64_t> diag2_nums;

void exchange(int a, int b)
{
	int temp = queen_state[a];
	queen_state[a] = queen_state[b];
	queen_state[b] = temp; 
}

int64_t conflict() {
    if (n < 100)
        return n;
    else if (n < 1000)
        return 30;
    else if (n < 10000)
        return 50;
    else if (n < 100000)
        return 80;
    else
        return 100;
}

void calcu_count()
{
	for(int i = 0;i < 2 * n - 1;i++)
	{
		diag1_nums[i] = 0;
		diag2_nums[i] = 0;
	}

	for(int i = 0;i < n;i++)
	{
		diag2_nums[i - queen_state[i] + n - 1] ++;
		diag1_nums[i + queen_state[i]] ++;		
	}

	for(int i = 0;i < 2 * n - 1;i++)
		count += (diag1_nums[i] * (diag1_nums[i] - 1) + diag2_nums[i] * (diag2_nums[i] - 1)) / 2;
}

void random_init_state()
{
	count = 0;
	for(int i = 0;i < n;i++)
		queen_state[i] = i;

	int64_t t = (1 + sqrt(1 + 8 * m)) / 2;
	int64_t ex_m = m - (t * (t - 1)) / 2;

	int con_num = conflict();
	if(ex_m > con_num)
		con_num = ex_m + sqrt(ex_m);

	int i, j, r, bound = n - t - con_num;

	// cout << t << " " << ex_m << " " << n - t << " " << n - t - bound << endl;
	for(int i = 0;i < 2 * n - 1;i++)
	{
		diag1_nums[i] = 0;
		diag2_nums[i] = 0;
	}

	struct timeb timeSeed;
	ftime(&timeSeed);
	srand(timeSeed.time * 1000 + timeSeed.millitm);
	// srand((unsigned)time(NULL));
    for (i = 0, j = n - t; i < bound; i++, j--) 
    {
        do {
            r = i + rand() % j;
        } while (diag2_nums[i - queen_state[r] + n - 1] > 0 || diag1_nums[i + queen_state[r]] > 0);
       	
		exchange(i, r);
        diag2_nums[i - queen_state[i] + n - 1] ++;
        diag1_nums[i + queen_state[i]] ++;
    }
    // cout << bound << " " << n - t - bound << " " << n << endl;

    for (i = max(bound, 0), j = n - t - bound; i < n - t; i++, j--) 
    {
        r = i + rand() % j;
		exchange(i, r);
    }


	calcu_count();

}

void update_diag(int i, int j)
{
	diag1_nums[i + queen_state[i]] --;
	diag1_nums[j + queen_state[j]] --;
	diag1_nums[i + queen_state[j]] ++;
	diag1_nums[j + queen_state[i]] ++;

	diag2_nums[i - queen_state[i] + n - 1] --;
	diag2_nums[j - queen_state[j] + n - 1] --;
	diag2_nums[i - queen_state[j] + n - 1] ++;
	diag2_nums[j - queen_state[i] + n - 1] ++;
}


bool get_best_swap()
{
	int64_t temp_i, temp_j, curr_count, min_count = count, temp_count = count;
	for(int64_t i = 0;i < n;i++)
	{
		// 优化 1
		if(diag1_nums[i + queen_state[i]] == 1 && diag2_nums[i - queen_state[i] + n - 1] == 1)
			continue;
		for(int64_t j = i + 1;j < n;j++)
		{
			curr_count = count;
			// cout << i << "," << j << "," << count << endl;
			curr_count -= diag1_nums[i + queen_state[i]] + diag2_nums[i - queen_state[i] + n - 1] + \
					 	  diag1_nums[j + queen_state[j]] + diag2_nums[j - queen_state[j] + n - 1] - 4; 
			if(abs(queen_state[i] - queen_state[j]) == j - i)
				curr_count += 2;
			curr_count += diag1_nums[i + queen_state[j]] + diag2_nums[i - queen_state[j] + n - 1] + \
					 	  diag1_nums[j + queen_state[i]] + diag2_nums[j - queen_state[i] + n - 1];
			if(curr_count < min_count && curr_count >= m)
			{
				temp_i = i;
				temp_j = j;
				min_count = curr_count;
				update_diag(temp_i, temp_j);
				exchange(temp_i, temp_j);
				count = min_count;
			}
		}
	}
	if(temp_count > count)
		return true;
	return false;
}

void show_queen()
{
	cout << "count:" << count << endl;
	for(int i = 0;i < n;i++)
		cout << queen_state[i] << " ";
	cout << endl;
	for(int i = 0;i < n;i++)
	{
		for(int j = 0;j < n;j++)
		{
			if(queen_state[j] == i)
				cout << "Q ";
			else
				cout << ". ";
		}
		cout << endl;
	}
}

bool hill_climbing()
{
	bool success = false;
	int k = 1;
	while(true)
	{
		if(count == m)
			return true;
		// cout << "[STEP] " << k++ << ", count:" << count <<endl; 
		// if(n < 16)
		// 	show_queen();
		success = get_best_swap();
		if(!success)
			return false;
	}
}


int main(int argc, char const *argv[])
{
	fstream fin, fout;
	clock_t start, end;
	double totaltime;
	bool success = false;

	cout << "[INFO] hill_climbing for n queens gets started." << endl;
	cout << "[INFO] Loading input files..." << endl;
	fin.open("input.txt", ios::in);
	fout.open("output_hill_climbing.txt", ios::out);
	if(!fin || !fout)
	{
		cout << "[ERROR] cannot open file!" << endl;
		return -1;
	}

	fin >> n;
	fin >> m;
	if(n < 4 || n > 1000000 || m > n * (n - 1) / 2)
	{
		cout << "[ERROR] wrong input of n(4~1000000) or m > " << n * (n - 1) / 2 <<endl;
		return -1;

	}
	queen_state = vector<int64_t>(n, -1);
	diag1_nums = vector<int64_t>(2 * n - 1, -1);
	diag2_nums = vector<int64_t>(2 * n - 1, -1);

	cout << "[INFO] executing hill climbing algorithm..." << endl;
	start = clock();
	int k = 0;
	while(!success && k < MAX_TIMES)
	{
		do {
			random_init_state();
			// cout << "[INFO] count: " << count << endl;
		} while(count < m);
		// show_queen();
		k ++;
		success = hill_climbing();
	}

	if(!success)
	{
		cout << "[ERROR] cannot find a solution!" << endl;
		return 0;
	}

	end = clock();
	totaltime = (double)(end - start) / CLOCKS_PER_SEC;

	cout << "[INFO] N Queens done！Writing to file..." << endl;
	for(int64_t i = 0;i < n;i++)
		fout << queen_state[i] << endl;
	fout << setprecision(10) << totaltime * 1000 << "ms" << endl;
	// if(n < 16)
	// 	show_queen();
	count = 0;
	calcu_count();
	cout << "[TIME] " << totaltime * 1000 << "ms" << endl;
	cout << "[CHECK] final attack counts:" << count << endl;
	fin.close();
	fout.close();
	return 0;
}