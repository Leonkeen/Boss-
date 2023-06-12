from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import csv

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Navigate to a website
driver.get("https://login.zhipin.com/")
# 15秒的登录时间, 有时候会触发验证来来得及.
time.sleep(15)
driver.get("https://www.zhipin.com/web/geek/chat")
time.sleep(3)

# Find the element to click
element = driver.find_element_by_xpath("//div[@class='user-list-content']")
element.click()
time.sleep(3)

# Loop through all friend-content elements
elements = driver.find_elements_by_xpath("//li[@role='listitem']//div[@class='friend-content']")
data = []

for element in elements:
    element.click()
    time.sleep(3)
    # Get HR information
    friendname = driver.find_element_by_xpath("//li[@role='listitem']//div[@class='friend-content selected']")
    # 获取人名和公司名称 新版7点
    name_element = friendname.find_element_by_xpath(".//span[@class='name-text']")
    name00 = name_element.text
    company_element = friendname.find_element_by_xpath(".//span[@class='name-box']/span[2]")
    company_name00 = company_element.text
    # Open job position details
    job_position_content = driver.find_element_by_css_selector("a.position-content")
    job_position_content.click()
    time.sleep(8)
    # Switch to the new window 切换到子页面
    driver.switch_to.window(driver.window_handles[-1])
    # Get company information
    company_div = driver.find_element_by_class_name("job-detail-company")
    # name不能用 因为有些公司用logo和没用logo位置不一样, name = company_div.find_element(By.CSS_SELECTOR, ".company-info a").get_attribute("title")
    # 这段也不能用了 改掉了scale = company_div.find_element(By.CSS_SELECTOR,"p:nth-child(4)").text
    scale = driver.find_element_by_css_selector("p i.icon-scale") 
    parent = scale.find_element_by_xpath('..')
    scale_text = parent.text
    # Get job description information
    job_details = driver.find_element_by_class_name("job-detail-section").text
    # Get company introduction information
    company_info = driver.find_element_by_class_name("job-sec-text").text
    # Get business information
    # info_div = driver.find_element_by_class_name("job-sec.company-info")
    info_div = driver.find_element_by_css_selector('.detail-section-item.business-info-box')
    company_name = info_div.find_element_by_css_selector(".company-name").text.split("\n")[1]
    legal_person = info_div.find_element_by_css_selector(".company-user").text.split("\n")[1]
    established_time = info_div.find_element_by_css_selector(".res-time").text.split("\n")[1]
    company_type = info_div.find_element_by_css_selector(".company-type").text.split("\n")[1]  
    operation_status = info_div.find_element_by_css_selector(".manage-state").text.split("\n")[1]
    registered_capital = info_div.find_element_by_css_selector(".company-fund").text.split("\n")[1]
    # Get job location
    address_div = driver.find_element_by_class_name("job-location")
    address = address_div.find_element_by_class_name("location-address").text
    # Get job basic information
    status = driver.find_element_by_class_name("job-status").text
    job_name = driver.find_element_by_css_selector("h1[title]").get_attribute("title")
    salary = driver.find_element_by_class_name("salary").text
    city = driver.find_element_by_css_selector(".text-city").text
    data.append([
        [name00, company_name00], # HR information    
        [scale_text], # Company information            
        [job_details], # Job description information      
        [company_info], # Company introduction information        
        [company_name, legal_person, established_time, company_type, operation_status, registered_capital], # Business information
        [address], # Job location
        [status, job_name, salary, city] # Job basic information
    ])
    # Go back to main window
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)
# Save data to a CSV file
df = pd.DataFrame(data, columns=['HR名字', '公司名', '规模大小', '岗位标签', '岗位描述', '工商信息', '工作地点', '职位基本信息'])
df.to_csv('zhipin.csv', index=False, encoding='utf-8-sig')
# Close the driver
driver.quit()