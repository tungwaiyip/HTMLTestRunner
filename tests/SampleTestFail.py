import unittest


class SampleTestFail(unittest.TestCase):
    EXPECTED_RESULT = """
<tr class='failClass'>
    <td>tests.SampleTestFail.SampleTestFail</td>
    <td>1</td>
    <td>0</td>
    <td>1</td>
    <td>0</td>
    <td><a href="javascript:showClassDetail('c2',1)">Detail</a></td>
</tr>

<tr id='ft2.1' class='none'>
    <td class='failCase'><div class='testcase'>test_run_1</div></td>
    <td colspan='5' align='center'>

    <!--css div popup start-->
    <a class="popup_link" onfocus='this.blur();' href="javascript:showTestDetail('div_ft2.1')" >
        fail</a>

    <div id='div_ft2.1' class="popup_window">
        <div style='text-align: right; color:red;cursor:pointer'>
        <a onfocus='this.blur();' onclick="document.getElementById('div_ft2.1').style.display = 'none' " >
           [x]</a>
        </div>
        <pre>
        
ft2.1: Traceback (most recent call last):
    """
    
    def test_run_1(self):
        self.fail()
