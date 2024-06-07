from flask import Flask, request, jsonify
import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def driversetup():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Selenium in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
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

driver = driversetup()
#L_id=[]
##########
@app.route('/creat_user', methods=['POST'])
def creat_user():
  data = request.get_json()
  n_id = data['id']
  password = data['password']
  return jsonify(res= n_id+"\n"+password),login(n_id,password)
  
@app.route('/creat_sms', methods=['POST'])  
def creat_sms():
  data = request.get_json()
  sms = data['sms']
  url = "https://sakani.sa/app/land-projects/"+data['url']
  res = sms_code(sms)
  #if res ==200:
    #res = land(url)
  return jsonify(res=res),100

#@app.route('/creat_land', methods=['POST'])  
#def creat_land():
  #data = request.get_json()
  #url = "https://sakani.sa/app/land-projects/"+data['url']
 # n_id=data['id']
 # return jsonify(res=url),100#land(url,n_id)  

#################################
def login(n_id,password):
    global driver
    #global L_id
    
    driver=driversetup()
    driver.get("https://sakani.sa/app/authentication/login")
    try:
      WebDriverWait(driver, 200).until(
                EC.presence_of_element_located((By.ID, 'nationId'))).send_keys(n_id)

      WebDriverWait(driver, 200).until(
                EC.presence_of_element_located((By.ID, 'password'))).send_keys(password)

    except Exception as e:
      #driver.quit()
      #driver.close()
      return 400

    Btn_login = driver.find_elements(By.CSS_SELECTOR, '.btn-primary')
    if len( Btn_login)<1:
      #driver.quit()
      #driver.close()
      return 400
    driver.execute_script("arguments[0].click();", Btn_login[0])
    try:
      Rt = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.flex-auto'))
            )
    except Exception as e:
      if "رقم الهوية او كلمة المرور غير صحيحة" in driver.find_element(By.XPATH, "/html/body").text:
        #driver.quit()
        #driver.close()
        return 300
      #driver.quit()
      #driver.close()
      return 400
    #List_driver[n_id]=[driver,0]
    #L_id.append(n_id)
    return 200
    
def sms_code(sms):
   # global driver
    return "driver.current_url"
    #return List_driver
    #global L_id
    #if len(L_id)<1:
      #return 401
    #md=""
   # for i in List_driver:
    #  if List_driver[i][1]==0:
     #   md=i
     #   driver = List_driver[i][0]
      #  List_driver[i][1]=1
   # if md=="":
   #   return 400
    
    #n_d = L_id[0]
    #del L_id[0]
'''    
    try:
      Rt = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.flex-auto'))
            )
      if len(Rt)<4:
        #driver.quit()
        #driver.close()
        return 401
      for i in range(4):
        Rt[i].send_keys(sms[i])
    except Exception as e:
      #driver.quit()
      #driver.close()
      return 402
    Btnsms = driver.find_elements(By.CSS_SELECTOR, '.btn-primary')
    if len(Btnsms)<4:
      #driver.quit()
      #driver.close()
      return 403
    driver.execute_script("arguments[0].click();", Btnsms[3])
    if WebDriverWait(driver, 150).until(EC.url_contains("marketplace")):
      return 200
    #driver.quit()
    #driver.close()
    return 404'''

def land(url):
    global driver
    #driver = List_driver[n_id][0]
    driver.get(url)
    try:
      Btn_new=WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//span[text()='بدء حجز جديد']")))
      driver.execute_script("arguments[0].click();", Btn_new)
    except Exception as e:
      b=5
    try:
      Lis = WebDriverWait(driver, 150).until(
                EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'text-neutral-n5')]"))
            )
      if len(Lis)<1:
        driver.quit()
        driver.close()
        return 300
      X=random.randint(0,len(Lis))
      driver.execute_script("arguments[0].click();", Lis[X])
    except Exception as e:
      driver.quit()
      driver.close()
      return 400
    try:
      Btn_land=WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, "//span[text()='حجز قطعة أرض']")))
      driver.execute_script("arguments[0].click();", Btn_land)
    except Exception as e:
      driver.quit()
      driver.close()
      return 400
    try:
      Btn_ok=WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//button[text()=' وقع لاحقًا ']")))
      driver.execute_script("arguments[0].click();", Btn_ok)
    except Exception as e:
      b=6
    driver.quit()
    driver.close()
    return 200
    
if __name__ == '__main__':
  app.run(debug=True)