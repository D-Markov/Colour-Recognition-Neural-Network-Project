def add(matA, matB):
    matC = []
    for r in range(len(matA)):
        for c in range(len(matA[r])):
            matC.append(matA[r][c] + matB[r][c])

def subtract(matA, matB):
    matC = []
    for r in range(len(matA)):
        for c in range(len(matA[r])):
            matC.append(matA[r][c] - matB[r][c])



def dot(MatA, MatB):
    if len(MatA) != len(MatB):
        return ("Change the dimensions")
    else:
        val_sum = 0
        for i in len(MatA):
            val_sum += MatA[i] * MatB[i]
    return val_sum
    

# def multiply(MatA, MatB):
#     matC = []
#     if len(MatA) != len(MatB[0]):
#         return ("Invalid dimensions")
#     elif len(MatB) == 1 and len(MatB[0] == 1):
#         for r in MatA:
#             matC.append([r * MatB])
#     else: 
#         for i in MatA:
#             subArr = []
#             for j in i: 
#                 subArr.append(MatA[i][j] * MatB[j][i] + Mat)
#             matC.append(subArr)

def rtocol(Matrix):
    new_Matrix = []
    for a in range(len(Matrix)):
        arr = []
        for i in a:
            arr.append(Matrix[a][i])
        new_Matrix.append(arr)


def Multiply(MatA, MatB):
    if len(MatA) != len(MatB[0]) or len(MatA[0]) != len(MatB):
        raise ValueError("Invalid dimensions")
    
    matC = []

    for r in range(len(MatA)):
        arr = []
        for c in range(len(MatA[r])):
            sum = 0
            for i in range(len(MatA)):
                sum += MatA[r][i] * MatB[i][c]
            
            arr.append(sum)
        
        matC.append(arr)
    
    return matC

# def T3*3(Matrix):
#     new_Matrix = []
#     for i in range(len(Matrix[0])):
#         arr = []
#         arr.append([Matrix[i][0], Matrix[i][1], Matrix[i][2]])
#         new_Matrix.append(arr)
    
#     return new_Matrix