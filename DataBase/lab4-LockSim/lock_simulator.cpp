#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <map>
#include <set>
#include <queue>
#include <iomanip>

using namespace std;
vector<string> input;
vector<string> output;
vector<string> inst;

struct target  
{  
    string name;  
    string xlock_trans;  
    queue<string> xlock_trans_queue;  
    set<string> slock_set;  
};   
struct transaction  
{  
    string name;  
    set<target*> lock_set;  
};  

class LockSim {  
public:     
    map<string, target*> target_table;   
    map<string, transaction*> trans_table;
  
public:  
    LockSim(){}  

    string sim_run(vector<string>& inst)  
    {  
        string res = "";
        //  Start or End 
        if(inst.size() == 2)  
        { 
            map<string, transaction*>::iterator trans = trans_table.find(inst[1]);  
            // Transaction exsit
            if(trans != trans_table.end())  
            {  
                // End inst
                if(inst[0] == "End")  
                {  
                    res += "Transaction "+ inst[1] +" ended\n";  
                    // Release all locks
                    set<target*>::iterator target_p;  
                    while(trans->second->lock_set.size() != 0)  
                    {  
                        target_p = trans->second->lock_set.begin();
                        sim_unlock(trans->second, *target_p, res);  
                    }
                    // remove transaction from table
                    trans_table.erase(trans);  
                }
                else
                    res = "Wrong Inst\n";
            }  
            // Start inst
            else if(inst[0] == "Start") 
            {  
                transaction* trans_p = new transaction();  
                trans_p->name = inst[1];  
                // insert new transaction into table
                trans_table[inst[1]] = trans_p;  
                res += "Transaction " + inst[1] +" started\n";  
            }
            else
                res = "Wrong Inst\n";
        }

        // Lock or Unlock
        else
        {   
            // No this transaction
            if(trans_table.find(inst[1]) == trans_table.end())
                return "[ERROR]Transaction" + inst[1] + " doesn't exist\n";
             // insert new target into table
            if(target_table.find(inst[2]) == target_table.end())  
            {  
                target* new_target = new target();  
                new_target->name = inst[2];  
                new_target->xlock_trans = "";  
                target_table[inst[2]] = new_target;  
            }  
            // Unlock
            if (inst[0] == "Unlock")  
            {  
                // release trans->O.bj  
                sim_unlock(trans_table[inst[1]], target_table[inst[2]], res);  
            }
            // SLock or XLock
            else if(inst[0] == "SLock" || inst[0] == "XLock")
            {  
                // add new lock  
                sim_lock(inst[0], trans_table[inst[1]], target_table[inst[2]], res);  
            }
            else
                res = "[ERROR]Wrong Inst\n";
        }  
        return res;  
    }  
      
    void sim_lock(string inst_op, transaction* trans_p, target* target_p, string& res)  
    {  
        if(inst_op == "SLock")  
        {  
            // No XLock, SLock is granted
            if(target_p->xlock_trans == "")
            {
                target_p->slock_set.insert(trans_p->name);  
                trans_p->lock_set.insert(target_p);  
                res += "S-Lock granted\n";  
            }
            // XLock exists, SLock waiting
            else  
            {
                target_p->slock_set.insert(trans_p->name);  
                res += "Waiting for lock (X-lock held by: " + target_p->xlock_trans +")\n";  
            }  
        }

        else if(inst_op == "XLock")  
        {  
            // No XLock
            if(target_p->xlock_trans == "")  
            {
                int shareNum = target_p->slock_set.size();  
                if(shareNum > 1)
                {
                    string sTemp = "";
                    for(set<string>::iterator it_index = target_p->slock_set.begin();  
                        it_index != target_p->slock_set.end(); it_index++)  
                    {
                        sTemp += " " + *it_index;
                    }
                    target_p->xlock_trans_queue.push(trans_p->name);  
                    res += "Waiting for lock (S-lock held by:" + sTemp + "\n";  
                }

                else if(shareNum == 1)  
                {  
                    // update
                    if(*(target_p->slock_set.begin()) == trans_p->name)  
                    {  
                        target_p->xlock_trans = trans_p->name;  
                        target_p->slock_set.clear();  
                        res += "Upgrade to XLock granted\n";  
                    }  
                    else
                    {
                        target_p->xlock_trans_queue.push(trans_p->name);  
                        res += "Waiting for lock (S-lock held by:" + *(target_p->slock_set.begin()) + ")\n";  
                    }
                }

                else if(shareNum == 0)  
                {  
                    target_p->xlock_trans = trans_p->name;  
                    trans_p->lock_set.insert(target_p);  
                    res += "XLock granted\n";  
                }  
            }
            // XLock exists, XLock waiting
            else
            {  
                target_p->xlock_trans_queue.push(trans_p->name);  
                res += "Waiting for lock (X-lock held by: "+ target_p->xlock_trans +")\n";  
            }  
        }  
    }  
      
    void sim_unlock(transaction* trans_p, target* target_p, string& res)  
    {  
        if(target_p->xlock_trans != "")  
        {  
            if (target_p->xlock_trans == trans_p->name)  
            {  
                target_p->xlock_trans = "";  
                trans_p->lock_set.erase(target_p);
                res += "Lock released\n";  
            }  
            else  
            {  
                res += "I can not find the transaction.\n";  
            }  
        } 
        else   
        {  
            set<string>::iterator shareIndex = target_p->slock_set.find(trans_p->name);  
            if(shareIndex != target_p->slock_set.end())  
            {  
                target_p->slock_set.erase(shareIndex);  
                trans_p->lock_set.erase(target_p);  
                res += "Lock released\n";  
            }  
            else  
            {  
                res += "I can not find the transaction.\n";  
            }  
        }

        // FIFO and XLock takes precedence
        int flag = 0;
        if(target_p->xlock_trans_queue.size() != 0)  
        {  
            string s = "";
            while(!target_p->xlock_trans_queue.empty())
            {
                s = target_p->xlock_trans_queue.front();
                target_p->xlock_trans_queue.pop();
                if(trans_table.find(s) != trans_table.end())
                    break;
                s = "";
            }

            if(s != "")
            {
                target_p->xlock_trans = s;
                res += "X-Lock on "+ target_p->name +" granted to "+ target_p->xlock_trans +"\n";  
                flag = 1;
            }
        }

        if(target_p->slock_set.size() != 0 && flag == 0)  
        {  
            string temp = "";  
            for(set<string>::iterator it_index = target_p->slock_set.begin();  
                it_index != target_p->slock_set.end(); it_index++)  
            {  
                temp += " " + *it_index;  
            }  
            res += "S-Lock on "+ target_p->name +" granted to "+ temp +"\n";  
        }  
    } 
};

LockSim sim;

void print_table()
{
    for(int i = 0;i < output.size();i++)
    {
        cout << "[" << i << "]" << left << setw(12) << input[i];

	    string temp = "";
	    int k = 0;
	    for(int j = 0;j < output[i].size();j++)
	    {
	        if(output[i][j] == '\n')
	        {
	        	if(k == 0)
	        		cout << "  " << temp << endl;
	        	else
	        		cout << "                 " << temp << endl;
	            k = 1;
	            temp = "";
	            continue;
	        }
	        temp += output[i][j];
	    }
    }
}

void get_inst(string str)
{
    string temp = "";
    for(int i = 0;i < str.size();i++)
    {
        if(str[i] == ' ')
        {
            inst.push_back(temp);
            temp = "";
            continue;
        }
        temp += str[i];
    }

    inst.push_back(temp);
}

void print_info()
{
	if(inst[0] == "PrintLock")
	{
		map<string, transaction*>::iterator trans = sim.trans_table.find(inst[1]);
        if(trans == sim.trans_table.end())
        {
            cout << "[ERROR]Transaction " + inst[1] + " doesn't exist\n";
        	return;
        }

        set<target*>::iterator target_p = trans->second->lock_set.begin();
        cout << "[INFO]Transaction " << inst[1] << " all targets:";
	    while(target_p != trans->second->lock_set.end())  
	    {  
	        cout << (*target_p)->name << "  ";  
	        ++target_p;
	    }
	    cout << endl;
	}

	if(inst[0] == "PrintSLock")
	{
		map<string, target*>::iterator tar = sim.target_table.find(inst[1]);
        if(tar == sim.target_table.end())
        {
            cout << "[ERROR]Target " + inst[1] + " doesn't exist\n";
        	return;
        }

        set<string>::iterator slock_p = tar->second->slock_set.begin();
        cout << "[INFO]Target " << inst[1] << " all Transactions who share/wait this SLock:";
	    while(slock_p != tar->second->slock_set.end())  
	    {  
	        cout << *slock_p << "  ";  
	        ++slock_p;
	    }
	    cout << endl;
	}
}

int main(int argc, char const *argv[])
{
    /* code */
    string str;

    // input
    cout << "[info]Please input instructions, shut down with \"exit\" instruction\n";
    while(true)
    {
        inst.clear();
        cout << ">>> ";
        getline(cin, str);
        if(str == "Exit")
             break;
    	else if(str == "PrintAll")
    		print_table();
    	else if(str != "")
    	{
  			get_inst(str);

  			if(inst[0] == "PrintLock" || inst[0] == "PrintSLock")
  				print_info();
  			else
  			{
	        	input.push_back(str);
	        	string out = sim.sim_run(inst);
	        	output.push_back(out);
	        	cout << out;
  			}
	    }
    }
    
    return 0;
}