from flask import Flask, request
import redis
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
# إعداد الاتصال ب Redis
redis_url ="redis://:p5347bec6bfe2865a7483552281f975cfcaa86dd4e13d7d69761ca839d4d8641d@ec2-44-207-232-130.compute-1.amazonaws.com:14739"
r = redis.Redis.from_url(redis_url)

def c(user):
  #d =driversetup()
  #u = d.command_executor._url
  #s = d.session_id
  
  #d.get("https://sakani.sa/app/authentication/login")
  r.set(user, "ggg")#{"u":u,"s":s})

def g(u):
  d =driversetup()
  u=r[u]["u"]#
  s=r[u]["s"]#
  d.command_executor._url =u
  d.session_id =s
  return d.current_url

@app.route('/home', methods=["POST"])
def home():
    data = request.get_json()
    u = data["user"]
    return g(u)

@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    u = data["user"]
    c(u)
    return "ok"


@app.route('/creat_user', methods=['POST'])
def creat_user():
  data = request.get_json()
  n_id = data['id']
  password = data['password']
  return jsonify(res= n_id+"\n"+password),login(n_id,password)
def login(n_id,password):
    #global List_driver
    #global L_id
    driver=driversetup()
    u=r[n_id]["u"]#
    s=r[n_id]["s"]#
    driver.command_executor._url =u
    driver.session_id =s
    driver.get("https://sakani.sa/app/authentication/login")
    try:
      WebDriverWait(driver, 200).until(
                EC.presence_of_element_located((By.ID, 'nationId'))).send_keys(n_id)

      WebDriverWait(driver, 200).until(
                EC.presence_of_element_located((By.ID, 'password'))).send_keys(password)

    except Exception as e:
      driver.close()
      return 400

    Btn_login = driver.find_elements(By.CSS_SELECTOR, '.btn-primary')
    if len( Btn_login)<1:
      driver.close()
      return 400
    driver.execute_script("arguments[0].click();", Btn_login[0])
    try:
      Rt = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.flex-auto'))
            )
    except Exception as e:
      if "رقم الهوية او كلمة المرور غير صحيحة" in driver.find_element(By.XPATH, "/html/body").text:
        driver.close()
        return 300
      driver.close()
      return 400
    r[n_id]=driver
    #L_id.append(n_id)
    return 200  
    
    
if __name__ == '__main__':
    app.run(debug=True)
