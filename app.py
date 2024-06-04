from flask import Flask, request, jsonify
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import threading
import pickle
import os

app = Flask(__name__)

# المسار لحفظ جلسات المستخدمين
SESSIONS_DIR = "sessions"
if not os.path.exists(SESSIONS_DIR):
    os.makedirs(SESSIONS_DIR)

def login_user(username, password):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # استبدل هذا بالرابط الفعلي لموقع تسجيل الدخول
        driver.get("https://sakani.sa/app/authentication/login")
        
        '''# قم بإضافة كود التفاعل مع عناصر الصفحة لتسجيل الدخول
        username_input = driver.find_element(By.ID, "username")
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "loginButton")
        
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()
        
        # انتظر حتى يتم تسجيل الدخول بنجاح (يمكنك تحسين هذه الخطوة بفحص معين)
        driver.implicitly_wait(10)'''
        
        # حفظ جلسة المستخدم
        session_file = os.path.join(SESSIONS_DIR, f"{username}_session.pkl")
        with open(session_file, 'wb') as f:
            pickle.dump(driver.get_cookies(), f)
        
        return {'status': 'Login successful'}
    
    except Exception as e:
        return {'error': str(e)}
    
    finally:
        driver.quit()

def get_session(username):
    session_file = os.path.join(SESSIONS_DIR, f"{username}_session.pkl")
    if os.path.exists(session_file):
        with open(session_file, 'rb') as f:
            cookies = pickle.load(f)
            return cookies
    return None

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    users = data.get('users', [])
    
    if not users or not isinstance(users, list):
        return jsonify({'error': 'A list of users is required'}), 400
    
    threads = []
    results = []

    def login_wrapper(username, password):
        result = login_user(username, password)
        results.append({'username': username, 'result': result})

    for user in users:
        username = user.get('username')
        password = user.get('password')
        if username and password:
            thread = threading.Thread(target=login_wrapper, args=(username, password))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()
    
    return jsonify(results), 200

@app.route('/session/<username>', methods=['GET'])
def get_user_session(username):
    cookies = get_session(username)
    if cookies:
        return jsonify({'username': username, 'session': cookies})
    return jsonify({'error': 'Session not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
