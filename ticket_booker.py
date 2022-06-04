import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from PIL import Image
import ddddocr

# import urllib
# import requests
# import pytesseract


class BookQuanrantineHotel:
    def __init__(self, chromedriver_path):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)    
        self.login_url = "https://hk.sz.gov.cn:8118/"
        self.driver = webdriver.Chrome(executable_path=chromedriver_path,options=chrome_options)
        self.driver.maximize_window()
        self.driver.get(self.login_url)
        

        time.sleep(2)
        # 关闭弹窗
        self.driver.find_element_by_xpath(
            '//*[@class="winpop" and @id="winLoginNotice"]/div[1]/div[1]/button'
        ).click()

    def login(self, account, password, account_type=2):
        self.select_account_type(account_type)
        self.fill_account(account)
        self.fill_psw(password)
        self.verificaton_code()

    def select_account_type(self, account_type):
        # 证件类型选择
        selectbox1 = Select(
            self.driver.find_element_by_xpath('//*[@class="login_form"]/div[1]/div[1]/select')
        )
        selectbox1.select_by_value(str(account_type))

    def fill_account(self, account):
        # 账号(e.g.港澳通行证)
        account_input = self.driver.find_element_by_xpath('//*[@class="login_form"]/div[2]/input')
        account_input.clear()  # 先清空输入框
        account_input.send_keys(str(account))  # 账号栏填入账号

    def fill_psw(self, password):
        # 密码
        pwd_input = self.driver.find_element_by_xpath('//*[@class="login_form"]/div[3]/input')
        pwd_input.clear()  # 先清空输入框
        pwd_input.send_keys(str(password))  # 密码栏填入密码

    def verificaton_code(self):
        # 验证码
        while True:
            try:
                # 截图
                verification_code_image = self.driver.find_element_by_xpath(
                    '//*[@class="login_form"]/div[5]/a/img'
                )
                verification_code_image.screenshot("code.png")
                # 识别
                ocr = ddddocr.DdddOcr(old=True)
                with open("code.png", "rb") as f:
                    img_bytes = f.read()
                ocr_result = ocr.classification(img_bytes)
                print(ocr_result)
                verification_input = self.driver.find_element_by_xpath(
                    '//*[@class="login_form"]/div[4]/input'
                )
                verification_input.clear()
                verification_input.send_keys(ocr_result)
                # 点击登陆
                self.driver.find_element_by_xpath('//*[@class="Btngroup"]/button[1]').click()
                time.sleep(2)
            except:
                # 如果成功登陆，就找不到“登陆”按钮了，报exception,说明成功登陆了，跳出循环
                break
        # 点击确定，关闭弹窗
        self.driver.find_element_by_xpath('//*[@class="flexbox btngroup"]/div[1]/button').click()
        time.sleep(0.2)

    def reserve(self, day):
        # 点击预约
        while True:
            # 点击"我要预约"
            try:
                self.driver.find_element_by_xpath(
                    '//*[@class="wrap"]/a[@id="a_canBookHotel"]'
                ).click()
                # 进入下一个页面，点击“预约”
                self.driver.find_element_by_xpath(
                    '//*[@class="tzlist tongguanlist yuyuelist"]/div[1]/section['
                    + str(day)
                    + "]/div/div[3]/div/button"
                ).click()
                # print(x.text)
            except Exception as e:
                #time.sleep(0.1)
                print(e)
                continue
            else:
                #  print(
                #      self.driver.find_element_by_xpath(
                #          '//*[@class="tzlist tongguanlist yuyuelist"]/div[1]/section['
                #          + str(day)
                #          + "]/div/div[3]/div/button"
                #      ).text
                #  )
                break
        # 持续点击
        x=0
        while True:
            x=x+1
            if x==1000:
                self.driver.refresh()
                x=0             
            try:
                self.driver.find_element_by_xpath(
                    '//*[@class="tzlist tongguanlist yuyuelist"]/div[1]/section['
                    + str(day)
                    + "]/div/div[3]/div/button"
                ).click()
            except Exception as e:
                break
  
