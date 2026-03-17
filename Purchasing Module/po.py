from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import random
import time
import traceback
from datetime import datetime

class PurchaseOrder:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.main_window = None

    def login_and_prepare(self, login_func, url, username, password, database):
        login_func(driver=self.driver, url=url, username=username, password=password, database=database)
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(0)

    def select_purchasing_module(self):
        purchasing_module = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Purchasing']")))
        purchasing_module.click()

    def select_purchase_order(self):
        purchase_order_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Purchase Order*")))
        purchase_order_link.click()

    def select_vendor(self):
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(0)
        self.driver.switch_to.frame("iframeBody")
        self.main_window = self.driver.current_window_handle
        vendor_lookup_img = self.wait.until(EC.element_to_be_clickable((By.ID, "cfl_u_po_vendorcode")))
        time.sleep(3)
        vendor_lookup_img.click()
        print("Vendor lookup opened")
        
        time.sleep(2)
        for handle in self.driver.window_handles:
            if handle != self.main_window:
                self.driver.switch_to.window(handle)
                break

        vendor_link = self.wait.until(EC.element_to_be_clickable((By.ID, "dd_suppnameT1r5")))
        vendor_link.click()
        print("Vendor selected in popup")

        ok_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='OK']")))
        ok_button.click()
        
        self.driver.switch_to.window(self.main_window)
        self.driver.switch_to.default_content()        
        self.driver.switch_to.frame(0)
        self.driver.switch_to.frame("iframeBody")
        print("Switch back to main window")
        # Add popup handling here if needed

    def select_contact_person(self):
        contact_person_select = self.wait.until(EC.presence_of_element_located((By.ID, "df_u_po_contactperson1")))
        try:
            select_contact_person = Select(contact_person_select)
            self.wait.until(lambda d: len(select_contact_person.options) > 1)
            options = select_contact_person.options
            if len(options) > 1:
                random_choice = random.randint(1, len(options) - 1)
                select_contact_person.select_by_index(random_choice)
            else:
                select_contact_person.select_by_index(0)
        except Exception:
            contact_person_dropdown = self.wait.until(EC.element_to_be_clickable((By.ID, "df_u_po_contactperson1")))
            contact_person_dropdown.click()
            # Add custom dropdown handling here

    def enter_invoice_number(self):
        unique_invoice_number = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
        invoice_number_field = self.wait.until(EC.presence_of_element_located((By.ID, "df_u_po_refno")))
        invoice_number_field.clear()
        time.sleep(2)
        invoice_number_field.send_keys(unique_invoice_number)
        return unique_invoice_number

    def select_item_code(self):
        self.main_window = self.driver.current_window_handle

        item_lookup_img = self.wait.until(EC.presence_of_element_located((By.ID, "cfl_u_polines_itemcodeT1")))
        time.sleep(3)
        item_lookup_img.click()
        print("Item code lookup opened")

        time.sleep(2)
        for handle in self.driver.window_handles:
            if handle != self.main_window:
                self.driver.switch_to.window(handle)
                break
        search_item = self.wait.until(EC.presence_of_element_located((By.ID, "df_inputfilter")))
        search_item.clear()
        search_item.send_keys("Acer")

        click_filter = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "button")))
        click_filter.click()
        print("Successfully selected an Item")

        # Switch back to main window
        self.driver.switch_to.window(self.main_window)
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(0)
        self.driver.switch_to.frame("iframeBody")
        print("Switched back to main window")
        # Add popup handling for item code selection

    def enter_quantity_and_price(self):
        quantity_field = self.wait.until(EC.element_to_be_clickable((By.ID, "df_u_polines_qtyT1")))
        time.sleep(3)
        quantity_field.click()
        random_quantity = random.randint(1, 50)
        quantity_field.clear()
        quantity_field.send_keys(str(random_quantity))
        quantity_field.send_keys(Keys.TAB)
        item_name_field = self.wait.until(EC.presence_of_element_located((By.ID, "df_u_polines_itemdescT1")))
        self.wait.until(lambda d: item_name_field.get_attribute("value") != "" or item_name_field.text != "")
        item_name = item_name_field.get_attribute("value") or item_name_field.text
        unit_price_field = self.wait.until(EC.element_to_be_clickable((By.ID, "df_u_polines_unitpriceT1")))
        if "NOTEBOOK" in item_name.upper():
            random_price = random.randint(20000, 60000)
        else:
            random_price = 0
        unit_price_field.clear()
        unit_price_field.send_keys(str(random_price))
        unit_price_field.send_keys(Keys.ENTER)
        return random_quantity, item_name, random_price

    def enter_logistics(self):
        logistics_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Logistics']")))
        time.sleep(1.5)
        logistics_tab.click()
        vendor_address = self.wait.until(EC.element_to_be_clickable((By.ID, "df_u_po_vendoraddress")))
        vendor_address.clear()
        vendor_address.send_keys("Mandaluyong")
        shipping_method = self.driver.find_element(By.ID, "df_u_po_shipvia")
        shipping_method.clear()
        shipping_method.send_keys("Cargo")

    def enter_accounting(self):
        accounting_tab = self.wait.until(EC.element_to_be_clickable((By.ID, "tab1nav3")))
        time.sleep(1.5)
        accounting_tab.click()
        site_field = self.wait.until(EC.element_to_be_clickable((By.ID, "df_u_po_paymentsite")))
        site_field.clear()
        site_field.send_keys("cubao")

    def add_purchase_order(self):
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(1)
        add_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Add']")))
        self.driver.execute_script("arguments[0].click();", add_button)
        time.sleep(3)

    # Add more methods as needed for your workflow
