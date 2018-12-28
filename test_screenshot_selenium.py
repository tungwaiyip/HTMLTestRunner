# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 11:26
# @File    : aaa.py
# @Author  : 守望@天空~
"""HTMLTestRunner 截图版示例 selenium 版"""
from selenium import webdriver
import unittest
import time
from HTMLTestRunner_cn import HTMLTestRunner
import sys


class case_01(unittest.TestCase):
    """
    def setUp(cls):
        cls.driver = webdriver.Chrome()

    def tearDown(cls):
        cls.driver.quit()

        """
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def add_img(self):
        self.imgs.append(self.driver.get_screenshot_as_base64())
        return True

    def setUp(self):
        # 在是python3.x 中，如果在这里初始化driver ，因为3.x版本 unittest 运行机制不同，会导致用力失败时截图失败
        self.imgs = []
        self.addCleanup(self.cleanup)

    def cleanup(self):
        pass


    def test_case1(self):
        """ 百度搜索
        呵呵呵呵
        """
        print("本次校验没过？")
        print ("超级长"*66)
        self.driver.get("https://www.baidu.com")
        self.add_img()
        self.driver.find_element_by_id('kw').send_keys(u'百度一下')
        self.add_img()
        self.driver.find_element_by_id('su').click()
        time.sleep(1)
        self.add_img()

    def test_case2(self):
        """搜狗首页"""
        self.driver.get("http://www.sogou.com")
        print("本次校验没过？")
        self.assertTrue(False,"这是相当的睿智了")

    def test_case3(self):
        """ QQ邮箱"""
        self.driver.get("https://mail.qq.com")
        self.imgs.append(self.driver.get_screenshot_as_base64())
        print("没法打印？")
        self.assertIn(u"中文", u'中华','小当家？')

    def test_case4(self):
        u""" 淘宝"""
        self.driver.get("http://www.taobao.com/")
        raise Exception
        self.add_img()
        self.assertTrue(True)


class case_02(unittest.TestCase):
    """
    def setUp(cls):
        cls.driver = webdriver.Chrome()

    def tearDown(cls):
        cls.driver.quit()

        """
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def add_img(self):
        self.imgs.append(self.driver.get_screenshot_as_base64())
        return True

    def setUp(self):
        # 在是python3.x 中，如果在这里初始化driver ，因为3.x版本 unittest 运行机制不同，会导致用力失败时截图失败
        self.imgs = []
        self.addCleanup(self.cleanup)

    def cleanup(self):
        pass


    def test_case1(self):
        """ 百度搜索
        呵呵呵呵
        """
        print("校验了一下")
        self.driver.get("https://www.baidu.com")
        self.add_img()
        self.driver.find_element_by_id('kw').send_keys(u'百度一下')
        self.add_img()
        self.driver.find_element_by_id('su').click()
        time.sleep(1)
        self.add_img()

    @unittest.skip('跳过')
    def test_case2(self):
        """搜狗首页"""
        self.driver.get("http://www.sogou.com")
        print("本次校验没过？")
        self.assertTrue(False,"这是相当的睿智了")

    def test_case3(self):
        """ QQ邮箱"""
        self.driver.get("https://mail.qq.com")
        self.imgs.append(self.driver.get_screenshot_as_base64())
        print("没法打印？")
        self.assertIn(u"中文", u'中文')

    def test_case4(self):
        u""" 淘宝"""
        self.driver.get("http://www.taobao.com/")
        self.add_img()
        self.assertTrue(True)

if __name__ == "__main__":
    suite1 = unittest.TestLoader().loadTestsFromTestCase(case_01)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(case_02)
    suites =  unittest.TestSuite()
    suites.addTests([suite2,suite1])
    runer = HTMLTestRunner(title="带截图的测试报告", description="小试牛刀", stream=open("sample_test_report.html", "wb"), verbosity=2, retry=2, save_last_try=True)
    runer.run(suite1)
    runer.run(suite2)
