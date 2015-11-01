import datetime
import StringIO
import sys
import unittest
from xml.sax import saxutils

__author__ = "Wai Yip Tung"
__version__ = "0.8.3"


# TODO: color stderr
# TODO: simplify javascript using ,ore than 1 class in the class attribute?


# ---------------------------------------------------------------------------- #
# The redirectors below are used to capture output during testing. Output
# sent to sys.stdout and sys.stderr are automatically captured. However
# in some cases sys.stdout is already cached before HTMLTestRunner is
# invoked (e.g. calling logging.basicConfig). In order to capture those
# output, use the redirectors for the cached stream.
#
# e.g.
#   >>> logging.basicConfig(stream=HTMLTestRunner.stdout_redirector)
#   >>>
# ---------------------------------------------------------------------------- #


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

    DEFAULT_TITLE = 'Unit Test Report'
    DEFAULT_DESCRIPTION = ''

# ---------------------------------------------------------------------------- #
# HTML Template
# ---------------------------------------------------------------------------- #
    # variables: (title, generator, stylesheet, heading, report, ending)
    HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>%(title)s</title>
    <meta name="generator" content="%(generator)s"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    %(stylesheet)s
</head>
<body>
<script language="javascript" type="text/javascript"><!--
output_list = Array();

/* level - 0:Summary; 1:Failed; 2:All; 3:Skipped */
function showCase(level) {
    trs = document.getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        tr = trs[i];
        id = tr.id;
        if (id.substr(0,2) == 'ft') {
            if (level < 1) {
                tr.className = 'hiddenRow';
            }
            else {
                tr.className = '';
            }
        }
        if (id.substr(0,2) == 'pt') {
            if (level > 1) {
                tr.className = '';
            }
            else {
                tr.className = 'hiddenRow';
            }
        }
    }
}


function showClassDetail(cid, count) {
    var id_list = Array(count);
    var toHide = 1;
    for (var i = 0; i < count; i++) {
        tid0 = 't' + cid.substr(1) + '.' + (i+1);
        tid = 'f' + tid0;
        tr = document.getElementById(tid);
        if (!tr) {
            tid = 'p' + tid0;
            tr = document.getElementById(tid);
        }
        id_list[i] = tid;
        if (tr.className) {
            toHide = 0;
        }
    }
    for (var i = 0; i < count; i++) {
        tid = id_list[i];
        if (toHide) {
            document.getElementById('div_'+tid).style.display = 'none'
            document.getElementById(tid).className = 'hiddenRow';
        }
        else {
            document.getElementById(tid).className = '';
        }
    }
}


function showTestDetail(div_id){
    var details_div = document.getElementById(div_id)
    var displayState = details_div.style.display
    // alert(displayState)
    if (displayState != 'block' ) {
        displayState = 'block'
        details_div.style.display = 'block'
    }
    else {
        details_div.style.display = 'none'
    }
}


function html_escape(s) {
    s = s.replace(/&/g,'&amp;');
    s = s.replace(/</g,'&lt;');
    s = s.replace(/>/g,'&gt;');
    return s;
}

/* obsoleted by detail in <div>
function showOutput(id, name) {
    var w = window.open("", //url
                    name,
                    "resizable,scrollbars,status,width=800,height=450");
    d = w.document;
    d.write("<pre>");
    d.write(html_escape(output_list[id]));
    d.write("\n");
    d.write("<a href='javascript:window.close()'>close</a>\n");
    d.write("</pre>\n");
    d.close();
}
*/
--></script>

%(heading)s
%(report)s
%(ending)s

</body>
</html>"""

# ---------------------------------------------------------------------------- #
# Stylesheet
# ---------------------------------------------------------------------------- #
# alternatively use a <link> for external style sheet, e.g.
#   <link rel="stylesheet" href="$url" type="text/css">
    STYLESHEET_TMPL = r"""
<style type="text/css" media="screen">
body {
    font-family: verdana, arial, helvetica, sans-serif;
    font-size: 80%;
}

table {
    font-size: 100%;
}

pre { }

/* -- heading --------------------------------------------------------------- */

h1 {
    font-size: 16pt;
    color: gray;
}

.heading {
    margin-top: 0ex;
    margin-bottom: 1ex;
}

.heading .attribute {
    margin-top: 1ex;
    margin-bottom: 0;
}

.heading .description {
    margin-top: 4ex;
    margin-bottom: 6ex;
}

/* -- css div popup --------------------------------------------------------- */

a.popup_link {
}

a.popup_link:hover {
    color: red;
}

.popup_window {
    display: none;
    position: relative;
    width: 95%;
    height: 95%;
    margin: 10px 0 15px 0;
    /*border: solid #627173 1px; */
    padding: 4px;
    background-color: #CCC;
    font-family: "Lucida Console", "Courier New", Courier, monospace;
    text-align: left;
    font-size: 8pt;

    word-wrap: break-word;

}

/* -- report ---------------------------------------------------------------- */

#show_detail_line {
    margin-top: 3ex;
    margin-bottom: 1ex;
}

#result_table {
    width: 100%;
    border-collapse: collapse;
    border: 1px solid black;
}

#header_row {
    font-weight: bold;
    color: white;
    background-color: #777;
}

#result_table td {
    border: 1px solid black;
    border: 1px solid black;
    padding: 2px;
    width: auto;
}

#total_row {
    font-weight: bold;
    background-color: #777;
    color: white;
}

.passClass  { background-color: #0F0; font-weight: bold;}
.failClass  { background-color: #F00; font-weight: bold;}
.errorClass { background-color: #A20; font-weight: bold;}
.skipClass  { background-color: #FF0; font-weight: bold;}

.passCase   { color: #000; }
.failCase   { color: #000; }
.errorCase  { color: #000; }
.skipCase   { color: #000; }

.hiddenRow  { display: none; }
.testcase   { margin-left: 2em; }

#close_button {
    text-align: right;
    color:red;
    cursor:pointer;
    font-weight: bold;
}

/* -- ending ---------------------------------------------------------------- */

#ending { }

</style>"""

# ---------------------------------------------------------------------------- #
# Heading
# ---------------------------------------------------------------------------- #
    # variables: (title, parameters, description)
    HEADING_TMPL = r"""<div class='heading'>
<h1>%(title)s</h1>
%(parameters)s
<p class='description'>%(description)s</p>
</div>"""

    # variables: (name, value)
    HEADING_ATTRIBUTE_TMPL = r"""
    <p class='attribute'><strong>%(name)s:</strong> %(value)s</p>"""


# ---------------------------------------------------------------------------- #
# Report
# ---------------------------------------------------------------------------- #
    # variables: (test_list, count, Pass, fail, error, skip)
    REPORT_TMPL = r"""
<p id='show_detail_line'>Show
<a href='javascript:showCase(0)'>Summary</a>
<a href='javascript:showCase(1)'>Failed</a>
<a href='javascript:showCase(3)'>Skipped</a>
<a href='javascript:showCase(2)'>All</a>
</p>
<table id='result_table'>
<colgroup>
<col align='left' />
<col align='center' />
<col align='center' />
<col align='center' />
<col align='center' />
<col align='center' />
</colgroup>
<tr id='header_row'>
    <td>Test Group/Test case</td>
    <td align='center' >Count</td>
    <td align='center' >Pass</td>
    <td align='center' >Fail</td>
    <td align='center' >Error</td>
    <td align='center' >Skip</td>
    <td align='center' >View</td>
</tr>
%(test_list)s
<tr id='total_row'>
    <td>Total</td>
    <td align='center' >%(count)s</td>
    <td align='center' >%(Pass)s</td>
    <td align='center' >%(fail)s</td>
    <td align='center' >%(error)s</td>
    <td align='center' >%(skip)s</td>
    <td align='center' >&nbsp;</td>
</tr>
</table>"""

    # variables: (style, desc, count, Pass, fail, error, cid)
    REPORT_CLASS_TMPL = r"""
<tr class='%(style)s'>
    <td>%(desc)s</td>
    <td align='center' >%(count)s</td>
    <td align='center' >%(Pass)s</td>
    <td align='center' >%(fail)s</td>
    <td align='center' >%(error)s</td>
    <td align='center' >%(skip)s</td>
    <td align='center' >
        <a href="javascript:showClassDetail('%(cid)s',%(count)s)">Detail</a>
    </td>
</tr>"""

    # variables: (tid, Class, style, desc, status)
    REPORT_TEST_WITH_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='6' align='center'>

    <!--css div popup start-->
    <a class="popup_link"
        onfocus='this.blur();' href="javascript:showTestDetail('div_%(tid)s')">
        %(status)s</a>

    <div id='div_%(tid)s' class="popup_window">
        <div id='close_button'>
        <a onfocus='this.blur();'
        onclick="document.getElementById('div_%(tid)s').style.display = 'none'">
           [x]</a>
        </div>
        <pre>
        %(script)s
        </pre>
    </div>
    <!--css div popup end-->
    </td>
</tr>"""

    # variables: (tid, Class, style, desc, status)
    REPORT_TEST_NO_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'>
        <div class='testcase'>%(desc)s</div>
    </td>
    <td colspan='6' align='center'>%(status)s</td>
</tr>"""

    # variables: (id, output)
    REPORT_TEST_OUTPUT_TMPL = r"""%(id)s: %(output)s"""


# ---------------------------------------------------------------------------- #
# ENDING
# ---------------------------------------------------------------------------- #
    ENDING_TMPL = r"""<div id='ending'>&nbsp;</div>"""


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
            sys.stderr.write('ok ')
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
            sys.stderr.write('E  ')
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
            sys.stderr.write('F  ')
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
    r = [(cls, rmap[cls]) for cls in classes]
    return r


class HTMLTestRunner(TemplateMixin):
    def __init__(self, stream=sys.stdout, verbosity=1, title=None,
                 description=None):
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

        self.startTime = datetime.datetime.now()
        self.stopTime = None

    def run(self, test):
        """Run the given test case or test suite."""
        result = _TestResult(self.verbosity)
        test(result)
        self.stopTime = datetime.datetime.now()
        self.generate_report(result)
        print >> sys.stderr, '\nTime Elapsed: %s' % \
                             (self.stopTime - self.startTime)
        return result

    def get_report_attributes(self, result):
        """
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        """
        start_time = str(self.startTime)[:19]
        duration = str(self.stopTime - self.startTime)
        status = []
        if result.success_count:
            status.append('Pass %s' % result.success_count)
        if result.skip_count:
            status.append('Skip %s' % result.skip_count)
        if result.failure_count:
            status.append('Failure %s' % result.failure_count)
        if result.error_count:
            status.append('Error %s' % result.error_count)
        if status:
            status = ', '.join(status)
        else:
            status = 'none'
        return [
            ('Start Time', start_time),
            ('Duration', duration),
            ('Status', status),
        ]

    def generate_report(self, result):
        report_attrs = self.get_report_attributes(result)
        generator = 'HTMLTestRunner %s' % __version__
        stylesheet = self._generate_stylesheet()
        heading = self._generate_heading(report_attrs)
        report = self._generate_report(result)
        ending = self._generate_ending()
        output = self.HTML_TMPL % dict(
            title=saxutils.escape(self.title),
            generator=generator,
            stylesheet=stylesheet,
            heading=heading,
            report=report,
            ending=ending,
        )
        self.stream.write(output.encode('utf8'))

    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL

    def _generate_heading(self, report_attrs):
        a_lines = []
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                name=saxutils.escape(name),
                value=saxutils.escape(value),
            )
            a_lines.append(line)
        heading = self.HEADING_TMPL % dict(
            title=saxutils.escape(self.title),
            parameters=''.join(a_lines),
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

            row = self.REPORT_CLASS_TMPL % dict(
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
        report = self.REPORT_TMPL % dict(
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
        test_id = (n == 0 and 'p' or 'f') + 't%s.%s' % (class_id+1, test_id+1)
        name = t.id().split('.')[-1]
        doc = t.shortDescription() or ""
        desc = doc and ('%s: %s' % (name, doc)) or name
        # tmpl = has_output and self.REPORT_TEST_WITH_OUTPUT_TMPL or \
        #        self.REPORT_TEST_NO_OUTPUT_TMPL
        if has_output:
            tmpl = self.REPORT_TEST_WITH_OUTPUT_TMPL
        else:
            tmpl = self.REPORT_TEST_NO_OUTPUT_TMPL
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

        script = self.REPORT_TEST_OUTPUT_TMPL % dict(
            id=test_id,
            output=saxutils.escape(uo + ue),
        )
        row = tmpl % dict(
            tid=test_id,
            Class=(n == 0 and 'hiddenRow' or 'none'),
            style=n == 2 and 'errorCase' or (
                n == 1 and 'failCase' or n == 3 and 'skipCase' or 'passCase'),
            desc=desc,
            script=script,
            status=self.STATUS[n],
        )
        rows.append(row)
        if not has_output:
            return

    def _generate_ending(self):
        return self.ENDING_TMPL


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
