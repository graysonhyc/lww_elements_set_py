import unittest
from lww_python import LWW_ElementSet

class Test_LWW_ElementSet(unittest.TestCase):
    # Test for Idempotent property
    def test1(self):
        lww = LWW_ElementSet()
        lww.add(1,1)
        lww.add(1,1)
        self.assertTrue(lww.exist(1))
        lww.add(1,0)
        expected_res = [1]
        self.assertEqual(lww.get(), expected_res)

    # Test for Communtative property
    def test2(self):
        pass

    # Test for Associative property
    def test3(self):
        pass

    # Test for thread-safety

if __name__ == "__main__":
    unittest.main()