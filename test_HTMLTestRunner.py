# -*- coding: utf-8 -*-

import io as StringIO
import sys
import unittest
import HTMLTestRunner

import tests
from tests.SampleTestPass import SampleTestPass
from tests.SampleTestFail import SampleTestFail
from tests.SampleTestBasic import SampleTestBasic

class TestHTMLTestRunner(unittest.TestCase):
    
    def setUp(self):
   
        self.suite = unittest.TestSuite()
        self.loader = unittest.TestLoader()

        self.suite.addTests(self.loader.loadTestsFromModule(tests.SampleTestPass))
        self.suite.addTests(self.loader.loadTestsFromModule(tests.SampleTestFail))
        self.suite.addTests(self.loader.loadTestsFromModule(tests.SampleTestBasic))

        self.results_output_buffer = StringIO.StringIO()
        HTMLTestRunner.HTMLTestRunner(stream=self.results_output_buffer).run(self.suite)
        self.byte_output = self.results_output_buffer.getvalue()

    def test_SampleTestPass(self):
        output1="".join(self.byte_output.split())
        output2="".join(SampleTestPass.EXPECTED_RESULT.split())
        self.assertGreater(output1.find(output2),0)
    
    @unittest.skip("Test Skipping")
    def test_SampleTestSkip(self):
        self.fail("This error should never be displayed")
        
    def test_SampleTestFail(self):
        output1="".join(self.byte_output.split())
        output2="".join(SampleTestFail.EXPECTED_RESULT.split())
        self.assertGreater(output1.find(output2),0)
        
    def test_SampleTestBasic(self):
        output1="".join(self.byte_output.split())
        output2="".join(SampleTestBasic.EXPECTED_RESULT.split())
        self.assertGreater(output1.find(output2),0)


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHTMLTestRunner)
    unittest.TextTestRunner().run(suite)

if __name__ == "__main__":
    main()
