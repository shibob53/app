from flask import Flask, request, jsonify
import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask_executor import Executor
import redis
import json


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
    
d=driversetup()
d1=driversetup()
d2=driversetup()
@app.route('/user', methods=["POST"])
def user():
  data = request.get_json()
  y = data['d']
  u = data['u']
  if y=='d':
    d.get(u)
  if y=='d1':
    d1.get(u)
  if y=='d2':
    d2.get(u)
    
  return "Ok"

@app.route('/na', methods=["POST"])
def na():
  data = request.get_json()
  y = data['d']
  if y=='d':
    return d.current_url
  if y=='d1':
    return d1.current_url
  if y=='d2':
    return d2.current_url
   
if __name__ == '__main__':
    app.run(debug=True)  