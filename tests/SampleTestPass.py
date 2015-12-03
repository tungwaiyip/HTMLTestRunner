import unittest

class SampleTestPass(unittest.TestCase):
    EXPECTED_RESULT = """
<tr class='passClass'>
    <td>tests.SampleTestPass.SampleTestPass</td>
    <td>1</td>
    <td>1</td>
    <td>0</td>
    <td>0</td>
    <td><a href="javascript:showClassDetail('c1',1)">Detail</a></td>
</tr>

<tr id='pt1.1' class='hiddenRow'>
    <td class='none'><div class='testcase'>test_run_1</div></td>
    <td colspan='5' align='center'>pass</td>
</tr>
    """

    def test_run_1(self):
        pass