from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from login import login
import time

# Setup browser
service = Service(r"C:\Users\PSI-Christian\Documents\QA Testing\geckodriver.exe")
driver = webdriver.Firefox(service=service)

try:
    login(
        driver=driver,
        url="http://192.168.1.196:81/PSI/login.php?userAction=logout&requestorURL=/PSI/index.php&objectcode=&df_code=&df_docno=",
        username="tester_christiandv",
        password="yoS7Bt",
        database="psi_test_v7 - PHENOMENAL SOLUTIONS INC. - EDSA- Ortigas (2022.10.09.2330)"
    )

    time.sleep(10)

except Exception as e:
    print("❌ Test Failed")
    print(e)

finally:
    driver.quit()
