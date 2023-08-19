# Take in k, then input from .csv file
# Defining k^2(1 to k^2, K^2+1 to 2K^2, ...) for each cell and starting from k^6+1 for the other
# Make Encodings
# Output filled sudoku, modulo k^2 for each cell then print both sudoku's one after the other
import csv
from pysat.solvers import Solver
import  numpy as np
import datetime

k = input("Enter the size of the sudoku: ")
k=int(k)
a = datetime.datetime.now()
file_path="./"
file_name=input("Enter the file name: ")
file_path+=file_name
rows = []
# Change name of file.
with open(file_path, 'r') as csvfile:
    
    csvreader = csv.reader(csvfile)
    
    for row in csvreader:
        rows.append(row)

assmp=[]

for i in range(k**2):
    for j in range(k**2):
        if (int(rows[i][j])!=0):
            rows[i][j]=int(rows[i][j])
            assmp.append(i*(k**4)+j*(k**2)+rows[i][j])
            

for i in range(k**2,2*(k**2)):
    for j in range(k**2):
        if (int(rows[i][j])!=0):
            rows[i][j]=int(rows[i][j])
            assmp.append(i*(k**4)+j*(k**2)+rows[i][j])

s=Solver()
# At least one filled
for i in range (k**2):
    for j in range (k**2):
        r=[]
        for n in range (k**2):
            r.append((i*(k**4))+ (j*(k**2)) +(n+1))
        s.add_clause(r)
for i in range (k**2):
    for j in range (k**2):
        r=[]
        for n in range (k**2):
            r.append(k**6+ (i*(k**4))+ (j*(k**2)) +(n+1))
        s.add_clause(r)
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
                s.add_clause([-num1 , -num2])
for i in range (k**2):
    for j in range (k**2):
        for c1 in range (k**2):
            for c2 in range (k**2):
                if(c2<=c1):
                    continue
                
                num1 = (k**6 + i*(k**4))+ (j*(k**2)) + c1+1
                num2 = (k**6 + i*(k**4))+ (j*(k**2)) + c2+1
#                 print(i," ",j," ",c1," ",c2," ",num1," ",num2)
                s.add_clause([-num1 , -num2])

# Each number in the row is unique
# Each number comes at least once in the row
for row in range (k**2):
    for num in range (k**2):
        r=[]
        for j in range (k**2):
            r.append(row*(k**4) + j*(k**2) + num+1)
        s.add_clause(r)
# Each number comes at most once in the row
for row in range (k**2):
    for num in range (k**2):
        for b1 in range (k**2):
            for b2 in range (k**2):
                if(b2<=b1):
                    continue
                num1 = row*(k**4) + b1*(k**2) + num+1
                num2 = row*(k**4) + b2*(k**2) + num+1
                s.add_clause([-num1,-num2])
# for row in range (k**2):
    for num in range (k**2):
        r=[]
        for j in range (k**2):
            r.append(k**6 + row*(k**4) + j*(k**2) + num+1)
        s.add_clause(r)
# Each number comes at most once in the row
for row in range (k**2):
    for num in range (k**2):
        for b1 in range (k**2):
            for b2 in range (k**2):
                if(b2<=b1):
                    continue
                num1 = k**6 + row*(k**4) + b1*(k**2) + num+1
                num2 = k**6 + row*(k**4) + b2*(k**2) + num+1
                s.add_clause([-num1,-num2])
# Ensuring each box has different values
# at least one of 
for x in range(k):
    for y in range (k):
        for c in range (k**2):
            this_clause=[]
            for i in range(x*k,(x+1)*k):
                for j in range (y*k,(y+1)*k):
                    this_clause.append(i*(k**4)+j*(k**2)+c+1)
        s.add_clause(this_clause)
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
                            s.add_clause([-num1,-num2])
                            num1 = num1 + k**6
                            num2 = num2 + k**6
                            s.add_clause([-num1,-num2])
# Each number in the column in unique
# Each number comes at least once in the column
for col in range (k**2):
    for num in range (k**2):
        r=[]
        for i in range (k**2):
            r.append(i*(k**4) + col*(k**2) + num+1)
        s.add_clause(r)
# Each number comes at most once in a column
for col in range (k**2):
    for num in range (k**2):
        for b1 in range (k**2):
            for b2 in range (k**2):
                if(b2<=b1):
                    continue
                num1 = b1*(k**4) + col*(k**2) + num+1
                num2 = b2*(k**4) + col*(k**2) + num+1
                s.add_clause([-num1,-num2])
for col in range (k**2):
    for num in range (k**2):
        r=[]
        for i in range (k**2):
            r.append(k**6 + i*(k**4) + col*(k**2) + num+1)
        s.add_clause(r)
# Each number comes at most once in a column
for col in range (k**2):
    for num in range (k**2):
        for b1 in range (k**2):
            for b2 in range (k**2):
                if(b2<=b1):
                    continue
                num1 = k**6 + b1*(k**4) + col*(k**2)+ num+1
                num2 = k**6 + b2*(k**4) + col*(k**2) + num+1
                s.add_clause([-num1,-num2])
# Making the corresponding mirror cells of the sudoku pairs different
for i in range (k**2):
    for j in range (k**2):
        for num in range (k**2):
            num1 = i*(k**4) + j*(k**2) + num+1
            num2 = k**6 + i*(k**4) + j*(k**2) + num+1
            s.add_clause([-num1,-num2])
solPresent=0
if(s.solve(assumptions = assmp)):
    solPresent=1
b = datetime.datetime.now()
out = s.get_model()
if(solPresent==0):
    print("None")
else:
    sudoku1 = np.empty((0,k**2),int)
    sudoku2 = np.empty((0,k**2),int)
    for i in range (k**2):
        lst=[]
        for j in range (k**4):
            if(out[i*(k**4)+j]>0):
                n=out[i*(k**4)+j]
                if(n%(k**2)==0):
                    lst.append(k**2)
                else:
                    lst.append(n%(k**2))
        sudoku1 = np.append(sudoku1,np.array([lst]),axis=0)
    np.set_printoptions(threshold=np.inf)
    print(np.matrix(sudoku1))
    for i in range (k**2):
        lst=[]
        for j in range (k**4):
            if(out[k**6+i*(k**4)+j]>0):
                n=out[k**6+i*(k**4)+j]
                if(n%(k**2)==0):
                    lst.append(k**2)
                else:
                    lst.append(n%(k**2))
        sudoku2 = np.append(sudoku2,np.array([lst]),axis=0)
    print(np.matrix(sudoku2))

print(b-a)
print(s.nof_vars(),s.nof_clauses())