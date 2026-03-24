from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class WarehouseReceiving:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
    
    def process_receiving(self, invoice_number):
        self.select_wrr_page()
        self.click_supplier_cfl()
        # Add more steps here later
    
    def select_wrr_page(self):
        print("🔄 Attempting to navigate to WRR page...")
        time.sleep(3)  # Wait for PO to be saved
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(0)
        
        # Click Purchasing module again to ensure we're in the right place
        purchasing_module = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Purchasing']")))
        purchasing_module.click()
        time.sleep(2)
        
        # Now click WRR link
        wrr_link = self.wait.until(EC.element_to_be_clickable((By.ID, "subtab112.0")))
        wrr_link.click()
        time.sleep(3)  # Wait for WRR page to load
        print("✅ Navigated to WHSE Receiving Report page")
    
    def click_supplier_cfl(self):
        print("🔄 Attempting to click Supplier CFL...")
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(0)
        self.driver.switch_to.frame("iframeBody")
        self.main_window = self.driver.current_window_handle
        click_vendor = self.wait.until(EC.element_to_be_clickable((By.ID, "cfl_u_wrr_suppcode")))
        click_vendor.click()
        print("✅ Opened Vendor CFL")
        time.sleep(3)
        time.sleep(5)

    def click_supplier_cfl(self):
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(0)
        self.driver.switch_to.frame("iframeBody")
        self.main_window = self.driver.current_window_handle
        click_vendor = self.wait.until(EC.element_to_be_clickable((By.ID, "cfl_u_wrr_suppcode")))
        click_vendor.click()
        print("✅ Opened Vendor CFL")
        time.sleep(3)

        for handle in self.driver.window_handles:
            if handle != self.main_window:
                self.driver.switch_to.window(handle)
                break
        
        click_vendor_whse = self.wait.until(EC.element_to_be_clickable((By.ID, "dd_suppnameT1r5")))
        click_vendor_whse.click()
        print("Vendor selected in popup")

        ok_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='OK']")))
        ok_button.click()

        self.driver.switch_to.window(self.main_window)
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(0)
        self.driver.switch_to.frame("iframeBody")
        print("Switched back to main window")

        time.sleep(3)   
    
    def click_fowarder_cfl(self):
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(0)
        self.driver.switch_to.frame("iframeBody")
        self.main_window = self.driver.current_window_handle
        click_vendor = self.wait.until(EC.element_to_be_clickable((By.ID, "cfl_u_wrr_fwdrcode")))
        click_vendor.click()
        print("✅ Opened Vendor CFL")
        time.sleep(3)