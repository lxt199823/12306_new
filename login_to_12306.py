# 登录网址https://kyfw.12306.cn/otn/resources/login.html
# 登录成功跳转到 https://kyfw.12306.cn/otn/view/index.html
import time

import requests
from selenium import webdriver
import base64
import numpy
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def init(driver):
    driver.maximize_window()
    driver.get('https://kyfw.12306.cn/otn/resources/login.html')
    time.sleep(3)
    driver.find_element_by_class_name('login-hd-account').click()
    time.sleep(3)


def input(driver):
    driver.find_element_by_id('J-userName').send_keys('账号')
    driver.find_element_by_id('J-password').send_keys('密码')


def get_pic(driver):
    img_url = driver.find_element_by_class_name('imgCode').get_attribute('src')
    img_url = str(img_url).replace('data:image/jpg;base64,', '')
    img_code = base64.b64decode(img_url)
    with open('static/imgCode.jpg', 'wb') as f:
        f.write(img_code)
        print('图片下载成功！')


def identify_pic(driver):
    body_list = []
    url = 'http://littlebigluo.qicp.net:47720/'
    files = {'pic_xxfile': ('imgCode.jpg', open('static/imgCode.jpg', 'rb'), 'image/png')}
    r = requests.post(url, files=files)
    # print(r.text)
    if u'图片貌似选' in r.text:
        body_str_1 = r.text.split(u'<B>')
        body_str = body_str_1[1].split(u'<')[0].split()
        # print(body_str)
        for index in body_str:
            body_list.append(int(index))
        return numpy.array(body_list)
    elif u'访问过于频繁' in r.text:
        print('服务器繁忙，请稍后再试！')
    else:
        print('识别失败！')


def click_small_pic(driver, i):
    img_element = driver.find_element_by_class_name('imgCode')
    if i <= 4:
        ActionChains(driver).move_to_element_with_offset(img_element, 40 + 72 * (i - 1), 73).click().perform()
    else:
        i -= 4
        ActionChains(driver).move_to_element_with_offset(img_element, 40 + 72 * (i - 1), 145).click().perform()


def click_pic(driver, body_list):
    try:
        for i in range(len(body_list)):
            click_small_pic(driver, body_list[i])
            time.sleep(1)
    except TypeError:
        print('识别失败！')


def login(driver):
    driver.find_element_by_class_name('login-btn').click()


def main():
    # driver = webdriver.Chrome()
    dcap = dict(DesiredCapabilities.CHROME)
    dcap['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, ' \
                                                'like Gecko) Chrome/68.0.3440.75 Safari/537.36 '
    driver = webdriver.Chrome(desired_capabilities=dcap)

    init(driver)
    input(driver)
    get_pic(driver)
    body_list = identify_pic(driver)
    print('识别到的图片序号为（横向）：')
    print(body_list)
    click_pic(driver, body_list)
    login(driver)
    time.sleep(3)
    # driver.quit()

main()
