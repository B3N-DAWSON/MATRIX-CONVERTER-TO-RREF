import sys
from sympy import *

def parse_input():
    rows = []
    for line in sys.stdin:
        rowstr = line.strip().split(',')
        if len(rowstr) == 0 or len(rowstr[0].strip()) == 0:
            break
        row = []
        for item in rowstr:
            nd = item.split('/')
            if len(nd) == 1:
                nd.append(1)
            row.append(Rational(nd[0],nd[1]))
        rows.append(row)
    return Matrix(rows)

def rational_string(r, sep="."):
    if r.q == 1:
        return str(r.p)
    else:
        return "{0}{1}{2}".format(r.p, sep, r.q)

def print_matrix(M):
    r = M.shape[0]
    c = M.shape[1]
    for i in range(r):
        row = []
        for j in range(c):
            row.append(rational_string(A[i,j], sep="/"))
        print(",".join(row))

def swap_string(i,j): # Ri <-> Rj
    return "s{0}:{1}".format(i,j)

def replace_string(i,j,c): # Ri = Ri + cRj
    return "r{0}:{1}:{2}".format(j,rational_string(c),i)

def scale_string(i,c): # Ri = cRi
    return "m{0}:{1}".format(i,rational_string(c))

A = parse_input()
# ---------------------------------------------------------------------- # 

ops = []

num_rows = A.shape[0] 
num_cols = A.shape[1]

i = 0 
j = 0
n = 0
  
################################################################################### 
                                # FIND NONZERO VAL #
###################################################################################  
   
# LOCATES PIVOT POINTS / FIRST NON ZERO VAL
def find_nonzeroV(A,r,c):

    # Iterates the column 
    for nonzero in range(c,num_cols):

        # if column of row is zero
        if A[r,nonzero] == 0:
            found_nonzero = False  
            continue
    
        # if nonzero found in col + row
        else:
            found_nonzero = True          
            return found_nonzero,nonzero,A
    return found_nonzero,nonzero,A
    
################################################################################### 
                                    # SWAP ROWS #
###################################################################################

# checks if there is a value 
def swap_rows(A,n):
    
    # row_Swapped = False
    if n < num_cols and n < num_rows:
    # CHECKS IF 0 IS IN PIVOT POINT (DONT WANT)
        if A[n,n] == 0:
            for cols in range(n,num_cols,1):
                for rows in range(n+1,num_rows,1):
                    # IF NONZERO VAL IS FOUND 
                    if A[rows,cols] != 0:
                        ops.append(swap_string(n,rows))
                        A = A.elementary_row_op("n<->m",row1= n ,row2 = rows)
                   
                        return A 

    return A 

################################################################################### 
                                    # SCALE ROWS #
###################################################################################

# # DEALS WITH ALL / MOSTLY 0 MATRIXES

def scale_rows(A,n,nonzero):
    
    print("---------------------------")  
    print(". SCALE ROWS . ")
    print("---------------------------")  
    print("n - ",n)
    print("nonzero =",nonzero)
    if A[n,nonzero] != 1 and A[n,nonzero] != 0:
        print("n - ",n)
        print("nonzero =",nonzero)
        print("current non frac val",A[n,nonzero])        
        
        
        # RECIPROCAL OF VAL IN ORDER TO MAKE '1' IF NOT ALREADY

        recip_val = 1/A[n,nonzero]
        ops.append(scale_string(n,recip_val))
        A = A.elementary_row_op("n->kn",row=n,k=recip_val)

        return A
    
    # SAFETY NET
    return A
         
################################################################################### 
                                    # ROW REPLACEMENT #
###################################################################################    

def row_replacement(A,n,nonzero):
  
    # loops rows below pivot point 
    for bp in range(n+1,num_rows):
        
        # if row below pivot != 0 then row replace
        if A[bp,nonzero] != 0:

            ops.append(replace_string(bp,n,-A[bp,nonzero]))
            A = A.elementary_row_op("n->n+km",row=bp,row2=n,k=-A[bp,nonzero])
            
        # otherwise continue looping rows for row replacement    
        else:
            bp += 1
            continue 
    
    # safety net
    return A
 
################################################################################### 
                             # ROW above pivot #
################################################################################### 

def clear_ap(A,n,nonzero): 


    # checking pivot point == 1
    if A[n,nonzero] == 1:
        print("- n = ",n)
            
        # row index - loops above pivot
        for ap in range(n-1,-1,-1):    
            print("- ap =",ap)
                
            # if index above pivot DOES NOT = 0 then ROW REPLACE 
            if A[ap,nonzero] != 0:  
                ops.append(replace_string(ap,n,-A[ap,nonzero]))
                A = A.elementary_row_op("n->n+km",row=ap,row2=n,k=-A[ap,nonzero])

    # safety net        
    return A
        
################################################################################### 
                                    # MAIN #
###################################################################################

while n < num_rows:

    found_nonzero,nonzero,A = find_nonzeroV(A,n,0) # LOCATES PIVOT POINTS / FIRST NON ZERO VAL + CAN ALSO BE USED TO DETERMINE IF MATRIX ROW IS FULL OF 'ZEROS' 
    A = swap_rows(A,n) # CHECKS IF PIVOT INDEX [n,n] is zero + if so loops below and across cols through the matrix and find a nonzero val in the same col to swap 
    found_nonzero,nonzero,A = find_nonzeroV(A,n,0) # LOCATES PIVOT POINTS / FIRST NON ZERO VAL + CAN ALSO BE USED TO DETERMINE IF MATRIX ROW IS FULL OF 'ZEROS'   
    A = scale_rows(A,n,nonzero)  # scales nonzero value if it isnt '1' in order to make it '1' be a pivot point
    print(A)    
    A = row_replacement(A,n,nonzero) # CLEARS VALUES BELOW BUT IN THE SAME COL AS THE PIVOT POINT (n,nonzero)  
    A = clear_ap(A,n,nonzero) 
    print("RREF = ",A)
    print(ops)
    n += 1
        

    

        
     

