#-*- coding: utf-8 -*-
# @Time    : 2017/9/6 11:26
# @File    : aaa.py
# @Author  : 守望@天空~
"""HTMLTestRunner 截图版示例"""
from selenium import webdriver
import unittest
import time
from HTMLTestRunner import  HTMLTestRunner

class case_01(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.addCleanup(self.cleanup)

    def cleanup(self):
        time.sleep(1)

    def test_case1(self):
        """百度首页"""
        self.driver.get("https://www.baidu.com")
        self.driver.find_element_by_id('kw').send_keys(u'百度一下')
        self.driver.find_element_by_id('su').click()
        self.assertTrue(True)

    def test_case2(self):
        """搜狗首页"""
        self.driver.get("http://www.sogou.com")
        self.assertTrue(False,u'中文')


    def test_case3(self):
        """ QQ邮箱"""
        self.driver.get("https://mail.qq.com")
        self.assertIn(u"中文",u'中华')


    def test_case4(self):
        u""" 淘宝"""
        self.driver.get("http://www.taobao.com/")
        self.assertTrue(True)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(case_01)
    runer = HTMLTestRunner(title="带截图的测试报告",description="小试牛刀",stream=open("sample_test_report.html","wb"),verbosity=2,retry=2)
    runer.run(suite)






