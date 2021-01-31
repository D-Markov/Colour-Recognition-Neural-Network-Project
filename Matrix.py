from typing import Callable, Union, Sequence, List
import random

Scalar = Union[int, float]

class Matrix(Sequence[List[Scalar]]):
    def __init__(self, inputs: Union[List[List[int]], List[List[float]]]):
        if len(inputs) == 0:
            raise ValueError("Matrix cannot be empty")
        self.rows: int = len(inputs)
        self.colomns: int = len(inputs[0])
        for i in inputs:
            if len(i) != self.colomns:
                raise ValueError("Invalid Dimension")
        self.__data = [c for c in inputs]
    
    def __len__(self):
        return len(self.__data)
    
    def __getitem__(self, i: int):
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
 
    @staticmethod
    def zeroMatrix(r: int, c: int) -> 'Matrix':
        newMatrix = []
        
        for _ in range(r):
            newRow = [0 for _ in range(c)]
            newMatrix.append(newRow)
        
        return Matrix(newMatrix)

    @staticmethod
    def randomMatrix(r: int, c: int) -> 'Matrix':
        newMatrix = []
        
        for _ in range(r):
            newRow = [random.gauss(0, 1) for _ in range(c)]
            newMatrix.append(newRow)

        return Matrix(newMatrix)
 

    def dot(self, MatB: 'Matrix') -> 'Matrix':
        if self.colomns != MatB.rows: #l self.rows != MatB.colomns:
            raise ValueError("Change the dimensions")
        else:
            new_data = [[0.0] * MatB.colomns for _ in range(self.rows)]
            
            for r in range(self.rows):
                for c in range(MatB.colomns):
                    val_sum: Scalar = 0
                    for idx in range(self.colomns):
                        val_sum += self.__data[r][idx] * MatB.__data[idx][c]
                    new_data[r][c] = val_sum
        
            return Matrix(new_data)

   
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
        return Matrix.__broadcast(self, other, lambda a, b: a * b)


    def divide(self, other: Union[Scalar, 'Matrix']) -> 'Matrix':
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
        left: 'Matrix',
        right: Union[Scalar, 'Matrix'],
        operation: Callable[[Scalar, Scalar], Scalar]) -> 'Matrix':
        
        if not(type(right) is int or type(right) is float or type(right) is Matrix):
            raise ValueError("Only int, float or Matrix allowed")

        if isinstance(right,int) or isinstance(right, float):
            new_data = []
            for row_idx in range(left.rows):
                new_row = []
                for col_idx in range(left.colomns):
                    new_row.append(operation(left.__data[row_idx][col_idx],  right))
                new_data.append(new_row)
            return Matrix(new_data)
        else:
            if left.rows == right.rows and (left.colomns == 1 or right.colomns == 1):
                colomns =  left.colomns if left.colomns >= right.colomns else right.colomns
                new_data = [[0.0] * colomns for _ in range(left.rows)]
                for row_idx in range(left.rows):
                    for col_idx in range(colomns):
                        left_operand = left[row_idx][0] if left.colomns == 1 else left[row_idx][col_idx]
                        right_operand = right[row_idx][0] if right.colomns == 1 else right[row_idx][col_idx]
                        new_data[row_idx][col_idx] = operation(left_operand , right_operand)
                return Matrix(new_data)
            elif left.colomns == right.colomns and (left.rows == 1 or right.rows == 1):
                rows = left.rows if left.rows >= right.rows else right.rows
                new_data = [[0.0] * left.colomns for _ in range(rows)]
                for  col_idx in range(left.colomns):
                    for row_idx in range(rows):
                        left_operand = left[0][col_idx] if left.rows == 1 else left[row_idx][col_idx]
                        right_operand = right[0][col_idx] if right.rows == 1 else right[row_idx][col_idx]
                        new_data[row_idx][col_idx] = operation(left_operand, right_operand)
                return Matrix(new_data)
            elif left.rows == right.rows and left.colomns == right.colomns:
                new_data = []
                for row_idx in range(left.rows):
                    new_row = []
                    for col_idx in range(left.colomns):
                        new_row.append(operation(left.__data[row_idx][col_idx],  right.__data[row_idx][col_idx]))
                    new_data.append(new_row)
                return Matrix(new_data)
            elif (left.rows == 1 and right.colomns == 1) or (left.colomns == 1 and right.rows == 1):
                rows_count = max(left.rows, right.rows)
                colomn_count = max(left.colomns, right.colomns)
                new_data = [[0.0] * colomn_count for _ in range(rows_count)]

                for row_idx in range(rows_count):
                    for col_idx in range(colomn_count):
                        left_operand = left[0][col_idx] if left.rows == 1 else left[row_idx][0]
                        right_operand = right[0][col_idx] if right.rows == 1 else right[col_idx][0]
                        new_data[row_idx][col_idx] = operation(left_operand, right_operand)
                return Matrix(new_data)
            else:
                raise ValueError("Invalid matrix dimensions")


    def apply(self, func: Callable[[Scalar], Scalar]) -> 'Matrix':
        new_data = []
        for row in self.__data:
            new_row = []
            for i in range(len(row)):
                new_row.append(func(row[i]))
            new_data.append(new_row)
        return Matrix(new_data)          


    def __add(self, other: Union['Matrix', Scalar]) -> 'Matrix':
        return Matrix.__broadcast(self, other, lambda a, b: a + b)

    def __subtract(self, other: Union['Matrix', Scalar], isRight: bool = False) -> 'Matrix':
        return Matrix.__broadcast(self, other, lambda a, b: b - a if isRight else a - b)