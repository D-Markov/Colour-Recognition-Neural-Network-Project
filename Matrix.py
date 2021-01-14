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

    def __str__(self):
        return f"Shape:[{self.rows},{self.colomns}]\n{self.__data.__str__()}"
        
    def __repr__(self):
        return self.__str__()
        
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

        new_data = []
        
        for rowIdx in range(matB.rows):
            newRow = []
            for c in range(len(matB[rowIdx])):
                newRow.append(self.__data[rowIdx][c] + matB.__data[rowIdx][c])
            
            new_data.append(newRow)
        
        return Matrix(new_data)


    def subtract(self, matA, matB):
        matC = []
        for r in range(len(matA)):
            for c in range(len(matA[r])):
                matC.append(matA[r][c] - matB[r][c])

    
    def dot(self, MatB):
        if self.rows != MatB.rows:
            return ("Change the dimensions")
        else:
            val_sum = 0
            for i in range(self.rows):
                for c in range(self.rows):
                    val_sum += self.__data[i][c] * MatB.__data[i][c]
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

    def rtocol(self):
        new_data = []
        for a in range(len(self.__data[0])):
            arr = []
            for i in range(self.rows):
                arr.append(self.__data[i][a])
            new_data.append(arr)

        return Matrix(new_data)

        #self.__data = new_data
        #self.rows = len(self.__data)
        #self.colomns = len(self.__data[0])


    def multiply_scalar(self, n):
        new_data = []
        for r in range(self.rows):
            new_row = []
            for c in range(self.colomns):
                new_row.append(self.__data[r][c] * n)
            new_data.append(new_row)
        return Matrix(new_data)

    def multiply(self, MatB):
        if self.rows != len(MatB.__data[0]) or len(self.__data[0]) != MatB.rows:
           raise ValueError("Invalid dimensions")
        
        new_data = []
        for r in range(self.rows):
            new_row = []
            for c2 in range (MatB.colomns):
                sum = 0
                for c in range(self.colomns):
                    sum += self.__data[r][c] * MatB.__data[c][c2]
                new_row.append(sum)
            new_data.append(new_row)
        return Matrix(new_data)
        # self.__data = matC
        # self.rows = len(self.__data)
        # self.colomns = len(self.__data[0])


    def apply(self, func):
        new_data = []
        for row in self.__data:
            new_row = []
            for i in range(len(row)):
                new_row.append(func(row[i]))
            new_data.append(new_row)
        return Matrix(new_data)          

            # for i, value in enumerate(row):
            #     row[i] = func(value)          

    # def T3*3(Matrix):
    #     new_Matrix = []
    #     for i in range(len(Matrix[0])):
    #         arr = []
    #         arr.append([Matrix[i][0], Matrix[i][1], Matrix[i][2]])
    #         new_Matrix.append(arr)
        
    #     return new_Matrix