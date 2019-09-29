#!/usr/bin/env python3

import unittest

def div(a, b):
  if (b == 0):
    raise ArithmeticError
  return a / b

class DivTest(unittest.TestCase):
  def test_pos(self):
    self.assertEqual(div(6, 3), 2)
  
  def test_neg(self):
    self.assertEqual(div(-10, 2), -5)
  
  def test_zero(self):
    with self.assertRaises(ArithmeticError):
      div(1, 0)

if __name__ == "__main__":
  unittest.main()
