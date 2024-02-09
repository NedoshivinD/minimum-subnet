import min_subnet
import unittest

class Subnet_tests(unittest.TestCase):
    def test_input1(self):
        with self.assertRaises(Exception):
            min_subnet.calc('')

    def test_input2(self):
        with self.assertRaises(Exception):
            min_subnet.calc('123 3213')

    def test_input3(self):
        with self.assertRaises(Exception):
            min_subnet.calc('999.999.999.999', '-999.-999.-999.-999', 4)

    def test_input4(self):
        with self.assertRaises(Exception):
            min_subnet.calc('ghjsfdgfhs')

    def test_input5(self):
        with self.assertRaises(Exception):
            min_subnet.calc('34.23.89.190', 6)
        
    def test_input6(self):
        with self.assertRaises(Exception):
            min_subnet.calc('190.30.15.5', 'four')

    def test_eq1(self):
        x = min_subnet.calc('34.23.89.190', '34.23.101.190', 4)
        x1 = min_subnet.calc('34.23.89.190', '34.23.101.190', 4)
        self.assertEqual(x, x1)

    def test_eq2(self):
        x = min_subnet.calc('34.23.89.190', '34.23.101.190', 4)
        x1 = min_subnet.calc('34.23.101.190', '34.23.89.190', 4)
        self.assertEqual(x, x1)

    def test_alg1(self):
        x = min_subnet.calc('122.22.22.2', '122.22.22.2', 4)
        self.assertTrue(x == '122.22.22.2/32')

    def test_alg2(self):
        x = min_subnet.calc('0.0.0.0', '0.0.0.0', 4)
        self.assertTrue(x == '0.0.0.0/32')

    def test_alg3(self):
        x = min_subnet.calc('255.255.255.255', '255.255.255.255', 4)
        self.assertTrue(x == '255.255.255.255/32')

    def test_alg4(self):
        x = min_subnet.calc('255.255.255.255', '0.0.0.0', 4)
        self.assertTrue(x == '0.0.0.0/0')

if __name__ == "__main__":
    unittest.main()