import time
import csv
import re  # 用于处理正则表达式
import chardet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 初始化第一个 WebDriver 实例
driver1 = webdriver.Edge()  # 用于第一个网站
driver1.get("https://ms.ecovacs.cn/feeOrder/listPage")  # 打开第一个看钱网址

# 第一个网站的登录操作
username_input_1 = driver1.find_element(By.NAME, "account")
password_input_1 = driver1.find_element(By.NAME, "password")
login_button_1 = driver1.find_element(By.ID, 'submitButton')

# 输入登录信息并点击登录
username_input_1.send_keys("13386201123")  # 替换为第一个网站的用户名
password_input_1.send_keys("AAAaaa12345678")  # 替换为第一个网站的密码
login_button_1.click()
# 登录第一个 WebDriver 成功

# 操作第一个网站：
element = WebDriverWait(driver1, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '维修管理') and contains(@class, 'dropdown-toggle')]")))
element.click()
print("第一个网站 - 点击维修管理成功")

# 进入目标页面
element = WebDriverWait(driver1, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "维修费用单查询")))
element.click()
# 进入第一个网页页面不用变了


# 初始化第二个 WebDriver 实例
driver2 = webdriver.Edge()  # 用于第二个网站
driver2.get("http://aux.bangjia.me/")  # 打开第二个结算钱网址

# 第二个网站的登录操作
username_input_2 = driver2.find_element(By.NAME, "username")
password_input_2 = driver2.find_element(By.NAME, "password")
login_button_2 = driver2.find_element(By.ID, 'fm-login-submit')

# 输入登录信息并点击登录
username_input_2.send_keys("13816576822")  # 替换为第二个网站的用户名
password_input_2.send_keys("753159")  # 替换为第二个网站的密码
login_button_2.click()

print("第二个网站 - 登录成功")
# 登录第二个 WebDriver 成功
#操作第二个网站
# 选择"财务管理"并进行操作
finance_management_option = WebDriverWait(driver2, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '财务管理')]"))
)
finance_management_option.click()

fee_settlement_link = WebDriverWait(driver2, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "费用结算")))
fee_settlement_link.click()

# 选择下拉菜单“全部品牌”并选择 "KWS"
dropdown = WebDriverWait(driver2, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[@class='filter-option pull-left' and text()='全部品牌']"))
)
dropdown.click()

target_option = WebDriverWait(driver2, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='KWS']"))
)
ActionChains(driver2).move_to_element(target_option).click().perform()
print("已选择 'KWS' 选项！")
#进入第二个网址不用变了

#下面开始循环操作
# 打开并读取 CSV 文件
import pandas as pd

# 指定文件路径和编码方式
file_path = "待结算工资.csv"

# 打开 CSV 文件并读取
with open(file_path, mode="r", encoding="mbcs") as file:
    reader = csv.reader(file)

    # 跳过标题行（第一行）
    next(reader)

    # 用 for 循环提取第二列
    for row in reader:
        # 使用正则表达式提取字符串中的数字部分
        numeric_data = re.findall(r'\d+', row[1])  # 提取所有数字部分   如果不按时间区分的话  就用这个
        #raw_data = row[1]  # 直接提取第二列数据内容
        # 打印结果
        if not numeric_data:  # 检查是否为空
            numeric_data = 0
            print(numeric_data)
            feiyong_heji =0
            print("费用合计:", feiyong_heji)

        else:
            numeric_data = int(''.join(numeric_data))  # 如果非空，将数字部分连接并转换为整数
            # 打印结果
            print(numeric_data)
            # 获取快递费 网站1
            driver1.get("https://ms.ecovacs.cn/repairOrder/view?repairOrderNo=" + str(numeric_data))
            feiyong_heji = WebDriverWait(driver1, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//label[contains(text(), '费用合计')]/following-sibling::span"))).text
            print("费用合计:", feiyong_heji)







        # 先点查询  这个可以刷新 网站2
        button = driver2.find_element(By.XPATH, "//input[@class='btn btn-default form-click' and @value='查询']")
        button.click()

        # 点击第一个网站的费用结算
        element = WebDriverWait(driver2, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='check' and text()='费用结算']")))
        element.click()

        # 填入厂家的快递费用
        input_box = WebDriverWait(driver2, 10).until(EC.presence_of_element_located((By.NAME, "factory")))
        input_box.send_keys(feiyong_heji)
        time.sleep(5)

        #点击确认
        confirm_button = WebDriverWait(driver2, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and text()='确认']")))
        confirm_button.click()
        print("费用结算成功！")

        time.sleep(5)












