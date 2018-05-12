#include <iostream>
#include <fstream>
#include <algorithm>
#include <ctime>
#include <queue>
#include <cstdlib>
#include <cmath>
#include <string>
#include <iomanip>
#include <set>

using namespace std;

struct Node
{
	string state;
	int h2;
	int g;
	char move;
	friend bool operator < (Node a, Node b)
	{
		// 定义估计代价小的节点优先级高
		return a.h2 + a.g >= b.h2 + b.g;
	}
};

static string target;
static priority_queue<Node> AStar_queue;
static set<string> visited;


int target_row[22];
int target_column[22];
int column_check[5][5] = {{0, 0, 1, 1, 2}, 
						  {0, 0, 0, 0, 1},
						  {1, 0, 0, 0, 1},
					   	  {1, 0, 0, 0, 0}, 
					   	  {2, 1, 1, 0, 0}};

int row_check[5][5] = {{0, 0, 0, 2, 2}, 
					   {0, 0, 0, 2, 2},
					   {0, 0, 0, 0, 0},
					   {2, 2, 0, 0, 0}, 
					   {2, 2, 0, 0, 0}};			   

char move_path[100];

int get_h2(string state)
{
	int dis = 0, r1, c1, r2, c2;
	for(int i = 0;i < 25;i++)
		if(state[i] != '@' && state[i] != 'A')
		{
			int pos = target.find(state[i]);
			r1 = pos / 5;
			c1 = pos % 5;
			r2 = i / 5;
			c2 = i % 5;
			dis += abs(r1 - r2) + abs(c1- c2);
			if((r1 <= 2 && r2 >= 2) || (r1 >= 2 && r2 <= 2))
				dis -= column_check[c1][c2];
			if((c1 == 1 && c2 == 1) || (c1 == 3 && c2 == 3))
				dis += row_check[r1][r2];
		}
	// cout << dis << endl;
	return dis;
}


void get_NextState(const Node curr_node, char last_move)
{
	string curr_state = curr_node.state;
	int pos = (int)curr_state.find_first_of('A');
    int r1 = pos / 5;
	int c1 = pos % 5;

	if(pos > 4 && pos != 16 && pos != 18 && last_move != 'D')
	{
		Node next_node ;
		int r2 = target_row[(int)curr_state[pos - 5] - 66];
		int c2 = target_column[(int)curr_state[pos - 5] - 66];
		next_node.state = curr_state;
		next_node.h2 = curr_node.h2;
		// cout << "U>>" << next_node.h2 << endl;

		next_node.state[pos - 5] = 'A';
		next_node.state[pos] = curr_state[pos - 5];
		next_node.g = curr_node.g + 1;

		if(visited.find(next_node.state) == visited.end())
		{

			if(r1 - 1 >= r2)
				next_node.h2 ++;
			else
				next_node.h2 --;
			if(r1 == 2 && r2 < 2)
				next_node.h2 -= column_check[c1][c2];
			if(r1 == 3 && r2 > 2)
				next_node.h2 += column_check[c1][c2];


			next_node.move = 'U';
			AStar_queue.push(next_node);
		}

	}

	if(pos < 20 && pos != 6 && pos != 8 && last_move != 'U')
	{
		Node next_node;
		int r2 = target_row[(int)curr_state[pos + 5] - 66];
		int c2 = target_column[(int)curr_state[pos + 5] - 66];
		next_node.state = curr_state;
		next_node.h2 = curr_node.h2;
		// cout << "D>>" << next_node.h2 << endl;

		next_node.state[pos + 5] = 'A';
		next_node.state[pos] = curr_state[pos + 5];
		if(visited.find(next_node.state) == visited.end())
		{
			next_node.g = curr_node.g + 1;

			if(r1 + 1 <= r2)
				next_node.h2 ++;
			else
				next_node.h2 --;
			if(r1 == 2 && r2 > 2)
				next_node.h2 -= column_check[c1][c2];
			if(r1 == 1 && r2 < 2)
				next_node.h2 += column_check[c1][c2];

			next_node.move = 'D';
			AStar_queue.push(next_node);
		}
	}

	if(c1 > 0 && last_move != 'R')
	{
		Node next_node;
		next_node.state = curr_state;
		next_node.h2 = curr_node.h2;
		// cout << "L>>" << next_node.h2 << endl;
		if(pos == 14 || pos == 12)
		{
			int r2 = target_row[(int)curr_state[pos - 2] - 66];
			int c2 = target_column[(int)curr_state[pos - 2] - 66];
			next_node.state[pos - 2] = 'A';
			next_node.state[pos] = curr_state[pos - 2];	

			if(c1 - 2 >= c2)
				next_node.h2 ++;
			if(c1 <= c2)
				next_node.h2 --;
		}
		else
		{
			int r2 = target_row[(int)curr_state[pos - 1] - 66];
			int c2 = target_column[(int)curr_state[pos - 1] - 66];
			next_node.state[pos - 1] = 'A';
			next_node.state[pos] = curr_state[pos - 1];	

			if(c1 - 1 >= c2)
				next_node.h2 ++;
			else
				next_node.h2 --;

			if((r1 <= 2 && r2 >= 2) || (r1 >= 2 && r2 <= 2))
				next_node.h2 -=  column_check[c1][c2] - column_check[c1 - 1][c2];
			
			if((c1 == 1 && c2 == 1) || (c1 == 3 && c2 == 3))
				next_node.h2 += row_check[r1][r2];
			if((c1 == 2 && c2 == 1) || (c1 == 4 && c2 == 3))
				next_node.h2 -= row_check[r1][r2];


		}
		if(visited.find(next_node.state) == visited.end())
		{
			next_node.g = curr_node.g + 1;
			next_node.move = 'L';
			AStar_queue.push(next_node);
		}

	}

	if(c1 < 4 && last_move != 'L')
	{
		Node next_node;
		next_node.state = curr_state;
		next_node.h2 = curr_node.h2;
		// cout << "R>>" << next_node.h2 << endl;
		if(pos == 10 || pos == 12)
		{
			int r2 = target_row[(int)curr_state[pos + 2] - 66];
			int c2 = target_column[(int)curr_state[pos + 2] - 66];
			next_node.state[pos + 2] = 'A';
			next_node.state[pos] = curr_state[pos + 2];

			if(c1 >= c2)
				next_node.h2 --;
			if(c1 + 2 <= c2)
				next_node.h2 ++;	
		}
		else
		{
			int r2 = target_row[(int)curr_state[pos + 1] - 66];
			int c2 = target_column[(int)curr_state[pos + 1] - 66];
			next_node.state[pos + 1] = 'A';
			next_node.state[pos] = curr_state[pos + 1];	

			if(c1 + 1 <= c2)
				next_node.h2 ++;
			else
				next_node.h2 --;
			if((r1 <= 2 && r2 >= 2) || (r1 >= 2 && r2 <= 2))
			next_node.h2 -=  column_check[c1][c2] - column_check[c1 + 1][c2];

			// if(c1 == 1 || c1 == 3)
			if((c1 == 1 && c2 == 1) || (c1 == 3 && c2 == 3))
				next_node.h2 += row_check[r1][r2];
			if((c1 == 0 && c2 == 1) || (c1 == 2 && c2 == 3))
				next_node.h2 -= row_check[r1][r2];
			// cout << "R>>" << next_node.h2 << endl;
		}

		if(visited.find(next_node.state) == visited.end())
		{
			next_node.g = curr_node.g + 1;
			next_node.move = 'R';
			AStar_queue.push(next_node);
		}
	}

}

int AStar_search()
{
	Node temp_node;
	char last_move = '#';

	while(!AStar_queue.empty())
	{
		temp_node = AStar_queue.top();
		AStar_queue.pop();
		if(temp_node.h2 == 0)
		{
			move_path[temp_node.g] = temp_node.move;
			return temp_node.g;
		}

		// cout << "debug a " << endl;
		vector<string> states;
		visited.insert(temp_node.state);

		if(temp_node.move != '#')
			last_move = temp_node.move;
		get_NextState(temp_node, last_move);

		move_path[temp_node.g] = last_move;

	}
	return -1;
}

void load_input()
{
	Node root;
	int a, b;
	fstream f1, f2;
	string state = "";

	f1.open("input.txt", ios::in);
	f2.open("target.txt", ios::in);
	if(!f1 || !f2)
	{
		cout << "[ERROR] Open file failed!\n";
		exit(-1);
	}

	// 查询用的map
	for(int i = 0;i < 10;i++)
	{
		
		// char c = char(i + 66);
		target_row[i] = i / 5;
		target_column[i] = i % 5;
	}
	target_row[10] = 2;
	target_row[11] = 2;
	target_row[12] = 2;
	target_column[10] = 0;
	target_column[11] = 2;
	target_column[12] = 4;
	for(int i = 13;i < 22;i++)
	{
		// char c = char(i + 64);
		target_row[i] = (i + 2) / 5;
		target_column[i] = (i + 2) % 5;
	}


	for(int i = 0;i < 25;i++)
	{
		f1 >> a;
		f2 >> b;
		state += (char)(a + 65);
		target += (char)(b + 65);
	}

	root.state = state;
	root.h2 = get_h2(state);
	root.g = 0;
	root.move = '#';
	AStar_queue.push(root);
	f1.close();
	f2.close();
}

int main(int argc, char const *argv[])
{
	fstream f;
	clock_t start, end;
	double totaltime;

	cout << "[INFO] A* Search based on h2 gets started." << endl;
	cout << "[INFO] Loading input files..." << endl;
	load_input();

	cout << "[INFO] A* Search executing..." << endl;
	start = clock();
	int result = AStar_search();
	end = clock();
	totaltime = (double)(end - start) / CLOCKS_PER_SEC;
	if(result == -1)
	{
		cout << "[ERROR] Cannot find a solution!" << endl;
	}
	else
	{
		cout << "[INFO] IDA* search done! It cost " << totaltime << "s" << endl;
		cout << "[INFO] result saving..." << endl;
		cout << "[RESULT] ";
		int k = 0;
		f.open("output_Ah2.txt", ios::out);
		f.setf(ios::fixed);
		f << setprecision(10) << totaltime << endl;
		for(int i = 0;i <= result;i++)
			if(move_path[i] != '#')
			{
				k++;
				f << move_path[i];
				cout << move_path[i];
			}
		cout << ", steps:" << k << endl;
		cout << "[TIME] " << totaltime << endl;

  		f << endl << k << endl;
		f.close();
	}
	return 0;
}