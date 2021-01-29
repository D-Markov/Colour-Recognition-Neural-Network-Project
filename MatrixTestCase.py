from unittest import TestCase
from Matrix import Matrix
import math 

class MatrixTestCase(TestCase):

    def assertMatrixAreEqual(self, actual: Matrix, expected: Matrix) -> None:
        if(actual.rows != expected.rows or actual.colomns != expected.colomns):
            raise AssertionError("The Matrix are different")

        rindex = 0
        for row in expected: 
            cindex = 0
            for cell in row:
                if not math.isclose(cell, actual[rindex][cindex], rel_tol=1e-05):
                    raise AssertionError("The Matrix are different")
                cindex += 1
            rindex += 1