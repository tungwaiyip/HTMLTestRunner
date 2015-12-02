import unittest
import sys

class SampleTestBasic(unittest.TestCase):
    EXPECTED_RESULT = """
<tr class='errorClass'>
    <td>tests.SampleTestBasic.SampleTestBasic</td>
    <td>4</td>
    <td>2</td>
    <td>1</td>
    <td>1</td>
    <td><a href="javascript:showClassDetail('c3',4)">Detail</a></td>
</tr>

<tr id='pt3.1' class='hiddenRow'>
    <td class='none'><div class='testcase'>test_run_1</div></td>
    <td colspan='5' align='center'>

    <!--css div popup start-->
    <a class="popup_link" onfocus='this.blur();' href="javascript:showTestDetail('div_pt3.1')" >
        pass</a>

    <div id='div_pt3.1' class="popup_window">
        <div style='text-align: right; color:red;cursor:pointer'>
        <a onfocus='this.blur();' onclick="document.getElementById('div_pt3.1').style.display = 'none' " >
           [x]</a>
        </div>
        <pre>
        
pt3.1: basic test


        </pre>
    </div>
    <!--css div popup end-->

    </td>
</tr>

<tr id='pt3.2' class='hiddenRow'>
    <td class='none'><div class='testcase'>test_run_2</div></td>
    <td colspan='5' align='center'>

    <!--css div popup start-->
    <a class="popup_link" onfocus='this.blur();' href="javascript:showTestDetail('div_pt3.2')" >
        pass</a>

    <div id='div_pt3.2' class="popup_window">
        <div style='text-align: right; color:red;cursor:pointer'>
        <a onfocus='this.blur();' onclick="document.getElementById('div_pt3.2').style.display = 'none' " >
           [x]</a>
        </div>
        <pre>
        
pt3.2: basic test
basic test


        </pre>
    </div>
    <!--css div popup end-->

    </td>
</tr>

<tr id='ft3.3' class='none'>
    <td class='failCase'><div class='testcase'>test_run_3</div></td>
    <td colspan='5' align='center'>

    <!--css div popup start-->
    <a class="popup_link" onfocus='this.blur();' href="javascript:showTestDetail('div_ft3.3')" >
        fail</a>

    <div id='div_ft3.3' class="popup_window">
        <div style='text-align: right; color:red;cursor:pointer'>
        <a onfocus='this.blur();' onclick="document.getElementById('div_ft3.3').style.display = 'none' " >
           [x]</a>
        </div>
        <pre>
        
ft3.3: basic test
basic test
    """
    MESSAGE = 'basic test'
    
    def test_run_1(self):
        print(self.MESSAGE)

    def test_run_2(self):
        print(self.MESSAGE, file=sys.stderr)
    
    def test_run_3(self):
        self.fail(self.MESSAGE)
        
    def test_run_4(self):
        raise RuntimeError(self.MESSAGE)
