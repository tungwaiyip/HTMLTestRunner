在原作者的基础上对整个测试报告进行了汉化处理
此版本增加了如下功能
- 测试报告完全汉化，包括错误日志的中文处理
- 针对selenium UI测试增加失败自动截图功能
- 增加失败自动重试功能
- 测试报告增加饼图统计
- 同事兼容python2.x 和3.x

# selenium 截图
截图功能根据测试截图，提取用例中的driver变量获取webdriver对象，所以要实现截图功能必须定义webdriver 为driver
```python
def setUp(self):
    self.driver = webdriver.Chrome()
```
# 用例失败重试
在实例化HTMLTestRunner 对象时最佳参数，retry，指定重试次数，重试的测试也会收集到测试报告中。
`HTMLTestRunner(title="带截图的测试报告",description="小试牛刀",stream=open("test1.html","wb"),verbosity=2，retry=1)`

详情请参考 test_screemshot.py