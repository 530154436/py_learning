import os
from selenium import webdriver

# --------------------------------------------------------------------
# 配置 webdriver
# --------------------------------------------------------------------
driver_path = f'{os.path.dirname(__file__)}'
driver_path = os.path.join(driver_path, 'chromedriver_87_xx_88')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # Headless模式-无界面模式

# --------------------------------------------------------------------
# 请求页面
# --------------------------------------------------------------------
driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)
driver.get('http://www.baidu.com/')

input = driver.find_element_by_id('kw')  # 获取输入框
submit = driver.find_element_by_id('su') # 获取搜索按钮

input.send_keys("Python")   # 输入框输入"Python"
submit.click()              # 搜索

html = driver.page_source
print(html)

driver.close()
driver.quit()