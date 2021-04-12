# distutils: language=c++
# cython: language_level=3

from typing import Callable, Union, List
import cython
from cpython cimport array
import array
import random

Scalar = Union[int, float]

cdef class Matrix:
    array_template = array.array('d',[])

    cdef:
        int rows, colomns
        array.array __new_data

    def __init__(self, inputs: Union[List[List[int]], List[List[float]], array.array], rows: int = None, colomns: int = None):
        if len(inputs) == 0:
            raise ValueError("Matrix cannot be empty")

        if isinstance(inputs, array.array):
            if(inputs.typecode != 'd'): raise TypeError("data must be of type 'double'")
            if(rows == None): raise ValueError("Must specify number of rows")
            if(colomns == None): raise ValueError("Must specify number of colomns")
            if(len(inputs) / rows != colomns):  raise ValueError(f"number of inputs({len(inputs)}) don't match to number of rows({rows}) and colomns({colomns})")
            
            self.rows = rows
            self.colomns = colomns
            self.__new_data = inputs
        
        elif(isinstance(inputs, list)):
            self.rows = int(len(inputs))
            self.colomns = int(len(inputs[0]))
            
            for i in inputs:
                if len(i) != self.colomns:
                    raise ValueError("Invalid Dimension")

            self.__new_data = array.array('d', [d for row in inputs for d in row])
        else:
            raise TypeError(f"{type(inputs)} not acceptable")

    
    def __len__(self):
        return self.rows
    
    def __getitem__(self, cython.int i):
        if(abs(i) >= self.rows):
            raise IndexError(f"The index {i} is out of range.")

        cdef double[:,:] datav = <double[:self.rows, :self.colomns]> self.__new_data.data.as_doubles
        return list(datav[i,:])

    def __str__(self):
        return f"Shape:[{self.rows},{self.colomns}]\n{self.__new_data.__str__()}"
        
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

    cdef double[:,:] get_view(self):
        return <double[:self.rows, :self.colomns]> self.__new_data.data.as_doubles

    cdef Matrix create_empty(self, int rows, int colomns, zero=False):
        return Matrix(array.clone(Matrix.array_template, rows * colomns, zero), rows, colomns)

    @staticmethod
    def zeroMatrix(cython.int rows, cython.int colomns) -> 'Matrix':
        return Matrix(array.clone(Matrix.array_template, rows * colomns, True), rows, colomns)

    @staticmethod
    def randomMatrix(cython.int rows, cython.int colomns) -> 'Matrix':
        cdef:
            int i
            double r
            array.array new_data = array.clone(Matrix.array_template, rows * colomns, zero=True)
            double[:] datav = <double[:rows * colomns]>new_data.data.as_doubles

        for i in range(rows * colomns):
            r = random.gauss(0, 1)
            datav[i] = r

        return Matrix(new_data, rows, colomns)
 
    cpdef Matrix dot(self, Matrix MatB):
        if self.colomns != MatB.rows:
            raise ValueError("Change the dimensions")
        
        cdef:
            int row_idx, col_idx, idx
            double val_sum, a, b
            Matrix new_matrix = self.create_empty(self.rows, MatB.colomns, False)
            double[:,:] ndatav = new_matrix.get_view()
            double[:,:] sdatav = self.get_view()
            double[:,:] odatav = MatB.get_view()

        for row_idx in range(self.rows):
            for col_idx in range(MatB.colomns):
                val_sum = 0
                for idx in range(self.colomns):
                    a = sdatav[row_idx, idx]
                    b = odatav[idx, col_idx]
                    val_sum += a * b
                ndatav[row_idx, col_idx] = val_sum
    
        return new_matrix


    def rowsSum(self) -> 'Matrix':
        cdef:
            int row_idx, col_idx
            double row_sum
            Matrix new_matrix = self.create_empty(self.rows, 1, False)
            double[:,:] ndatav = new_matrix.get_view()
            double[:,:] sdatav = self.get_view()
        
        for row_idx in range(self.rows):
            row_sum = 0
            for col_idx in range(self.colomns):
                row_sum += sdatav[row_idx, col_idx]
            ndatav[row_idx, 0] = row_sum

        return new_matrix


    def rtocol(self):
        cdef:
            int row_idx, col_idx
            Matrix new_matrix = self.create_empty(self.colomns, self.rows, False)
            double[:,:] ndatav = new_matrix.get_view()
            double[:,:] sdatav = self.get_view()

        for row_idx in range(self.rows):
            for col_idx in range(self.colomns):
                ndatav[col_idx, row_idx] = sdatav[row_idx, col_idx]

        return new_matrix

    
    def sum(self):
        cdef:
            int row_idx, col_idx
            double result = 0
            double[:,:] sdatav = self.get_view()

        for row_idx in range(self.rows):
            for col_idx in range(self.colomns):
                result += sdatav[row_idx, col_idx]
        
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

    cdef Matrix __broadcast_n(self, double right, operation: Callable[[Scalar, Scalar], Scalar]):
        cdef:
            Py_ssize_t row_idx, col_idx
            double left, result
            Matrix new_matrix = self.create_empty(self.rows, self.colomns, False)
            double[:,:] ndatav = new_matrix.get_view()
            double[:,:] sdatav = self.get_view()

        for row_idx in range(self.rows):
            for col_idx in range(self.colomns):
                left = sdatav[row_idx, col_idx]
                result = operation(left,  right)
                ndatav[row_idx, col_idx] = result 

        return new_matrix

    cdef Matrix __broadcast_m(self, Matrix right, operation: Callable[[Scalar, Scalar], Scalar]):
        cdef:
            int row_idx, col_idx, rows_count, colomns_count
            double left_operand, right_operand, result
            Matrix new_matrix
            double[:,:] ndatav
            double[:,:] sdatav = self.get_view()
            double[:,:] rdatav = right.get_view()

        if self.rows == right.rows and (self.colomns == 1 or right.colomns == 1):
            colomns =  self.colomns if self.colomns >= right.colomns else right.colomns
            new_matrix = self.create_empty(self.rows, colomns, False)
            ndatav = new_matrix.get_view()
            for row_idx in range(self.rows):
                for col_idx in range(colomns):
                    left_operand = sdatav[row_idx, 0] if self.colomns == 1 else sdatav[row_idx, col_idx]
                    right_operand = rdatav[row_idx, 0] if right.colomns == 1 else rdatav[row_idx, col_idx]
                    result = operation(left_operand , right_operand)
                    ndatav[row_idx, col_idx] = result
            return new_matrix
        elif self.colomns == right.colomns and (self.rows == 1 or right.rows == 1):
            rows = self.rows if self.rows >= right.rows else right.rows
            new_matrix = self.create_empty(rows, self.colomns, False)
            ndatav = new_matrix.get_view()
            for  col_idx in range(self.colomns):
                for row_idx in range(rows):
                    left_operand = sdatav[0, col_idx] if self.rows == 1 else sdatav[row_idx, col_idx]
                    right_operand = rdatav[0, col_idx] if right.rows == 1 else rdatav[row_idx, col_idx]
                    result =  operation(left_operand, right_operand)
                    ndatav[row_idx, col_idx] = result
            return new_matrix
        elif self.rows == right.rows and self.colomns == right.colomns:
            new_matrix = self.create_empty(self.rows, self.colomns, False)
            ndatav = new_matrix.get_view()
            for row_idx in range(self.rows):
                for col_idx in range(self.colomns):
                    left_operand = sdatav[row_idx, col_idx]
                    right_operand = rdatav[row_idx, col_idx]
                    result = operation(left_operand, right_operand)
                    ndatav[row_idx, col_idx] = result
            return new_matrix
        elif (self.rows == 1 and right.colomns == 1) or (self.colomns == 1 and right.rows == 1):
            rows_count = max(self.rows, right.rows)
            colomns_count = max(self.colomns, right.colomns)
            new_matrix = self.create_empty(rows_count, colomns_count, False)
            ndatav = new_matrix.get_view()
            for row_idx in range(rows_count):
                for col_idx in range(colomns_count):
                    left_operand = sdatav[0, col_idx] if self.rows == 1 else sdatav[row_idx, 0]
                    right_operand = rdatav[0, col_idx] if right.rows == 1 else rdatav[col_idx, 0]
                    result = operation(left_operand, right_operand)
                    ndatav[row_idx, col_idx] = result
            return new_matrix
        else:
            raise ValueError(f"Invalid matrix dimensions: left ({self.rows}, {self.colomns}); right ({right.rows}, {right.colomns})")

    cpdef Matrix apply(self, func: Callable[[Scalar], Scalar]):
        cdef:
            Py_ssize_t r, c
            double res
            double[:,:] sdatav = self.get_view()
            Matrix new_matrix = self.create_empty(self.rows, self.colomns, False)
            double[:,:] ndatav = new_matrix.get_view()

        for r in range(self.rows):
            for c in range(self.colomns):
                res = func(sdatav[r, c])
                ndatav[r, c] = res

        return new_matrix        


    def __add(self, other: Union['Matrix', Scalar]) -> 'Matrix':
        return self.__broadcast(other, lambda a, b: a + b)

    def __subtract(self, other: Union['Matrix', Scalar], isRight: bool = False) -> 'Matrix':
        return self.__broadcast(other, lambda a, b: b - a if isRight else a - b)