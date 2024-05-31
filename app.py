from flask import Flask
import time 

app = Flask(__name__)

@app.route('/')
def home():
    time.sleep(200) 
    return "Hello, اتحداك تشغله"

if __name__ == '__main__':
    app.run(debug=True)
