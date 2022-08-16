import random
import time

import selenium
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, StaleElementReferenceException
from selenium.webdriver import Keys


def wait_elem_by_id(driver, id):
    elm_found = False
    while not elm_found:
        try:
            elm = driver.find_element_by_id(id)
            return elm
        except Exception as e:
            time.sleep(1)
            pass


def wait_elem_by_xpath(driver, xpath):
    elm_found = False
    while not elm_found:
        try:
            elm = driver.find_element_by_xpath(xpath)
            return elm
        except Exception as e:
            print('wait elem')
            time.sleep(0.5)
            pass


def wait_elem_by_selector(driver, selectors, validate_attr_key='', validate_attr_val=''):
    elm_found = False
    while not elm_found:
        for selector in selectors:
            try:
                elm = driver.find_element_by_css_selector(selector)
                if validate_attr_val is '' or elm.get_attribute(validate_attr_key) == validate_attr_val:
                    return elm
                else:
                    print('wait elem')
                    time.sleep(0.5)
            except Exception as e:
                print('wait elem')
                time.sleep(0.5)


def go(username, password, need_wandering=False):
    # 登录
    driver = webdriver.Firefox(executable_path='geckodriver.exe')
    driver.get("https://devops.linewellcloud.com/")
    uname = wait_elem_by_id(driver, "uname")
    uname.clear()
    uname.send_keys(username)
    upass = driver.find_element_by_id("upass")
    upass.clear()
    upass.send_keys(password)
    login_btn = driver.find_element_by_xpath('/html/body/div/div/div/div/div[3]/button')
    login_btn.click()
    my_home = wait_elem_by_xpath(driver, '/html/body/div[1]/div[1]/div[2]/div/div/div[1]/a[2]')
    my_home.click()
    # 待处理大于0条，则查找处理中的任务，将其进度+5
    un_deal = wait_elem_by_xpath(driver, '/html/body/div[2]/div/div/div[1]/div[2]/div[3]/div[1]/div[1]/div[1]/div[1]')
    print(un_deal.text)
    # 找进度的输入框，会遇到好几种selector
    input_process_selectors = ['.J-selected-cvfs > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)',
                               '.J-selected-custom-cvfs > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)',
                               '.J-custom-cfs > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)',
                               '.J-selected-custom-cvfs > div:nth-child(2) > div:nth-child(2) > input:nth-child(1)',
                               '.J-selected-custom-cvfs > div:nth-child(3) > div:nth-child(2) > input:nth-child(1)',
                               '.J-selected-custom-cvfs > div:nth-child(4) > div:nth-child(2) > input:nth-child(1)']
    if un_deal and int(un_deal.text) > 0:
        print('待处理 > 0 ，查找任务')
        job_list = wait_elem_by_xpath(driver, '/html/body/div[2]/div/div/div[1]/div[2]/div[3]/div[2]/ul')
        for lis in job_list.find_elements_by_tag_name('li'):
            driver.switch_to.window(driver.window_handles[0])
            status = lis.find_element_by_xpath('.//span/span/button/span')
            if status.text == '处理中':
                a = lis.find_element_by_xpath('.//a')
                while len(driver.window_handles) < 2:
                    # 检查a标签是否打开，有时候一次click会打不开
                    a.click()
                    print('a click ,wait new page')
                    time.sleep(0.5)
                driver.switch_to.window(driver.window_handles[1])
                input_process = wait_elem_by_selector(driver, input_process_selectors, "placeholder", "进度百分比")
                process_percent = input_process.get_attribute('value')
                if process_percent != '100':
                    if process_percent == '':
                        process_percent = '0'
                    not_succeed = True
                    while not_succeed:
                        try:
                            input_process.click()
                            input_process.clear()
                            # 进度+5
                            percent = int(process_percent) + 5
                            if percent > 100:
                                percent = 100
                            input_process.send_keys(str(percent))
                            time.sleep(3)
                            title = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/div[2]/form/div[1]/div/div[1]/div/div/div[1]')
                            print(title.text + ':' + str(int(percent)) + "%")
                            not_succeed = False
                        except ElementNotInteractableException as e:
                            # print(e)
                            time.sleep(1)
                            input_process = wait_elem_by_selector(driver, input_process_selectors, "placeholder", "进度百分比")

                        except StaleElementReferenceException as e:
                            # print(e)
                            time.sleep(1)
                            input_process = wait_elem_by_selector(driver, input_process_selectors, "placeholder", "进度百分比")
                # 关闭标签页
                driver.close()
    # 是否瞎逛
    if need_wandering:
        wandering(driver)
    return driver


def wandering(driver):
    job_list = wait_elem_by_xpath(driver, '/html/body/div[2]/div/div/div[1]/div[2]/div[3]/div[2]/ul')
    li_list = job_list.find_elements_by_tag_name('li')
    # 打开大约25-40个a标签
    for i in range(0, random.randint(25, 40)//len(li_list)):
        for lis in li_list:
            driver.switch_to.window(driver.window_handles[0])
            a = lis.find_element_by_xpath('.//a')
            while len(driver.window_handles) < 2:
                # 检查a标签是否打开，有时候一次click会打不开
                try:
                    a.click()
                except selenium.common.exceptions.ElementClickInterceptedException:
                    print('ElementClickInterceptedException error')
                    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
                time.sleep(0.5)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(3)
            # 关闭标签页
            driver.close()


if __name__ == '__main__':
    pass
