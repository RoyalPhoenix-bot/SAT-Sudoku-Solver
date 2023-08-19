# Instructions to Run
## DPLL Algorithm
- Code is implemented in `C++`.
- Make sure the input file is in the same directory as the `C++` file.
- To read the `.cnf` file as input, either change the name of the file to `dimacsEncoding.cnf` or write the name of the file in line `27` of the file `pysatSolver_DPLL.cnf`. 
- To run the code, type `g++ pysatSolver_DPLL.cpp -o a`.
- After pressing enter, run the executable by typing `.\a.exe`.
- An output file `output.txt` is created with the output. The output is also displayed on the terminal.

## Extra - Semantic Tableau
- All the same steps to run as the `DPLL` file.(Replace `pysatSolver_DPLL.cpp` with `pysatSolver_Semantic.cpp` everywhere).
- Output is displayed on the terminal.

**Note** - Since Semantic Tableau is a Brute Force method, the time complexity can increase exponentially as we increase the number of clauses. So the code can take a lot of time to run when the number of clause is quite large.