from typing import Callable, Any, Union
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

    def __add__(self, other: Union['Matrix', int, float]) -> 'Matrix':
        return self.__add(other)

    def __radd__(self, other: Union['Matrix', int, float]) -> 'Matrix':
        return self.__add(other)
    
    def __sub__(self, other: Union['Matrix', int, float]) -> 'Matrix':
        return self.__subtract(other)     
    
    def __rsub__(self, other: Union['Matrix', int, float]) -> 'Matrix':
        return self.__subtract(other, True)     
 
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
 

    def dot(self, MatB):
        if self.rows != MatB.rows:
            return ("Change the dimensions")
        else:
            val_sum = 0
            for i in range(self.rows):
                for c in range(self.rows):
                    val_sum += self.__data[i][c] * MatB.__data[i][c]
        return val_sum

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

    def multiply(self, other):
        return Matrix.__broadcast(self, other, lambda a, b: a * b)


    def divide(self, other):
        return Matrix.__broadcast(self, other, lambda a, b: a / b)


    # def __mul__(self, other):
    #     return Matrix.__broadcast(self, other, lambda a, b: a * b)

    # def __rmul__(self, other):
    #     return Matrix.__broadcast(self, other, lambda a, b: a * b)

    # def __div__(self, other):
    #     return Matrix.__broadcast(self, other, lambda a, b: a / b)

    # def __rdiv__(self, other):
    #     return Matrix.__broadcast(other, self, lambda a, b: a / b)

    @staticmethod
    def __broadcast( 
        left: Union[int, float, 'Matrix'],
        right: Union[int, float, 'Matrix'], 
        operation: Callable[[Union[int, float], Union[int, float]], Union[int, float]]) -> 'Matrix':
        
        if not(type(right) is int or type(right) is float or type(right) is Matrix):
            raise ValueError("Only int, float or Matrix allowed")

        if type(right) is int or type(right) is float:
            new_data = []
            for row_idx in range(left.rows):
                new_row = []
                for col_idx in range(left.colomns):
                    new_row.append(operation(left.__data[row_idx][col_idx],  right))
                new_data.append(new_row)
            return Matrix(new_data)
        
        if left.rows == right.rows:
            colomns =  left.colomns if left.colomns >= right.colomns else right.colomns
            new_data = [[0] * colomns for _ in range(left.rows)]
            for row_idx in range(left.rows):
                for col_idx in range(colomns):
                    left_operand = left[row_idx][0] if left.colomns == 1 else left[row_idx][col_idx]
                    right_operand = right[row_idx][0] if right.colomns == 1 else right[row_idx][col_idx]
                    new_data[row_idx][col_idx] = operation(left_operand , right_operand)
            return Matrix(new_data)
        
        if left.colomns == right.colomns:
            rows = left.rows if left.rows >= right.rows else right.rows
            new_data = [[0] * left.colomns for _ in range(rows)]
            for  col_idx in range(left.colomns):
                for row_idx in range(rows):
                    left_operand = left[0][col_idx] if left.rows == 1 else left[row_idx][col_idx]
                    right_operand = right[0][col_idx] if right.rows == 1 else right[row_idx][col_idx]
                    new_data[row_idx][col_idx] = operation(left_operand, right_operand)
            return Matrix(new_data)
        
        raise ValueError("Invalid matrix dimensions")


    def apply(self, func: Callable[[float], float]) -> Any:
        new_data = []
        for row in self.__data:
            new_row = []
            for i in range(len(row)):
                new_row.append(func(row[i]))
            new_data.append(new_row)
        return Matrix(new_data)          


    def __add(self, other: Union['Matrix', int, float]) -> 'Matrix':
        return Matrix.__broadcast(self, other, lambda a, b: a + b)

    def __subtract(self, other: Union['Matrix', int, float], isRight: bool = False) -> 'Matrix':
        return Matrix.__broadcast(self, other, lambda a, b: b - a if isRight else a - b)