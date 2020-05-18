# -*- coding: utf-8 -*-
# @Time    : 2017/9/6 11:26
# @File    : aaa.py
# @Author  : 守望@天空~
"""HTMLTestRunner 截图版示例 appium版"""
from appium import webdriver
import unittest
from HTMLTestRunner_cn import HTMLTestRunner


class case_01(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4.2'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['app'] = 'com.tencent.mobileqq'
        desired_caps['appActivity'] = 'com.tencent.mobileqq.activity.SplashActivity'
        cls.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


    def add_img(self):
        # 在是python3.x 中，如果在这里初始化driver ，因为3.x版本 unittest 运行机制不同，会导致用力失败时截图失败
        self.imgs.append(self.driver.get_screenshot_as_base64())
        return True

    def setUp(self):
        self.imgs = []
        self.addCleanup(self.cleanup)

    def cleanup(self):
        pass


    def test_case1(self):
        """ 手机QQ截图"""
        self.add_img()
        self.add_img()
        self.add_img()
        self.add_img()
        self.add_img()



if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(case_01)
    runer = HTMLTestRunner(title="带截图的测试报告", description="小试牛刀", stream=open("sample_test_report_appium.html", "wb"), verbosity=2, retry=1, save_last_try=True)
    runer.run(suite)
