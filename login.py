from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


def login(driver, url, username, password, database):
    """
    Reusable login function for eBT
    """

    wait = WebDriverWait(driver, 10)

    # Open eBT login page
    driver.get(url)

    # Enter username
    username_field = wait.until(
        EC.visibility_of_element_located((By.ID, "df_userid"))
    )
    username_field.clear()
    username_field.send_keys(username)

    # Enter password
    password_field = driver.find_element(By.ID, "df_password")
    password_field.clear()
    password_field.send_keys(password)

    # Select database
    db_dropdown = Select(driver.find_element(By.ID, "df_dbname"))
    db_dropdown.select_by_visible_text(database)

    # Click login button
    driver.find_element(By.ID, "btnLogin").click()

    # Switch to dashboard frame
    wait.until(EC.frame_to_be_available_and_switch_to_it(0))

    # Verify login success (element that only appears after login)
    wait.until(
        EC.presence_of_element_located((By.ID, "subtab2.0"))
    )

    print("✅ Login successful")
