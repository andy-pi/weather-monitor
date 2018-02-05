import unittest
from air_quality import sensor

class TestCases(unittest.TestCase):

    def test_pcs_to_ugm3(self):
        """Does conversion of concentration of PM2.5 particles per 0.01 cubic feet to µg/ metre return a correct value?"""
        self.assertEqual(round(sensor.pcs_to_ugm3(None, 5), 11), 0.01039584505)
        self.assertRaises(ValueError, sensor.pcs_to_ugm3, None, -1)

if __name__ == '__main__':
    unittest.main()

