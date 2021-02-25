from unittest import TestCase
from src.Mathematics.Matrix import Matrix
import math 

class MatrixTestCase(TestCase):

    def assertMatrixAreEqual(self, actual: Matrix, expected: Matrix) -> None:
        if(actual.rows != expected.rows):
            raise AssertionError(f"Number of rows is different (actual: {actual.rows}; expected: {expected.rows}).\nThe Matrix are different\nactual:\n{actual}\nexpected\n{expected}")

        if(actual.colomns != expected.colomns):
            raise AssertionError(f"Number of columns is different (actual: {actual.colomns}; expected: {expected.colomns}).\nThe Matrix are different\nactual:\n{actual}\nexpected\n{expected}")

        rindex = 0
        for row in expected: 
            cindex = 0
            for cell in row:
                if not math.isclose(cell, actual[rindex][cindex], rel_tol=1e-05):
                    raise AssertionError(f"Value is different (actual: {actual[rindex][cindex]}; expected: {cell}).\nThe Matrix are different\nactual:\n{actual}\nexpected\n{expected}")
                cindex += 1
            rindex += 1
