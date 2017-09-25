# HTMLTestRunner 汉化版
在原作者的基础上对整个测试报告进行了汉化处理
此版本增加了如下功能
- 测试报告完全汉化，包括错误日志的中文处理
- 针对selenium UI测试增加失败自动截图功能
- 增加失败自动重试功能
- 增加饼图统计
- 同时兼容python2.x 和3.x

#报告汉化
![](https://testerhome.com/uploads/photo/2017/d3adb2cd-56e6-4ea0-8dad-d0067467d3ac.png!large)
# selenium 截图
截图功能根据测试结果，当结果为fail或error时自动截图
截图方法在_TestResult 的测试结果收集中，可以根据自己使用的框架不同自行调整，selenium 使用的是get_screenshot_as_base64 获取页面截图的base64编码，避免了图片文件存储的尴尬
![](https://testerhome.com/uploads/photo/2017/6c499d11-e8a2-4988-88b1-0251347de506.png!large)
因此要提取用例中的driver变量获取webdriver对象，所以要实现截图功能必须定义在用例中定义webdriver 为driver
```python
def setUp(self):
    self.driver = webdriver.Chrome()
```
**效果**
![](https://testerhome.com/uploads/photo/2017/db1ca9ab-2dec-476b-90f1-6b7d27689720.png!large)

# 用例失败重试
在实例化HTMLTestRunner 对象时追加参数，retry，指定重试次数，重试的测试也会收集到测试报告中。
`HTMLTestRunner(title="带截图的测试报告",description="小试牛刀",stream=open("test1.html","wb"),verbosity=2，retry=1)`
![](https://testerhome.com/uploads/photo/2017/acd3a581-46f9-4872-ae1a-d231ed9227d4.png!large)
