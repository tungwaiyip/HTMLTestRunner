# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 11:26
# @File    : aaa.py
# @Author  : 守望@天空~
"""HTMLTestRunner 截图版示例"""
from selenium import webdriver
import unittest
import time
from HTMLTestRunner_cn import HTMLTestRunner


class case_01(unittest.TestCase):
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
        self.imgs = []
        self.addCleanup(self.cleanup)

    def cleanup(self):
        pass

    def test_case1(self):
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
        self.assertTrue(False)

    def test_case3(self):
        """ QQ邮箱"""
        self.driver.get("https://mail.qq.com")
        self.imgs.append(self.driver.get_screenshot_as_base64())
        self.assertIn(u"中文", u'中华')

    def test_case4(self):
        u""" 淘宝"""
        self.driver.get("http://www.taobao.com/")
        self.add_img()
        self.assertTrue(True)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(case_01)
    runer = HTMLTestRunner(title="带截图的测试报告", description="小试牛刀", stream=open("sample_test_report.html", "wb"), verbosity=2, retry=1, save_last_try=True)
    runer.run(suite)
