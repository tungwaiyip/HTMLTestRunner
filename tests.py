import unittest
import HTMLTestRunner


class PassTestCase(unittest.TestCase):
    def test_pass(self):
        """A test that passes"""
        self.assertTrue(True)


class FailTestCase(unittest.TestCase):
    def test_fail(self):
        """A test that fails"""
        self.assertTrue(False)


class ErrorTestCase(unittest.TestCase):
    def test_error(self):
        """A test that raise an exception"""
        raise Exception


class SkipBeforeTestMethodTestCase(unittest.TestCase):
    @unittest.skip('Skip before test method')
    def test_skip_before_test_method(self):
        pass


class SkipInsideTestMethodTestCase(unittest.TestCase):
    def test_skip_inside_test_method(self):
        self.skipTest('Skip inside test method')


@unittest.skip('Skip class')
class SkipClassTestCase(unittest.TestCase):
    def test_skip_class(self):
        pass

if __name__ == '__main__':
    html_report = open('sample_test_report.html', 'w')
    runner = HTMLTestRunner.HTMLTestRunner(stream=html_report, verbosity=2)

    tests = [ErrorTestCase, FailTestCase, PassTestCase,
             SkipBeforeTestMethodTestCase, SkipClassTestCase,
             SkipInsideTestMethodTestCase]

    loader = unittest.TestLoader()
    t_list = []
    for t in tests:
        cases = loader.loadTestsFromTestCase(t)
        t_list.append(cases)
    suite = unittest.TestSuite(t_list)

    runner.run(suite)
