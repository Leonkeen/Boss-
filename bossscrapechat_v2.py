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
# 找到所有元素
elements = driver.find_elements_by_xpath("//li[@role='listitem']//div[@class='friend-content']")
# 创建一个已单击元素的列表
clicked_elements = []
# 循环单击所有元素
while len(elements) > 0:
    # 循环单击每个元素
    for element in elements:
        if element not in clicked_elements:
            try:
                # 滚动到元素位置
                driver.execute_script("arguments[0].scrollIntoView();", element)
                # 等待元素变为可单击状态
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[@role='listitem']//div[@class='friend-content']")))
                # 单击元素
                element.click()
                time.sleep(3)
                # 从这里开始就是循环了 -- Get HR information
                friendname = driver.find_element_by_xpath("//li[@role='listitem']//div[@class='friend-content selected']")
                # 获取人名和公司名称 新版7点
                name_element = friendname.find_element_by_xpath(".//span[@class='name-text']")
                name00 = name_element.text
                company_element = friendname.find_element_by_xpath(".//span[@class='name-box']/span[2]")
                company_name00 = company_element.text
                #往下滚动 加载多几家公司出来
                actions = ActionChains(driver)
                actions.move_to_element(element).perform()
                actions.click().perform()
                actions.click().perform()
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
                # 循环点击子页面结束的位置
                # 将已单击元素添加到列表中
                clicked_elements.append(element)
            except:
                # 如果出现异常，则跳过该元素
                continue
    # 更新元素列表
    try:
        # 等待新元素的出现
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//li[@role='listitem']//div[@class='friend-content']")))
        # 更新元素列表，排除已单击元素
        elements = driver.find_elements_by_xpath("//li[@role='listitem']//div[@class='friend-content'][not(. = following::div[@class='friend-content'])]")
    except:
        # 如果出现异常，则认为所有元素已经单击完成
        elements = []
# Save data to a CSV file
df = pd.DataFrame(data, columns=['HR名字', '公司名', '规模大小', '岗位标签', '岗位描述', '工商信息', '工作地点', '职位基本信息'])
df.to_csv('zhipin.csv', index=False, encoding='utf-8-sig')
# Close the driver
driver.quit()