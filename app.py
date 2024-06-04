from flask import Flask, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import redis
import time
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')

# إعداد اتصال Redis
redis_url = os.getenv('REDIS_URL', 'your_redis_url')
r = redis.Redis.from_url(redis_url)

# إعداد Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, session_url=None, session_id=None):
        self.id = id
        self.username = username
        self.session_url = session_url
        self.session_id = session_id

@login_manager.user_loader
def load_user(user_id):
    user_data = r.hgetall(user_id)
    if user_data:
        return User(user_id, user_data[b'username'].decode(), user_data.get(b'session_url'), user_data.get(b'session_id'))
    return None

# إعدادات السيلينيوم
def driversetup():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
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

def create_session(user):
    driver = driversetup()
    driver.get("https://sakani.sa/app/authentication/login")
    time.sleep(5)
    user.session_url = driver.command_executor._url
    user.session_id = driver.session_id
    r.hset(user.id, mapping={
        'username': user.username,
        'session_url': user.session_url,
        'session_id': user.session_id
    })
    return user.session_url, user.session_id

def get_session(user):
    if user.session_url and user.session_id:
        driver = driversetup()
        driver.command_executor._url = user.session_url.decode()
        driver.session_id = user.session_id.decode()
        return driver
    return None

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    user_id = username  # أو استخدم معرّف فريد
    user_data = r.hgetall(user_id)
    if not user_data:
        user = User(user_id, username)
        r.hset(user_id, mapping={'username': username})
    else:
        user = User(user_id, username, user_data.get(b'session_url'), user_data.get(b'session_id'))
    login_user(user)
    return jsonify(message="Logged in successfully"), 200

@app.route('/home', methods=["POST"])
@login_required
def home():
    driver = get_session(current_user)
    if driver:
        return jsonify(current_url=driver.current_url)
    return jsonify(error="Session not found"), 404

@app.route('/add', methods=['POST'])
@login_required
def add():
    session_url, session_id = create_session(current_user)
    return jsonify(u=session_url, s=session_id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify(message="Logged out successfully"), 200

@app.route('/create_user', methods=['POST'])
@login_required
def create_user():
    data = request.get_json()
    n_id = data['id']
    password = data['password']
    login_result = selenium_login(n_id, password)
    return jsonify(res=n_id + "\n" + password, login_status=login_result)

def selenium_login(n_id, password):
    driver = get_session(current_user)
    if not driver:
        return 404

    try:
        driver.get("https://sakani.sa/app/authentication/login")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'nationId'))).send_keys(n_id)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(password)
        Btn_login = driver.find_elements(By.CSS_SELECTOR, '.btn-primary')
        if Btn_login:
            driver.execute_script("arguments[0].click();", Btn_login[0])
            WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.flex-auto')))
            r.hset(current_user.id, mapping={
                'session_url': driver.command_executor._url,
                'session_id': driver.session_id
            })
            return 200
        return 400
    except Exception as e:
        logging.error(f'Login failed for {n_id}: {e}')
        driver.quit()
        if "رقم الهوية او كلمة المرور غير صحيحة" in driver.page_source:
            return 300
        return 400

if __name__ == '__main__':
    app.run(debug=True)
