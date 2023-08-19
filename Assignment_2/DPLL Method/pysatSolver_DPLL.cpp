#include <bits/stdc++.h>
using namespace std;
typedef long long int ll;
vector<vector<ll>> encoding; // encoding[i] represents the ith clause, encoding[i][j] represents the jth literal of the ith clause

vector<ll> model ; // stores the current model
ll propositions,clauses; // total number of propositions and clauses

ll randomNumGen (ll from, ll to){

    ll range_from  = from;
    ll range_to    = to;
    random_device rand_dev;
    mt19937 generator(rand_dev());
    uniform_int_distribution<int> distr(range_from, range_to);
    return distr(generator);
}

// Function to take input and store it as vector of vectors (in 'encoding')
void readCNF (){   //tested -> ok

   

    string data;
    ifstream f;
    f.open("dimacsEncoding.cnf");
    while(1){
        getline(f,data);
        if(data[0]=='p')//First line of the encoding.
        {
            istringstream iss(data);
            vector<string> results((istream_iterator<string>(iss)), istream_iterator<string>());
            propositions = stoi(results[2]);
            clauses = stoi(results[3]);
            break;
        }
    }
    vector<vector<ll>> temp(clauses);
    for(ll i=0;i<clauses;i++){
        getline(f,data);
        istringstream iss(data);
        vector<string> results((istream_iterator<string>(iss)), istream_iterator<string>());
        ll l = results.size();
        for(ll j=0;j<l-1;j++){
            temp[i].push_back(stoi(results[j]));
        }
    }
    f.close();
    encoding=temp;
   
}

// Function which reduces the encoding in the following way:
// -- removes the clauses where the literal exists (that clause is satisfied)
// -- removes negative of the literal if it exists in some clause 
vector<vector<ll>> simplify(vector<vector<ll>> tempEncoding,ll literal){

    vector<ll> clause_index_to_remove ;
    // We can't remove it on the go as it will diturb the indexing in the loop


    for (ll i=0;i<tempEncoding.size();i++){

        for (ll j=0;j<tempEncoding[i].size();j++){

            if (tempEncoding[i][j]==literal){ // remove this clause and continue
                clause_index_to_remove.push_back(i) ;
                break ;
            }

            if (tempEncoding[i][j]==(-1*literal)){
                tempEncoding[i].erase(tempEncoding[i].begin()+j) ;
            }
        }
    }

    // Now, we remove the clauses
    for(int i=0;i<clause_index_to_remove.size();i++){
		tempEncoding.erase(tempEncoding.begin()+clause_index_to_remove[i]-i);
	}


    return tempEncoding;


}

// The primary function that checks for SAT/UNSAT (and returns model if SAT)
bool DPLL (vector<vector<ll>> tempEncoding){

    // if there are no clauses left, it is SAT 
    if (tempEncoding.size()==0)
            return true ;
    
    // if there is an empty clause, it can't be true, hence the whole formula can't be true
    for (ll i=0;i<tempEncoding.size();i++){

        if (tempEncoding[i].size()==0) 
            return false ;
    }

    // if there's a unit clause, simplify w.r.t. this literal (this literal has to be true)
    for (ll i=0;i<tempEncoding.size();i++){

        if (tempEncoding[i].size()==1){
            model.push_back(tempEncoding[i][0]) ;
            // cout<<"pushed "<<tempEncoding[i][0]<<"\n" ;
            if ( DPLL(simplify(tempEncoding, tempEncoding[i][0]))==true){
                return true ;
            }
            else{

                model.pop_back() ;
                return false ;
            }
        }
                 
    }

    //if size of each clause >1, we choose the a random literal and simplify w.r.t. it
    ll p=randomNumGen(0,tempEncoding.size()-1) ;
    ll q=randomNumGen(0,tempEncoding[p].size()-1) ;
    

    model.push_back(tempEncoding[p][q]) ;
    // cout<<"pushed "<<tempEncoding[p][q]<<"\n" ;
    if (DPLL(simplify(tempEncoding,tempEncoding[p][q]))==true){

        return true ;
    }
    else{
        //  cout<<"popped "<<model[model.size()-1]<<"\n" ;
         model.pop_back() ;
        model.push_back(-1*tempEncoding[p][q]) ;
        // cout<<"pushed "<<-tempEncoding[p][q]<<"\n" ;
        

        
        if(DPLL(simplify(tempEncoding,-1*tempEncoding[p][q]))==true){//if the encoding is satisfiable
			return true;
		}
		else{//otherwise
        //   cout<<"popped "<<model[model.size()-1]<<"\n" ;
			model.pop_back();//remove the negative of prop from solution
			return false;
		}
    }

}


int main(){
    clock_t start = clock();
    //Taking input 
    readCNF() ;
    ofstream o;
    o.open("output.txt");
    if (DPLL(encoding)==true){
        cout<<"SAT\nModel:\n " ;
        o <<"SAT\nModel:\n " ;
        ll arr[propositions+1] ;
        for (ll i=0;i<=propositions;i++)
            arr[i]=1 ;
        
        for (ll i=0;i<model.size();i++){
            if (model[i]<0){
                arr[-model[i]]=0 ;
            }      
        }

        for (ll i=1;i<propositions+1;i++){
            
            if (arr[i]==1){
                cout<<i<<" ";
                o<<i<<" ";
            }
            else{
                cout<<-i<<" ";
                o<<-i<<" ";  
            }
        }
        cout << '0';
        o << '0'; 

    }
    else{
        cout<<"UNSAT" ;
    }    
    printf("\nTime taken: %.2fs\n", (double)(clock() - start)/CLOCKS_PER_SEC);
    return 0;
}