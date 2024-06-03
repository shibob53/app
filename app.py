#from flask import Flask
from flask import Flask, request, jsonify
import time 
#import request
app = Flask(__name__)

listd={}

def c(user):
  global listd
  listd[user]=1 
def g():
  global listd
  return len(listd)

@app.route('/home',methods=["POST"])
def home():
  data = request.get_json()
  u = data["user"]
  return str(g())#"Hello, اتحداك تشغله"
@app.route('/add', methods=['POST'])
def add():
  data = request.get_json()
  u = data["user"]
  c(u)
  return "ok"
if __name__ == '__main__':
    app.run(debug=True)
