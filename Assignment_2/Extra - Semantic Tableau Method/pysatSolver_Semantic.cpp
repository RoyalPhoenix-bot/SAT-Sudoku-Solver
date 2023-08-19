#include <bits/stdc++.h>
using namespace std;
typedef long long int ll;
vector<vector<ll>> encoding;// stores encoding
vector<pair<ll,ll>> noOfClauses;// Stores the size of each row and the current position of iterator.
ll propositions,clauses;
vector<ll> model;

int solve(){
    // Exits when we have tried all combinations
    while(noOfClauses[0].first<noOfClauses[0].second){
        int flag=0;
        ll index=clauses-1;
        set<ll> currModel; //current model
        for(ll i=0;i<clauses;i++){
            ll j=noOfClauses[i].first;
            if(currModel.find(-encoding[i][j])==currModel.end()){
                currModel.insert(encoding[i][j]);//Add literal and continue
            }else{
                //Contradiction
                flag=1;
                index=i;
                break;
            }
        }
        if(flag==0){
            // We have found a model satisfying the equation
            while(!currModel.empty()){
                ll num = *(currModel.begin());
                model.push_back(num);
                currModel.erase(currModel.begin());
            }
            return 0;
        }else{
            // The current Model (leaf node) is a contradiction and we proceed to the next model.
            while(index>0 && noOfClauses[index].first+1==noOfClauses[index].second){
                noOfClauses[index].first=0;
                index--;
            }
            noOfClauses[index].first++;
            for(ll i=index+1;i<clauses;i++){
                noOfClauses[i].first=0;
            }
        }
    }

    return 1;
}

void initialize_noOfClauses_vector(){
    for(ll i=0;i<clauses;i++){
        noOfClauses.push_back(make_pair(0,encoding[i].size()));
    }
    return;
}

void takeInput(){
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
        for(ll j=0;j<l;j++){
            if(stoi(results[j]))temp[i].push_back(stoi(results[j]));
        }
    }
    f.close();
    encoding=temp;
    sort(encoding.begin(),encoding.end());
    return;
}

void printModel(){
    //The literals present in the vector 'model' have to be the same, while the remaining ones are 'don't care'.
    // Assigned the 'don't care' literals to be true and then printed the model.
    vector<ll> m(propositions+1,0);
    ll l = model.size();
    for(ll i=0;i<l;i++){
        m[abs(model[i])]= model[i]/abs(model[i]);
    }
    for(ll i=1;i<=propositions;i++){
        if(m[i]==0)m[i]=1;
    }
    cout << "SAT\nA Model for the formula is:\n";
    for(ll i=1;i<=propositions;i++){
        cout << m[i]*i << " ";
    }
    cout << endl;
}

int main(){

    //Taking input the clauses.
    takeInput();
    initialize_noOfClauses_vector();
    int unsat = solve();
    if(unsat){
        cout << "The Formula is Unsatisfiable.\n";
    }else{
        printModel();
    }
    return 0;
}