#asks for the scale of the square matrix
scale = int(input('scale of the matrix? '))
#asks if you want to use the solving function
promt = input('solve? y/n: ')

matrix = []
index_matrix = []
vector = []

#creates matrix of the size of the input value and allocates the input values to the correct positions
#also creates an index matrix of the same size
for index in range(scale):
    matrix.append([])
    index_matrix.append([])
    for sub_index in range(scale):
        matrix[index].append(float(input(f'value at location {index}, {sub_index} : ')))
        if sub_index == index:
            index_matrix[index].append(1)
        else:
            index_matrix[index].append(0)

#checks if you want to use the solving function            
if promt == 'y':    
    #asks for the vector values    
    for index in range(scale):
        vector.append(float(input(f'right-hand side vector value {index} : ')))
        
print('\nyour matrix:')
for row in matrix:
    print(row)

if promt == 'y':
    print('\nyour right-hand side vector:')
    print(vector)

#creates submatrix for the calculation of the determinant
def sub_matirx(matrix, i, j):   
    submat = []
    for row in (matrix[:i] + matrix[i+1:]):
        submat.append(row[:j] + row[j+1:])
    return submat

#calcualtes the determinant using recursion and the Laplace expansion theorem
def determinant(matrix):
    scale = len(matrix)
    if scale == 1:
        return matrix[0][0]
    elif scale == 2:
        det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        return det
    elif scale == 3:
        det = matrix[0][0]*matrix[1][1]*matrix[2][2] + matrix[0][1]*matrix[1][2]*matrix[2][0] + matrix[0][2]*matrix[1][0]*matrix[2][1] - matrix[0][2]*matrix[1][1]*matrix[2][0] - matrix[0][1]*matrix[1][0]*matrix[2][2] - matrix[0][0]*matrix[1][2]*matrix[2][1]
        return det
    else:    
        det = 0
        for j in range(scale):
            det +=  ((-1) ** j) * matrix[1][j] * determinant(sub_matirx(matrix, 1, j))
        return det

#solves the system of equations using the inverse and the right-hand side vector b
def solve(inverse, vector):
    solution = [0.0]*len(vector)
    for index in range(len(solution)):
        for sub_index in range(len(vector)):
            solution[index] += inverse[index][sub_index] * vector[sub_index]
    return solution
            


#if the determinant is 0 the matrix is singular and not invertible    
if determinant(matrix) == 0:
    print('\nmatrix is not invertible as it is singular')
    quit()

#Step 5: checks if the n or m are reached    
pivot = [0,0]
ongoing = True
while ongoing:
    #Step 1: chooses the initial positon for the pivot
    change_pivot = True
    for column in range(scale-pivot[1]):
        for row in range(scale-pivot[0]):
            if matrix[row+pivot[0]][column+pivot[1]] != 0 and change_pivot:
                change_pivot = False
                pivot[1] = column+pivot[1]

    #Step 2: switches the pivot row with next row that has a value other the zero in the column j
    change_row = True
    if matrix[pivot[0]][pivot[1]] == 0:
        for row in range(scale-pivot[0]):
            if matrix[row+pivot[0]][pivot[1]] != 0 and change_row:
                placeholder = matrix[row+pivot[0]]
                matrix[row+pivot[0]] = matrix[pivot[0]]
                matrix[pivot[0]] = placeholder
                
                placeholder = index_matrix[row+pivot[0]]
                index_matrix[row+pivot[0]] = index_matrix[pivot[0]]
                index_matrix[pivot[0]] = placeholder
                change_row = False

    #Step 3: multiplies the pivot row with the pivot^-1 so the pivot is 1
    if matrix[pivot[0]][pivot[1]] != 1 and matrix[pivot[0]][pivot[1]] != 0:
        a = 1/matrix[pivot[0]][pivot[1]]
        for index in range(scale):
            matrix[pivot[0]][index] = matrix[pivot[0]][index] * a
            index_matrix[pivot[0]][index] = index_matrix[pivot[0]][index] * a

    #Step 4: subtracting the rows which aren't 0 beneath the pivot whit the pivot row times the value of the element in the pivot column 
    for row in range(scale):
        if row != pivot[0] and matrix[row][pivot[1]] != 0:
            a = matrix[row][pivot[1]]
            for index in range(scale):
                matrix[row][index] = matrix[row][index] - (matrix[pivot[0]][index] * a)
                index_matrix[row][index] = index_matrix[row][index] - (index_matrix[pivot[0]][index] * a)
            
    #Step 5: checks if the end of the matrix is reached
    if pivot[0] == scale - 1 or pivot[1] == scale - 1:
        ongoing = False
    else:
        pivot[0] += 1
        pivot[1] += 1
        
print('\nrow reduced form:')
for row in matrix:
    print(row)
    
print('\ninverse matrix:')
for row in index_matrix:
    print(row)

if promt == 'y':    
    print('\nSolution:')
    print(solve(index_matrix, vector))
