#include <iostream>
#include <fstream>
#include <algorithm>
#include <ctime>
#include <queue>
#include <cstdlib>
#include <cmath>
#include <string>
#include <cstring>
#include <iomanip>
#include <set>
#include <map>
#include <stack>
#define INF 0x3F3F3F3F

using namespace std;

struct Node
{
	string state;
	int h1;
	int g;
	char move;
};
char move_path[100];
stack<Node> IDA_stack;
static string target;
static vector<Node> AStar_queue;

int get_h1(string state)
{
	int wrong_num = 0;
	for(int i = 0;i < 25;i++)
		if(state[i] != target[i] && state[i] != 'A')
			wrong_num += 1;
	return wrong_num;
}


void get_NextState(const Node curr_node, char last_move)
{
	string curr_state = curr_node.state;
	int pos = (int)curr_state.find_first_of('A');

	if(pos > 4 && pos != 16 && pos != 18 && last_move != 'D')
	{
		Node next_node = curr_node;

		next_node.state[pos - 5] = 'A';
		next_node.state[pos] = curr_state[pos - 5];
		next_node.g ++;
		if(curr_state[pos - 5] == target[pos - 5])
			next_node.h1 ++;
		if(curr_state[pos - 5] == target[pos])
		{
			// cout << 'U' << endl;
			next_node.h1 --;
		}
		next_node.move = 'U';
		IDA_stack.push(next_node);
	}

	if(pos < 20 && pos != 6 && pos != 8 && last_move != 'U')
	{
		Node next_node = curr_node;

		next_node.state[pos + 5] = 'A';
		next_node.state[pos] = curr_state[pos + 5];
		next_node.g ++;
		if(curr_state[pos + 5] == target[pos + 5])
			next_node.h1 ++;
		if(curr_state[pos + 5] == target[pos])
		{
			// cout << 'D' << "***" << curr_state[pos + 5] <<endl;
			next_node.h1 --;
		}
		next_node.move = 'D';
		IDA_stack.push(next_node);
	}

	if(pos % 5 > 0 && last_move != 'R')
	{
		Node next_node = curr_node;

		if(pos == 14 || pos == 12)
		{
			next_node.state[pos - 2] = 'A';
			next_node.state[pos] = curr_state[pos - 2];	

			if(curr_state[pos - 2] == target[pos - 2])
				next_node.h1 ++;
			if(curr_state[pos - 2] == target[pos])
				next_node.h1 --;	
		}
		else
		{
			next_node.state[pos - 1] = 'A';
			next_node.state[pos] = curr_state[pos - 1];	

			if(curr_state[pos - 1] == target[pos - 1])
				next_node.h1 ++;
			if(curr_state[pos - 1] == target[pos])
			{
				// cout << 'L' << endl;
				next_node.h1 --;				
			}
		}

		next_node.g ++;
		next_node.move = 'L';
		IDA_stack.push(next_node);

	}

	if(pos % 5 < 4 && last_move != 'L')
	{
		Node next_node = curr_node;

		if(pos == 10 || pos == 12)
		{
			next_node.state[pos + 2] = 'A';
			next_node.state[pos] = curr_state[pos + 2];

			if(curr_state[pos + 2] == target[pos + 2])
				next_node.h1 ++;
			if(curr_state[pos + 2] == target[pos])
				next_node.h1 --;			
		}
		else
		{
			next_node.state[pos + 1] = 'A';
			next_node.state[pos] = curr_state[pos + 1];	

			if(curr_state[pos + 1] == target[pos + 1])
				next_node.h1 ++;
			if(curr_state[pos + 1] == target[pos])
			{
				next_node.h1 --;		
			}
			// cout << "R>>" << next_node.h1 << endl;
		}

		next_node.g ++;
		next_node.move = 'R';
		IDA_stack.push(next_node);

	}

}

int IDAStar_search()
{
	Node start_state = AStar_queue[0];
	// start_state.move = '#';
	char last_move = '#';
	int d_limit = start_state.h1 + start_state.g;
	cout << start_state.state << endl;
	while(d_limit < INF)
	{
		int next_d_limit = INF;

		IDA_stack.push(start_state);
		int k = 0;
		last_move = '#';
		cout << d_limit << endl;

		while(!IDA_stack.empty())
		{

			Node temp_node = IDA_stack.top();
			IDA_stack.pop();

			int d_temp_node = temp_node.h1 + temp_node.g;

			if(d_temp_node > d_limit)
				next_d_limit = (next_d_limit < d_temp_node) ? next_d_limit : d_temp_node;
			else
			{
			    if(temp_node.h1 == 0)
				{
					move_path[temp_node.g] = temp_node.move;
					return temp_node.g;
				}

				k++;
				if(temp_node.move != '#')
					last_move = temp_node.move;
				get_NextState(temp_node, last_move);

			}
			move_path[temp_node.g] = last_move;
		}
		// cout << "k = " << k << endl;
		d_limit = next_d_limit;
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

	for(int i = 0;i < 25;i++)
	{
		f1 >> a;
		f2 >> b;
		state += (char)(a + 65);
		target += (char)(b + 65);
	}

	root.state = state;
	root.h1 = get_h1(state);
	root.g = 0;
	root.move = '#';
	AStar_queue.push_back(root);
	f1.close();
	f2.close();
}

int main(int argc, char const *argv[])
{
	fstream f;
	clock_t start, end;
	double totaltime;

	cout << "[INFO] IDA* Search based on h1 gets started." << endl;
	cout << "[INFO] Loading input files..." << endl;
	load_input();

	cout << "[INFO] IDA* Search executing..." << endl;
	start = clock();
	int result = IDAStar_search();
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
		f.open("output_IDAh1.txt", ios::out);
		f.setf(ios::fixed);
		f << setprecision(10) << totaltime << endl;
		for(int i = 0;i <= result;i++)
			if(move_path[i] != '#')
			{
				k++;
				cout << move_path[i];
				f << move_path[i];
			}
		cout << ", steps:" << k << endl;
		cout << "[TIME] " << totaltime << endl;
  	    f << endl << k << endl;
		f.close();
	}
	return 0;
}