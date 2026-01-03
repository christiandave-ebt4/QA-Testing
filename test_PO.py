from selenium import webdriver
from selenium.webdriver.firefox.service import Service  
from login import login
import time
import random
from window_utils import switch_to_popup
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys


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

    driver.switch_to.default_content()
    driver.switch_to.frame(0)

    # Select Purchasing Module
    purchasing_module = driver.find_element(By.XPATH, "//a[text()='Purchasing']")
    time.sleep(1)
    purchasing_module.click()

    # Select Purchase Order Add-On
    purchase_order_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Order*"))
    )
    purchase_order_link.click()

    # Select Vendor
    driver.switch_to.default_content()
    driver.switch_to.frame(0)
    driver.switch_to.frame("iframeBody")

    # Save main window once
    main_window = driver.current_window_handle

    # Select cfl to open vendor lookup popup
    vendor_lookup_img = wait.until(
        EC.element_to_be_clickable((By.ID, "cfl_u_po_vendorcode"))
    )
    time.sleep(3)
    vendor_lookup_img.click()
    print("✅ Vendor lookup opened")

    switch_to_popup(driver, wait, main_window)
    time.sleep(2)
    print("✅ Switched to vendor popup")

    # Select Vendor from Popup
    vendor_link = wait.until(
        EC.element_to_be_clickable((By.ID, "dd_suppnameT1r5"))
    )
    time.sleep(3)
    vendor_link.click()

    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='OK']"))).click()
    print("✅ Vendor selected")

    # Switch back to main window
    driver.switch_to.window(main_window)
    driver.switch_to.default_content()
    driver.switch_to.frame(0)
    driver.switch_to.frame("iframeBody")
    print("✅ Switched back to main window successfully")

    # Select Contact Person
    contact_person_select = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "df_u_po_contactperson1"))
    )

    try:
        # Try using Select class for standard dropdowns
        select_contact_person = Select(contact_person_select)

        # Wait until options are populated
        wait.until(lambda d: len(select_contact_person.options) > 1)

        options = select_contact_person.options
        total_options = len(options)

        print(f"ℹ️ Contact person options found: {total_options}")

        if total_options == 1:
            selected = select_contact_person.first_selected_option.text
            print(f"✅ Only one contact person available (auto-selected): {selected}")
        else:
            random_choice = random.randint(1, total_options - 1)
            select_contact_person.select_by_index(random_choice)
            print(f"✅ Selected random contact person (index {random_choice})")

    except Exception as e:
        # Handle non-standard dropdowns
        print("⚠️ Dropdown is not a standard <select> element. Handling manually.")
        contact_person_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "df_u_po_contactperson1"))
        )
        contact_person_dropdown.click()

        dropdown_options = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//xpath_to_dropdown_options"))
        )

        if len(dropdown_options) == 1:
            dropdown_options[0].click()
            print("✅ Only one contact person available — selected")
        else:
            random_choice = random.choice(dropdown_options)
            random_choice.click()
            print("✅ Selected a random contact person")

    for i, opt in enumerate(select_contact_person.options):
        print(f"Option {i}: '{opt.text}' | selected={opt.is_selected()}")

    unique_invoice_number = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
    print(f"Generated unique invoice number: {unique_invoice_number}")

    invoice_number_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "df_u_po_refno"))
    )
    invoice_number_field.clear()
    invoice_number_field.send_keys(unique_invoice_number)
    print("✅ Invoice number entered successfully")
    
    item_lookup_img = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "cfl_u_polines_itemcodeT1"))
    )
    time.sleep(1)
    item_lookup_img.click()
    print("✅ Item Code lookup opened successfully")    


    # Enter Item Code from Popup
    switch_to_popup(driver, wait, main_window)
    print("✅ Switched to Item Code popup successfully")

    search_item_code = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "df_inputfilter"))
    )   
    search_item_code.send_keys("Acer")
    print("✅ Item Code entered in popup search field")

    filter_button = driver.find_element(By.CLASS_NAME, "button")
    time.sleep(2)
    filter_button.click()
    print("✅ Filter applied in Item Code popup")

    select_filter = driver.find_element(By.XPATH, "//img[contains(@src, 'imgs/sort_blue.gif')]")
    time.sleep(2)
    select_filter.click()
    print("✅ Item Code filtered from popup")


    try:
        # Generate a random number between 1 and 54
        random_row = random.randint(1, 54)
        print(f"ℹ️ Randomly selected Acer item row: {random_row}")

        # Construct the ID of the Acer item
        acer_item_id = f"dd_itemdescT1r{random_row}"  
        print(f"ℹ️ Acer item ID: {acer_item_id}")

        # Locate and click the Acer item
        acer_item = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, acer_item_id))
        )
        acer_item.click()
        print(f"✅ Random Acer item (ID: {acer_item_id}) selected successfully.")

        driver.find_element(By.XPATH, "//a[text()='OK']").click()
        print("✅ Item Code selection confirmed.")

    except TimeoutException:
        print("❌ Failed to select an Acer item. Check the IDs or page state.")

    # Switch back to main window
    driver.switch_to.window(main_window)
    driver.switch_to.default_content()
    driver.switch_to.frame(0)
    driver.switch_to.frame("iframeBody")
    print("✅ Switched back to main window successfully after Item Code selection")


    try:
        # Add random Quantity
        quantity_field = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "df_u_polines_qtyT1"))
        )
        quantity_field.click()
        time.sleep(1)
        random_quantity = random.randint(1, 50)
        quantity_field.clear()  
        quantity_field.send_keys(str(random_quantity))
        quantity_field.send_keys(Keys.TAB)
        print(f"✅ Entered random quantity: {random_quantity}")

         # Item name (wait until populated)
        item_name_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "df_u_polines_itemdescT1"))
        )
        wait.until(lambda d: item_name_field.get_attribute("value") != "")
        item_name = item_name_field.get_attribute("value")
        print(f"ℹ️ Item name detected: {item_name}")


        # Move to the unit price field
        unit_price_field = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "df_u_polines_unitpriceT1"))  
        )

        # Set the unit price based on the item name
        if "NOTEBOOK" in item_name.upper():
            random_price = random.randint(20000, 60000)
        else:
            random_price = 0

        unit_price_field.clear()
        unit_price_field.send_keys(str(random_price))
        time.sleep(3)
        unit_price_field.send_keys(Keys.ENTER)
        print(f"✅ Entered unit price: {random_price}")

    except TimeoutException:
        print("❌ Failed to locate one of the fields. Check the IDs or page state.")


    try:
        # Enter details to logistics tab
        logistics_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='Logistics']"))
        )
        time.sleep(3)
        logistics_tab.click()

        # Enter vendor address
        vendor_address = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "df_u_po_vendoraddress"))
        )
        vendor_address.clear()
        vendor_address.send_keys("Mandaluyong")

        # Enter Shipping Method
        shipping_method = driver.find_element(By.ID, "df_u_po_shipvia")
        shipping_method.clear()
        shipping_method.send_keys("Cargo")

    except TimeoutException:
        print("❌ Failed to enter logistics details. Check the IDs or page state.")


    # Enter Accounting Details
    try:
        accounting_tab = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "tab1nav3"))
        )
        time.sleep(3)
        accounting_tab.click()

        # Enter Site
        site_field = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "df_u_po_paymentsite"))
        )
        site_field.clear()
        site_field.send_keys("site")
        print("✅ Accounting details entered successfully")

    except TimeoutException:
        print("❌ Failed to enter accounting details. Check the IDs or page state.")

    try:
        driver.switch_to.default_content()
        outer_frame = WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//frame"))
        )

        # Locate add button
        driver.find_element(By.NAME, "btnAdd']").click()
        print("✅ Add button clicked successfully to save the Purchase Order")

    except TimeoutException:
        print("❌ Failed to click Add button. Check the IDs or page state.")
    except Exception as e:
        print("❌ Test Failed")
        print(e)


finally:
    time.sleep(10)


