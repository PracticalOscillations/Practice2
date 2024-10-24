import unittest


class TestEulerSolver(unittest.TestCase):
    def test_initial_conditions(self):
        x, y, z, t = euler_solver(dt=0.01, t_max=1000)
        self.assertEqual(x[0], 1)
        self.assertEqual(y[0], 0)
        self.assertEqual(z[0], 0)

    def test_result_size(self):
        x, y, z, t = euler_solver(dt=0.01, t_max=1000)
        self.assertEqual(x.shape[0], t.shape[0])
        self.assertEqual(y.shape[0], t.shape[0])
        self.assertEqual(z.shape[0], t.shape[0])


class TestRungeKuttaSolver(unittest.TestCase):
    def test_initial_conditions(self):
        x, y, z, t = runge_kutta_solver(dt=0.01, t_max=1000)
        self.assertEqual(x[0], 1)
        self.assertEqual(y[0], 0)
        self.assertEqual(z[0], 0)

    def test_result_size(self):
        x, y, z, t = runge_kutta_solver(dt=0.01, t_max=1000)
        self.assertEqual(x.shape[0], t.shape[0])
        self.assertEqual(y.shape[0], t.shape[0])
        self.assertEqual(z.shape[0], t.shape[0])


if __name__ == '__main__':
    unittest.main()
