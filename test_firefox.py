from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Point to your geckodriver.exe
service = Service(r"C:\Users\PSI-Christian\Documents\QA Testing\geckodriver.exe")
driver = webdriver.Firefox(service=service)

# Open eBT
driver.get("http://192.168.1.196:81/PSI/login.php?userAction=logout&requestorURL=/PSI/index.php&objectcode=&df_code=&df_docno=")

# Login 
try:
    wait = WebDriverWait(driver, 10)

    # Enter username
    username = wait.until(
        EC.visibility_of_element_located((By.ID, "df_userid"))
    )
    username.send_keys("tester_christiandv")

    # Enter password
    password = driver.find_element(By.ID, "df_password")
    password.send_keys("yoS7Bt")

    # Select database
    db_dropdown = Select(driver.find_element(By.ID, "df_dbname"))
    db_dropdown.select_by_visible_text("psi_test_v7 - PHENOMENAL SOLUTIONS INC. - EDSA- Ortigas (2022.10.09.2330)")

    # Click login button
    login_button = driver.find_element(By.ID, "btnLogin")
    login_button.click()
    
    # Verify login by checking for an element on the landing page
    wait.until(EC.frame_to_be_available_and_switch_to_it(0))

    dashboard_element = wait.until(
        EC.presence_of_element_located((By.ID, "subtab2.0"))
    )

    print("Login successful!")
    
except Exception as e:
    print("Test Failed")
    print(e)

finally:
    import time
    time.sleep(10)  # Pause to see the result before closing

    driver.quit()