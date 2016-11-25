import unittest

import HTMLTestRunner


class PassTestCase(unittest.TestCase):
    def test_pass(self):
        """A test that passes"""
        print 'test_pass'
        self.assertTrue(True)


class FailTestCase(unittest.TestCase):
    def test_fail(self):
        """A test that fails"""
        print 'test_fail'
        self.assertTrue(False)


class ErrorTestCase(unittest.TestCase):
    def test_error(self):
        """A test that raise an exception"""
        print 'test_error'
        raise Exception


class SkipBeforeTestMethodTestCase(unittest.TestCase):
    @unittest.skip('Skip before test method')
    def test_skip_before_test_method(self):
        print 'test_skip_before_test_method'
        pass


class SkipInsideTestMethodTestCase(unittest.TestCase):
    def test_skip_inside_test_method(self):
        print 'test_skip_inside_test_method'
        self.skipTest('Skip inside test method')


@unittest.skip('Skip class')
class SkipClassTestCase(unittest.TestCase):
    def test_skip_class(self):
        print 'test_skip_class'
        pass


def fake_attrs():
    g2attrs = [
        ('My Project Name', 'Fake Project Name'),
        ('Reponsible Team', 'Fake Team'),
        ('Build Number', '42'),
    ]
    g3attrs = [
        ('Produc Under Test', 'The Fake Product Site'),
        ('Product Team', 'Fake Product Team')
    ]
    attrs = {'group2': g2attrs, 'group3': g3attrs}
    return attrs


def fake_description():
    desc = """This is a fake description
    divided in two lines."""
    return desc


if __name__ == '__main__':
    # Create the report file
    html_report = open('sample_test_report.html', 'w')
    # Create the runner and set the file as output and higher verbosity
    runner = HTMLTestRunner.HTMLTestRunner(stream=html_report, verbosity=2, attrs=fake_attrs(),
                                           description=fake_description())
    # Create a test list
    tests = [
        ErrorTestCase, FailTestCase, PassTestCase, SkipBeforeTestMethodTestCase, SkipClassTestCase,
        SkipInsideTestMethodTestCase
    ]
    # Load test cases
    loader = unittest.TestLoader()
    # Create a SuiteCase
    test_list = []
    for test in tests:
        cases = loader.loadTestsFromTestCase(test)
        test_list.append(cases)
    suite = unittest.TestSuite(test_list)
    # Run the suite
    runner.run(suite)
