from selenium import webdriver
from selenium.webdriver.firefox.service import Service  
from login import login
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select

# Setup browser
service = Service(r"C:\Users\PSI-Christian\Documents\QA Testing\geckodriver.exe")
driver = webdriver.Firefox(service=service)
wait = WebDriverWait(driver, 20)

try:
    login(
        driver=driver,
        url="http://192.168.1.196:81/PSI/login.php?userAction=logout&requestorURL=/PSI/index.php&objectcode=&df_code=&df_docno=",
        username="tester_christiandv",
        password="yoS7Bt",
        database="psi_test_v7 - PHENOMENAL SOLUTIONS INC. - EDSA- Ortigas (2022.10.09.2330)"
    )
    print("✅ Login successful")

    driver.switch_to.default_content()
    driver.switch_to.frame(0)

    # Select Purchasing Module
    purchasing_module = driver.find_element(By.XPATH, "//a[text()='Purchasing']")
    purchasing_module.click()

    purchase_order_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Order"))
    )
    purchase_order_link.click()

finally:
    time.sleep(10)
