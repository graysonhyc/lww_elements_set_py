import unittest
import threading
from lww_python import LWW_ElementSet

class Test_LWW_ElementSet(unittest.TestCase):
    """This test cases suite intends to test the LWW element set CDRT implementation for its various 
    properties, including idempotence, commutativity and associativity.
    """

    # Test 1 - 6 test for idempotence property: (a + a = a)
    def test1(self):
        lww_set = LWW_ElementSet()
        lww_set.add('a', 1)
        self.assertTrue(lww_set.exist('a'))
        lww_set.add('a', 1)
        self.assertTrue(lww_set.exist('a'))
        self.assertEqual(lww_set.get(), ['a'])

    def test2(self):
        lww_set = LWW_ElementSet()
        lww_set.add('a', 1)
        self.assertTrue(lww_set.exist('a'))
        lww_set.add('a', 0)
        self.assertTrue(lww_set.exist('a'))
        self.assertEqual(lww_set.get(), ['a'])

    def test3(self):
        lww_set = LWW_ElementSet()
        lww_set.add('a', 1)
        self.assertTrue(lww_set.exist('a'))
        lww_set.add('a', 2)
        self.assertTrue(lww_set.exist('a'))
        self.assertEqual(lww_set.get(), ['a'])

    def test4(self):
        lww_set = LWW_ElementSet()
        lww_set.remove('a', 1)
        self.assertFalse(lww_set.exist('a'))
        lww_set.remove('a', 1)
        self.assertFalse(lww_set.exist('a'))
        self.assertEqual(lww_set.get(), [])

    def test5(self):
        lww_set = LWW_ElementSet()
        lww_set.remove('a', 1)
        self.assertFalse(lww_set.exist('a'))
        lww_set.remove('a', 0)
        self.assertFalse(lww_set.exist('a'))
        self.assertEqual(lww_set.get(), [])

    def test6(self):
        lww_set = LWW_ElementSet()
        lww_set.remove('a', 1)
        self.assertFalse(lww_set.exist('a'))
        lww_set.remove('a', 2)
        self.assertFalse(lww_set.exist('a'))
        self.assertEqual(lww_set.get(), [])

    # Test 7 - 12 test for communtativity property: (a + b) = (b + a)
    def test7(self):
        lww_set = LWW_ElementSet()
        lww_set.add('a', 1)
        self.assertTrue(lww_set.exist('a'))
        lww_set.remove('a', 1)
        self.assertTrue(lww_set.exist('a'))
        self.assertEqual(lww_set.get(), ['a'])

    def test8(self):
        lww_set = LWW_ElementSet()
        lww_set.remove('a', 1)
        self.assertFalse(lww_set.exist('a'))
        lww_set.add('a', 1)
        self.assertTrue(lww_set.exist('a'))
        self.assertEqual(lww_set.get(), ['a'])
        
    def test9(self):
        lww_set = LWW_ElementSet()
        lww_set.add('a', 1)
        self.assertTrue(lww_set.exist('a'))
        lww_set.remove('a', 0)
        self.assertTrue(lww_set.exist('a'))
        self.assertEqual(lww_set.get(), ['a'])

    def test10(self):
        lww_set = LWW_ElementSet()
        lww_set.remove('a', 0)
        self.assertFalse(lww_set.exist('a'))
        lww_set.add('a', 1)
        self.assertTrue(lww_set.exist('a'))
        self.assertEqual(lww_set.get(), ['a'])

    def test11(self):
        lww_set = LWW_ElementSet()
        lww_set.add('a', 1)
        self.assertTrue(lww_set.exist('a'))
        lww_set.remove('a', 2)
        self.assertFalse(lww_set.exist('a'))
        self.assertEqual(lww_set.get(), [])

    def test12(self):
        lww_set = LWW_ElementSet()
        lww_set.remove('a', 2)
        self.assertFalse(lww_set.exist('a'))
        lww_set.add('a', 1)
        self.assertFalse(lww_set.exist('a'))
        self.assertEqual(lww_set.get(), [])

    # Test 13 - 14 test for associativity property: (a + b) + c = a + (b + c)
    def test13(self):
        lww_set = LWW_ElementSet()
        lww_set.add('a', 1)
        self.assertTrue(lww_set.exist('a'))
        lww_set.add('b', 2)
        self.assertTrue(lww_set.exist('b'))
        lww_set.remove('b', 3)
        self.assertFalse(lww_set.exist('b'))
        self.assertEqual(lww_set.get(), ['a'])

    def test14(self):
        lww_set = LWW_ElementSet()
        lww_set.add('b', 2)
        self.assertTrue(lww_set.exist('b'))
        lww_set.remove('b', 3)
        self.assertFalse(lww_set.exist('b'))
        lww_set.add('a', 1)
        self.assertTrue(lww_set.exist('a'))
        self.assertEqual(lww_set.get(), ['a'])

if __name__ == "__main__":
    unittest.main()