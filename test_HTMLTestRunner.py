# -*- coding: utf-8 -*-

import StringIO
import sys
import unittest
import HTMLTestRunner


# ----------------------------------------------------------------------
def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)


def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape')


# ----------------------------------------------------------------------
# Sample tests to drive the HTMLTestRunner
class SampleTest0(unittest.TestCase):
    """ A class that passes.

    This simple class has only one test case that passes.
    """
    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)

    def test_pass_no_output(self):
        """        test description
        """
        pass


class SampleTest1(unittest.TestCase):
    """ A class that fails.

    This simple class has only one test case that fails.
    """
    def test_fail(self):
        u""" test description (描述) """
        self.fail()


class SampleOutputTestBase(unittest.TestCase):
    """ Base TestCase. Generates 4 test cases x different content type. """
    def test_1(self):
        print self.MESSAGE

    def test_2(self):
        print >>sys.stderr, self.MESSAGE

    def test_3(self):
        self.fail(self.MESSAGE)

    def test_4(self):
        raise RuntimeError(self.MESSAGE)


class SampleTestBasic(SampleOutputTestBase):
    MESSAGE = 'basic test'


class SampleTestHTML(SampleOutputTestBase):
    MESSAGE = 'the message is 5 symbols: <>&"\'\nplus the HTML entity string: [&copy;] on a second line'


class SampleTestLatin1(SampleOutputTestBase):
    MESSAGE = u'the message is áéíóú'.encode('latin-1')


class SampleTestUnicode(SampleOutputTestBase):
    u""" Unicode (統一碼) test """
    MESSAGE = u'the message is \u8563'
    # 2006-04-25 Note: Exception would show up as
    # AssertionError: <unprintable instance object>
    #
    # This seems to be limitation of traceback.format_exception()
    # Same result in standard unittest.

    # 2011-03-28 Note: I think it is fixed in Python 2.6
    def test_pass(self):
        u""" A test with Unicode (統一碼) docstring """
        pass


# ------------------------------------------------------------------------
# This is the main test on HTMLTestRunner
class TestHTMLTestRunner(unittest.TestCase):

    def test0(self):
        self.suite = unittest.TestSuite()
        buf = StringIO.StringIO()
        runner = HTMLTestRunner.HTMLTestRunner(buf)
        runner.run(self.suite)
        # didn't blow up? ok.
        self.assert_('</html>' in buf.getvalue())

    def test_main(self):
        # Run HTMLTestRunner. Verify the HTML report.

        # suite of TestCases
        self.suite = unittest.TestSuite()
        self.suite.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(SampleTest0),
            unittest.defaultTestLoader.loadTestsFromTestCase(SampleTest1),
            unittest.defaultTestLoader.loadTestsFromTestCase(SampleTestBasic),
            unittest.defaultTestLoader.loadTestsFromTestCase(SampleTestHTML),
            unittest.defaultTestLoader.loadTestsFromTestCase(SampleTestLatin1),
            unittest.defaultTestLoader.loadTestsFromTestCase(SampleTestUnicode),
            ])

        # Invoke TestRunner
        buf = StringIO.StringIO()
        # runner = unittest.TextTestRunner(buf)       #0DEBUG: this is the unittest baseline
        runner = HTMLTestRunner.HTMLTestRunner(
                    stream=buf,
                    title='<Demo Test>',
                    description='This demonstrates the report output by HTMLTestRunner.'
                    )
        runner.run(self.suite)

        # Define the expected output sequence. This is imperfect but should
        # give a good sense of the well being of the test.
        expected = u"""
Demo Test

>SampleTest0:

>SampleTest1:

>SampleTestBasic
>test_1<
pass
basic test

>test_2<
pass
basic test

>test_3<
fail
AssertionError: basic test

>test_4<
error
RuntimeError: basic test


>SampleTestHTML
>test_1<
pass
the message is 5 symbols: &lt;&gt;&amp;"'
plus the HTML entity string: [&amp;copy;] on a second line

>test_2<
pass
the message is 5 symbols: &lt;&gt;&amp;"'
plus the HTML entity string: [&amp;copy;] on a second line

>test_3<
fail
AssertionError: the message is 5 symbols: &lt;&gt;&amp;"'
plus the HTML entity string: [&amp;copy;] on a second line

>test_4<
error
RuntimeError: the message is 5 symbols: &lt;&gt;&amp;"'
plus the HTML entity string: [&amp;copy;] on a second line


>SampleTestLatin1
>test_1<
pass
the message is áéíóú

>test_2<
pass
the message is áéíóú

>test_3<
fail
AssertionError: the message is áéíóú

>test_4<
error
RuntimeError: the message is áéíóú


>SampleTestUnicode
>test_1<
pass
the message is \u8563

>test_2<
pass
the message is \u8563

>test_3<
fail
AssertionError:

>test_4<
error
RuntimeError:

Total
>19<
>10<
>5<
>4<
</html>
"""
        # check out the output
        byte_output = buf.getvalue()
        # output the main test output for debugging & demo
        print byte_output
        # HTMLTestRunner pumps UTF-8 output
        output = byte_output.decode('utf-8')
        self._checkoutput(output, expected)

    def _checkoutput(self, output, EXPECTED):
        i = 0
        for lineno, p in enumerate(EXPECTED.splitlines()):
            if not p:
                continue
            j = output.find(p, i)
            if j < 0:
                self.fail(safe_str('Pattern not found lineno %s: "%s"' % (lineno+1, p)))
            i = j + len(p)


##############################################################################
# Executing this module from the command line
##############################################################################
if __name__ == "__main__":
    if len(sys.argv) > 1:
        argv = sys.argv
    else:
        argv = ['test_HTMLTestRunner.py', 'TestHTMLTestRunner']
    unittest.main(argv=argv, verbosity=2)
    # Testing HTMLTestRunner with HTMLTestRunner would work. But instead
    # we will use standard library's TextTestRunner to reduce the nesting
    # that may confuse people.
    # HTMLTestRunner.main(argv=argv)
