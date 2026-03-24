import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import random
import time
from login import login
from po import PurchaseOrder
from wrr import WarehouseReceiving
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("PSI_USERNAME")
PASSWORD = os.getenv("PSI_PASSWORD")
DATABASE = os.getenv("PSI_DATABASE")
URL = os.getenv("PSI_URL")

# Setup browser
service = Service(r"C:\Users\PSI-Christian\Documents\QA Testing\geckodriver.exe")

options = Options()
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"

driver = webdriver.Firefox(service=service, options=options)
wait = WebDriverWait(driver, 20)
main_window = driver.current_window_handle

try:
    # Create Purchase Order
    po = PurchaseOrder(driver, wait)
    po.login_and_prepare(login, URL, USERNAME, PASSWORD, DATABASE)
    po.select_purchasing_module()
    po.select_purchase_order()
    po.select_vendor()
    po.select_contact_person()
    invoice_number = po.enter_invoice_number()
    po.select_item_code()
    quantity, item_name, price = po.enter_quantity_and_price()
    po.enter_logistics()
    po.enter_accounting()
    po.add_purchase_order()
    print(f"✅ PO created with invoice number: {invoice_number}, item: {item_name}, quantity: {quantity}, price: {price}")
    
    # Continue with Warehouse Receiving
    wrr = WarehouseReceiving(driver, wait)
    wrr.process_receiving(invoice_number)
    print(f"✅ WRR completed for invoice: {invoice_number}")
except Exception as e:
    import traceback
    print("❌ An error occurred:")
    traceback.print_exc()
    # Optionally, save a screenshot for debugging
    try:
        screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        timestamp = time.strftime("%Y%m%d%H%M")
        screenshot_name = os.path.join(screenshots_dir, f"screenshot_failure_{timestamp}.png")
        driver.save_screenshot(screenshot_name)
        print(f"📸 Screenshot saved: {screenshot_name}")
    except Exception as ex:
        print("⚠️ Failed to save screenshot:", ex)
finally:
    driver.quit()

        