import random
from multipledispatch import dispatch
from collections.abc import Sequence

class Matrix(Sequence):
    def __init__(self, inputs):
        if len(inputs) == 0:
            raise ValueError("Matrix cannot be empty")

        self.rows = len(inputs)
        self.colomns = len(inputs[0])
        for i in inputs:
            if len(i) != self.colomns:
                raise ValueError("Invalid Dimension")
        self.__data = [c for c in inputs]
    

    def __len__(self):
        return len(self.__data)
    

    def __getitem__(self, i):
        return self.__data[i]
        

    @staticmethod
    def zeroMatrix(r, c):
        newMatrix = []
        
        for _ in range(r):
            newRow = [0 for _ in range(c)]
            newMatrix.append(newRow)
        
        return Matrix(newMatrix)

    @staticmethod
    def randomMatrix(r, c):
        newMatrix = []
        
        for _ in range(r):
            newRow = [random.random() for _ in range(c)]
            newMatrix.append(newRow)

        return Matrix(newMatrix)
    #range()


    def add(self, matB):
        if self.rows != matB.rows or self.colomns != matB.colomns:
            raise ValueError("Invalid Dimensions")
        
        for r in range(matB.rows):
            for c in range(len(matB[r])):
                self.__data[r][c] + matB.__data[r][c]

    def subtract(self, matA, matB):
        matC = []
        for r in range(len(matA)):
        
            for c in range(len(matA[r])):
                matC.append(matA[r][c] - matB[r][c])



    def dot(self, MatA, MatB):
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

    def rtocol(self, Matrix):
        new_Matrix = []
        for a in range(len(Matrix)):
            arr = []
            for i in a:
                arr.append(Matrix[a][i])
            new_Matrix.append(arr)

    def multiply(self, MatA, MatB):
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