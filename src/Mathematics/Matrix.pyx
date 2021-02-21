# cython: profile=True
# cython: linetrace=True

# distutils: define_macros=CYTHON_TRACE=1
# distutils: language=c++
# cython: language_level=3

from typing import Callable, Union, List
import random

Scalar = Union[int, float]

cdef class Matrix:
    cdef:
        Py_ssize_t rows, colomns
        list __data

    def __init__(self, inputs: Union[List[List[int]], List[List[float]]]):
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

    def __add__(self, other: Union['Matrix', Scalar]) -> 'Matrix':
        return self.__add(other)

    def __radd__(self, other: Union['Matrix', Scalar]) -> 'Matrix':
        return self.__add(other)
    
    def __sub__(self, other: Union['Matrix', Scalar]) -> 'Matrix':
        return self.__subtract(other)     
    
    def __rsub__(self, other: Union['Matrix', Scalar]) -> 'Matrix':
        return self.__subtract(other, True)     
 
    @property
    def rows(self):
        return self.rows
 
    @property
    def colomns(self):
        return self.colomns
        
    @staticmethod
    def zeroMatrix(r, c) -> 'Matrix':
        newMatrix = []
        
        for _ in range(r):
            newRow = [0 for _ in range(c)]
            newMatrix.append(newRow)
        
        return Matrix(newMatrix)

    @staticmethod
    def randomMatrix(r, c) -> 'Matrix':
        newMatrix = []
        
        for _ in range(r):
            newRow = [random.gauss(0, 1) * 0.01 for _ in range(c)]
            newMatrix.append(newRow)

        return Matrix(newMatrix)
 
    cpdef Matrix dot(self, Matrix MatB):
        if self.colomns != MatB.rows: #l self.rows != MatB.colomns:
            raise ValueError("Change the dimensions")
        
        cdef:
            int r, c, idx
            float val_sum, a, b

        new_data = [[0.0] * MatB.colomns for _ in range(self.rows)]
        
        for r in range(self.rows):
            s_row = self.__data[r]
            n_row = new_data[r]
            
            for c in range(MatB.colomns):
                val_sum = 0
                for idx in range(self.colomns):
                    a = s_row[idx]
                    b = MatB.__data[idx][c]
                    val_sum += a * b
                n_row[c] = val_sum
    
        return Matrix(new_data)

#    def dot1(self, MatB):
#        matrixR = MatB.rtocol()

#       new_data = [[0] * self.rows for _ in range(MatB.colomns)]
#      for r in range(self.rows):
#            for c in range(MatB.colomns):
#                value_sum = 0
                
#                value_sum += self.__data[r][c] * matrixR.__data[r][c]
#                new_data[r][c]


    def rowsSum(self) -> 'Matrix':
        new_data = [[0.0] for _ in range(self.rows)]
        for row_idx, row in enumerate(self.__data):
            new_data[row_idx][0] = sum(row)
        return Matrix(new_data) 


    def rtocol(self):
        new_data = []
        for a in range(len(self.__data[0])):
            arr = []
            for i in range(self.rows):
                arr.append(self.__data[i][a])
            new_data.append(arr)

        return Matrix(new_data)

    
    def sum(self):
        result = 0
        for row in self.__data:
            result += sum(row)

        return result

    def multiply(self, other: Union[Scalar, 'Matrix']) -> 'Matrix':
        return self.__broadcast(other, lambda a, b: a * b)


    def divide(self, other: Union[Scalar, 'Matrix']) -> 'Matrix':
        return self.__broadcast(other, lambda a, b: a / b)


    # def __mul__(self, other):
    #     return Matrix.__broadcast(self, other, lambda a, b: a * b)

    # def __rmul__(self, other):
    #     return Matrix.__broadcast(self, other, lambda a, b: a * b)

    # def __div__(self, other):
    #     return Matrix.__broadcast(self, other, lambda a, b: a / b)

    # def __rdiv__(self, other):
    #     return Matrix.__broadcast(other, self, lambda a, b: a / b)

    def __broadcast(self, other: Union[Matrix, Scalar], operation: Callable[[Scalar, Scalar], Scalar]) -> Matrix:
        if(isinstance(other, int) or isinstance(other, float)):
            return self.__broadcast_n(other, operation)
        elif(isinstance(other, Matrix)):
            return self.__broadcast_m(other, operation)
        else:
            raise TypeError

    cpdef Matrix __broadcast_n(self, float right, operation: Callable[[Scalar, Scalar], Scalar]):
        new_data = []

        for row_idx in range(self.rows):
            new_row = []
            for col_idx in range(self.colomns):
                new_row.append(operation(self.__data[row_idx][col_idx],  right))
            new_data.append(new_row)

        return Matrix(new_data)

    cpdef Matrix __broadcast_m(self, Matrix right, operation: Callable[[Scalar, Scalar], Scalar]):
        if self.rows == right.rows and (self.colomns == 1 or right.colomns == 1):
            colomns =  self.colomns if self.colomns >= right.colomns else right.colomns
            new_data = [[0.0] * colomns for _ in range(self.rows)]
            for row_idx in range(self.rows):
                for col_idx in range(colomns):
                    left_operand = self[row_idx][0] if self.colomns == 1 else self[row_idx][col_idx]
                    right_operand = right[row_idx][0] if right.colomns == 1 else right[row_idx][col_idx]
                    new_data[row_idx][col_idx] = operation(left_operand , right_operand)
            return Matrix(new_data)
        elif self.colomns == right.colomns and (self.rows == 1 or right.rows == 1):
            rows = self.rows if self.rows >= right.rows else right.rows
            new_data = [[0.0] * self.colomns for _ in range(rows)]
            for  col_idx in range(self.colomns):
                for row_idx in range(rows):
                    left_operand = self[0][col_idx] if self.rows == 1 else self[row_idx][col_idx]
                    right_operand = right[0][col_idx] if right.rows == 1 else right[row_idx][col_idx]
                    new_data[row_idx][col_idx] = operation(left_operand, right_operand)
            return Matrix(new_data)
        elif self.rows == right.rows and self.colomns == right.colomns:
            new_data = []
            for row_idx in range(self.rows):
                new_row = []
                for col_idx in range(self.colomns):
                    new_row.append(operation(self.__data[row_idx][col_idx],  right.__data[row_idx][col_idx]))
                new_data.append(new_row)
            return Matrix(new_data)
        elif (self.rows == 1 and right.colomns == 1) or (self.colomns == 1 and right.rows == 1):
            rows_count = max(self.rows, right.rows)
            colomn_count = max(self.colomns, right.colomns)
            new_data = [[0.0] * colomn_count for _ in range(rows_count)]

            for row_idx in range(rows_count):
                for col_idx in range(colomn_count):
                    left_operand = self[0][col_idx] if self.rows == 1 else self[row_idx][0]
                    right_operand = right[0][col_idx] if right.rows == 1 else right[col_idx][0]
                    new_data[row_idx][col_idx] = operation(left_operand, right_operand)
            return Matrix(new_data)
        else:
            raise ValueError(f"Invalid matrix dimensions: left ({self.rows}, {self.colomns}); right ({right.rows}, {right.colomns})")


    def apply(self, func: Callable[[Scalar], Scalar]) -> 'Matrix':
        new_data = []
        for row in self.__data:
            new_row = []
            for i in range(len(row)):
                new_row.append(func(row[i]))
            new_data.append(new_row)
        return Matrix(new_data)          


    def __add(self, other: Union['Matrix', Scalar]) -> 'Matrix':
        return self.__broadcast(other, lambda a, b: a + b)

    def __subtract(self, other: Union['Matrix', Scalar], isRight: bool = False) -> 'Matrix':
        return self.__broadcast(other, lambda a, b: b - a if isRight else a - b)