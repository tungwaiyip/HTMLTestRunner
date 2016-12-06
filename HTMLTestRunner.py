import StringIO
import datetime
import sys
import unittest
from xml.sax import saxutils

__author__ = "Wai Yip Tung"
__version__ = "2.0.0"


# TODO: color stderr
# TODO: simplify javascript using , more than 1 class in the class attribute?


# ------------------------------------------------------------------- #
# The redirectors below are used to capture output during testing.
# Output sent to sys.stdout and sys.stderr are automatically captured.
# However in some cases sys.stdout is already cached before
# HTMLTestRunner is invoked (e.g. calling logging.basicConfig).
# In order to capture those output, use the redirectors for the cached
# stream.
# e.g.
#   >>> logging.basicConfig(stream=HTMLTestRunner.stdout_redirector)
#   >>>
# ------------------------------------------------------------------- #


def to_unicode(s):
    try:
        return unicode(s)
    except UnicodeDecodeError:
        # s is non ascii byte string
        return s.decode('unicode_escape')


class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """

    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(to_unicode(s))

    def writelines(self, lines):
        lines = map(to_unicode, lines)
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()


stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)


class TemplateMixin(object):
    """
    Define a HTML template for report customization and generation.

    Overall structure of an HTML report

    HTML
    +------------------------+
    |<html>                  |
    |  <head>                |
    |                        |
    |   STYLESHEET           |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </head>               |
    |                        |
    |  <body>                |
    |                        |
    |   HEADING              |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   REPORT               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   ENDING               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </body>               |
    |</html>                 |
    +------------------------+
    """

    STATUS = {
        0: 'PASS',
        1: 'FAIL',
        2: 'ERROR',
        3: 'SKIP',
    }

    DEFAULT_TITLE = 'Test Report'
    DEFAULT_DESCRIPTION = 'This is a simple description. And it has two phrases.'

    # ------------------------------------------------------------------- #
    # HTML Template
    # ------------------------------------------------------------------- #

    # variables: (title, generator, stylesheet, heading, report, ending)
    HTML_TEMPLATE = open('templates/report.html', 'r').read().encode('utf-8')

    # ------------------------------------------------------------------- #
    # Stylesheet
    # ------------------------------------------------------------------- #
    # alternatively use a <link> for external style sheet, e.g.
    #   <link rel="stylesheet" href="$url" type="text/css">
    STYLESHEET_TEMPLATE = open('templates/head_inserts.html', 'r').read() \
        .encode('utf-8')

    # ------------------------------------------------------------------- #
    # Heading
    # ------------------------------------------------------------------- #
    # variables: (title, parameters, description)
    HEADING_TEMPLATE = open('templates/header.html', 'r').read() \
        .encode('utf-8')

    # variables: (name, value)
    HEADING_ATTRIBUTE_TEMPLATE = open('templates/header_parameters.html', 'r')\
        .read().encode('utf-8')

    # ------------------------------------------------------------------- #
    # Report
    # ------------------------------------------------------------------- #
    # variables: (test_list, count, Pass, fail, error, skip)
    REPORT__TABLE_TEMPLATE = open('templates/result_table.html', 'r') \
        .read().encode('utf-8')

    # variables: (style, desc, count, Pass, fail, error, cid)
    REPORT_CLASS_TEMPLATE = open('templates/test_class.html', 'r').read()\
        .encode('utf-8')

    # variables: (tid, Class, style, desc, status)
    REPORT_TEST_WITH_OUTPUT_TMPL = \
        open('templates/report_test_with_output.html', 'r').read()\
        .encode('utf-8')

    # variables: (tid, Class, style, desc, status)
    REPORT_TEST_NO_OUTPUT_TEMPLATE = \
        open('templates/report_test_no_output.html', 'r').read()\
        .encode('utf-8')

    # variables: (id, output)
    REPORT_TEST_OUTPUT_TEMPLATE = r"""%(id)s: %(output)s"""

    # ------------------------------------------------------------------- #
    # ENDING
    # ------------------------------------------------------------------- #
    ENDING_TEMPLATE = open('templates/footer.html', 'r').read()\
        .encode('utf-8')


# -------------------- The end of the Template class -------------------

TestResult = unittest.TestResult


class _TestResult(TestResult):
    # Note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability
    # compares to unittest._TextTestResult.

    def __init__(self, verbosity=1):
        super(_TestResult, self).__init__()
        # TestResult.__init__(self)
        self.outputBuffer = StringIO.StringIO()
        self.stdout0 = None
        self.stderr0 = None
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.skip_count = 0
        self.verbosity = verbosity

        # result is a list of result in 5 tuple
        # (
        #   result code (0: success; 1: fail; 2: error; 3: skip),
        #   TestCase object,
        #   Test output (byte string),
        #   stack trace,
        # )
        self.result = []

    def startTest(self, test):
        TestResult.startTest(self, test)
        # just one buffer for both stdout and stderr
        self.outputBuffer = StringIO.StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector

    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()

    def stopTest(self, test):
        # Usually one of addSuccess, addError or addFailure
        # would have been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(),
        # which is guaranteed to be called.
        self.complete_output()

    def addSuccess(self, test):
        self.success_count += 1
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        self.result.append((0, test, output, ''))
        if self.verbosity > 1:
            sys.stderr.write('passed  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('.')

    def addSkip(self, test, reason):
        self.skip_count += 1
        TestResult.addSkip(self, test, reason)
        output = self.complete_output()
        self.result.append((3, test, output, reason))
        if self.verbosity > 1:
            sys.stderr.write('skipped ')
            sys.stderr.write(str(test))
            sys.stderr.write(' - ' + str(reason))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('S')

    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('error   ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')

    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('failed  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')


def sort_result(result_list):
    # unittest does not seems to run in any particular order.
    # Here at least we want to group them together by class.
    rmap = {}
    classes = []
    for n, t, o, e in result_list:
        cls = t.__class__
        if cls not in rmap:
            rmap[cls] = []
            classes.append(cls)
        rmap[cls].append((n, t, o, e))
    r = [(clazz, rmap[clazz]) for clazz in classes]
    return r


class HTMLTestRunner(TemplateMixin):
    def __init__(self, stream=sys.stdout, verbosity=1, title=None,
                 description=None, attrs=None):
        self.stream = stream
        self.verbosity = verbosity

        if title is None:
            self.title = self.DEFAULT_TITLE
        else:
            self.title = title

        if description is None:
            self.description = self.DEFAULT_DESCRIPTION
        else:
            self.description = description

        self.attributes = attrs

        self.startTime = datetime.datetime.now()
        self.stopTime = None

    def run(self, test):
        """Run the given test case or test suite."""
        result = _TestResult(self.verbosity)
        test(result)
        self.stopTime = datetime.datetime.now()
        self.generate_report(result)
        total_time = self.stopTime - self.startTime
        print >> sys.stderr, '\nTime Elapsed: %s' % total_time
        return result

    def get_report_attributes(self, result):
        """
        Return report attributes as a list of tuples with (name, value).
        Override this to add custom attributes.
        """
        start_time = str(self.startTime)
        duration = str(self.stopTime - self.startTime)
        statuses = []
        if result.success_count:
            statuses.append('Passed %s' % result.success_count)
        if result.skip_count:
            statuses.append('Skipped %s' % result.skip_count)
        if result.failure_count:
            statuses.append('Failed %s' % result.failure_count)
        if result.error_count:
            statuses.append('Errors %s' % result.error_count)
        if statuses:
            statuses = ', '.join(statuses)
        else:
            statuses = 'None'
        group1 = [
            ('Start Time', start_time),
            ('Stop Time', str(self.stopTime)),
            ('Duration', duration),
            ('Status', statuses),
        ]

        return group1

    def generate_report(self, result):
        generator = 'HTMLTestRunner %s' % __version__
        stylesheet = self._generate_stylesheet()
        heading = self._generate_heading(result)
        report = self._generate_report(result)
        ending = self._generate_ending()
        output = self.HTML_TEMPLATE % dict(
            title=saxutils.escape(self.title),
            generator=generator,
            version=__version__,
            head_inserts=stylesheet,
            header=heading,
            result_table=report,
            footer=ending,
        )
        self.stream.write(output.encode('utf8'))

    def _generate_stylesheet(self):
        return self.STYLESHEET_TEMPLATE

    def _parse_attributes_group(self, group):
        attrs_list = []
        for attr_name, attr_value in group:
            attr_line = self.HEADING_ATTRIBUTE_TEMPLATE % dict(
                name=saxutils.escape(attr_name),
                value=saxutils.escape(attr_value),
            )
            attrs_list.append(attr_line)
        return attrs_list

    def _generate_heading(self, result):
        g1 = self.get_report_attributes(result)
        g2 = self.attributes['group2']
        g3 = self.attributes['group3']

        pg1 = self._parse_attributes_group(g1)
        pg2 = self._parse_attributes_group(g2)
        pg3 = self._parse_attributes_group(g3)

        heading = self.HEADING_TEMPLATE % dict(
            title=saxutils.escape(self.title),
            parameters_1=''.join(pg1),
            parameters_2=''.join(pg2),
            parameters_3=''.join(pg3),
            description=saxutils.escape(self.description),
        )
        return heading

    def _generate_report(self, result):
        rows = []
        sorted_result = sort_result(result.result)
        for cid, (cls, cls_results) in enumerate(sorted_result):
            # subtotal for a class
            np = nf = ne = ns = 0
            for n, t, o, e in cls_results:
                if n == 0:
                    np += 1
                elif n == 1:
                    nf += 1
                elif n == 2:
                    ne += 1
                elif n == 3:
                    ns += 1
                    # else:
                    #     # ne += 1
                    #     print 'TESTING'

            # format class description
            if cls.__module__ == "__main__":
                name = cls.__name__
            else:
                name = "%s.%s" % (cls.__module__, cls.__name__)
            doc = cls.__doc__ and cls.__doc__.split("\n")[0] or ""
            desc = doc and '%s: %s' % (name, doc) or name

            s = ne > 0 and 'errorClass' \
                or nf > 0 and 'failClass' \
                or ns > 0 and 'skipClass' \
                or 'passClass'

            row = self.REPORT_CLASS_TEMPLATE % dict(
                style=s,
                desc=desc,
                count=np + nf + ne + ns,
                Pass=np,
                fail=nf,
                error=ne,
                skip=ns,
                cid='c%s' % (cid + 1),
            )
            rows.append(row)

            for tid, (n, t, o, e) in enumerate(cls_results):
                self._generate_report_test(rows, cid, tid, n, t, o, e)
        result_sum = result.success_count \
            + result.failure_count \
            + result.error_count \
            + result.skip_count
        report = self.REPORT__TABLE_TEMPLATE % dict(
            test_list=''.join(rows),
            count=str(result_sum),
            Pass=str(result.success_count),
            fail=str(result.failure_count),
            error=str(result.error_count),
            skip=str(result.skip_count)
        )
        return report

    def _generate_report_test(self, rows, class_id, test_id, n, t, output, e):
        # e.g. 'pt1.1', 'ft1.1', etc
        has_output = bool(output or e)
        test_id = (n == 0 and 'p' or 'f') + 't%s.%s' \
                                            % (class_id + 1, test_id + 1)
        name = t.id().split('.')[-1]
        doc = t.shortDescription() or ""
        desc = doc and ('%s: %s' % (name, doc)) or name
        # tmpl = has_output and self.REPORT_TEST_WITH_OUTPUT_TMPL or \
        #        self.REPORT_TEST_NO_OUTPUT_TMPL
        if has_output:
            tmpl = self.REPORT_TEST_WITH_OUTPUT_TMPL
        else:
            tmpl = self.REPORT_TEST_NO_OUTPUT_TEMPLATE
        # o and e should be byte string because
        # they are collected from stdout and stderr?
        if isinstance(output, str):
            # TODO: some problem with 'string_escape':
            # it escape \n and mess up formatting
            # uo = unicode(o.encode('string_escape'))
            uo = output.decode('latin-1')
        else:
            uo = output
        if isinstance(e, str):
            # TODO: some problem with 'string_escape':
            # it escape \n and mess up formatting
            # ue = unicode(e.encode('string_escape'))
            ue = e.decode('latin-1')
        else:
            ue = e

        script = self.REPORT_TEST_OUTPUT_TEMPLATE % dict(
            id=test_id,
            output=saxutils.escape(uo.strip() + ue.strip()),
        )
        row = tmpl % dict(
            tid=test_id,
            Class=(n == 0 and 'hiddenRow' or 'none'),
            style=n == 2 and 'bg-info' or (
                n == 1 and 'bg-danger' or n == 3 and 'bg-warning' or 'bg-success'),
            desc=desc,
            script=script,
            status=self.STATUS[n],
        )
        rows.append(row)
        if not has_output:
            return

    def _generate_ending(self):
        return self.ENDING_TEMPLATE


##############################################################################
# Facilities for running tests from the command line
##############################################################################

# Note: Reuse unittest.TestProgram to launch test. In the future we may
# build our own launcher to support more specific command line
# parameters like test title, CSS, etc.
class TestProgram(unittest.TestProgram):
    """
    A variation of the unittest.TestProgram. Please refer to the base
    class for command line parameters.
    """

    def runTests(self):
        # Pick HTMLTestRunner as the default test runner.
        # base class's testRunner parameter is not useful because it means
        # we have to instantiate HTMLTestRunner before we know self.verbosity.
        if self.testRunner is None:
            self.testRunner = HTMLTestRunner(verbosity=self.verbosity)
        unittest.TestProgram.runTests(self)


main = TestProgram

##############################################################################
# Executing this module from the command line
##############################################################################

if __name__ == "__main__":
    main(module=None)
