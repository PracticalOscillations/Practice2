import unittest
import numpy as np
from methods.SciPy import Scipy_method

class TestScipyMethod(unittest.TestCase):

    def test_scipy_method(self):
        def f_x(x, y, z):
            return x + y + z

        def f_y(x, y, z):
            return x * y * z

        def f_z(x, y, z):
            return x - y - z

        w0 = [1, 2, 3]
        t = np.arange(0, 10, 1)

        expected_output = np.array([
            [1., 2., 3.],
            [6., 6., 0.],
            [12., 72., -6.],
            [78., 1728., -78.],
            [1728., 884736., -1728.],
            [884736., 109418989131512359209., -884736.],
            [109418989131512359209., 1.307674368e38, -109418989131512359209.],
            [1.307674368e38, 2.218265297e76, -1.307674368e38],
            [2.218265297e76, np.inf, -2.218265297e76],
            [np.inf, np.nan, -np.inf]
        ])

        output = Scipy_method(f_x, f_y, f_z, w0, t)
        np.testing.assert_array_almost_equal(output, expected_output)


if __name__ == '__main__':
    unittest.main()
