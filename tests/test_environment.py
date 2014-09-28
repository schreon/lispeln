from lispeln.environment import Environment
from lispeln.expressions import Symbol

__author__ = 'schreon'

import unittest


class EnvironmentTestCase(unittest.TestCase):
    def test_environment(self):
        root = Environment(None, a=1, b=2)

        for key, val in root.iteritems():
            self.assertIsInstance(key, Symbol)
            self.assertIn(val, [1, 2])

        child1 = Environment(root, c=3)
        child2 = Environment(root, d=4)

        self.assertIn('a', child1)
        self.assertIn('b', child1)
        self.assertIn('c', child1)
        self.assertNotIn('d', child1)

        self.assertIn('a', child2)
        self.assertIn('b', child2)
        self.assertNotIn('c', child2)
        self.assertIn('d', child2)

if __name__ == '__main__':
    unittest.main()
