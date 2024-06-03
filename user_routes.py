from flask import Blueprint, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import json
import logging

user_bp = Blueprint('user', __name__)
logger = logging.getLogger(__name__)

def driversetup():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Selenium in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("lang=en")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
    return driver

@user_bp.route('/creat_user', methods=['POST'])
def creat_user():
    data = request.get_json()
    n_id = data['id']
    password = data['password']
    future = executor.submit(login, n_id, password)
    return jsonify(res=f"{n_id}\n{password}", login_status=future.result())

@user_bp.route('/creat_sms', methods=['POST'])  
def creat_sms():
    data = request.get_json()
    sms = data['sms']
    future = executor.submit(sms_code, sms)
    return jsonify(res=sms, sms_status=future.result())

@user_bp.route('/creat_land', methods=['POST'])  
def creat_land():
    data = request.get_json()
    url = data['url']
    future = executor.submit(land, url)
    return jsonify(res=url, land_status=future.result())

def login(n_id, password):
    driver = driversetup()
    try:
        driver.get("https://sakani.sa/app/authentication/login")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'nationId'))
        ).send_keys(n_id)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'password'))
        ).send_keys(password)
        
        Btn_login = driver.find_elements(By.CSS_SELECTOR, '.btn-primary')
        if Btn_login:
            driver.execute_script("arguments[0].click();", Btn_login[0])
        
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.flex-auto'))
        )
        save_session(n_id, json.dumps({"password": password}))
        return 200
    except Exception as e:
        logger.error(f"Login failed for user {n_id}: {e}")
        if "رقم الهوية او كلمة المرور غير صحيحة" in driver.page_source:
            return 300
        return 400
    finally:
        driver.quit()
    
def sms_code(sms):
    # تحديث لاستخدام الجلسات
    try:
        elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.flex-auto'))
        )
        if len(elements) < 4:
            return 400
        for i in range(4):
            elements[i].send_keys(sms[i])
        
        Btnsms = driver.find_elements(By.CSS_SELECTOR, '.btn-primary')
        if Btnsms and len(Btnsms) >= 4:
            driver.execute_script("arguments[0].click();", Btnsms[3])
        
        if WebDriverWait(driver, 150).until(EC.url_contains("marketplace")):
            return 200
    except Exception as e:
        logger.error(f"SMS code entry failed: {e}")
        return 400
    finally:
        driver.quit()

def land(url):
    driver = driversetup()
    try:
        driver.get(url)
        Btn_new = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='بدء حجز جديد']"))
        )
        driver.execute_script("arguments[0].click();", Btn_new)
        
        Lis = WebDriverWait(driver, 150).until(
            EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'text-neutral-n5')]"))
        )
        if not Lis:
            return 300
        X = random.randint(0, len(Lis) - 1)
        driver.execute_script("arguments[0].click();", Lis[X])
        
        Btn_land = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='حجز قطعة أرض']"))
        )
        driver.execute_script("arguments[0].click();", Btn_land)
        
        Btn_ok = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, "//button[text()=' وقع لاحقًا ']"))
        )
        driver.execute_script("arguments[0].click();", Btn_ok)
        
        return 200
    except Exception as e:
        logger.error(f"Land booking failed for URL {url}: {e}")
        return 400
    finally:
        driver.quit()
