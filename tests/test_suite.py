import unittest
from tests.test_constants import ConstantsTestCase
from tests.test_parser import ParserTestCase
from tests.test_printer import PrinterTestCase
from tests.test_recursive import RecursiveEvaluatorTestCase
from tests.test_scanner import ScannerTestCase


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(ScannerTestCase))
suite.addTest(unittest.makeSuite(ParserTestCase))
suite.addTest(unittest.makeSuite(ConstantsTestCase))
suite.addTest(unittest.makeSuite(PrinterTestCase))
suite.addTest(unittest.makeSuite(RecursiveEvaluatorTestCase))

runner = unittest.TextTestRunner()
runner.run(suite)