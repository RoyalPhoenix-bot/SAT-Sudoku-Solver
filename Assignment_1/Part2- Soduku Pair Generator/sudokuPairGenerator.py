# Fill empty sudoku diagonals of both the sudokus (one random value per box)
# Give this as input to part 1 of the Assignemnt, we get two solved sudokus

# randomly empty cells from the two sudokus and check model. If multiple solutions exist (check only if >2), 
# place that value back, and try removing other cells 

# When none of the cells can be emptied without having multiple solutions, we would have our solution
import random
from pysat.solvers import Solver
import numpy as np
from pysat.formula import CNF
import datetime
import os

def cellConstraints():
    # At least one filled
    for i in range (k**2):
        for j in range (k**2):
            r=[]
            for n in range (k**2):
                r.append((i*(k**4))+ (j*(k**2)) +(n+1))
            cnf.append(r)
    for i in range (k**2):
        for j in range (k**2):
            r=[]
            for n in range (k**2):
                r.append(k**6+ (i*(k**4))+ (j*(k**2)) +(n+1))
            cnf.append(r)
    # At most one filled, after this each cell will have a unique value
    for i in range (k**2):
        for j in range (k**2):
            for c1 in range (k**2):
                for c2 in range (k**2):
                    if(c2<=c1):
                        continue

                    num1 = (i*(k**4))+ (j*(k**2)) + c1+1
                    num2 = (i*(k**4))+ (j*(k**2)) + c2+1
    #                 print(i," ",j," ",c1," ",c2," ",num1," ",num2)
                    cnf.append([-num1 , -num2])
    for i in range (k**2):
        for j in range (k**2):
            for c1 in range (k**2):
                for c2 in range (k**2):
                    if(c2<=c1):
                        continue

                    num1 = (k**6 + i*(k**4))+ (j*(k**2)) + c1+1
                    num2 = (k**6 + i*(k**4))+ (j*(k**2)) + c2+1
    #                 print(i," ",j," ",c1," ",c2," ",num1," ",num2)
                    cnf.append([-num1 , -num2])
        

def rowConstraints():
    # Each number in the row is unique
    # Each number comes at least once in the row
    for row in range (k**2):
        for num in range (k**2):
            r=[]
            for j in range (k**2):
                r.append(row*(k**4) + j*(k**2) + num+1)
            cnf.append(r)
    # Each number comes at most once in the row
    for row in range (k**2):
        for num in range (k**2):
            for b1 in range (k**2):
                for b2 in range (k**2):
                    if(b2<=b1):
                        continue
                    num1 = row*(k**4) + b1*(k**2) + num+1
                    num2 = row*(k**4) + b2*(k**2) + num+1
                    cnf.append([-num1,-num2])
    # for row in range (k**2):
        for num in range (k**2):
            r=[]
            for j in range (k**2):
                r.append(k**6 + row*(k**4) + j*(k**2) + num+1)
            cnf.append(r)
    # Each number comes at most once in the row
    for row in range (k**2):
        for num in range (k**2):
            for b1 in range (k**2):
                for b2 in range (k**2):
                    if(b2<=b1):
                        continue
                    num1 = k**6 + row*(k**4) + b1*(k**2) + num+1
                    num2 = k**6 + row*(k**4) + b2*(k**2) + num+1
                    cnf.append([-num1,-num2])
                    
def colConstraints():
    # Each number in the column in unique
    # Each number comes at least once in the column
    for col in range (k**2):
        for num in range (k**2):
            r=[]
            for i in range (k**2):
                r.append(i*(k**4) + col*(k**2) + num+1)
            cnf.append(r)
    # Each number comes at most once in a column
    for col in range (k**2):
        for num in range (k**2):
            for b1 in range (k**2):
                for b2 in range (k**2):
                    if(b2<=b1):
                        continue
                    num1 = b1*(k**4) + col*(k**2) + num+1
                    num2 = b2*(k**4) + col*(k**2) + num+1
                    cnf.append([-num1,-num2])
    for col in range (k**2):
        for num in range (k**2):
            r=[]
            for i in range (k**2):
                r.append(k**6 + i*(k**4) + col*(k**2) + num+1)
            cnf.append(r)
    # Each number comes at most once in a column
    for col in range (k**2):
        for num in range (k**2):
            for b1 in range (k**2):
                for b2 in range (k**2):
                    if(b2<=b1):
                        continue
                    num1 = k**6 + b1*(k**4) + col*(k**2)+ num+1
                    num2 = k**6 + b2*(k**4) + col*(k**2) + num+1
                    cnf.append([-num1,-num2])

def boxConstraints():
    # Ensuring each box has different values
    # at least one of 
    for x in range(k):
        for y in range (k):
            for c in range (k**2):
                this_clause=[]
                for i in range(x*k,(x+1)*k):
                    for j in range (y*k,(y+1)*k):
                        this_clause.append(i*(k**4)+j*(k**2)+c+1)
            cnf.append(this_clause)
    # At most once in a box
    for x in range (k):
        for y in range (k):
            for c in range (k**2):
                for i1 in range (x*k,(x+1)*k):
                    for y1 in range (y*k,(y+1)*k):
                        for i2 in range (x*k,(x+1)*k):
                            for y2 in range (y*k,(y+1)*k):
                                if(i2==i1 and y2==y1):
                                    continue
                                num1 = (i1*(k**4) + y1*(k**2) +c+1)
                                num2 = (i2*(k**4) + y2*(k**2) +c+1)
                                cnf.append([-num1,-num2])
                                num1 = num1 + k**6
                                num2 = num2 + k**6
                                cnf.append([-num1,-num2])
                                
def mirrorSudokuConstraints():
    # Making the corresponding mirror cells of the sudoku pairs different
    for i in range (k**2):
        for j in range (k**2):
            for num in range (k**2):
                num1 = i*(k**4) + j*(k**2) + num+1
                num2 = k**6 + i*(k**4) + j*(k**2) + num+1
                cnf.append([-num1,-num2])
                
def getAssumptions():
#     print(type(sudoku1[0][0]))   
    for i in range(k**2):
        for j in range(k**2):
            if ((sudoku1[i][j])!=0):
                assmn.append(i*(k**4)+j*(k**2)+int(sudoku1[i][j]))
    for i in range(k**2):
        for j in range(k**2):
            if ((sudoku2[i][j])!=0):
                assmn.append(k**6 + i*(k**4)+j*(k**2)+int(sudoku2[i][j]))
                

# import functionSudoku
# sudoku1 and sudoku2
global k
global sudoku1
global sudoku2
global assmn
assmn=[]
k = input("Enter the size of the sudoku: ")
k = int(k)
cnf = CNF()
cellConstraints()
rowConstraints()
colConstraints()
boxConstraints()
mirrorSudokuConstraints()
s = Solver(bootstrap_with = cnf)
sudoku1=np.zeros((k**2,k**2),int)  

sudoku2=np.zeros((k**2,k**2),int)

for t in range (k):
    i=t*k
    j=t*k
    r=random.randint(1,k**2)
    sudoku1[i][j]=r
    
for q in range (k):
    i=q*k
    j=(q*k+(k-1))
    p=random.randint(1,k**2)
    sudoku2[i][j]=p
getAssumptions()
s.solve(assumptions = assmn)
out = s.get_model()
for i in range (k**2):
    lst1=[]
    lst2=[]
    for j in range (k**4):
        if(out[i*(k**4)+j]>0):
            n=out[i*(k**4)+j]
            if(n%(k**2)==0):
                lst1.append(k**2)
            else:
                lst1.append(n%(k**2))
        if(out[k**6+i*(k**4)+j]>0):
            n=out[k**6+i*(k**4)+j]
            if(n%(k**2)==0):
                lst2.append(k**2)
            else:
                lst2.append(n%(k**2))
    for q in range (k**2):
        sudoku1[i][q]=lst1[q]
        sudoku2[i][q]=lst2[q]
list =[]
for i in range (2*(k**4)):
    list.append(i)
random.shuffle(list)
for itr in list:
    # Checking sudoku and finding cell
    i =0
    j =0
    val =0
    s1 = int(itr/(k**4))
    if(s1==1):
        i = int((itr-k**4)/(k**2))
        j = (itr-k**4)%(k**2)
        val = sudoku2[i][j]
        sudoku2[i][j]=0
    else:
        i = int((itr)/(k**2))
        j = (itr)%(k**2)
        val = sudoku1[i][j] 
        sudoku1[i][j]=0
    assmn = []
    getAssumptions()
    s.solve(assumptions = assmn)
    soln1 = s.get_model()
    temp = Solver(bootstrap_with = cnf)
    temp.add_clause([-v for v in soln1])
    if(temp.solve(assumptions = assmn)):
        # print(temp.get_model())
        if(s1):
            sudoku2[i][j]=val
        else:
            sudoku1[i][j]=val
    else:
        continue
print (sudoku1) 
print("\n")
    
print (sudoku2)

f = open("sudokuPair.txt","a")
for i in range (k**2):
    for j in range (k**2):
        f.write(str(sudoku1[i][j]))
        f.write(",")
    f.write("\n")
for i in range (k**2):
    for j in range (k**2):
        f.write(str(sudoku2[i][j]))
        f.write(",")
    f.write("\n")
f.close()
# Removing csv file if it is already present.
if(os.path.exists("sudokuPair.csv")):
    os.remove("sudokuPair.csv")
os.rename("sudokuPair.txt","sudokuPair.csv")